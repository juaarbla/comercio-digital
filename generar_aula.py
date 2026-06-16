#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Genera docs/aula.html usando el style.css principal de Comercio Digital.

Uso:
    python generar_aula.py
    python generar_aula.py --entrada noticias_clasificadas.json --salida docs/aula.html --max-noticias 25

Si existe docs/fichas-aula/index_fichas.json, añade un botón "Ver ficha docente"
en las noticias que tengan ficha generada.
"""

import argparse
import html
import json
from pathlib import Path
from datetime import datetime

from paths import NOTICIAS_CLASIFICADAS



MENU = [
    ("index.html", "Portada"),
    ("comercio-electronico.html", "E-commerce"),
    ("internacional.html", "Internacional"),
    ("digitalizacion.html", "Digitalización"),
    ("ia-marketing.html", "IA & Marketing"),
    ("marketing.html", "Marketing"),
    ("aula.html", "Aula"),
    ("del-autor.html", "Del autor"),
]

FICHAS_INDEX = Path("docs/fichas-aula/index_fichas.json")


def h(valor):
    if valor is None:
        return ""
    return html.escape(str(valor), quote=True)


def cargar_noticias(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        for clave in ("noticias", "items", "data"):
            if clave in data and isinstance(data[clave], list):
                return data[clave]

    raise ValueError("No se ha encontrado una lista de noticias en el JSON.")


def cargar_indice_fichas():
    if not FICHAS_INDEX.exists():
        return {}
    try:
        with open(FICHAS_INDEX, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def fuente(noticia):
    return (
        noticia.get("fuente_detectada")
        or noticia.get("fuente")
        or noticia.get("medio")
        or ""
    )


def fecha(noticia):
    raw = (
        noticia.get("fecha_detectada")
        or noticia.get("fecha_publicacion")
        or noticia.get("fecha")
        or ""
    )
    return formatear_fecha_rss(raw)


def fecha_cabecera():
    """Fecha compacta para la cabecera — igual que en generar_web.py."""
    hoy = datetime.now()
    meses = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN",
             "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]
    return f"{hoy.day} {meses[hoy.month - 1]} {hoy.year}"


def formatear_fecha_rss(s):
    """Convierte 'Wed, 10 Jun 2026 14:50:00 +0000' → '10 jun. 2026'."""
    if not s:
        return ""
    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(s)
        meses = ["ene", "feb", "mar", "abr", "may", "jun",
                 "jul", "ago", "sep", "oct", "nov", "dic"]
        return f"{dt.day} {meses[dt.month - 1]}. {dt.year}"
    except Exception:
        return s[:10] if len(s) >= 10 else s


def normalizar_modulo_visible(noticia):
    return (
        noticia.get("modulo_relacionado")
        or noticia.get("modulo_asignado")
        or noticia.get("modulo")
        or "General"
    )


def seleccionar_noticias(noticias, max_noticias):
    candidatas = []

    for noticia in noticias:
        valor = str(noticia.get("valor_docente", "")).lower()
        generar_ficha = bool(noticia.get("generar_ficha", False))
        newsletter = bool(noticia.get("seleccion_newsletter", False))

        if valor == "alto" or generar_ficha or newsletter:
            candidatas.append(noticia)

    def orden(n):
        return (
            1 if n.get("seleccion_newsletter") else 0,
            int(n.get("score_docente") or 0),
            1 if n.get("imagen_url") else 0,
            str(fecha(n)),
        )

    candidatas.sort(key=orden, reverse=True)
    return candidatas[:max_noticias]


def render_nav(activa="aula.html"):
    docs = Path("docs")
    items = []
    for href, texto in MENU:
        # Portada, aula y del-autor se incluyen siempre
        # El resto solo si el archivo ya existe en docs/
        if href not in ("index.html", "aula.html", "del-autor.html"):
            if not (docs / href).exists():
                continue
        clase = "active" if href == activa else ""
        items.append(f'<li><a class="{clase}" href="{href}">{h(texto)}</a></li>')
    return "\n".join(items)


def conceptos_lista(conceptos):
    if isinstance(conceptos, str):
        return [c.strip() for c in conceptos.split(",") if c.strip()]
    if isinstance(conceptos, list):
        return [str(c).strip() for c in conceptos if str(c).strip()]
    return []


def render_conceptos(conceptos, noticia=None):
    conceptos = conceptos_lista(conceptos)
    if not conceptos and noticia is not None:
        conceptos = conceptos_fallback(noticia)

    chips = "\n".join(
        f'<span class="concepto-chip">{h(c)}</span>'
        for c in conceptos[:8]
        if c
    )

    if not chips:
        return ""

    return f"""
    <div class="conceptos-clave">
      <strong>Conceptos clave:</strong><br>
      {chips}
    </div>
    """


def render_linea_docente(label, valor):
    valor = h(valor)
    if not valor:
        return ""
    return f"<p><strong>{label}:</strong><br>{valor}</p>"



def actividad_fallback(noticia):
    modulo = normalizar_modulo_visible(noticia)
    return (
        f"Lee la noticia y analiza en pequeños grupos qué cambio plantea para una empresa vinculada a {modulo}. "
        "Después, elaborad una propuesta breve de actuación: qué debería revisar la empresa, qué decisión tomaría "
        "y qué indicador usaría para comprobar si la decisión funciona."
    )


def pregunta_fallback(noticia):
    return "¿Qué decisión debería tomar una empresa si esta noticia afectara directamente a su actividad digital?"


def justificacion_fallback(noticia):
    modulo = normalizar_modulo_visible(noticia)
    ra = noticia.get("ra_asignado") or "el resultado de aprendizaje correspondiente"
    return (
        f"La noticia permite conectar la actualidad del sector con contenidos de {modulo} y trabajar {ra} "
        "a partir de una situación real de empresa."
    )


def conceptos_fallback(noticia):
    modulo = normalizar_modulo_visible(noticia).lower()
    titulo = (noticia.get("titulo") or "").lower()

    if "marketplace" in titulo or "amazon" in titulo:
        return ["Marketplace", "Catálogo online", "SEO", "Ficha de producto"]
    if "logistic" in titulo or "almac" in titulo or "wms" in titulo:
        return ["Logística e-commerce", "Almacén inteligente", "Automatización", "Cadena de suministro"]
    if "ia" in titulo or "inteligencia artificial" in titulo or "tiktok" in titulo:
        return ["Inteligencia artificial", "Social commerce", "Retail media", "Estrategia digital"]
    if "internacional" in modulo:
        return ["Comercio internacional", "Aduanas", "Plataformas globales", "Normativa"]
    if "digitalización" in modulo or "digitalizacion" in modulo:
        return ["Digitalización", "Ciberseguridad", "Transformación digital", "Riesgo tecnológico"]
    return ["Comercio digital", "Modelo de negocio", "Cliente online", "Estrategia digital"]


def etiqueta_tipo_uso(tipo_uso):
    tipo = str(tipo_uso or "").strip().lower()
    equivalencias = {
        "actividad": "Actividad de aula",
        "actividad_aula": "Actividad de aula",
        "caso_empresa": "Caso de empresa",
        "caso": "Caso de empresa",
        "debate": "Debate",
        "seguimiento": "Seguimiento de actualidad",
        "seguimiento_actualidad": "Seguimiento de actualidad",
    }
    return equivalencias.get(tipo, tipo_uso or "Uso en el aula")


def render_docente_box(noticia):
    pregunta = noticia.get("pregunta_aula") or pregunta_fallback(noticia)
    actividad = noticia.get("actividad_breve") or actividad_fallback(noticia)
    tipo_uso = etiqueta_tipo_uso(noticia.get("tipo_uso") or "uso en el aula")
    modulo = normalizar_modulo_visible(noticia)
    ra = noticia.get("ra_asignado") or ""
    justificacion = noticia.get("ra_justificacion") or justificacion_fallback(noticia)
    conceptos = render_conceptos(noticia.get("conceptos_clave") or [], noticia)

    datos = []
    if modulo:
        datos.append(f"<span class='concepto-chip'>Módulo: {h(modulo)}</span>")
    if ra:
        datos.append(f"<span class='concepto-chip'>RA: {h(ra)}</span>")

    datos_html = ""
    if datos:
        datos_html = f"""
        <div class="conceptos-clave">
          {"".join(datos)}
        </div>
        """

    return f"""
    <details class="docente-box" open>
      <summary class="docente-box-title">Ficha docente · {h(tipo_uso)}</summary>
      <div class="docente-box-content">
        {datos_html}
        {render_linea_docente("Pregunta detonadora", pregunta)}
        {render_linea_docente("Actividad breve", actividad)}
        {conceptos}
        {render_linea_docente("Por qué encaja en el RA", justificacion)}
      </div>
    </details>
    """


def ficha_links_html(noticia, indice_fichas):
    clave = noticia.get("url") or noticia.get("titulo") or ""
    ficha = indice_fichas.get(clave)
    if not ficha:
        return ""

    html_href = ficha.get("html") or ""
    md_href = ficha.get("md") or ""

    links = []
    if html_href:
        links.append(f'<a class="read-more" href="{h(html_href)}">Ver ficha docente →</a>')
    if md_href:
        links.append(f'<a class="read-more" href="{h(md_href)}">Descargar Markdown →</a>')

    return "\n        ".join(links)


def render_noticia(noticia, indice_fichas):
    titulo = h(noticia.get("titulo") or "Sin título")
    url = h(noticia.get("url") or "#")
    resumen = h(noticia.get("resumen") or "")
    modulo = h(normalizar_modulo_visible(noticia))
    tipo_uso = h(etiqueta_tipo_uso(noticia.get("tipo_uso") or ""))
    imagen = h(noticia.get("imagen_url") or "")
    fecha_txt = h(fecha(noticia))
    fuente_txt = h(fuente(noticia))
    ra = h(noticia.get("ra_asignado") or "")

    has_img = "has-img" if imagen else ""

    imagen_html = ""
    if imagen:
        imagen_html = f"""
        <a href="{url}" target="_blank" rel="noopener">
          <img src="{imagen}" alt="">
        </a>
        """

    ra_html = f'<span class="ra-badge">{ra}</span>' if ra else ""
    fecha_html = f'<span class="fecha">{fecha_txt}</span>' if fecha_txt else ""
    tipo_html = f'<span class="ra-badge">{tipo_uso}</span>' if tipo_uso else ""

    fuente_html = ""
    if fuente_txt:
        fuente_html = f'<p class="justificacion">Fuente: {fuente_txt}</p>'

    return f"""
    <article class="noticia-full {has_img}">
      {imagen_html}
      <div>
        <div class="meta">
          <span class="cat-badge">{modulo}</span>
          {ra_html}
          {tipo_html}
          {fecha_html}
        </div>

        <h2 class="n-title">
          <a href="{url}" target="_blank" rel="noopener">{titulo}</a>
        </h2>

        <p class="n-summary">{resumen}</p>

        {fuente_html}
        {render_docente_box(noticia)}

        {ficha_links_html(noticia, indice_fichas)}
        <a class="read-more" href="{url}" target="_blank" rel="noopener">Leer noticia completa →</a>
      </div>
    </article>
    """


def render_html(noticias, indice_fichas):
    listado = "\n".join(render_noticia(n, indice_fichas) for n in noticias)

    if not listado:
        listado = """
        <section class="seccion-lista">
          <p>No hay noticias seleccionadas para trabajar en clase.</p>
        </section>
        """

    fecha_hoy = h(fecha_cabecera())

    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Noticias para trabajar en clase · Comercio Digital</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Selección de noticias de comercio digital para trabajar en clase con preguntas, actividades breves, conceptos clave y enfoque docente.">
  <link rel="stylesheet" href="assets/style.css">\n  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg">\n  <link rel="shortcut icon" href="assets/favicon.svg">
</head>
<body class="aula-page">

  <header class="masthead">
    <div class="masthead-side">
      Formación Profesional<br>
      Comercio y Marketing
    </div>

    <div class="site-title">
      <a href="index.html">Comercio Digital</a>
    </div>

    <div class="masthead-side right">
      {fecha_hoy}<br>
      comerciodigital.net
    </div>
  </header>

  <nav>
    <ul>
      {render_nav("aula.html")}
    </ul>
  </nav>

  <div class="subtitle-bar">
    <span>Aula · {len(noticias)} noticias seleccionadas</span>
    <span>Ficha docente, pregunta, actividad y conceptos clave</span>
  </div>

  <main class="container">
    <h1 class="sec-header">Para trabajar en clase</h1>

    <section class="autor-compact">
      <div class="autor-compact-head">
        <div>
          <div class="autor-compact-kicker">Uso docente</div>
          <p class="autor-compact-bio">
            Noticias seleccionadas para conectar la actualidad del comercio digital con módulos,
            resultados de aprendizaje, actividades, conceptos clave y debates para Formación Profesional.
          </p>
        </div>
        <a class="autor-compact-link" href="index.html">Volver a portada →</a>
      </div>
    </section>

    <section class="seccion-lista">
      {listado}
    </section>
  </main>

  <footer>
    <strong>Comercio Digital</strong><br>
    Selección editorial para uso educativo.
  </footer>

</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser()
    #parser.add_argument("--entrada", default="noticias_clasificadas.json")
    parser.add_argument("--entrada", default=str(NOTICIAS_CLASIFICADAS))
    parser.add_argument("--salida", default="docs/aula.html")
    parser.add_argument("--max-noticias", type=int, default=25)
    args = parser.parse_args()

    entrada = Path(args.entrada)
    salida = Path(args.salida)

    noticias = cargar_noticias(entrada)
    seleccionadas = seleccionar_noticias(noticias, args.max_noticias)
    indice_fichas = cargar_indice_fichas()

    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(render_html(seleccionadas, indice_fichas), encoding="utf-8")

    print(f"Página generada: {salida}")
    print(f"Noticias para aula: {len(seleccionadas)}")
    print(f"Fichas enlazadas disponibles: {len(indice_fichas)}")


if __name__ == "__main__":
    main()
