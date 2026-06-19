from __future__ import annotations

import argparse
import html
import json
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any

from paths import DOCS_DIR, NOTICIAS_CLASIFICADAS


NEWSLETTER_DIR = DOCS_DIR / "newsletter"
FICHAS_DIR = DOCS_DIR / "fichas-aula"


def e(value: Any) -> str:
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def slugify(text: str) -> str:
    text = (text or "").strip().lower()
    replacements = {
        "á": "a", "à": "a", "ä": "a",
        "é": "e", "è": "e", "ë": "e",
        "í": "i", "ì": "i", "ï": "i",
        "ó": "o", "ò": "o", "ö": "o",
        "ú": "u", "ù": "u", "ü": "u",
        "ñ": "n", "ç": "c",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:90]


def load_json(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"No existe el archivo de noticias: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def flatten_news(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]

    if isinstance(data, dict):
        for key in ("noticias", "items", "data", "resultados"):
            if isinstance(data.get(key), list):
                return [x for x in data[key] if isinstance(x, dict)]

        noticias: list[dict[str, Any]] = []
        for value in data.values():
            if isinstance(value, list):
                noticias.extend(x for x in value if isinstance(x, dict))
        return noticias

    return []


def pick(n: dict[str, Any], *keys: str, default: str = "") -> str:
    for key in keys:
        value = n.get(key)
        if value not in (None, ""):
            return str(value)
    return default


def normalize_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "sí", "si", "yes", "y"}


def score_news(n: dict[str, Any]) -> tuple[int, str]:
    valor = pick(n, "valor_docente", "valor", "nivel_docente").lower()
    seleccion = normalize_bool(n.get("seleccion_newsletter"))
    uso = pick(n, "tipo_uso", "uso_propuesto", "uso").lower()
    modulo = pick(n, "modulo_relacionado", "módulo_relacionado", "modulo", "categoria").lower()

    score = 0
    if seleccion:
        score += 100
    if valor == "alto":
        score += 50
    elif valor == "medio":
        score += 20
    if uso in {"actividad", "caso_empresa", "debate", "seguimiento"}:
        score += 10
    if modulo:
        score += 5

    fecha = pick(n, "fecha", "published", "fecha_publicacion", default="")
    return score, fecha


def select_news(all_news: list[dict[str, Any]], max_items: int) -> list[dict[str, Any]]:
    candidates = []
    for n in all_news:
        titulo = pick(n, "titulo", "title")
        url = pick(n, "url", "link", "enlace")
        if not titulo or not url:
            continue

        valor = pick(n, "valor_docente", "valor", "nivel_docente").lower()
        seleccion = normalize_bool(n.get("seleccion_newsletter"))

        if seleccion or valor == "alto":
            candidates.append(n)

    if len(candidates) < max_items:
        seen = {pick(x, "url", "link", "enlace") for x in candidates}
        for n in all_news:
            url = pick(n, "url", "link", "enlace")
            if url and url not in seen:
                candidates.append(n)
                seen.add(url)
            if len(candidates) >= max_items:
                break

    candidates.sort(key=score_news, reverse=True)
    return candidates[:max_items]


def period_info(fecha: date, periodicidad: str) -> dict[str, str]:
    iso_year, iso_week, _ = fecha.isocalendar()

    if periodicidad == "quincenal":
        quincena = 1 if fecha.day <= 15 else 2
        label = f"Quincena {quincena} de {fecha.month:02d}/{fecha.year}"
        slug = f"{fecha.year}-{fecha.month:02d}-Q{quincena}"
    else:
        label = f"Semana {iso_week} de {iso_year}"
        slug = f"{iso_year}-W{iso_week:02d}"

    return {
        "label": label,
        "slug": slug,
    }


def ficha_url_for(noticia: dict[str, Any]) -> str:
    explicit = pick(
        noticia,
        "ficha_html",
        "ruta_ficha_html",
        "url_ficha",
        "ficha_aula_html",
        default="",
    )
    if explicit:
        explicit = explicit.replace("\\", "/")
        if explicit.endswith(".html"):
            if explicit.startswith("docs/"):
                explicit = explicit[5:]
            if explicit.startswith("fichas-aula/"):
                return "../" + explicit
            return explicit

    titulo = pick(noticia, "titulo", "title")
    slug = slugify(titulo)
    if not slug or not FICHAS_DIR.exists():
        return ""

    for path in sorted(FICHAS_DIR.glob("*.html")):
        name = path.stem.lower()
        if slug[:45] and slug[:45] in name:
            return "../fichas-aula/" + path.name

    return ""


def render_nav(active: str = "newsletter") -> str:
    """Menú principal de las páginas de newsletter.

    Usa rutas relativas porque los HTML viven dentro de docs/newsletter/.
    Debe mantenerse alineado con el menú generado por generar_web.py,
    generar_aula.py y generar_fichas_aula.py.
    """
    def active_class(name: str) -> str:
        return ' class="active"' if name == active else ""

    return f"""
<nav class="site-nav">
  <input type="checkbox" id="nav-toggle" class="nav-toggle">
  <label for="nav-toggle" class="nav-toggle-label" aria-label="Abrir menú">
    <span></span><span></span><span></span><strong>Menú</strong>
  </label>
  <ul class="nav-menu">
    <li><a href="../index.html"{active_class("portada")}>Portada</a></li>
    <li><a href="../comercio-electronico.html"{active_class("comercio-electronico")}>Comercio Electrónico</a></li>
    <li><a href="../internacional.html"{active_class("internacional")}>Internacional</a></li>
    <li><a href="../digitalizacion.html"{active_class("digitalizacion")}>Digitalización</a></li>
    <li><a href="../ia-marketing.html"{active_class("ia-marketing")}>IA y Marketing</a></li>
    <li><a href="../aula.html"{active_class("aula")}>Aula</a></li>
    <li><a href="index.html"{active_class("newsletter")}>Newsletter</a></li>
    <li><a href="../del-autor.html"{active_class("del-autor")}>Del Autor</a></li>
  </ul>
</nav>
""".strip()


def render_masthead() -> str:
    hoy = date.today().strftime("%d/%m/%Y")
    return f"""
<header class="masthead">
  <div class="masthead-side">Noticias, aula y comercio digital</div>
  <div class="site-title"><a href="../index.html">Comercio Digital</a></div>
  <div class="masthead-side right">Newsletter docente<br>{hoy}</div>
</header>
{render_nav("newsletter")}
<div class="subtitle-bar">
  <span>Selección curada para Formación Profesional</span>
  <span>Comercio, Marketing, Digitalización e IA</span>
</div>
""".strip()


def render_card(n: dict[str, Any], number: int) -> str:
    titulo = pick(n, "titulo", "title", default="Sin título")
    url = pick(n, "url", "link", "enlace")
    resumen = pick(
        n,
        "resumen_docente",
        "resumen",
        "summary",
        "descripcion",
        "description",
        default="Sin resumen disponible.",
    )
    modulo = pick(n, "modulo_relacionado", "módulo_relacionado", "modulo", "categoria", default="Sin módulo")
    uso = pick(n, "tipo_uso", "uso_propuesto", "uso", default="uso docente")
    valor = pick(n, "valor_docente", "valor", "nivel_docente", default="sin valorar")
    ficha = ficha_url_for(n)

    ficha_btn = ""
    if ficha:
        ficha_btn = f'<a class="newsletter-btn newsletter-btn-secondary" href="{e(ficha)}">Ver ficha de aula</a>'

    return f"""
<article class="newsletter-card">
  <div class="newsletter-card-num">{number:02d}</div>
  <div class="newsletter-card-content">
    <h2>{e(titulo)}</h2>
    <div class="newsletter-tags">
      <span class="newsletter-tag">{e(modulo)}</span>
      <span class="newsletter-tag secondary">{e(uso)}</span>
      <span class="newsletter-tag success">Valor docente: {e(valor)}</span>
    </div>
    <p>{e(resumen)}</p>
    <div class="newsletter-actions">
      <a class="newsletter-btn" href="{e(url)}" target="_blank" rel="noopener">Leer noticia</a>
      {ficha_btn}
    </div>
  </div>
</article>
""".strip()


def render_html(noticias: list[dict[str, Any]], periodo: dict[str, str], periodicidad: str) -> str:
    titulo = "Comercio Digital en el aula"
    descripcion = "Newsletter docente de Comercio Digital para trabajar noticias de comercio electrónico, digitalización e IA en el aula."
    cards = "\n".join(render_card(n, i + 1) for i, n in enumerate(noticias))

    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(titulo)} - {e(periodo['label'])}</title>
  <meta name="description" content="{e(descripcion)}">
  <link rel="stylesheet" href="../assets/style.css">
</head>
<body class="newsletter-body">
  {render_masthead()}

  <main class="container newsletter-page">
    <a class="newsletter-back" href="index.html">← Volver al índice de newsletters</a>

    <section class="newsletter-hero">
      <div class="newsletter-kicker">Newsletter docente</div>
      <h1>{e(titulo)}</h1>
      <p class="newsletter-subtitle">
        Selección de noticias útiles para trabajar en clase contenidos de comercio electrónico,
        digitalización, marketing digital e inteligencia artificial aplicada al comercio.
      </p>
      <div class="newsletter-meta">
        <span class="newsletter-meta-badge">{e(periodo['label'])}</span>
        <span class="newsletter-meta-badge">{len(noticias)} noticias seleccionadas</span>
        <span class="newsletter-meta-badge">Periodicidad: {e(periodicidad)}</span>
      </div>
    </section>

    <div class="newsletter-intro">
      Esta edición resume noticias con posible uso didáctico para abrir una clase, plantear un debate,
      proponer una actividad breve o conectar contenidos del módulo con casos reales del sector.
    </div>

    <h2 class="newsletter-section-title">Noticias destacadas</h2>

    <section class="newsletter-list">
      {cards}
    </section>

    <section class="newsletter-activity">
      <h2>Propuesta rápida para clase</h2>
      <p>Elige una de las noticias destacadas y pide al alumnado que identifique:</p>
      <ul>
        <li>Qué cambio introduce en el comercio digital.</li>
        <li>Qué impacto puede tener en consumidores, empresas o canales de venta.</li>
        <li>Qué decisión tomaría una empresa pequeña ante esa situación.</li>
      </ul>
    </section>

    <section class="newsletter-quote">
      ¿Qué noticia muestra mejor cómo está cambiando la relación entre tecnología, comercio y cliente?
    </section>

    <div class="newsletter-footer-note">
      Esta newsletter forma parte del proyecto <strong>Comercio Digital</strong>.
      Se genera como material reutilizable para aula, web y distribución externa.
    </div>
  </main>

  <footer>
    <strong>Comercio Digital</strong> · Noticias y recursos docentes para Formación Profesional.
  </footer>
</body>
</html>
"""


def render_markdown(noticias: list[dict[str, Any]], periodo: dict[str, str], periodicidad: str) -> str:
    lines = [
        "# Comercio Digital en el aula",
        "",
        f"## {periodo['label']}",
        "",
        f"Periodicidad: {periodicidad}",
        "",
        "Selección de noticias útiles para trabajar en clase contenidos de comercio electrónico, digitalización, marketing digital e inteligencia artificial aplicada al comercio.",
        "",
        "## Noticias destacadas",
        "",
    ]

    for i, n in enumerate(noticias, 1):
        titulo = pick(n, "titulo", "title", default="Sin título")
        url = pick(n, "url", "link", "enlace")
        resumen = pick(n, "resumen_docente", "resumen", "summary", "descripcion", "description", default="")
        modulo = pick(n, "modulo_relacionado", "módulo_relacionado", "modulo", "categoria", default="Sin módulo")
        uso = pick(n, "tipo_uso", "uso_propuesto", "uso", default="uso docente")
        valor = pick(n, "valor_docente", "valor", "nivel_docente", default="sin valorar")

        lines.extend([
            f"### {i}. {titulo}",
            "",
            f"**Módulo relacionado:** {modulo}",
            "",
            f"**Uso propuesto:** {uso}",
            "",
            f"**Valor docente:** {valor}",
            "",
            resumen,
            "",
            f"[Leer noticia original]({url})",
            "",
        ])

        ficha = ficha_url_for(n)
        if ficha:
            lines.extend([f"[Ver ficha de aula]({ficha})", ""])

    lines.extend([
        "## Propuesta rápida para clase",
        "",
        "Elige una de las noticias destacadas y pide al alumnado que identifique:",
        "",
        "- Qué cambio introduce en el comercio digital.",
        "- Qué impacto puede tener en consumidores, empresas o canales de venta.",
        "- Qué decisión tomaría una empresa pequeña ante esa situación.",
        "",
        "## Pregunta para debate",
        "",
        "> ¿Qué noticia muestra mejor cómo está cambiando la relación entre tecnología, comercio y cliente?",
        "",
    ])

    return "\n".join(lines)


def render_index() -> str:
    files = sorted(NEWSLETTER_DIR.glob("newsletter-*.html"), reverse=True)
    cards = []
    for f in files:
        title = f.stem.replace("newsletter-", "Newsletter ")
        cards.append(f"""
<article class="newsletter-index-card">
  <a href="{e(f.name)}">{e(title)}</a>
  <p>Edición publicada en formato HTML. También puede existir su versión Markdown en la misma carpeta.</p>
</article>
""".strip())

    cards_html = "\n".join(cards) if cards else "<p>Todavía no hay newsletters generadas.</p>"

    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Newsletter | Comercio Digital</title>
  <meta name="description" content="Archivo de newsletters docentes de Comercio Digital.">
  <link rel="stylesheet" href="../assets/style.css">
</head>
<body class="newsletter-body">
  {render_masthead()}

  <main class="container newsletter-page">
    <section class="newsletter-hero">
      <div class="newsletter-kicker">Archivo</div>
      <h1>Newsletter</h1>
      <p class="newsletter-subtitle">
        Selecciones periódicas de noticias para trabajar en clase contenidos de comercio electrónico,
        digitalización, marketing digital e inteligencia artificial.
      </p>
    </section>

    <h2 class="newsletter-section-title">Ediciones disponibles</h2>
    <section class="newsletter-index-list">
      {cards_html}
    </section>
  </main>

  <footer>
    <strong>Comercio Digital</strong> · Noticias y recursos docentes para Formación Profesional.
  </footer>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera una newsletter docente en Markdown y HTML.")
    parser.add_argument("--periodicidad", choices=["semanal", "quincenal"], default="semanal")
    parser.add_argument("--max", type=int, default=5, help="Número máximo de noticias.")
    parser.add_argument("--fecha", default="", help="Fecha base en formato YYYY-MM-DD.")
    parser.add_argument("--force", action="store_true", help="Sobrescribe si la newsletter ya existe.")
    args = parser.parse_args()

    fecha = datetime.strptime(args.fecha, "%Y-%m-%d").date() if args.fecha else date.today()
    periodo = period_info(fecha, args.periodicidad)

    NEWSLETTER_DIR.mkdir(parents=True, exist_ok=True)

    out_md = NEWSLETTER_DIR / f"newsletter-{periodo['slug']}.md"
    out_html = NEWSLETTER_DIR / f"newsletter-{periodo['slug']}.html"
    out_index = NEWSLETTER_DIR / "index.html"

    if out_html.exists() and not args.force:
        print(f"Ya existe: {out_html}")
        print("Usa --force para regenerarla.")
        return

    data = load_json(NOTICIAS_CLASIFICADAS)
    noticias = select_news(flatten_news(data), args.max)

    if not noticias:
        raise RuntimeError("No se han encontrado noticias válidas para generar la newsletter.")

    out_md.write_text(render_markdown(noticias, periodo, args.periodicidad), encoding="utf-8")
    out_html.write_text(render_html(noticias, periodo, args.periodicidad), encoding="utf-8")
    out_index.write_text(render_index(), encoding="utf-8")

    print("Newsletter generada correctamente:")
    print(f"- {out_md}")
    print(f"- {out_html}")
    print(f"- {out_index}")


if __name__ == "__main__":
    main()
