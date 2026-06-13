# -*- coding: utf-8 -*-
"""
generar_aula.py — versión 3

Genera docs/aula.html con las noticias de mayor valor docente.

Uso:
    python generar_aula.py

Con archivo de prueba:
    python generar_aula.py --entrada noticias_clasificadas_v3.json

Opcional:
    python generar_aula.py --max-noticias 30
"""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any, Dict, List


def cargar_json(ruta: Path) -> Any:
    if not ruta.exists():
        raise FileNotFoundError(f"No se encuentra el archivo: {ruta}")
    with ruta.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def extraer_noticias(datos: Any) -> List[Dict[str, Any]]:
    if isinstance(datos, list):
        return datos
    if isinstance(datos, dict) and isinstance(datos.get("noticias"), list):
        return datos["noticias"]
    raise ValueError("No se ha encontrado una lista de noticias válida.")


def resolver_entrada(ruta: str | None) -> Path:
    if ruta:
        return Path(ruta)

    for candidato in [
        Path("noticias_clasificadas.json"),
        Path("data/noticias_clasificadas.json"),
        Path("datos/noticias_clasificadas.json"),
        Path("noticias_clasificadas_v3.json"),
        Path("noticias_clasificadas_v2.json"),
    ]:
        if candidato.exists():
            return candidato

    return Path("noticias_clasificadas.json")


def campo(n: Dict[str, Any], *nombres: str, defecto: str = "") -> str:
    for nombre in nombres:
        valor = n.get(nombre)
        if valor:
            return str(valor)
    return defecto


def filtrar_ordenar(noticias: List[Dict[str, Any]], max_noticias: int) -> List[Dict[str, Any]]:
    seleccionadas = [
        n for n in noticias
        if str(n.get("valor_docente", "")).lower() == "alto" or n.get("generar_ficha") is True
    ]

    seleccionadas.sort(
        key=lambda n: (
            int(n.get("score_docente", 0)),
            1 if n.get("seleccion_newsletter") else 0,
            1 if n.get("imagen_url") else 0,
        ),
        reverse=True,
    )

    return seleccionadas[:max_noticias]


def render_tarjeta(n: Dict[str, Any]) -> str:
    titulo = html.escape(campo(n, "titulo", "title", defecto="Sin título"))
    resumen = html.escape(campo(n, "resumen", "summary", "descripcion", "description", defecto="Sin resumen disponible."))
    url = html.escape(campo(n, "url", "link", defecto="#"))
    fuente = html.escape(campo(n, "fuente_detectada", "fuente", "source", defecto="Fuente no indicada"))
    fecha = html.escape(campo(n, "fecha_detectada", "fecha_publicacion", "fecha", "date", defecto=""))
    modulo = html.escape(campo(n, "modulo_relacionado", "modulo_asignado", "modulo", defecto="General"))
    valor = html.escape(campo(n, "valor_docente", defecto=""))
    tipo = html.escape(campo(n, "tipo_uso", defecto=""))
    pregunta = html.escape(campo(n, "pregunta_aula", defecto=""))
    actividad = html.escape(campo(n, "actividad_breve", defecto=""))
    score = html.escape(campo(n, "score_docente", defecto=""))
    imagen = campo(n, "imagen_url", defecto="")
    newsletter = n.get("seleccion_newsletter") is True

    imagen_html = f'<img class="thumb" src="{html.escape(imagen)}" alt="">' if imagen else ""

    newsletter_html = '<span class="newsletter">Newsletter</span>' if newsletter else ""

    actividad_html = ""
    if actividad:
        actividad_html = f"""
        <div class="activity">
          <strong>Actividad breve:</strong><br>
          {actividad}
        </div>
        """

    return f"""
    <article class="card">
      {imagen_html}
      <div class="content">
        <div class="meta">
          <span>{modulo}</span>
          <span>Valor docente: {valor}</span>
          <span>{tipo}</span>
          <span>Score: {score}</span>
          {newsletter_html}
        </div>
        <h2>{titulo}</h2>
        <p class="source">{fuente} · {fecha}</p>
        <p>{resumen}</p>
        <div class="question">
          <strong>Pregunta para el aula:</strong><br>
          {pregunta}
        </div>
        {actividad_html}
        <p><a href="{url}" target="_blank" rel="noopener">Leer noticia original</a></p>
      </div>
    </article>
    """


def generar_html(noticias: List[Dict[str, Any]]) -> str:
    tarjetas = "\n".join(render_tarjeta(n) for n in noticias)

    if not tarjetas:
        tarjetas = """
        <section class="empty">
          <p>No hay noticias con valor docente alto.</p>
          <p>Ejecuta primero: <code>python enriquecer_docente.py --forzar</code></p>
        </section>
        """

    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Noticias para trabajar en clase</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {{
      margin: 0;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: #f5f5f5;
      color: #222;
    }}
    header {{
      background: #111827;
      color: white;
      padding: 2rem 1rem;
    }}
    header .wrap, main {{
      max-width: 1050px;
      margin: 0 auto;
    }}
    h1 {{
      margin: 0 0 .5rem 0;
      font-size: 2rem;
    }}
    header p {{
      margin: 0;
      color: #d1d5db;
    }}
    main {{
      padding: 1.5rem 1rem 3rem;
    }}
    .card {{
      background: white;
      border-radius: 14px;
      margin-bottom: 1rem;
      box-shadow: 0 8px 24px rgba(0,0,0,.06);
      border: 1px solid #e5e7eb;
      overflow: hidden;
    }}
    .content {{
      padding: 1.2rem;
    }}
    .thumb {{
      width: 100%;
      max-height: 230px;
      object-fit: cover;
      display: block;
      background: #e5e7eb;
    }}
    .card h2 {{
      margin: .7rem 0 .4rem;
      font-size: 1.35rem;
    }}
    .source {{
      color: #6b7280;
      font-size: .92rem;
    }}
    .meta {{
      display: flex;
      flex-wrap: wrap;
      gap: .5rem;
      font-size: .82rem;
    }}
    .meta span {{
      background: #eef2ff;
      color: #3730a3;
      padding: .25rem .55rem;
      border-radius: 999px;
    }}
    .meta .newsletter {{
      background: #ecfdf5;
      color: #047857;
    }}
    .question, .activity {{
      background: #f9fafb;
      border-left: 4px solid #111827;
      padding: .8rem 1rem;
      margin: 1rem 0;
    }}
    .activity {{
      border-left-color: #4b5563;
    }}
    a {{
      color: #1d4ed8;
      font-weight: 600;
    }}
    .empty {{
      background: white;
      padding: 1.2rem;
      border-radius: 12px;
    }}
  </style>
</head>
<body>
  <header>
    <div class="wrap">
      <h1>Noticias para trabajar en clase</h1>
      <p>Selección editorial generada a partir del valor docente de las noticias clasificadas.</p>
    </div>
  </header>
  <main>
    {tarjetas}
  </main>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera docs/aula.html desde el JSON enriquecido.")
    parser.add_argument("--entrada", help="Ruta del JSON enriquecido.")
    parser.add_argument("--salida", default="docs/aula.html", help="Ruta del HTML de salida.")
    parser.add_argument("--max-noticias", type=int, default=40, help="Número máximo de noticias en aula.html.")
    args = parser.parse_args()

    entrada = resolver_entrada(args.entrada)
    salida = Path(args.salida)

    datos = cargar_json(entrada)
    noticias = extraer_noticias(datos)
    noticias_aula = filtrar_ordenar(noticias, args.max_noticias)

    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(generar_html(noticias_aula), encoding="utf-8")

    print(f"Página generada: {salida}")
    print(f"Noticias para aula: {len(noticias_aula)}")
    print(f"Archivo de entrada: {entrada}")


if __name__ == "__main__":
    main()
