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
MONTH_NAMES = {
    "01": "enero",
    "02": "febrero",
    "03": "marzo",
    "04": "abril",
    "05": "mayo",
    "06": "junio",
    "07": "julio",
    "08": "agosto",
    "09": "septiembre",
    "10": "octubre",
    "11": "noviembre",
    "12": "diciembre",
}


def clean_text(value: Any) -> str:
    return str(value or "").replace("\n", " ").strip()


def plural(count: int, singular: str, plural_text: str | None = None) -> str:
    text = singular if count == 1 else (plural_text or f"{singular}s")
    return f"{count} {text}"


def friendly_period_label(periodo: dict[str, str]) -> str:
    slug = periodo.get("slug", "")
    if "-Q" in slug:
        try:
            year, month, quarter = slug.split("-")
            quincena = quarter.replace("Q", "")
            month_name = MONTH_NAMES.get(month, month)
            return f"Quincena {quincena} de {month_name} de {year}"
        except ValueError:
            return periodo["label"]
    return periodo["label"]


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


def title_for(noticia: dict[str, Any]) -> str:
    return pick(noticia, "titulo", "title", default="Sin titulo")


def url_for(noticia: dict[str, Any]) -> str:
    return pick(noticia, "url", "link", "enlace", default="")


def module_for(noticia: dict[str, Any]) -> str:
    return pick(noticia, "modulo_relacionado", "modulo_asignado", "modulo", default="Sin módulo")


def summary_for(noticia: dict[str, Any]) -> str:
    return pick(noticia, "resumen_docente", "resumen", "summary", default="")


def question_for(noticia: dict[str, Any]) -> str:
    return pick(
        noticia,
        "pregunta_aula",
        default="¿Qué decisión podría tomar una pequeña empresa a partir de esta noticia?",
    )


def activity_for(noticia: dict[str, Any]) -> str:
    return pick(noticia, "actividad_breve", default="")


def source_for(noticia: dict[str, Any]) -> str:
    fuente = pick(noticia, "fuente_detectada", default="")
    if fuente:
        return fuente
    url = url_for(noticia)
    if "://" in url:
        return url.split("://", 1)[1].split("/", 1)[0].replace("www.", "")
    return "fuente no detectada"


def is_security_news(noticia: dict[str, Any]) -> bool:
    text = f"{source_for(noticia)} {title_for(noticia)} {module_for(noticia)}".lower()
    terms = ("incibe", "ciber", "seguridad", "vulnerabilidad", "vulnerabilidades", "sci")
    return any(term in text for term in terms)


def group_key(noticia: dict[str, Any]) -> str:
    title = title_for(noticia).lower()
    if "marketplace summit" in title:
        return "marketplace-summit"
    if "logístic" in title or "logistic" in title or "entrega" in title:
        return "logistica"
    if "muse image" in title or "imagen" in title or "instagram" in title or "whatsapp" in title:
        return "ia-visual"
    return title[:72]


def split_episode_items(
    noticias: list[dict[str, Any]],
) -> tuple[list[list[dict[str, Any]]], list[dict[str, Any]], list[dict[str, Any]]]:
    security: list[dict[str, Any]] = []
    normal: list[dict[str, Any]] = []
    for noticia in noticias:
        if is_security_news(noticia):
            security.append(noticia)
        else:
            normal.append(noticia)

    grouped: list[list[dict[str, Any]]] = []
    seen: dict[str, int] = {}
    for noticia in normal:
        key = group_key(noticia)
        if key in seen:
            grouped[seen[key]].append(noticia)
            continue
        seen[key] = len(grouped)
        grouped.append([noticia])

    main_groups = grouped[:3]
    reserved = [news for group in grouped[3:] for news in group]
    return main_groups, security[:1], reserved + security[1:]


def block_title(group: list[dict[str, Any]]) -> str:
    key = group_key(group[0])
    if key == "marketplace-summit":
        return "Vender dentro de plataformas y redes sociales"
    if key == "logistica":
        return "La compra no termina al pulsar el botón"
    if key == "ia-visual":
        return "Crear más rápido no significa crear mejor"
    return title_for(group[0])


def block_focus(group: list[dict[str, Any]]) -> str:
    key = group_key(group[0])
    if len(group) > 1:
        return (
            "Estas noticias tratan una tendencia similar. Conviene trabajarlas como un "
            "único bloque para evitar repeticiones y extraer una decisión práctica."
        )
    if key == "logistica":
        return "La noticia recuerda que una venta online también se decide en inventario, entrega y devoluciones."
    if key == "ia-visual":
        return "La noticia conecta creación visual con identidad de marca, no solo con rapidez de producción."
    return "La noticia sirve para traducir una tendencia digital en una decisión concreta de negocio."


def practical_decision(group: list[dict[str, Any]]) -> str:
    key = group_key(group[0])
    if key == "marketplace-summit":
        return (
            "Elegir un único canal para realizar una prueba pequeña y medible, "
            "en lugar de intentar estar en todas las plataformas al mismo tiempo."
        )
    if key == "logistica":
        return (
            "Revisar el recorrido completo de un pedido y automatizar primero el punto "
            "en el que se repiten más errores o tareas manuales."
        )
    if key == "ia-visual":
        return "Crear una pequeña guía visual de marca antes de utilizar herramientas de generación de imágenes con IA."
    if is_security_news(group[0]):
        return "Comprobar qué aplicaciones, dispositivos y cuentas siguen usando credenciales débiles o compartidas."
    return "Definir una prueba concreta, un indicador de resultado y un riesgo que conviene controlar."


def episode_theme(groups: list[list[dict[str, Any]]]) -> str:
    keys = {group_key(group[0]) for group in groups}
    if {"marketplace-summit", "logistica", "ia-visual"}.issubset(keys):
        return "Social commerce, logística e imágenes con IA: qué está cambiando en el comercio digital"
    if groups:
        return "Actualidad de comercio digital: decisiones prácticas para pymes y aula"
    return "Actualidad de comercio digital para llevar al aula"


def proposed_title(groups: list[list[dict[str, Any]]]) -> str:
    theme = episode_theme(groups)
    if ":" in theme:
        theme = theme.split(":", 1)[0]
    return f"[Actualidad] {theme}"


def render_news_reference(noticia: dict[str, Any]) -> list[str]:
    lines = [
        f"### {title_for(noticia)}",
        "",
        f"- Fuente: {source_for(noticia)}",
    ]
    url = url_for(noticia)
    if url:
        lines.append(f"- Enlace: {url}")
    return lines


def render_episode_block(group: list[dict[str, Any]], index: int) -> list[str]:
    first = group[0]
    resumen = summary_for(first)
    pregunta = question_for(first)
    actividad = activity_for(first)
    concepts = list_values(first.get("conceptos_clave"), max_items=5)

    lines = [
        f"# Bloque {index} - {block_title(group)}",
        "",
        "## Noticias fusionadas" if len(group) > 1 else "## Noticia",
        "",
    ]
    for noticia in group:
        lines.extend(render_news_reference(noticia))
        lines.append("")

    lines.extend(
        [
            "## Enfoque editorial",
            "",
            block_focus(group),
            "",
            "## Resumen para locución",
            "",
            resumen or "Pendiente de redactar resumen para locución.",
            "",
            "## Por qué importa",
            "",
            "La noticia ayuda a pasar del titular a una decisión concreta para una pyme, una tienda online o una actividad de aula.",
            "",
            "## Pregunta para el aula",
            "",
            f"**{pregunta}**",
            "",
        ]
    )
    if actividad:
        lines.extend(["## Actividad breve", "", actividad, ""])
    if concepts:
        lines.extend(["## Conceptos útiles", "", ", ".join(concepts), ""])
    lines.extend(
        [
            "## Decisión práctica para una pyme",
            "",
            practical_decision(group),
            "",
            "---",
            "",
        ]
    )
    return lines


def render_security_notice(noticia: dict[str, Any]) -> list[str]:
    return [
        "# Aviso breve de ciberseguridad",
        "",
        "## Noticia",
        "",
        f"### {title_for(noticia)}",
        "",
        f"- Fuente: {source_for(noticia)}",
        f"- Enlace: {url_for(noticia)}",
        "",
        "## Enfoque editorial",
        "",
        "No conviene desarrollar esta noticia como un bloque completo si el episodio ya tiene tres ideas principales. Puede funcionar como sección breve y recurrente.",
        "",
        "## Resumen para locución",
        "",
        summary_for(noticia) or "Recordatorio breve sobre seguridad, credenciales, actualizaciones y permisos.",
        "",
        "## Decisión práctica para una pyme",
        "",
        practical_decision([noticia]),
        "",
        "---",
        "",
    ]


def render_reserved_news(noticias: list[dict[str, Any]]) -> list[str]:
    if not noticias:
        return []
    lines = ["# Noticias reservadas", ""]
    for noticia in noticias:
        lines.extend(
            [
                f"## {title_for(noticia)}",
                "",
                f"- Fuente: {source_for(noticia)}",
                "- Motivo para reservarla: relevante, pero menos conectada con la idea central del episodio.",
                "- Posible uso futuro: mención secundaria, episodio monográfico o pieza de contexto.",
                "",
            ]
        )
    lines.extend(["---", ""])
    return lines


def render_brief(noticias: list[dict[str, Any]], periodo: dict[str, str], periodicidad: str) -> str:
    main_groups, security, reserved = split_episode_items(noticias)
    tema = episode_theme(main_groups)

    lines = [
        "# Brief de podcast - ComercIAliza Online",
        "",
        "## Periodo base",
        "",
        f"**{friendly_period_label(periodo)}**",
        "",
        "## Línea editorial",
        "",
        "**[Actualidad]**",
        "",
        "## Tema del episodio",
        "",
        f"**{tema}**",
        "",
        "## Idea central",
        "",
        (
            "El objetivo del episodio no es resumir titulares, sino traducir tendencias "
            "recientes en decisiones concretas para una pyme, una tienda online y el aula."
        ),
        "",
        "## Título propuesto",
        "",
        f"**{proposed_title(main_groups)}**",
        "",
        "## Título visual",
        "",
        "**Qué está cambiando en el comercio digital**",
        "",
        "## Duración objetivo",
        "",
        "**10-13 minutos**",
        "",
        "## Noticias seleccionadas",
        "",
        f"- {plural(len(main_groups), 'bloque principal', 'bloques principales')}.",
        f"- {plural(len(security), 'aviso breve de ciberseguridad')}.",
        f"- {plural(len(reserved), 'noticia reservada')} para futuros episodios o menciones secundarias.",
        f"- Periodicidad editorial: {periodicidad}.",
        "",
        "---",
        "",
        "## Apertura sugerida",
        "",
        (
            "Esta quincena revisamos varios cambios que merece la pena seguir de cerca: "
            "dónde se descubre el producto, cómo se entrega y qué papel empiezan a tener "
            "las herramientas de inteligencia artificial en la comunicación comercial."
        ),
        "",
        "Hoy no vamos a limitarnos a repasar titulares.",
        "",
        "Vamos a intentar responder una pregunta más útil:",
        "",
        "**¿Qué decisiones podría tomar una pequeña empresa a partir de estas noticias?**",
        "",
        "---",
        "",
    ]

    for index, group in enumerate(main_groups, 1):
        lines.extend(render_episode_block(group, index))

    if security:
        lines.extend(render_security_notice(security[0]))

    lines.extend(render_reserved_news(reserved))

    lines.extend(
        [
            "# Bloque docente final",
            "",
            "## Actividad transversal",
            "",
            "Elige una de las noticias del episodio y responde:",
            "",
            "1. ¿Qué problema empresarial aparece?",
            "2. ¿Qué tecnología o tendencia está implicada?",
            "3. ¿Qué decisión podría tomar una pequeña empresa?",
            "4. ¿Qué beneficio se espera?",
            "5. ¿Qué riesgo habría que controlar?",
            "6. ¿Qué dato faltaría antes de decidir?",
            "",
            "## Propuesta de debate",
            "",
            "**¿Una pequeña empresa debe adoptar rápido las nuevas herramientas digitales o esperar hasta comprobar que realmente aportan valor?**",
            "",
            "---",
            "",
            "# Cierre sugerido",
            "",
            (
                "La tecnología cambia deprisa, pero no todas las novedades exigen una reacción inmediata. "
                "La pregunta útil no es si una pequeña empresa debe utilizar cada nueva plataforma, "
                "automatización o herramienta de inteligencia artificial. La pregunta es otra: "
                "¿qué problema concreto me ayuda a resolver y cómo voy a comprobar si ha funcionado?"
            ),
            "",
            "---",
            "",
            "# CTA sugerida",
            "",
            "Entra en ComercioDigital.net, elige una noticia de esta quincena y anota una única decisión que podría tomar una pequeña empresa a partir de ella.",
            "",
            "---",
            "",
            "# Notas de producción",
            "",
            "- No enviar este brief directamente a ElevenLabs.",
            "- Transformarlo primero en un guion conversacional.",
            "- Revisar fusiones, noticias reservadas y enfoque editorial antes de grabar.",
            "- Evitar leer actividades completas durante la locución; pueden quedar desarrolladas en WordPress.",
            "- Comprobar cifras, nombres de herramientas y afirmaciones antes de publicar.",
            "- Presentar el episodio como selección e interpretación de actualidad, no como lectura de newsletter.",
            "",
        ]
    )
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
