# -*- coding: utf-8 -*-
"""
Genera un informe post-pipeline del agregador Comercio Digital.

v0.5 — Control de calidad y seguimiento

Este script no modifica noticias ni publica contenido.
Solo lee los archivos generados por el pipeline y crea un informe local en logs/.
"""

import json
from collections import Counter
from datetime import datetime
from pathlib import Path

from paths import (
    BASE_DIR,
    DOCS_DIR,
    FEEDS_FILE,
    HISTORIAL_FILE,
    LOGS_DIR,
    NOTICIAS_CLASIFICADAS,
    NOTICIAS_RESUMIDAS,
)


def cargar_json(ruta: Path, valor_defecto):
    if not ruta.exists():
        return valor_defecto

    try:
        with ruta.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR leyendo {ruta}: {e}")
        return valor_defecto


def contar_por(lista, campo: str) -> Counter:
    return Counter((item.get(campo) or "(vacío)") for item in lista)


def contar_booleano(lista, campo: str) -> int:
    return sum(1 for item in lista if item.get(campo) is True)


def contar_vacios(lista, campo: str) -> int:
    return sum(1 for item in lista if not item.get(campo))


def contar_listas_vacias(lista, campo: str) -> int:
    return sum(1 for item in lista if not item.get(campo))


def listar_ficheros(carpeta: Path, patron: str) -> list[Path]:
    if not carpeta.exists():
        return []
    return sorted(carpeta.glob(patron))


def generar_lineas_counter(counter: Counter) -> list[str]:
    if not counter:
        return ["- Sin datos"]

    return [f"- {clave}: {valor}" for clave, valor in counter.most_common()]


def generar_informe():
    ahora = datetime.now()
    fecha_archivo = ahora.strftime("%Y-%m-%d")

    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    noticias_resumidas = cargar_json(NOTICIAS_RESUMIDAS, [])
    noticias_clasificadas = cargar_json(NOTICIAS_CLASIFICADAS, [])
    feeds = cargar_json(FEEDS_FILE, [])
    historial = cargar_json(HISTORIAL_FILE, {})

    fichas_dir = DOCS_DIR / "fichas-aula"
    newsletter_dir = DOCS_DIR / "newsletter"

    fichas_html = listar_ficheros(fichas_dir, "*.html")
    fichas_md = [
        f for f in listar_ficheros(fichas_dir, "*.md")
        if f.name != "material-aula.md"
    ]

    newsletters_html = listar_ficheros(newsletter_dir, "newsletter-*.html")
    newsletters_md = listar_ficheros(newsletter_dir, "newsletter-*.md")

    por_modulo_original = contar_por(noticias_clasificadas, "modulo")
    por_modulo_asignado = contar_por(noticias_clasificadas, "modulo_asignado")
    por_modulo_relacionado = contar_por(noticias_clasificadas, "modulo_relacionado")
    por_fuente = contar_por(noticias_clasificadas, "fuente_detectada")
    por_valor_docente = contar_por(noticias_clasificadas, "valor_docente")
    por_tipo_uso = contar_por(noticias_clasificadas, "tipo_uso")

    total_clasificadas = len(noticias_clasificadas)

    sin_ra = contar_vacios(noticias_clasificadas, "ra_asignado")
    sin_conceptos = contar_listas_vacias(noticias_clasificadas, "conceptos_clave")
    sin_actividad = contar_vacios(noticias_clasificadas, "actividad_breve")

    generar_ficha = contar_booleano(noticias_clasificadas, "generar_ficha")
    seleccion_newsletter = contar_booleano(noticias_clasificadas, "seleccion_newsletter")

    alertas = []

    if not NOTICIAS_RESUMIDAS.exists():
        alertas.append(f"No se encuentra {NOTICIAS_RESUMIDAS}")

    if not NOTICIAS_CLASIFICADAS.exists():
        alertas.append(f"No se encuentra {NOTICIAS_CLASIFICADAS}")

    if total_clasificadas == 0:
        alertas.append("No hay noticias clasificadas.")

    if sin_ra > 0:
        alertas.append(f"Hay {sin_ra} noticia(s) sin RA asignado.")

    if sin_conceptos > 0:
        alertas.append(f"Hay {sin_conceptos} noticia(s) sin conceptos clave.")

    categorias_minimas = {
        "Comercio Electrónico": 1,
        "Digitalización": 1,
        "IA": 1,
        "CDI": 1,
        "Marketing Digital": 1,
    }

    for categoria, minimo in categorias_minimas.items():
        if por_modulo_relacionado.get(categoria, 0) < minimo:
            alertas.append(f"La categoría {categoria} tiene presencia muy baja o nula.")

    if por_modulo_relacionado.get("CDI", 0) <= 2:
        alertas.append("CDI aparece con muy poca presencia. Conviene revisar fuentes específicas.")

    if por_modulo_relacionado.get("Marketing Digital", 0) <= 2:
        alertas.append("Marketing Digital aparece con muy poca presencia. Conviene revisar fuentes específicas.")

    if por_fuente:
        fuente_principal, total_fuente_principal = por_fuente.most_common(1)[0]
        if total_clasificadas and total_fuente_principal / total_clasificadas > 0.60:
            porcentaje = round((total_fuente_principal / total_clasificadas) * 100, 1)
            alertas.append(
                f"La fuente {fuente_principal} concentra el {porcentaje}% de las noticias."
            )

    if not alertas:
        alertas.append("No se han detectado alertas relevantes.")

    informe = []

    informe.append(f"# Informe post-pipeline — {fecha_archivo}")
    informe.append("")
    informe.append(f"Generado: {ahora.strftime('%Y-%m-%d %H:%M:%S')}")
    informe.append("")
    informe.append("## Resumen general")
    informe.append("")
    informe.append(f"- Noticias resumidas: {len(noticias_resumidas)}")
    informe.append(f"- Noticias clasificadas: {len(noticias_clasificadas)}")
    informe.append(f"- Fuentes configuradas: {len(feeds) if isinstance(feeds, list) else 'No disponible'}")
    informe.append(f"- Registros en historial: {len(historial) if hasattr(historial, '__len__') else 'No disponible'}")
    informe.append(f"- Fichas HTML generadas: {len(fichas_html)}")
    informe.append(f"- Fichas MD generadas: {len(fichas_md)}")
    informe.append(f"- Newsletters HTML disponibles: {len(newsletters_html)}")
    informe.append(f"- Newsletters MD disponibles: {len(newsletters_md)}")
    informe.append("")

    informe.append("## Calidad docente")
    informe.append("")
    informe.append(f"- Noticias marcadas para ficha: {generar_ficha}")
    informe.append(f"- Noticias marcadas para newsletter: {seleccion_newsletter}")
    informe.append(f"- Noticias sin RA asignado: {sin_ra}")
    informe.append(f"- Noticias sin conceptos clave: {sin_conceptos}")
    informe.append(f"- Noticias sin actividad breve: {sin_actividad}")
    informe.append("")

    informe.append("## Distribución por módulo relacionado")
    informe.append("")
    informe.extend(generar_lineas_counter(por_modulo_relacionado))
    informe.append("")

    informe.append("## Distribución por módulo asignado")
    informe.append("")
    informe.extend(generar_lineas_counter(por_modulo_asignado))
    informe.append("")

    informe.append("## Distribución por módulo original")
    informe.append("")
    informe.extend(generar_lineas_counter(por_modulo_original))
    informe.append("")

    informe.append("## Distribución por valor docente")
    informe.append("")
    informe.extend(generar_lineas_counter(por_valor_docente))
    informe.append("")

    informe.append("## Distribución por tipo de uso")
    informe.append("")
    informe.extend(generar_lineas_counter(por_tipo_uso))
    informe.append("")

    informe.append("## Distribución por fuente")
    informe.append("")
    informe.extend(generar_lineas_counter(por_fuente))
    informe.append("")

    informe.append("## Últimas newsletters detectadas")
    informe.append("")
    if newsletters_html:
        for newsletter in newsletters_html[-5:]:
            informe.append(f"- {newsletter.name}")
    else:
        informe.append("- No se han encontrado newsletters HTML.")
    informe.append("")

    informe.append("## Alertas")
    informe.append("")
    for alerta in alertas:
        informe.append(f"- {alerta}")
    informe.append("")

    informe.append("## Archivos revisados")
    informe.append("")
    informe.append(f"- {NOTICIAS_RESUMIDAS.relative_to(BASE_DIR)}")
    informe.append(f"- {NOTICIAS_CLASIFICADAS.relative_to(BASE_DIR)}")
    informe.append(f"- {FEEDS_FILE.relative_to(BASE_DIR)}")
    informe.append(f"- {HISTORIAL_FILE.relative_to(BASE_DIR)}")
    informe.append(f"- {(DOCS_DIR / 'fichas-aula').relative_to(BASE_DIR)}")
    informe.append(f"- {(DOCS_DIR / 'newsletter').relative_to(BASE_DIR)}")
    informe.append("")

    ruta_informe = LOGS_DIR / f"informe_pipeline_{fecha_archivo}.md"
    ruta_informe.write_text("\n".join(informe), encoding="utf-8")

    print(f"Informe generado correctamente: {ruta_informe}")


if __name__ == "__main__":
    generar_informe()