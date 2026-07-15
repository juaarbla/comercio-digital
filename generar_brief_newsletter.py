from __future__ import annotations

import argparse
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

from generar_newsletter import (
    flatten_news,
    load_json,
    period_info,
    pick,
    select_news,
)
from paths import BASE_DIR, NOTICIAS_CLASIFICADAS


OUTPUT_DIR = BASE_DIR / "outputs" / "podcast"


def clean_text(value: Any) -> str:
    return str(value or "").replace("\n", " ").strip()


def list_values(value: Any, max_items: int = 6) -> list[str]:
    if isinstance(value, list):
        values = []
        for item in value:
            if isinstance(item, dict):
                text = item.get("texto") or item.get("codigo") or item.get("letra")
            else:
                text = item
            text = clean_text(text)
            if text:
                values.append(text)
        return values[:max_items]

    text = clean_text(value)
    return [text] if text else []


def source_for(noticia: dict[str, Any]) -> str:
    fuente = pick(noticia, "fuente_detectada", default="")
    if fuente:
        return fuente
    url = pick(noticia, "url", "link", "enlace", default="")
    if "://" in url:
        return url.split("://", 1)[1].split("/", 1)[0].replace("www.", "")
    return "fuente no detectada"


def episode_theme(noticias: list[dict[str, Any]]) -> str:
    modulos = [
        pick(n, "modulo_relacionado", "modulo_asignado", "modulo", default="")
        for n in noticias
    ]
    modulos = [m for m in modulos if m]
    if not modulos:
        return "Actualidad de comercio digital para llevar al aula"

    counts: dict[str, int] = {}
    for modulo in modulos:
        counts[modulo] = counts.get(modulo, 0) + 1
    principal = sorted(counts.items(), key=lambda item: item[1], reverse=True)[0][0]
    return f"Actualidad de {principal} aplicada a empresa, aula y decisiones digitales"


def render_news_block(noticia: dict[str, Any], index: int) -> list[str]:
    titulo = pick(noticia, "titulo", "title", default="Sin titulo")
    url = pick(noticia, "url", "link", "enlace", default="")
    resumen = pick(noticia, "resumen_docente", "resumen", "summary", default="")
    modulo = pick(noticia, "modulo_relacionado", "modulo_asignado", "modulo", default="Sin modulo")
    uso = pick(noticia, "tipo_uso", default="lectura")
    valor = pick(noticia, "valor_docente", default="sin valorar")
    pregunta = pick(noticia, "pregunta_aula", default="")
    actividad = pick(noticia, "actividad_breve", default="")
    conceptos = list_values(noticia.get("conceptos_clave"), max_items=5)

    lines = [
        f"### {index}. {titulo}",
        "",
        f"- Fuente: {source_for(noticia)}",
        f"- Módulo relacionado: {modulo}",
        f"- Uso docente: {uso}",
        f"- Valor docente: {valor}",
    ]
    if conceptos:
        lines.append(f"- Conceptos clave: {', '.join(conceptos)}")
    if url:
        lines.append(f"- Enlace: {url}")
    lines.extend([
        "",
        "**Resumen para locución**",
        "",
        resumen or "Pendiente de redactar resumen para locución.",
        "",
        "**Por qué importa**",
        "",
        "Conecta una noticia reciente con decisiones reales de empresas, clientes o docentes.",
        "",
    ])
    if pregunta:
        lines.extend(["**Pregunta para el aula**", "", pregunta, ""])
    if actividad:
        lines.extend(["**Actividad breve**", "", actividad, ""])
    return lines


def render_brief(noticias: list[dict[str, Any]], periodo: dict[str, str], periodicidad: str) -> str:
    destacada = noticias[0] if noticias else {}
    tema = episode_theme(noticias)
    titulo_destacado = pick(destacada, "titulo", "title", default="la noticia principal")

    lines = [
        f"# Brief podcast - comercIAaliza.online",
        "",
        f"Periodo base: {periodo['label']}",
        f"Periodicidad editorial: {periodicidad}",
        f"Noticias seleccionadas: {len(noticias)}",
        "",
        "## Tema del episodio",
        "",
        tema,
        "",
        "## Apertura sugerida",
        "",
        (
            "En este episodio revisamos varias noticias recientes de comercio digital "
            "y las traducimos a decisiones concretas para el aula, la pyme y el negocio online."
        ),
        "",
        "## Noticia de apertura",
        "",
        f"Abrir con: {titulo_destacado}",
        "",
        "## Bloque de noticias",
        "",
    ]

    for index, noticia in enumerate(noticias, 1):
        lines.extend(render_news_block(noticia, index))

    lines.extend([
        "## Bloque docente",
        "",
        "Ideas para convertir el episodio en actividad:",
        "",
        "1. Elegir una noticia y resumir el problema empresarial.",
        "2. Relacionarla con un módulo o resultado de aprendizaje.",
        "3. Proponer una decisión concreta para una pequeña empresa.",
        "4. Debatir riesgos, oportunidades y datos que faltarían antes de decidir.",
        "",
        "## Cierre sugerido",
        "",
        (
            "La tecnología cambia deprisa, pero lo importante para aprender comercio digital "
            "es convertir cada noticia en una pregunta: ¿qué decisión tomaría una empresa real?"
        ),
        "",
        "## Nota editorial",
        "",
        (
            "Este documento es un brief de trabajo. Conviene revisarlo y ajustar tono, "
            "duración y enfoque antes de convertirlo en guion final o audio."
        ),
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Genera un brief Markdown para podcast a partir de la selección de newsletter."
    )
    parser.add_argument("--periodicidad", choices=["semanal", "quincenal"], default="quincenal")
    parser.add_argument("--max", type=int, default=6, help="Número máximo de noticias.")
    parser.add_argument("--fecha", default="", help="Fecha base en formato YYYY-MM-DD.")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR), help="Carpeta de salida.")
    parser.add_argument("--stdout", action="store_true", help="Muestra el brief sin escribir archivo.")
    args = parser.parse_args()

    fecha = datetime.strptime(args.fecha, "%Y-%m-%d").date() if args.fecha else date.today()
    periodo = period_info(fecha, args.periodicidad)

    data = load_json(NOTICIAS_CLASIFICADAS)
    noticias = select_news(flatten_news(data), args.max)
    if not noticias:
        raise RuntimeError("No se han encontrado noticias válidas para generar el brief.")

    brief = render_brief(noticias, periodo, args.periodicidad)

    if args.stdout:
        print(brief)
        return

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"podcast-brief-{periodo['slug']}.md"
    output_file.write_text(brief, encoding="utf-8")

    print("Brief de podcast generado correctamente:")
    print(f"- {output_file}")


if __name__ == "__main__":
    main()
