#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

CSS_PATH = Path("docs/assets/style.css")
FAVICON_PATH = Path("docs/assets/favicon.svg")
AULA_PY = Path("generar_aula.py")
FICHAS_PY = Path("generar_fichas_aula.py")

FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" fill="#0d0d0d"/>
  <rect x="0" y="0" width="64" height="6" fill="#8f1717"/>
  <text x="32" y="42" text-anchor="middle" font-size="28" font-family="Georgia, serif" font-weight="700" fill="#f4eadf">CD</text>
</svg>
"""

CSS_APPEND = """
/* -------------------------------------------------------------
   Fichas docentes: diseno final
   ------------------------------------------------------------- */

body.ficha-page .container {
  max-width: 1080px;
}

body.ficha-page .subtitle-bar {
  max-width: 1080px;
}

body.ficha-page .ficha-hero {
  border-bottom: 2px solid #111;
  padding-bottom: 2rem;
  margin-bottom: 2rem;
}

body.ficha-page .ficha-hero.has-img {
  grid-template-columns: minmax(300px, 0.9fr) minmax(360px, 1.1fr);
  gap: 2rem;
  align-items: start;
}

body.ficha-page .lead-img img {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border: 1px solid #cdbfad;
  background: #f4eadf;
}

body.ficha-page .lead-title {
  font-size: clamp(2rem, 3.3vw, 3.7rem);
  line-height: 0.98;
  margin-top: 0.6rem;
  margin-bottom: 1rem;
}

body.ficha-page .lead-summary {
  font-size: 1.05rem;
  line-height: 1.75;
  max-width: 58ch;
}

body.ficha-page .ficha-datos {
  background: #f8f1e8;
  border-top: 3px solid #8f1717;
  border-bottom: 1px solid #d9cbbb;
  margin-top: 1rem;
  margin-bottom: 2.25rem;
  padding: 1.25rem 1.35rem;
}

body.ficha-page .ficha-datos .autor-compact-kicker {
  color: #8f1717;
  font-size: 0.82rem;
  letter-spacing: 0.12em;
}

body.ficha-page .ficha-datos .autor-compact-bio {
  line-height: 1.75;
}

body.ficha-page .ficha-download,
body.ficha-page .ficha-actions .read-more {
  display: inline-block;
  border: 1px solid #8f1717;
  padding: 0.55rem 0.75rem;
  background: #fffaf3;
  text-decoration: none;
}

body.ficha-page .ficha-download:hover,
body.ficha-page .ficha-actions .read-more:hover {
  background: #8f1717;
  color: #fffaf3;
}

body.ficha-page .ficha-section-title {
  font-size: 1.35rem;
  margin: 0 0 0.8rem;
  padding-top: 0.4rem;
  border-top: 1px solid #d4c4b2;
}

body.ficha-page .ficha-aula-card {
  display: block;
  padding-top: 0;
  border-top: 0;
}

body.ficha-page .ficha-docente-box {
  background: #f5eee4;
  border-left: 4px solid #8f1717;
  border-top: 1px solid #d8c8bb;
  border-right: 1px solid #d8c8bb;
  border-bottom: 1px solid #d8c8bb;
  padding: 1.15rem 1.25rem;
  margin: 0.75rem 0 1.5rem;
}

body.ficha-page .ficha-docente-box .docente-box-content {
  padding: 0;
}

body.ficha-page .ficha-docente-box p {
  margin: 0 0 1rem;
  line-height: 1.65;
}

body.ficha-page .ficha-docente-box p:last-child {
  margin-bottom: 0;
}

body.ficha-page .ficha-docente-box strong {
  color: #111;
}

body.ficha-page .conceptos-clave {
  margin: 0.4rem 0 1.1rem;
}

body.ficha-page .concepto-chip {
  display: inline-block;
  margin: 0.18rem 0.25rem 0.18rem 0;
  padding: 0.22rem 0.5rem;
  border: 1px solid #cdbfad;
  border-radius: 999px;
  background: #fffaf3;
  font-size: 0.82rem;
}

body.ficha-page .ficha-dinamica {
  background: #fffaf3;
  border: 1px solid #d8c8bb;
  padding: 1rem 1.15rem;
  margin-bottom: 1.25rem;
}

body.ficha-page .ficha-dinamica p {
  margin: 0;
  line-height: 1.7;
}

body.ficha-page .ficha-actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin-top: 1.25rem;
}

@media (max-width: 900px) {
  body.ficha-page .ficha-hero.has-img {
    grid-template-columns: 1fr;
  }

  body.ficha-page .lead-img img {
    height: 240px;
  }

  body.ficha-page .ficha-datos .autor-compact-head {
    align-items: flex-start;
    flex-direction: column;
    gap: 1rem;
  }
}
"""


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def crear_favicon() -> None:
    FAVICON_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not FAVICON_PATH.exists():
        FAVICON_PATH.write_text(FAVICON_SVG, encoding="utf-8")
        print(f"OK creado {FAVICON_PATH}")
    else:
        print(f"OK ya existe {FAVICON_PATH}")


def patch_aula_py() -> None:
    if not AULA_PY.exists():
        print("AVISO: no existe generar_aula.py")
        return

    text = read(AULA_PY)
    if 'href="assets/favicon.svg"' not in text:
        text = text.replace(
            '<link rel="stylesheet" href="assets/style.css">',
            '<link rel="stylesheet" href="assets/style.css">\\n'
            '  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg">\\n'
            '  <link rel="shortcut icon" href="assets/favicon.svg">'
        )
    write(AULA_PY, text)
    print("OK generar_aula.py actualizado con favicon")


def patch_fichas_py() -> None:
    if not FICHAS_PY.exists():
        print("AVISO: no existe generar_fichas_aula.py")
        return

    text = read(FICHAS_PY)

    if 'href="../assets/favicon.svg"' not in text:
        text = text.replace(
            '<link rel="stylesheet" href="../assets/style.css">',
            '<link rel="stylesheet" href="../assets/style.css">\\n'
            '  <link rel="icon" type="image/svg+xml" href="../assets/favicon.svg">\\n'
            '  <link rel="shortcut icon" href="../assets/favicon.svg">'
        )

    replacements = [
        ("<article class=\"lead-story {'has-img' if img else ''}\">",
         "<article class=\"lead-story ficha-hero {'has-img' if img else ''}\">"),
        ("<section class=\"autor-compact\">",
         "<section class=\"autor-compact ficha-datos\">"),
        ("<a class=\"autor-compact-link\" href=\"{h(md_file)}\">Descargar Markdown →</a>",
         "<a class=\"autor-compact-link ficha-download\" href=\"{h(md_file)}\">Descargar Markdown →</a>"),
        ("<article class=\"noticia-full\">",
         "<article class=\"noticia-full ficha-aula-card\">"),
        ("<h2 class=\"n-title\">Uso en el aula</h2>",
         "<h2 class=\"n-title ficha-section-title\">Uso en el aula</h2>"),
        ("<div class=\"docente-box\">",
         "<div class=\"docente-box ficha-docente-box\">"),
        ("<h2 class=\"n-title\">Propuesta de dinámica</h2>",
         "<h2 class=\"n-title ficha-section-title\">Propuesta de dinámica</h2>"),
        ("""<p class=\"n-summary\">
          <strong>Inicio:</strong> lectura breve de la noticia y contextualización.<br>
          <strong>Desarrollo:</strong> análisis individual, por parejas o en pequeños grupos.<br>
          <strong>Cierre:</strong> puesta en común y conexión con el módulo y el RA.
        </p>""",
         """<div class=\"ficha-dinamica\">
          <p>
            <strong>Inicio:</strong> lectura breve de la noticia y contextualización.<br>
            <strong>Desarrollo:</strong> análisis individual, por parejas o en pequeños grupos.<br>
            <strong>Cierre:</strong> puesta en común y conexión con el módulo y el RA.
          </p>
        </div>"""),
        ("""<a class=\"read-more\" href=\"{url}\" target=\"_blank\" rel=\"noopener\">Leer noticia original →</a>
        <a class=\"read-more\" href=\"../aula.html\">Volver a Aula →</a>""",
         """<div class=\"ficha-actions\">
          <a class=\"read-more\" href=\"{url}\" target=\"_blank\" rel=\"noopener\">Leer noticia original →</a>
          <a class=\"read-more\" href=\"../aula.html\">Volver a Aula →</a>
        </div>"""),
    ]

    for old, new in replacements:
        text = text.replace(old, new)

    write(FICHAS_PY, text)
    print("OK generar_fichas_aula.py actualizado con favicon y clases visuales")


def patch_css() -> None:
    if not CSS_PATH.exists():
        print(f"AVISO: no existe {CSS_PATH}")
        return

    text = read(CSS_PATH)
    marker = "Fichas docentes: diseno final"
    if marker not in text:
        text = text.rstrip() + "\\n\\n" + CSS_APPEND.strip() + "\\n"
        write(CSS_PATH, text)
        print("OK style.css actualizado con estilos de fichas")
    else:
        print("OK style.css ya contenia los estilos de fichas")


def main() -> None:
    crear_favicon()
    patch_aula_py()
    patch_fichas_py()
    patch_css()

    print("\\nAhora ejecuta:")
    print("  python generar_fichas_aula.py --max-fichas 10 --limpiar")
    print("  python generar_aula.py --max-noticias 25")
    print("  python generar_seo.py")


if __name__ == "__main__":
    main()
