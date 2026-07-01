from __future__ import annotations

import argparse
import html
import json
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any

from paths import DOCS_DIR, NOTICIAS_CLASIFICADAS
from web_ui_common import (
    SITE_TITLE,
    SITE_SUBTITLE,
    fecha_hoy_larga,
    masthead_html,
    nav_html as common_nav_html,
    footer_html,
)


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


def numeric_score(value: Any) -> float:
    """Convierte score_docente a número sin asumir una escala 0-100."""
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def editorial_score(n: dict[str, Any]) -> int:
    """Puntuación editorial para ordenar noticias de newsletter.

    Usa campos ya existentes en noticias_clasificadas.json. No crea una
    estructura nueva; solo prioriza mejor las candidatas.
    """
    valor = pick(n, "valor_docente", "valor", "nivel_docente").lower()
    seleccion = normalize_bool(n.get("seleccion_newsletter"))
    generar_ficha = normalize_bool(n.get("generar_ficha"))
    uso = pick(n, "tipo_uso", "uso_propuesto", "uso").lower()
    modulo = pick(n, "modulo_relacionado", "módulo_relacionado", "modulo", "categoria").lower()
    pregunta = pick(n, "pregunta_aula", default="")
    actividad = pick(n, "actividad_breve", default="")
    conceptos = pick(n, "conceptos_clave", "conceptos_modulo", "conceptos_ra", default="")
    ra = pick(n, "ra_asignado", "ra", default="")

    score = 0
    if seleccion:
        score += 100
    if valor == "alto":
        score += 40
    elif valor == "medio":
        score += 15
    if generar_ficha:
        score += 25
    if actividad:
        score += 15
    if pregunta:
        score += 10
    if conceptos:
        score += 10
    if ra:
        score += 5
    if uso in {"caso_empresa", "actividad", "debate"}:
        score += 8
    elif uso == "seguimiento":
        score += 4
    if modulo:
        score += 3

    # score_docente ya existe, pero su escala real es baja; se suma sin
    # convertirla artificialmente a 100.
    score += int(numeric_score(n.get("score_docente")))
    return score


def score_news(n: dict[str, Any]) -> tuple[int, str]:
    fecha = pick(n, "fecha", "published", "fecha_publicacion", default="")
    return editorial_score(n), fecha


def module_key(n: dict[str, Any]) -> str:
    modulo = pick(n, "modulo_relacionado", "módulo_relacionado", "modulo", "categoria", default="")
    modulo = modulo.strip().lower()

    if "electr" in modulo:
        return "comercio_electronico"
    if "digital" in modulo:
        return "digitalizacion"
    if modulo in {"ia", "inteligencia artificial"} or "ia" == modulo:
        return "ia"
    if "internacional" in modulo or modulo == "cdi":
        return "cdi"
    if "marketing" in modulo:
        return "marketing"
    return modulo or "otros"


def module_limit(modulo: str, max_items: int) -> int:
    """Límites suaves para que la newsletter no sea repetitiva."""
    limits = {
        "comercio_electronico": 3,
        "digitalizacion": 2,
        "ia": 1,
        "cdi": 1,
        "marketing": 1,
    }
    return min(limits.get(modulo, 2), max_items)


def valid_news(n: dict[str, Any]) -> bool:
    titulo = pick(n, "titulo", "title")
    url = pick(n, "url", "link", "enlace")
    return bool(titulo and url)


def append_unique(target: list[dict[str, Any]], items: list[dict[str, Any]], seen: set[str]) -> None:
    for n in items:
        url = pick(n, "url", "link", "enlace")
        if url and url not in seen:
            target.append(n)
            seen.add(url)


def select_with_module_balance(candidates: list[dict[str, Any]], max_items: int) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    selected_urls: set[str] = set()
    module_counts: dict[str, int] = {}

    # Primera pasada: respeta límites por módulo.
    for n in candidates:
        if len(selected) >= max_items:
            break
        url = pick(n, "url", "link", "enlace")
        modulo = module_key(n)
        if not url or url in selected_urls:
            continue
        if module_counts.get(modulo, 0) >= module_limit(modulo, max_items):
            continue
        selected.append(n)
        selected_urls.add(url)
        module_counts[modulo] = module_counts.get(modulo, 0) + 1

    # Segunda pasada: si faltan noticias, rellena con las mejores restantes.
    for n in candidates:
        if len(selected) >= max_items:
            break
        url = pick(n, "url", "link", "enlace")
        if url and url not in selected_urls:
            selected.append(n)
            selected_urls.add(url)

    return selected[:max_items]


def select_news(all_news: list[dict[str, Any]], max_items: int) -> list[dict[str, Any]]:
    newsletter_candidates: list[dict[str, Any]] = []
    high_value_candidates: list[dict[str, Any]] = []
    fallback_candidates: list[dict[str, Any]] = []
    seen: set[str] = set()

    for n in all_news:
        if not valid_news(n):
            continue

        url = pick(n, "url", "link", "enlace")
        if not url or url in seen:
            continue
        seen.add(url)

        valor = pick(n, "valor_docente", "valor", "nivel_docente").lower()
        seleccion = normalize_bool(n.get("seleccion_newsletter"))

        if seleccion:
            newsletter_candidates.append(n)
        elif valor == "alto":
            high_value_candidates.append(n)
        else:
            fallback_candidates.append(n)

    newsletter_candidates.sort(key=score_news, reverse=True)
    high_value_candidates.sort(key=score_news, reverse=True)
    fallback_candidates.sort(key=score_news, reverse=True)

    candidates: list[dict[str, Any]] = []
    candidate_urls: set[str] = set()
    append_unique(candidates, newsletter_candidates, candidate_urls)
    append_unique(candidates, high_value_candidates, candidate_urls)

    if len(candidates) < max_items:
        append_unique(candidates, fallback_candidates, candidate_urls)

    return select_with_module_balance(candidates, max_items)


def split_newsletter_sections(noticias: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Divide la selección en bloques editoriales sencillos.

    Mantiene una regla estable y fácil de revisar:
    - 1 noticia destacada
    - hasta 3 noticias para selección docente
    - hasta 2 breves
    """
    return {
        "destacada": noticias[:1],
        "seleccion_docente": noticias[1:4],
        "breves": noticias[4:6],
    }


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
    return common_nav_html(active, base_prefix="../")


def render_masthead() -> str:
    return (
        masthead_html(home_href="../index.html")
        + render_nav("newsletter")
        + "\n"
        + '<div class="subtitle-bar"><span>Selección curada para Formación Profesional</span><span>Comercio, Marketing, Digitalización e IA</span></div>'
    )


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


def render_featured_card(n: dict[str, Any]) -> str:
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
<article class="newsletter-card newsletter-featured-card">
  <div class="newsletter-card-num">★</div>
  <div class="newsletter-card-content">
    <div class="newsletter-kicker">Noticia destacada de la edición</div>
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


def render_brief_card(n: dict[str, Any]) -> str:
    titulo = pick(n, "titulo", "title", default="Sin título")
    url = pick(n, "url", "link", "enlace")
    modulo = pick(n, "modulo_relacionado", "módulo_relacionado", "modulo", "categoria", default="Sin módulo")
    resumen = pick(
        n,
        "resumen_docente",
        "resumen",
        "summary",
        "descripcion",
        "description",
        default="",
    )
    resumen = resumen[:240].rstrip() + ("…" if len(resumen) > 240 else "")

    return f"""
<article class="newsletter-index-card">
  <a href="{e(url)}" target="_blank" rel="noopener">{e(titulo)}</a>
  <p><strong>{e(modulo)}</strong> · {e(resumen)}</p>
</article>
""".strip()


def classroom_prompt(noticia: dict[str, Any] | None) -> str:
    if not noticia:
        return "Elige una noticia de la newsletter y relaciónala con una decisión real de una empresa."

    titulo = pick(noticia, "titulo", "title", default="esta noticia")
    modulo = pick(noticia, "modulo_relacionado", "módulo_relacionado", "modulo", "categoria", default="el módulo")
    uso = pick(noticia, "tipo_uso", "uso_propuesto", "uso", default="actividad")

    return (
        f"A partir de la noticia «{titulo}», plantea una {uso} en la que el alumnado "
        f"relacione el caso con contenidos de {modulo} y proponga una decisión razonada "
        "para una pequeña empresa."
    )


def render_html(noticias: list[dict[str, Any]], periodo: dict[str, str], periodicidad: str) -> str:
    titulo = "Comercio Digital en el aula"
    descripcion = "Newsletter docente de Comercio Digital para trabajar noticias de comercio electrónico, digitalización e IA en el aula."
    sections = split_newsletter_sections(noticias)

    destacada = sections["destacada"][0] if sections["destacada"] else None
    featured_html = render_featured_card(destacada) if destacada else "<p>No hay noticia destacada disponible.</p>"
    seleccion_html = "\n".join(render_card(n, i + 1) for i, n in enumerate(sections["seleccion_docente"]))
    breves_html = "\n".join(render_brief_card(n) for n in sections["breves"])
    propuesta = classroom_prompt(destacada)

    if not seleccion_html:
        seleccion_html = "<p>No hay más noticias docentes seleccionadas en esta edición.</p>"
    if not breves_html:
        breves_html = "<p>No hay breves adicionales en esta edición.</p>"

    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(titulo)} - {e(periodo['label'])}</title>
  <meta name="description" content="{e(descripcion)}">
  <link rel="icon" type="image/svg+xml" href="../assets/favicon.svg">
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

    <h2 class="newsletter-section-title">Noticia destacada</h2>
    <section class="newsletter-list">
      {featured_html}
    </section>

    <h2 class="newsletter-section-title">Selección docente de la quincena</h2>
    <section class="newsletter-list">
      {seleccion_html}
    </section>

    <h2 class="newsletter-section-title">Breves para seguir la actualidad</h2>
    <section class="newsletter-index-list">
      {breves_html}
    </section>

    <section class="newsletter-activity">
      <h2>Propuesta rápida para clase</h2>
      <p>{e(propuesta)}</p>
      <ul>
        <li>Identificar el cambio o tendencia que aparece en la noticia.</li>
        <li>Relacionarlo con contenidos del módulo.</li>
        <li>Proponer una decisión empresarial justificada.</li>
      </ul>
    </section>

    <section class="newsletter-quote">
      ¿Qué noticia de esta edición muestra mejor cómo está cambiando la relación entre tecnología, comercio y cliente?
    </section>

    <div class="newsletter-footer-note">
      Esta newsletter forma parte del proyecto <strong>Comercio Digital</strong>.
      Se genera como material reutilizable para aula, web y distribución externa.
    </div>
  </main>

  {footer_html()}
</body>
</html>
"""


def append_markdown_news(lines: list[str], noticia: dict[str, Any], heading: str) -> None:
    titulo = pick(noticia, "titulo", "title", default="Sin título")
    url = pick(noticia, "url", "link", "enlace")
    resumen = pick(noticia, "resumen_docente", "resumen", "summary", "descripcion", "description", default="")
    modulo = pick(noticia, "modulo_relacionado", "módulo_relacionado", "modulo", "categoria", default="Sin módulo")
    uso = pick(noticia, "tipo_uso", "uso_propuesto", "uso", default="uso docente")
    valor = pick(noticia, "valor_docente", "valor", "nivel_docente", default="sin valorar")

    lines.extend([
        heading,
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

    ficha = ficha_url_for(noticia)
    if ficha:
        lines.extend([f"[Ver ficha de aula]({ficha})", ""])


def render_markdown(noticias: list[dict[str, Any]], periodo: dict[str, str], periodicidad: str) -> str:
    sections = split_newsletter_sections(noticias)
    destacada = sections["destacada"][0] if sections["destacada"] else None

    lines = [
        "# Comercio Digital en el aula",
        "",
        f"## {periodo['label']}",
        "",
        f"Periodicidad: {periodicidad}",
        "",
        "Selección de noticias útiles para trabajar en clase contenidos de comercio electrónico, digitalización, marketing digital e inteligencia artificial aplicada al comercio.",
        "",
        "## Noticia destacada",
        "",
    ]

    if destacada:
        append_markdown_news(lines, destacada, f"### {pick(destacada, 'titulo', 'title', default='Sin título')}")
    else:
        lines.extend(["No hay noticia destacada disponible.", ""])

    lines.extend(["## Selección docente de la quincena", ""])
    for i, n in enumerate(sections["seleccion_docente"], 1):
        append_markdown_news(lines, n, f"### {i}. {pick(n, 'titulo', 'title', default='Sin título')}")

    if not sections["seleccion_docente"]:
        lines.extend(["No hay más noticias docentes seleccionadas en esta edición.", ""])

    lines.extend(["## Breves para seguir la actualidad", ""])
    for n in sections["breves"]:
        titulo = pick(n, "titulo", "title", default="Sin título")
        url = pick(n, "url", "link", "enlace")
        modulo = pick(n, "modulo_relacionado", "módulo_relacionado", "modulo", "categoria", default="Sin módulo")
        lines.extend([f"- **{modulo}:** [{titulo}]({url})"])
    lines.append("")

    lines.extend([
        "## Propuesta rápida para clase",
        "",
        classroom_prompt(destacada),
        "",
        "- Identificar el cambio o tendencia que aparece en la noticia.",
        "- Relacionarlo con contenidos del módulo.",
        "- Proponer una decisión empresarial justificada.",
        "",
        "## Pregunta para debate",
        "",
        "> ¿Qué noticia de esta edición muestra mejor cómo está cambiando la relación entre tecnología, comercio y cliente?",
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
  <link rel="icon" type="image/svg+xml" href="../assets/favicon.svg">
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

  {footer_html()}
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera una newsletter docente en Markdown y HTML.")
    parser.add_argument("--periodicidad", choices=["semanal", "quincenal"], default="quincenal")
    parser.add_argument("--max", type=int, default=6, help="Número máximo de noticias.")
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
