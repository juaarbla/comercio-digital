# -*- coding: utf-8 -*-
"""
SEO técnico para Comercio Digital.

Procesa los HTML ya generados en docs/ y añade o actualiza:
- title específico
- meta description específica
- canonical
- Open Graph
- Twitter Card
- sitemap.xml
- robots.txt
- JSON-LD Schema.org básico en portada

Uso:
    python generar_seo.py
"""

import html
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

from schema_utils import insertar_jsonld, schema_portada_basico

DOCS_DIR = Path("docs")
SITE_URL = "https://comerciodigital.net"
SITE_NAME = "Comercio Digital"
DEFAULT_DESCRIPTION = (
    "Actualidad de comercio, marketing, digitalización e inteligencia artificial "
    "seleccionada y preparada para trabajar en el aula de Formación Profesional."
)

SEO_SECCIONES = {
    "index.html": {
        "title": "Comercio Digital | Actualidad para el aula de FP",
        "description": (
            "Noticias de comercio electrónico, marketing, digitalización e inteligencia "
            "artificial clasificadas por resultados de aprendizaje y preparadas para FP."
        ),
    },
    "comercio-electronico.html": {
        "title": "Noticias de comercio electrónico para FP | Comercio Digital",
        "description": (
            "Actualidad de ecommerce, marketplaces, logística, pagos y marketing digital "
            "clasificada por resultados de aprendizaje para trabajar en el aula de FP."
        ),
    },
    "internacional.html": {
        "title": "Comercio digital internacional para FP | Comercio Digital",
        "description": (
            "Noticias sobre comercio electrónico internacional, mercados digitales, "
            "plataformas globales, aduanas y operativa exterior para Formación Profesional."
        ),
    },
    "digitalizacion.html": {
        "title": "Noticias de digitalización para FP | Comercio Digital",
        "description": (
            "Actualidad sobre transformación digital, automatización, datos, tecnologías "
            "habilitadoras y ciberseguridad aplicada a la empresa y al aula de FP."
        ),
    },
    "ia-marketing.html": {
        "title": "Inteligencia artificial y marketing para FP | Comercio Digital",
        "description": (
            "Noticias sobre inteligencia artificial aplicada al marketing, comercio, "
            "contenidos, automatización y atención al cliente para trabajar en FP."
        ),
    },
    "marketing.html": {
        "title": "Noticias de marketing digital para FP | Comercio Digital",
        "description": (
            "Campañas, redes sociales, publicidad, contenidos y tendencias de marketing "
            "digital seleccionadas para su uso educativo en Formación Profesional."
        ),
    },
    "del-autor.html": {
        "title": "Artículos de Juan Armada | Comercio Digital",
        "description": (
            "Artículos, recursos y contenidos propios de Juan Armada sobre comercio, "
            "marketing, digitalización, inteligencia artificial y Formación Profesional."
        ),
    },
    "otros.html": {
        "title": "Otras noticias digitales para FP | Comercio Digital",
        "description": (
            "Selección complementaria de noticias digitales relacionadas con empresa, "
            "tecnología, comercio y marketing para el aula de Formación Profesional."
        ),
    },
}


def pagina_base(nombre: str) -> str:
    """Relaciona una página paginada con su página principal."""
    return re.sub(r"-p\d+\.html$", ".html", nombre)


def datos_seo(nombre: str) -> tuple[str, str]:
    base = pagina_base(nombre)
    datos = SEO_SECCIONES.get(base)

    if datos:
        title = datos["title"]
        description = datos["description"]
    else:
        etiqueta = Path(nombre).stem.replace("-", " ").title()
        title = f"{etiqueta} | {SITE_NAME}"
        description = DEFAULT_DESCRIPTION

    match = re.search(r"-p(\d+)\.html$", nombre)
    if match:
        pagina = match.group(1)
        title = f"{title} — Página {pagina}"

    return title, description


def canonical_url(nombre: str) -> str:
    if nombre == "index.html":
        return f"{SITE_URL}/"
    return f"{SITE_URL}/{quote(nombre)}"


def reemplazar_o_insertar(texto: str, patron: str, etiqueta: str) -> str:
    if re.search(patron, texto, flags=re.IGNORECASE | re.DOTALL):
        return re.sub(
            patron,
            lambda _: etiqueta,
            texto,
            count=1,
            flags=re.IGNORECASE | re.DOTALL,
        )
    return texto.replace("</head>", f"  {etiqueta}\n</head>", 1)


def actualizar_html(ruta: Path) -> None:
    texto = ruta.read_text(encoding="utf-8-sig")
    title, description = datos_seo(ruta.name)
    canonical = canonical_url(ruta.name)

    title_esc = html.escape(title, quote=True)
    desc_esc = html.escape(description, quote=True)
    canonical_esc = html.escape(canonical, quote=True)
    site_esc = html.escape(SITE_NAME, quote=True)

    texto = reemplazar_o_insertar(
        texto,
        r"<title>.*?</title>",
        f"<title>{title_esc}</title>",
    )
    texto = reemplazar_o_insertar(
        texto,
        r'<meta\s+name=["\']description["\'][^>]*>',
        f'<meta name="description" content="{desc_esc}">',
    )
    texto = reemplazar_o_insertar(
        texto,
        r'<link\s+rel=["\']canonical["\'][^>]*>',
        f'<link rel="canonical" href="{canonical_esc}">',
    )

    etiquetas = [
        (
            r'<meta\s+property=["\']og:title["\'][^>]*>',
            f'<meta property="og:title" content="{title_esc}">',
        ),
        (
            r'<meta\s+property=["\']og:description["\'][^>]*>',
            f'<meta property="og:description" content="{desc_esc}">',
        ),
        (
            r'<meta\s+property=["\']og:url["\'][^>]*>',
            f'<meta property="og:url" content="{canonical_esc}">',
        ),
        (
            r'<meta\s+property=["\']og:type["\'][^>]*>',
            '<meta property="og:type" content="website">',
        ),
        (
            r'<meta\s+property=["\']og:site_name["\'][^>]*>',
            f'<meta property="og:site_name" content="{site_esc}">',
        ),
        (
            r'<meta\s+name=["\']twitter:card["\'][^>]*>',
            '<meta name="twitter:card" content="summary">',
        ),
        (
            r'<meta\s+name=["\']twitter:title["\'][^>]*>',
            f'<meta name="twitter:title" content="{title_esc}">',
        ),
        (
            r'<meta\s+name=["\']twitter:description["\'][^>]*>',
            f'<meta name="twitter:description" content="{desc_esc}">',
        ),
    ]

    for patron, etiqueta in etiquetas:
        texto = reemplazar_o_insertar(texto, patron, etiqueta)

    # v0.7 · Schema.org básico global
    # Primera integración controlada: solo portada.
    if ruta.name == "index.html":
        texto = insertar_jsonld(
            texto,
            schema_portada_basico(),
            reemplazar_existente=True,
        )

    ruta.write_text(texto, encoding="utf-8-sig")


def generar_sitemap(html_files: list[Path]) -> None:
    urls = []

    for ruta in sorted(html_files, key=lambda p: (p.name != "index.html", p.name)):
        canonical = canonical_url(ruta.name)
        fecha = datetime.fromtimestamp(
            ruta.stat().st_mtime,
            tz=timezone.utc,
        ).date().isoformat()

        urls.append(
            "  <url>\n"
            f"    <loc>{html.escape(canonical)}</loc>\n"
            f"    <lastmod>{fecha}</lastmod>\n"
            "  </url>"
        )

    contenido = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )

    (DOCS_DIR / "sitemap.xml").write_text(contenido, encoding="utf-8")


def generar_robots() -> None:
    contenido = (
        "User-agent: *\n"
        "Allow: /\n\n"
        f"Sitemap: {SITE_URL}/sitemap.xml\n"
    )
    (DOCS_DIR / "robots.txt").write_text(contenido, encoding="utf-8")


def main() -> None:
    if not DOCS_DIR.exists():
        print("No se encuentra la carpeta docs/. Ejecuta primero generar_web.py")
        raise SystemExit(1)

    html_files = sorted(DOCS_DIR.glob("*.html"))

    if not html_files:
        print("No se encontraron archivos HTML en docs/.")
        raise SystemExit(1)

    print("Aplicando SEO técnico...")

    for ruta in html_files:
        actualizar_html(ruta)
        print(f"  Metadatos -> {ruta}")

    generar_sitemap(html_files)
    print(f"  Sitemap -> {DOCS_DIR / 'sitemap.xml'}")

    generar_robots()
    print(f"  Robots -> {DOCS_DIR / 'robots.txt'}")

    print(f"\nSEO aplicado a {len(html_files)} páginas HTML.")


if __name__ == "__main__":
    main()
