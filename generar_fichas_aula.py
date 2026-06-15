#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Genera fichas docentes en HTML y Markdown para las mejores noticias de aula.

Salida:
    docs/fichas-aula/*.html
    docs/fichas-aula/*.md
    docs/fichas-aula/index_fichas.json

Uso:
    python generar_fichas_aula.py
    python generar_fichas_aula.py --max-fichas 10 --limpiar
"""

import argparse
import html
import json
import re
import unicodedata
from pathlib import Path


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
    return campo(n, "fecha_detectada", "fecha_publicacion", "fecha")


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

## Uso en el aula

### Pregunta detonadora

{n.get("pregunta_aula") or ""}

### Actividad breve

{n.get("actividad_breve") or ""}

### Conceptos clave

{lista_conceptos}

### Por qué encaja en este RA

{n.get("ra_justificacion") or ""}

## Propuesta de dinámica

- **Inicio:** lectura breve de la noticia y contextualización.
- **Desarrollo:** análisis individual, por parejas o en pequeños grupos.
- **Cierre:** puesta en común y conexión con el módulo y el RA.

---

Ficha generada por Comercio Digital para uso educativo.
"""


def nav_html():
    menu = [
        ("../index.html", "Portada"),
        ("../comercio-electronico.html", "E-commerce"),
        ("../internacional.html", "Internacional"),
        ("../digitalizacion.html", "Digitalización"),
        ("../ia-marketing.html", "IA & Marketing"),
        ("../marketing.html", "Marketing"),
        ("../aula.html", "Aula"),
        ("../del-autor.html", "Del autor"),
    ]
    return "\n".join(
        f'<li><a class="{"active" if txt == "Aula" else ""}" href="{href}">{h(txt)}</a></li>'
        for href, txt in menu
    )


def render_html(n, md_file):
    titulo = h(n.get("titulo") or "Sin título")
    url = h(n.get("url") or "#")
    resumen = h(n.get("resumen") or "")
    img = h(n.get("imagen_url") or "")
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
  <link rel="stylesheet" href="../assets/style.css">
</head>
<body class="ficha-page">

<header class="masthead">
  <div class="masthead-side">Formación<br>Profesional<br>Comercio y Marketing</div>
  <div class="site-title"><a href="../index.html">Comercio Digital</a></div>
  <div class="masthead-side right">Ficha docente<br>comerciodigital.net</div>
</header>

<nav><ul>{nav_html()}</ul></nav>

<div class="subtitle-bar">
  <span>Ficha docente</span>
  <span>{h(modulo(n))} · {h(n.get("ra_asignado") or "")}</span>
</div>

<main class="container">

  <article class="lead-story {'has-img' if img else ''}">
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

  <section class="autor-compact">
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
      <a class="autor-compact-link" href="{h(md_file)}">Descargar Markdown →</a>
    </div>
  </section>

  <section class="seccion-lista">
    <article class="noticia-full">
      <div>
        <h2 class="n-title">Uso en el aula</h2>
        <div class="docente-box">
          <div class="docente-box-content">
            <p><strong>Pregunta detonadora:</strong><br>{h(n.get("pregunta_aula") or "")}</p>
            <p><strong>Actividad breve:</strong><br>{h(n.get("actividad_breve") or "Analiza la noticia, identifica el problema principal y explica cómo afecta a una empresa de comercio digital.")}</p>
            <p><strong>Conceptos clave:</strong></p>
            <div class="conceptos-clave">{conceptos_html}</div>
            <p><strong>Por qué encaja en este RA:</strong><br>{h(n.get("ra_justificacion") or "")}</p>
          </div>
        </div>

        <h2 class="n-title">Propuesta de dinámica</h2>
        <p class="n-summary">
          <strong>Inicio:</strong> lectura breve de la noticia y contextualización.<br>
          <strong>Desarrollo:</strong> análisis individual, por parejas o en pequeños grupos.<br>
          <strong>Cierre:</strong> puesta en común y conexión con el módulo y el RA.
        </p>

        <a class="read-more" href="{url}" target="_blank" rel="noopener">Leer noticia original →</a>
        <a class="read-more" href="../aula.html">Volver a Aula →</a>
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


def limpiar(salida):
    salida.mkdir(parents=True, exist_ok=True)
    for patron in ("*.html", "*.md", "index_fichas.json"):
        for f in salida.glob(patron):
            f.unlink()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--entrada", default="noticias_clasificadas.json")
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

    (salida / "index_fichas.json").write_text(
        json.dumps(indice, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"Fichas generadas: {len(seleccionadas)}")
    print(f"Carpeta: {salida}")


if __name__ == "__main__":
    main()
