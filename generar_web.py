# -*- coding: utf-8 -*-
"""
Generador web Comercio Digital
Portada + páginas de sección - estilo periódico clásico
"""

import json
import math
import html
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse

from dotenv import load_dotenv

load_dotenv()

INPUT_FILE = Path("noticias_clasificadas.json")

def limpiar_texto(texto: str) -> str:
    import re as _re
    if not texto:
        return ""
    try:
        texto = texto.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass
    for mal, bien in [
        ("“", '"'), ("”", '"'),
        ("‘", "'"), ("’", "'"),
        ("…", "..."),
        ("–", "-"), ("—", "-"),
    ]:
        texto = texto.replace(mal, bien)
    texto = _re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", texto)
    texto = _re.sub(r"\*(.+?)\*",     r"<em>\1</em>",         texto)
    texto = _re.sub(r"`(.+?)`",       r"<code>\1</code>",     texto)
    return texto
DOCS_DIR = Path("docs")

SITE_TITLE = "Comercio Digital"
SITE_SUBTITLE = "La actualidad del sector para el aula de FP"
SITE_URL = "https://comerciodigital.net"

NOTICIAS_PORTADA_POR_SECCION = 3
NOTICIAS_POR_PAGINA = 8

SECCIONES = [
    {"id": "comercio-electronico", "modulos": ["Comercio Electrónico"], "label": "E-Commerce", "file": "comercio-electronico.html"},
    {"id": "internacional", "modulos": ["Comercio Digital Internacional"], "label": "Internacional", "file": "internacional.html"},
    {"id": "digitalizacion", "modulos": ["Digitalización GM", "Digitalización GS"], "label": "Digitalización", "file": "digitalizacion.html"},
    {"id": "ia-marketing", "modulos": ["IA para Marketing y Comercio"], "label": "IA & Marketing", "file": "ia-marketing.html"},
    {"id": "marketing", "modulos": ["Marketing Digital"], "label": "Marketing", "file": "marketing.html"},
    {"id": "del-autor", "modulos": ["Del Autor"], "label": "Del Autor", "file": "del-autor.html"},
    {"id": "otros", "modulos": [], "label": "Otros", "file": "otros.html"},
]

MODULO_ALIASES = {
    "Comercio Electr�nico": "Comercio Electrónico",
    "Comercio ElectrÃ³nico": "Comercio Electrónico",
    "Digitalizaci�n": "Digitalización",
    "DigitalizaciÃ³n": "Digitalización",
    "Digitalizaci�n GM": "Digitalización GM",
    "DigitalizaciÃ³n GM": "Digitalización GM",
    "Digitalizaci�n GS": "Digitalización GS",
    "DigitalizaciÃ³n GS": "Digitalización GS",
}

def normalizar_modulo(modulo: str) -> str:
    raw = str(modulo or "").strip()
    return MODULO_ALIASES.get(raw, raw)


def es_contenido_propio(n: dict) -> bool:
    url = (n.get("url") or "").lower()
    return "juanarmada.com" in url


def seccion_del_autor() -> dict | None:
    return next((s for s in SECCIONES if s["id"] == "del-autor"), None)

def modulo_a_seccion(modulo: str) -> dict | None:
    modulo = normalizar_modulo(modulo)
    if modulo == "Digitalización":
        return next((s for s in SECCIONES if s["id"] == "digitalizacion"), None)
    for seccion in SECCIONES:
        if modulo in seccion["modulos"]:
            return seccion
    return None


def esc_text(value: str) -> str:
    return html.escape(str(value or ""), quote=False)


def esc_attr(value: str) -> str:
    return html.escape(str(value or ""), quote=True)


def _valid_http_url(value: str) -> str:
    raw = str(value or "").strip()
    if not raw:
        return ""
    parsed = urlparse(raw)
    if parsed.scheme in ("http", "https") and parsed.netloc:
        return raw
    return ""


def safe_href(value: str) -> str:
    return _valid_http_url(value) or "#"


def safe_src(value: str) -> str:
    return _valid_http_url(value)


def fecha_orden(noticia: dict) -> float:
    from email.utils import parsedate_to_datetime

    for field in ("fecha_publicacion", "procesado_en"):
        raw = noticia.get(field, "")
        if not raw:
            continue
        try:
            if field == "procesado_en":
                dt = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
            else:
                dt = parsedate_to_datetime(raw)
            if dt.tzinfo is None:
                from datetime import timezone
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.timestamp()
        except Exception:
            continue
    return 0.0


def fecha_hoy() -> str:
    hoy = datetime.now()
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    return f"{dias[hoy.weekday()]}, {hoy.day} de {meses[hoy.month - 1]} de {hoy.year}"


def formatear_fecha(s: str) -> str:
    try:
        from email.utils import parsedate_to_datetime

        dt = parsedate_to_datetime(s)
        meses = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
        return f"{dt.day} {meses[dt.month - 1]}. {dt.year}"
    except Exception:
        return s[:10] if s else ""


def nav_html(activa: str = "", secciones_con_noticias: set = None) -> str:
    items = '<li><a href="index.html">Portada</a></li>\n'
    for seccion in SECCIONES:
        if secciones_con_noticias is not None and seccion["id"] not in secciones_con_noticias:
            continue
        cls = ' class="active"' if seccion["id"] == activa else ""
        items += f'    <li><a href="{seccion["file"]}"{cls}>{seccion["label"]}</a></li>\n'
    return f'<nav><ul>{items}</ul></nav>'


def masthead_html(subtitulo: str = "") -> str:
    return f"""
  <header>
    <div class="masthead">
      <div class="masthead-side">Formaci&oacute;n Profesional<br>Comercio y Marketing</div>
      <div class="site-title"><a href="index.html">{SITE_TITLE}</a></div>
      <div class="masthead-side right">{fecha_hoy()}<br>{SITE_URL.replace("https://","")}</div>
    </div>
  </header>"""


def footer_html() -> str:
    return f"""
  <footer>
    <strong>{SITE_TITLE}</strong> &middot; Generado el {fecha_hoy()} &middot;
    Res&uacute;menes generados con IA a partir de fuentes p&uacute;blicas &middot;
    Uso educativo &mdash; FP Comercio y Marketing CV
  </footer>"""


def head_html(titulo: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{titulo} &mdash; {SITE_TITLE}</title>
  <meta name="description" content="{SITE_SUBTITLE}">
  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>"""


def tipo_badge_html(tipo: str) -> str:
    if tipo == "podcast":
        return '<span class="tipo-badge tipo-podcast">&#127911; Podcast</span>'
    if tipo in ("video", "videotutorial"):
        return '<span class="tipo-badge tipo-video">&#9654; V&iacute;deo</span>'
    return '<span class="tipo-badge tipo-articulo">&#9998; Art&iacute;culo</span>'


def badge_html(n: dict, seccion: dict | None = None) -> str:
    modulo = n.get("modulo_asignado") or n.get("modulo", "")
    fecha = formatear_fecha(n.get("fecha_publicacion", ""))
    fecha_html = f'<span class="fecha">{esc_text(fecha)}</span>' if fecha else ""

    if modulo == "Del Autor":
        tipo = n.get("tipo", "articulo")
        return f'<div class="meta">{tipo_badge_html(tipo)}{fecha_html}</div>'

    cat = seccion["label"] if seccion else modulo[:20]
    ra = n.get("ra_asignado", "")
    ra_html = f'<span class="ra-badge">{esc_text(ra)}</span>' if ra and ra != "Sin clasificar" else ""
    return f'<div class="meta"><span class="cat-badge">{esc_text(cat)}</span>{ra_html}{fecha_html}</div>'


def card_lead(n: dict, seccion: dict | None = None) -> str:
    img = safe_src(n.get("imagen_url", ""))
    url = safe_href(n.get("url", ""))
    titulo = esc_text(n.get("titulo", ""))
    resumen = limpiar_texto(n.get("resumen", ""))
    cls = "lead-story has-img" if img else "lead-story"
    img_html = f'<div class="lead-img"><img src="{esc_attr(img)}" alt=""></div>' if img else ""
    return f"""
    <article class="{cls}">
      {img_html}
      <div>
        {badge_html(n, seccion)}
        <h2 class="lead-title"><a href="{esc_attr(url)}" target="_blank" rel="noopener noreferrer">{titulo}</a></h2>
        <p class="lead-summary">{resumen}</p>
        <a href="{esc_attr(url)}" class="read-more" target="_blank" rel="noopener noreferrer">Leer noticia completa &rarr;</a>
      </div>
    </article>"""
def card_story(n: dict, seccion: dict | None = None) -> str:
    url = safe_href(n.get("url", ""))
    titulo = esc_text(n.get("titulo", ""))
    resumen = limpiar_texto(n.get("resumen", ""))
    return f"""
      <div class="story-card">
        {badge_html(n, seccion)}
        <div class="story-title"><a href="{esc_attr(url)}" target="_blank" rel="noopener noreferrer">{titulo}</a></div>
        <div class="story-summary">{resumen[:180]}&hellip;</div>
        <a href="{esc_attr(url)}" class="read-more" target="_blank" rel="noopener noreferrer">Leer &rarr;</a>
      </div>"""


def docente_html(n: dict) -> str:
    pregunta = limpiar_texto(n.get("pregunta_aula", ""))
    actividad = limpiar_texto(n.get("actividad_breve", ""))
    conceptos = n.get("conceptos_clave", [])

    if isinstance(conceptos, str):
        conceptos = [c.strip() for c in conceptos.split(",") if c.strip()]
    elif not isinstance(conceptos, list):
        conceptos = []

    conceptos = [esc_text(c) for c in conceptos if str(c).strip()]

    if not pregunta and not actividad and not conceptos:
        return ""

    pregunta_html = f'<p><strong>Pregunta para el aula:</strong> {pregunta}</p>' if pregunta else ""
    actividad_html = f'<p><strong>Actividad breve:</strong> {actividad}</p>' if actividad else ""

    conceptos_html = ""
    if conceptos:
        chips = "".join(f'<span class="concepto-chip">{c}</span>' for c in conceptos)
        conceptos_html = f'<div class="conceptos-clave"><strong>Conceptos clave:</strong> {chips}</div>'

    return f"""
        <details class="docente-box">
          <summary class="docente-box-title">Uso en el aula</summary>
          <div class="docente-box-content">
            {pregunta_html}
            {actividad_html}
            {conceptos_html}
          </div>
        </details>"""

def noticia_full_html(n: dict) -> str:
    img = safe_src(n.get("imagen_url", ""))
    url = safe_href(n.get("url", ""))
    titulo = esc_text(n.get("titulo", ""))
    resumen = limpiar_texto(n.get("resumen", ""))
    cls = "noticia-full has-img" if img else "noticia-full"
    img_html = f'<img src="{esc_attr(img)}" alt="">' if img else ""
    just = n.get("ra_justificacion", "")
    just_html = f'<p class="justificacion">&#128218; {limpiar_texto(just)}</p>' if just else ""
    sec = seccion_del_autor() if es_contenido_propio(n) else modulo_a_seccion(n.get("modulo_asignado", ""))
    return f"""
    <article class="{cls}">
      {img_html}
      <div>
        {badge_html(n, sec)}
        <div class="n-title"><a href="{esc_attr(url)}" target="_blank" rel="noopener noreferrer">{titulo}</a></div>
        <p class="n-summary">{resumen}</p>
        {just_html}
        {docente_html(n)}
        <a href="{esc_attr(url)}" class="read-more" target="_blank" rel="noopener noreferrer">Leer noticia completa &rarr;</a>
      </div>
    </article>"""


# PORTADA

def generar_portada(noticias_por_seccion: dict, secciones_activas: set):
    bloques = ""

    primera_seccion = next((s for s in SECCIONES if noticias_por_seccion.get(s["id"])), None)
    if primera_seccion:
        ns = noticias_por_seccion[primera_seccion["id"]]
        if ns:
            bloques += card_lead(ns[0], primera_seccion)

    autor_noticias = noticias_por_seccion.get("del-autor", [])
    if autor_noticias:
        muestra_autor = autor_noticias[:3]
        cards_autor = "".join(card_story(n, {"label": "Del Autor"}) for n in muestra_autor)
        bloques += f'''<div class="autor-section">
          <div class="sec-header"><a href="del-autor.html">Del Autor &mdash; Juan Armada</a></div>
          <div class="autor-bio">
            <div class="autor-bio-text">
              <strong>Juan Armada</strong> &mdash; Docente FP Comercio y Marketing &middot;
              Blog, podcast y videotutoriales en
              <a href="https://juanarmada.com" target="_blank" rel="noopener noreferrer">juanarmada.com</a>
            </div>
          </div>
          <div class="stories-row">{cards_autor}</div>
        </div>'''

    for seccion in SECCIONES:
        sid = seccion["id"]
        if sid == "del-autor":
            continue
        ns = noticias_por_seccion.get(sid, [])
        if not ns:
            continue

        inicio = 1 if sid == (primera_seccion["id"] if primera_seccion else "") else 0
        muestra = ns[inicio: inicio + NOTICIAS_PORTADA_POR_SECCION]
        if not muestra:
            continue

        bloques += f'<div class="sec-header"><a href="{seccion["file"]}">{seccion["label"]}</a></div>\n'
        cards = "".join(card_story(n, seccion) for n in muestra)
        bloques += f'<div class="stories-row">{cards}</div>\n'

        if len(ns) > inicio + NOTICIAS_PORTADA_POR_SECCION:
            total_rest = len(ns) - inicio - NOTICIAS_PORTADA_POR_SECCION
            bloques += f'<div class="ver-mas"><a href="{seccion["file"]}">Ver {total_rest} noticias m&aacute;s en {seccion["label"]} &rarr;</a></div>\n'

    total = sum(len(v) for v in noticias_por_seccion.values())
    html = head_html(f"Portada &mdash; {fecha_hoy()}")
    html += masthead_html()
    html += nav_html(secciones_con_noticias=secciones_activas)
    html += f'<div class="subtitle-bar"><span>{SITE_SUBTITLE}</span><span>{total} noticias &middot; {fecha_hoy()}</span></div>\n'
    html += f'<main class="container">{bloques}</main>'
    html += footer_html()
    html += "\n</body>\n</html>"

    out = DOCS_DIR / "index.html"
    out.write_text(html, encoding="utf-8-sig")
    print(f"  Portada -> {out}")


# PAGINAS DE SECCION

def generar_seccion(seccion: dict, noticias: list, secciones_activas: set = None):
    total_pags = max(1, math.ceil(len(noticias) / NOTICIAS_POR_PAGINA))

    for pag in range(1, total_pags + 1):
        inicio = (pag - 1) * NOTICIAS_POR_PAGINA
        trozo = noticias[inicio: inicio + NOTICIAS_POR_PAGINA]

        cuerpo = f'<div class="sec-header">{seccion["label"]}</div>\n'
        cuerpo += '<div class="seccion-lista">'
        cuerpo += "".join(noticia_full_html(n) for n in trozo)
        cuerpo += "</div>"

        if total_pags > 1:
            pags_html = ""
            base = seccion["file"].replace(".html", "")
            for p in range(1, total_pags + 1):
                href = seccion["file"] if p == 1 else f"{base}-p{p}.html"
                if p == pag:
                    pags_html += f'<span class="current">{p}</span>'
                else:
                    pags_html += f'<a href="{href}">{p}</a>'
            cuerpo += f'<div class="paginacion">{pags_html}</div>'

        titulo_pag = f"{seccion['label']} &mdash; P&aacute;g. {pag}" if total_pags > 1 else seccion["label"]
        html = head_html(titulo_pag)
        html += masthead_html()
        html += nav_html(seccion["id"], secciones_activas)
        html += f'<div class="subtitle-bar"><span>{seccion["label"]} &middot; {len(noticias)} noticias</span><span>{fecha_hoy()}</span></div>\n'
        html += f'<main class="container">{cuerpo}</main>'
        html += footer_html()
        html += "\n</body>\n</html>"

        fname = seccion["file"] if pag == 1 else seccion["file"].replace(".html", f"-p{pag}.html")
        out = DOCS_DIR / fname
        out.write_text(html, encoding="utf-8-sig")
        print(f"  {seccion['label']} p.{pag} -> {out}")


# PRINCIPAL

def generar_web():
    if not INPUT_FILE.exists():
        print(f"No se encontro {INPUT_FILE}. Ejecuta primero el clasificador.")
        return

    with open(INPUT_FILE, encoding="utf-8") as f:
        noticias = json.load(f)

    noticias.sort(key=lambda n: (-fecha_orden(n), 0 if n.get("imagen_url") else 1))

    DOCS_DIR.mkdir(exist_ok=True)

    noticias_por_seccion = {s["id"]: [] for s in SECCIONES}
    sin_seccion = []
    for n in noticias:
        if es_contenido_propio(n):
            sec = seccion_del_autor()
        else:
            m = n.get("modulo_asignado") or n.get("modulo", "")
            sec = modulo_a_seccion(m)

        if sec:
            noticias_por_seccion[sec["id"]].append(n)
        else:
            sin_seccion.append(n)
            noticias_por_seccion["otros"].append(n)

    if sin_seccion:
        print(f"  ⚠ {len(sin_seccion)} noticias sin seccion asignada enviadas a 'Otros'")

    print("Generando paginas...")
    secciones_activas = {sid for sid, ns in noticias_por_seccion.items() if ns}
    generar_portada(noticias_por_seccion, secciones_activas)
    for seccion in SECCIONES:
        ns = noticias_por_seccion[seccion["id"]]
        if ns:
            generar_seccion(seccion, ns, secciones_activas)
        else:
            print(f"  {seccion['label']} -> sin noticias, pagina omitida")

    total = sum(len(v) for v in noticias_por_seccion.values())
    print(f"\nListo. {total} noticias en {sum(1 for v in noticias_por_seccion.values() if v)} secciones")
    print(f"Abre: {(DOCS_DIR / 'index.html').resolve()}")


if __name__ == "__main__":
    generar_web()
