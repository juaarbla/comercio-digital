from __future__ import annotations

import argparse
import csv
import os
import re
import sys
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    load_dotenv = None

from paths import BASE_DIR, DOCS_DIR, LOGS_DIR


NEWSLETTER_DIR = DOCS_DIR / "newsletter"
DEFAULT_SUBSCRIBERS = BASE_DIR / "data" / "private" / "suscriptores_newsletter.csv"
LOG_FILE = LOGS_DIR / "newsletter_mailgun.log"
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass(frozen=True)
class Subscriber:
    email: str
    name: str = ""


def env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()


def load_env_file(path: Path) -> None:
    if load_dotenv is not None:
        load_dotenv(path)
        return
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def log(message: str) -> None:
    try:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        LOG_FILE.open("a", encoding="utf-8").write(f"[{timestamp}] {message}\n")
    except OSError as exc:
        print(f"Aviso: no se pudo escribir el log {LOG_FILE}: {exc}", file=sys.stderr)


def latest_newsletter(explicit_path: str = "") -> Path:
    if explicit_path:
        path = Path(explicit_path)
        if not path.is_absolute():
            path = BASE_DIR / path
        if not path.exists():
            raise FileNotFoundError(f"No existe la newsletter indicada: {path}")
        return path

    candidates = sorted(
        NEWSLETTER_DIR.glob("newsletter-*.html"),
        key=lambda p: (p.stat().st_mtime, p.name),
        reverse=True,
    )
    if not candidates:
        raise FileNotFoundError("No se han encontrado newsletters HTML en docs/newsletter/.")
    return candidates[0]


def issue_url(newsletter_path: Path) -> str:
    base_url = env("NEWSLETTER_BASE_URL", "https://comerciodigital.net/newsletter/").rstrip("/")
    return f"{base_url}/{newsletter_path.name}"


def normalize_header(name: str) -> str:
    text = unicodedata.normalize("NFKD", name.strip().lower())
    text = "".join(char for char in text if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", "_", text).strip("_")


def truthy(value: str, default: bool = True, *, consent: bool = False) -> bool:
    text = (value or "").strip().lower()
    if not text:
        return default
    if consent and "acepto" in text:
        return True
    return text not in {"0", "no", "false", "falso", "baja", "inactivo", "inactive"}


def row_email(row: dict[str, Any]) -> str:
    for key in ("email", "correo", "correo_electronico", "e_mail", "mail"):
        value = row.get(key, "")
        if value:
            return str(value).strip().lower()
    return ""


def row_name(row: dict[str, Any]) -> str:
    for key in ("nombre", "name", "nombre_y_apellidos", "apellidos"):
        value = row.get(key, "")
        if value:
            return str(value).strip()
    return ""


def load_subscribers(path: Path) -> list[Subscriber]:
    if not path.exists():
        raise FileNotFoundError(
            f"No existe el CSV de suscriptores: {path}. "
            "Exporta Google Forms/Sheets a data/private/suscriptores_newsletter.csv."
        )

    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            return []
        reader.fieldnames = [normalize_header(name) for name in reader.fieldnames]

        subscribers: list[Subscriber] = []
        seen: set[str] = set()
        for row in reader:
            normalized = {normalize_header(str(k)): v for k, v in row.items()}
            email = row_email(normalized)
            if not EMAIL_RE.match(email):
                continue
            if not truthy(str(normalized.get("activo", "")), default=True):
                continue
            if not truthy(str(normalized.get("consentimiento", "")), default=True, consent=True):
                continue
            if email in seen:
                continue
            seen.add(email)
            subscribers.append(Subscriber(email=email, name=row_name(normalized)))
    return subscribers


def mail_subject(newsletter_path: Path, custom_subject: str = "") -> str:
    if custom_subject:
        return custom_subject
    stem = newsletter_path.stem.replace("newsletter-", "").replace("-", " ")
    return f"Comercio Digital en el aula - Selección {stem}"


def text_body(url: str) -> str:
    unsubscribe = env(
        "NEWSLETTER_UNSUBSCRIBE_TEXT",
        "Para dejar de recibir esta newsletter, responde a este correo con BAJA.",
    )
    return (
        "Hola,\n\n"
        "Ya está disponible una nueva selección de noticias de Comercio Digital para trabajar en clase.\n\n"
        f"Puedes verla aquí:\n{url}\n\n"
        "Incluye actualidad de comercio electrónico, digitalización, marketing digital e inteligencia artificial aplicada al comercio.\n\n"
        f"{unsubscribe}\n\n"
        "Un saludo,\n"
        "Juan\n"
    )


def html_body(url: str) -> str:
    unsubscribe = env(
        "NEWSLETTER_UNSUBSCRIBE_TEXT",
        "Para dejar de recibir esta newsletter, responde a este correo con BAJA.",
    )
    return f"""<!doctype html>
<html lang="es">
<body>
  <p>Hola,</p>
  <p>Ya está disponible una nueva selección de noticias de <strong>Comercio Digital</strong> para trabajar en clase.</p>
  <p><a href="{url}">Leer la newsletter publicada</a></p>
  <p>Incluye actualidad de comercio electrónico, digitalización, marketing digital e inteligencia artificial aplicada al comercio.</p>
  <p style="font-size: 13px; color: #666;">{unsubscribe}</p>
  <p>Un saludo,<br>Juan</p>
</body>
</html>"""


def mailgun_payload(to_email: str, subject: str, url: str) -> dict[str, str]:
    payload = {
        "from": env("MAILGUN_FROM"),
        "to": to_email,
        "subject": subject,
        "text": text_body(url),
        "html": html_body(url),
        "o:tag": "newsletter-comercio-digital",
    }
    reply_to = env("MAILGUN_REPLY_TO")
    if reply_to:
        payload["h:Reply-To"] = reply_to
    return payload


def validate_mailgun_config() -> None:
    missing = [
        key
        for key in ("MAILGUN_API_KEY", "MAILGUN_DOMAIN", "MAILGUN_FROM")
        if not env(key)
    ]
    if missing:
        raise RuntimeError(f"Faltan variables Mailgun en .env: {', '.join(missing)}")


def mailgun_api_base() -> str:
    return env("MAILGUN_API_BASE", "https://api.mailgun.net").rstrip("/")


def mask_secret(value: str) -> str:
    if not value:
        return "(vacío)"
    if len(value) <= 8:
        return "*" * len(value)
    return f"{value[:4]}...{value[-4:]}"


def print_diagnostics() -> None:
    domain = env("MAILGUN_DOMAIN")
    api_base = mailgun_api_base()
    print("Diagnóstico Mailgun")
    print(f"- MAILGUN_API_BASE: {api_base}")
    print(f"- MAILGUN_DOMAIN: {domain or '(vacío)'}")
    print(f"- MAILGUN_FROM: {env('MAILGUN_FROM') or '(vacío)'}")
    print(f"- MAILGUN_REPLY_TO: {env('MAILGUN_REPLY_TO') or '(vacío)'}")
    print(f"- MAILGUN_API_KEY: {mask_secret(env('MAILGUN_API_KEY'))}")
    if domain:
        print(f"- Endpoint mensajes: {api_base}/v3/{domain}/messages")


def send_one(to_email: str, subject: str, url: str) -> tuple[bool, str]:
    validate_mailgun_config()
    endpoint = f"{mailgun_api_base()}/v3/{env('MAILGUN_DOMAIN')}/messages"
    response = requests.post(
        endpoint,
        auth=("api", env("MAILGUN_API_KEY")),
        data=mailgun_payload(to_email, subject, url),
        timeout=30,
    )
    if response.ok:
        return True, response.text
    return False, f"{response.status_code} {response.text}"


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    load_env_file(BASE_DIR / ".env")

    parser = argparse.ArgumentParser(description="Prepara o envía la newsletter publicada mediante Mailgun.")
    parser.add_argument("--subscribers", default=str(DEFAULT_SUBSCRIBERS), help="CSV de suscriptores.")
    parser.add_argument("--newsletter", default="", help="HTML concreto de newsletter. Si se omite, usa la última.")
    parser.add_argument("--subject", default="", help="Asunto del correo.")
    parser.add_argument("--test", default="", help="Enviar/validar solo a este email.")
    parser.add_argument("--diagnose", action="store_true", help="Muestra configuración Mailgun sin enviar ni revelar la API key.")
    parser.add_argument("--send", action="store_true", help="Envía realmente por Mailgun.")
    parser.add_argument("--yes", action="store_true", help="Confirmación explícita para envío real.")
    args = parser.parse_args()

    if args.diagnose:
        print_diagnostics()
        return

    newsletter_path = latest_newsletter(args.newsletter)
    url = issue_url(newsletter_path)
    subject = mail_subject(newsletter_path, args.subject)

    if args.test:
        recipients = [Subscriber(email=args.test.strip().lower())]
    else:
        recipients = load_subscribers(Path(args.subscribers))

    if not recipients:
        raise RuntimeError("No hay destinatarios válidos.")

    mode = "SEND" if args.send else "DRY-RUN"
    print(f"Modo: {mode}")
    print(f"Newsletter: {newsletter_path}")
    print(f"URL pública: {url}")
    print(f"Asunto: {subject}")
    print(f"Destinatarios válidos: {len(recipients)}")

    if not args.send:
        print("No se ha enviado nada. Añade --send --yes para envío real.")
        log(f"DRY-RUN newsletter={newsletter_path.name} recipients={len(recipients)}")
        return

    if not args.yes:
        raise RuntimeError("Para envío real usa también --yes.")

    sent = 0
    failed = 0
    for recipient in recipients:
        ok, detail = send_one(recipient.email, subject, url)
        if ok:
            sent += 1
            log(f"SENT to={recipient.email} newsletter={newsletter_path.name}")
        else:
            failed += 1
            log(f"ERROR to={recipient.email} detail={detail}")

    print(f"Enviados: {sent}")
    print(f"Errores: {failed}")
    log(f"SEND newsletter={newsletter_path.name} sent={sent} failed={failed}")


if __name__ == "__main__":
    main()
