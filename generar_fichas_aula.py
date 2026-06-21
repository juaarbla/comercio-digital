#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Genera fichas docentes en HTML y Markdown para las mejores noticias de aula.

Salida:
    docs/fichas-aula/*.html
    docs/fichas-aula/*.md
    docs/fichas-aula/material-aula.md
    docs/fichas-aula/index_fichas.json
"""

import argparse
import html
import json
import re
import unicodedata
from pathlib import Path
from datetime import datetime

from paths import NOTICIAS_CLASIFICADAS


def fecha_corta():
    hoy = datetime.now()
    meses = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN",
             "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]
    return f"{hoy.day} {meses[hoy.month - 1]} {hoy.year}"


def formatear_fecha_rss(s):
    if not s:
        return ""
    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(s)
        meses = ["ene", "feb", "mar", "abr", "may", "jun",
                 "jul", "ago", "sep", "oct", "nov", "dic"]
        return f"{dt.day} {meses[dt.month - 1]}. {dt.year}"
    except Exception:
        return str(s)[:10] if s else ""


def h(v):
    return html.escape(str(v or ""), quote=True)


def cargar_json(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for k in ("noticias", "items", "data"):
            if isinstance(data.get(k), list):
                return data[k]
    raise ValueError("No se ha encontrado una lista de noticias en el JSON.")


def slugify(texto, max_len=70):
    texto = str(texto or "ficha-docente").lower().strip()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"[^a-z0-9]+", "-", texto).strip("-")
    return (texto[:max_len].strip("-") or "ficha-docente")


def campo(n, *keys):
    for k in keys:
        if n.get(k):
            return n.get(k)
    return ""


def modulo(n):
    return campo(n, "modulo_relacionado", "modulo_asignado", "modulo") or "General"


def fecha(n):
    raw = campo(n, "fecha_detectada", "fecha_publicacion", "fecha")
    return formatear_fecha_rss(raw)


def fuente(n):
    return campo(n, "fuente_detectada", "fuente", "medio")


def tipo_uso(n):
    raw = str(n.get("tipo_uso") or "").strip().lower()
    mapa = {
        "actividad": "Actividad de aula",
        "actividad_aula": "Actividad de aula",
        "caso_empresa": "Caso de empresa",
        "caso": "Caso de empresa",
        "debate": "Debate",
        "seguimiento": "Seguimiento de actualidad",
        "seguimiento_actualidad": "Seguimiento de actualidad",
    }
    return mapa.get(raw, n.get("tipo_uso") or "Uso en el aula")


def conceptos(n):
    cs = n.get("conceptos_clave") or []
    if isinstance(cs, str):
        return [c.strip() for c in cs.split(",") if c.strip()]
    if isinstance(cs, list):
        return [str(c).strip() for c in cs if str(c).strip()]
    return []




def normalizar_ce_textos(n):
    """
    Devuelve una lista homogénea de CE para pintar en la ficha.

    Espera preferentemente el formato generado por clasificador_ra_v2.py:
    ce_textos = [{"codigo": "RA1b", "letra": "b", "texto": "..."}]

    También tolera formatos antiguos o manuales:
    ce_asignados = ["a", "b"]
    """
    ce_textos = n.get("ce_textos") or []
    resultado = []

    if isinstance(ce_textos, list):
        for item in ce_textos:
            if isinstance(item, dict):
                codigo = str(item.get("codigo") or "").strip()
                letra = str(item.get("letra") or "").strip()
                texto = str(item.get("texto") or "").strip()
                if texto:
                    if not codigo:
                        codigo = f"{n.get('ra_asignado') or 'RA'}{letra}" if letra else "CE"
                    resultado.append({"codigo": codigo, "texto": texto})
            elif isinstance(item, str) and item.strip():
                resultado.append({"codigo": "CE", "texto": item.strip()})

    # Fallback: si solo tenemos letras de CE, al menos las mostramos.
    if not resultado:
        ce_asignados = n.get("ce_asignados") or []
        if isinstance(ce_asignados, str):
            ce_asignados = [c.strip() for c in ce_asignados.split(",") if c.strip()]
        if isinstance(ce_asignados, list):
            for letra in ce_asignados:
                letra = str(letra).strip()
                if letra:
                    codigo = f"{n.get('ra_asignado') or 'RA'}{letra}"
                    resultado.append({"codigo": codigo, "texto": "Criterio de evaluación relacionado pendiente de texto oficial."})

    return resultado


def bloque_curricular_md(n):
    ra = n.get("ra_asignado") or ""
    ra_texto = n.get("ra_texto") or ""
    ce_items = normalizar_ce_textos(n)

    lineas = [
        "## Vinculación curricular",
        "",
        f"- **Módulo:** {modulo(n)}",
        f"- **Resultado de aprendizaje:** {ra}",
    ]

    if ra_texto:
        lineas.extend(["", f"**{ra}.** {ra_texto}"])

    lineas.extend(["", "### Criterios de evaluación relacionados", ""])

    if ce_items:
        for ce in ce_items:
            lineas.append(f"- **{ce['codigo']}.** {ce['texto']}")
    else:
        lineas.append("- No se han indicado criterios de evaluación concretos.")

    lineas.extend([
        "",
        "### Justificación docente",
        "",
        n.get("ra_justificacion") or "Pendiente de justificación curricular.",
    ])

    return "\n".join(lineas)


def bloque_curricular_html(n):
    ra = h(n.get("ra_asignado") or "")
    ra_texto = h(n.get("ra_texto") or "")
    ce_items = normalizar_ce_textos(n)

    if ce_items:
        ce_html = "\n".join(
            f'<li><strong>{h(ce["codigo"])}.</strong> <span>{h(ce["texto"])}</span></li>'
            for ce in ce_items
        )
    else:
        ce_html = '<li class="ficha-vacio">No se han indicado criterios de evaluación concretos.</li>'

    ra_texto_html = ""
    if ra_texto:
        ra_texto_html = f'<p class="ficha-ra-texto"><strong>{ra}.</strong> {ra_texto}</p>'

    return f"""
        <h2 class="n-title ficha-section-title">Vinculación curricular</h2>
        <div class="ficha-curricular-box">
          <p><strong>Módulo:</strong> {h(modulo(n))}</p>
          <p><strong>Resultado de aprendizaje:</strong> {ra}</p>
          {ra_texto_html}

          <h3 class="ficha-mini-title">Criterios de evaluación relacionados</h3>
          <ul class="ficha-ce-list">
            {ce_html}
          </ul>

          <h3 class="ficha-mini-title">Justificación docente</h3>
          <p class="ficha-justificacion">{h(n.get("ra_justificacion") or "Pendiente de justificación curricular.")}</p>
        </div>
"""

def debe_generar_ficha(n):
    if n.get("generar_ficha") is True:
        return True

    valor = str(n.get("valor_docente", "")).lower()
    try:
        score = int(n.get("score_docente") or 0)
    except Exception:
        score = 0

    return (
        valor == "alto"
        and score >= 25
        and bool(n.get("pregunta_aula"))
        and bool(n.get("actividad_breve"))
        and bool(n.get("ra_asignado"))
    )


def seleccionar(noticias, max_fichas):
    candidatas = [n for n in noticias if debe_generar_ficha(n)]

    def orden(n):
        try:
            score = int(n.get("score_docente") or 0)
        except Exception:
            score = 0
        return (
            1 if n.get("seleccion_newsletter") else 0,
            score,
            1 if n.get("imagen_url") else 0,
            str(fecha(n)),
        )

    candidatas.sort(key=orden, reverse=True)
    return candidatas[:max_fichas]


def render_md(n):
    lista_conceptos = "\n".join(f"- {c}" for c in conceptos(n)) or "-"
    actividad = n.get("actividad_breve") or "Analiza la noticia, identifica el problema principal y explica cómo afecta a una empresa de comercio digital."

    return f"""# {n.get("titulo") or "Sin título"}

## Datos de la noticia

- **Fuente:** {fuente(n)}
- **Fecha:** {fecha(n)}
- **Enlace:** {n.get("url") or ""}
- **Módulo:** {modulo(n)}
- **Resultado de aprendizaje:** {n.get("ra_asignado") or ""}
- **Tipo de uso:** {tipo_uso(n)}

## Resumen

{n.get("resumen") or ""}

{bloque_curricular_md(n)}

## Uso en el aula

### Pregunta detonadora

{n.get("pregunta_aula") or ""}

### Actividad breve

{actividad}

### Conceptos clave

{lista_conceptos}

## Propuesta de dinámica

- **Inicio:** lectura breve de la noticia y contextualización.
- **Desarrollo:** análisis individual, por parejas o en pequeños grupos.
- **Cierre:** puesta en común y conexión con el módulo, el RA y los criterios de evaluación.

---

Ficha generada por Comercio Digital para uso educativo.
"""

def nav_html():
    docs = Path("docs")
    menu = [
        ("../index.html", "Portada", "index.html"),
        ("../comercio-electronico.html", "E-commerce", "comercio-electronico.html"),
        ("../internacional.html", "Internacional", "internacional.html"),
        ("../digitalizacion.html", "Digitalización", "digitalizacion.html"),
        ("../ia-marketing.html", "IA & Marketing", "ia-marketing.html"),
        ("../aula.html", "Aula", "aula.html"),
        ("../newsletter/index.html", "Newsletter", "newsletter/index.html"),
        ("../del-autor.html", "Del autor", "del-autor.html"),
    ]
    siempre = {"index.html", "aula.html", "newsletter/index.html", "del-autor.html"}
    items = []
    for href, txt, check in menu:
        if check not in siempre and not (docs / check).exists():
            continue
        cls = "active" if txt == "Aula" else ""
        items.append(f'<li><a class="{cls}" href="{href}">{h(txt)}</a></li>')
    return "\n".join(items)


def render_html(n, md_file):
    titulo = h(n.get("titulo") or "Sin título")
    url = h(n.get("url") or "#")
    resumen = h(n.get("resumen") or "")
    img = h(n.get("imagen_url") or "")
    actividad = h(n.get("actividad_breve") or "Analiza la noticia, identifica el problema principal y explica cómo afecta a una empresa de comercio digital.")
    conceptos_html = "".join(f'<span class="concepto-chip">{h(c)}</span>' for c in conceptos(n)[:10])

    imagen_html = ""
    if img:
        imagen_html = f'<div class="lead-img"><img src="{img}" alt=""></div>'

    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>{titulo} · Ficha docente · Comercio Digital</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Ficha docente para trabajar una noticia de comercio digital en clase.">
  <link rel="stylesheet" href="../assets/style.css">\n  <link rel="icon" type="image/svg+xml" href="../assets/favicon.svg">\n  <link rel="shortcut icon" href="../assets/favicon.svg">
</head>
<body class="ficha-page">

<header class="masthead">
  <div class="masthead-side">Formación<br>Profesional<br>Comercio y Marketing</div>
  <div class="site-title"><a href="../index.html">Comercio Digital</a></div>
  <div class="masthead-side right">{fecha_corta()}<br>comerciodigital.net</div>
</header>

<nav><ul>{nav_html()}</ul></nav>

<div class="subtitle-bar">
  <span>Ficha docente</span>
  <span>{h(modulo(n))} · {h(n.get("ra_asignado") or "")}</span>
</div>

<main class="container">

  <article class="lead-story ficha-hero {'has-img' if img else ''}">
    {imagen_html}
    <div>
      <div class="meta">
        <span class="cat-badge">{h(modulo(n))}</span>
        <span class="ra-badge">{h(n.get("ra_asignado") or "")}</span>
        <span class="ra-badge">{h(tipo_uso(n))}</span>
      </div>
      <h1 class="lead-title">{titulo}</h1>
      <p class="lead-summary">{resumen}</p>
    </div>
  </article>

  <section class="autor-compact ficha-datos">
    <div class="autor-compact-head">
      <div>
        <div class="autor-compact-kicker">Datos de la noticia</div>
        <p class="autor-compact-bio">
          <strong>Fuente:</strong> {h(fuente(n))}<br>
          <strong>Fecha:</strong> {h(fecha(n))}<br>
          <strong>Módulo:</strong> {h(modulo(n))}<br>
          <strong>Resultado de aprendizaje:</strong> {h(n.get("ra_asignado") or "")}<br>
          <strong>Tipo de uso:</strong> {h(tipo_uso(n))}
        </p>
      </div>
      <a class="autor-compact-link ficha-download" href="{h(md_file)}">Descargar Markdown →</a>
    </div>
  </section>

  <section class="seccion-lista">
    <article class="noticia-full ficha-aula-card">
      <div>
        {bloque_curricular_html(n)}

        <h2 class="n-title ficha-section-title">Uso en el aula</h2>
        <div class="docente-box ficha-docente-box">
          <div class="docente-box-content">
            <p><strong>Pregunta detonadora:</strong><br>{h(n.get("pregunta_aula") or "")}</p>
            <p><strong>Actividad breve:</strong><br>{actividad}</p>
            <p><strong>Conceptos clave:</strong></p>
            <div class="conceptos-clave">{conceptos_html}</div>
          </div>
        </div>

        <h2 class="n-title ficha-section-title">Propuesta de dinámica</h2>
        <div class="ficha-dinamica">
          <p>
            <strong>Inicio:</strong> lectura breve de la noticia y contextualización.<br>
            <strong>Desarrollo:</strong> análisis individual, por parejas o en pequeños grupos.<br>
            <strong>Cierre:</strong> puesta en común y conexión con el módulo, el RA y los criterios de evaluación.
          </p>
        </div>

        <div class="ficha-actions">
          <a class="read-more" href="{url}" target="_blank" rel="noopener">Leer noticia original →</a>
          <a class="read-more" href="../aula.html">Volver a Aula →</a>
        </div>
      </div>
    </article>
  </section>

</main>

<footer>
  <strong>Comercio Digital</strong><br>
  Ficha docente generada para uso educativo.
</footer>

</body>
</html>
"""


def render_material_aula_md(seleccionadas, indice_archivos):
    partes = [
        "# Material de aula · Comercio Digital",
        "",
        "Selección de fichas docentes generadas a partir de noticias clasificadas.",
        "",
        f"Fecha de generación: {fecha_corta()}",
        "",
        "---",
        "",
    ]

    for i, n in enumerate(seleccionadas, 1):
        partes.append(f"# {i}. {n.get('titulo') or 'Sin título'}")
        partes.append("")
        partes.append(f"- **Fuente:** {fuente(n)}")
        partes.append(f"- **Fecha:** {fecha(n)}")
        partes.append(f"- **Enlace:** {n.get('url') or ''}")
        partes.append(f"- **Módulo:** {modulo(n)}")
        partes.append(f"- **RA:** {n.get('ra_asignado') or ''}")
        if n.get("ra_texto"):
            partes.append(f"- **Texto RA:** {n.get('ra_texto')}")
        ce_items = normalizar_ce_textos(n)
        if ce_items:
            partes.append("- **CE relacionados:** " + ", ".join(ce["codigo"] for ce in ce_items))
        partes.append(f"- **Tipo de uso:** {tipo_uso(n)}")
        archivos = indice_archivos.get(n.get("url") or n.get("titulo") or "")
        if archivos:
            partes.append(f"- **Ficha HTML:** {archivos.get('html', '')}")
            partes.append(f"- **Ficha Markdown:** {archivos.get('md', '')}")
        partes.append("")
        partes.append("## Resumen")
        partes.append("")
        partes.append(n.get("resumen") or "")
        partes.append("")
        partes.append("## Vinculación curricular")
        partes.append("")
        partes.append(bloque_curricular_md(n).replace("## Vinculación curricular\n\n", ""))
        partes.append("")
        partes.append("## Pregunta detonadora")
        partes.append("")
        partes.append(n.get("pregunta_aula") or "")
        partes.append("")
        partes.append("## Actividad breve")
        partes.append("")
        partes.append(n.get("actividad_breve") or "Analiza la noticia, identifica el problema principal y explica cómo afecta a una empresa de comercio digital.")
        partes.append("")
        partes.append("## Conceptos clave")
        partes.append("")
        cs = conceptos(n)
        partes.extend([f"- {c}" for c in cs] or ["-"])
        partes.append("")
        partes.append("---")
        partes.append("")

    return "\n".join(partes)


def limpiar(salida):
    salida.mkdir(parents=True, exist_ok=True)
    for patron in ("*.html", "*.md", "index_fichas.json"):
        for f in salida.glob(patron):
            f.unlink()


def main():
    p = argparse.ArgumentParser()
    #p.add_argument("--entrada", default="noticias_clasificadas.json")
    p.add_argument("--entrada", default=str(NOTICIAS_CLASIFICADAS))
    p.add_argument("--salida", default="docs/fichas-aula")
    p.add_argument("--max-fichas", type=int, default=10)
    p.add_argument("--limpiar", action="store_true")
    args = p.parse_args()

    noticias = cargar_json(Path(args.entrada))
    seleccionadas = seleccionar(noticias, args.max_fichas)

    salida = Path(args.salida)
    if args.limpiar:
        limpiar(salida)
    else:
        salida.mkdir(parents=True, exist_ok=True)

    indice = {}

    for i, n in enumerate(seleccionadas, 1):
        base = f"{i:03d}-{slugify(n.get('titulo'))}"
        html_file = f"{base}.html"
        md_file = f"{base}.md"

        (salida / md_file).write_text(render_md(n), encoding="utf-8")
        (salida / html_file).write_text(render_html(n, md_file), encoding="utf-8")

        clave = n.get("url") or n.get("titulo") or base
        indice[clave] = {
            "html": f"fichas-aula/{html_file}",
            "md": f"fichas-aula/{md_file}",
            "titulo": n.get("titulo") or "",
        }

    (salida / "material-aula.md").write_text(
        render_material_aula_md(seleccionadas, indice),
        encoding="utf-8"
    )

    (salida / "index_fichas.json").write_text(
        json.dumps(indice, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"Fichas generadas: {len(seleccionadas)}")
    print(f"Material de aula: {salida / 'material-aula.md'}")
    print(f"Carpeta: {salida}")


if __name__ == "__main__":
    main()
