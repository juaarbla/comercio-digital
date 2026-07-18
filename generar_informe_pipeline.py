# -*- coding: utf-8 -*-
"""
Genera un informe post-pipeline del agregador Comercio Digital.

v0.6 — Observabilidad, diagnóstico de fuentes y preparación para despliegue permanente

Este script no modifica noticias ni publica contenido.
Solo lee los archivos generados por el pipeline y crea un informe local en logs/.
"""

import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

from paths import (
    BASE_DIR,
    DOCS_DIR,
    FEEDS_FILE,
    HISTORIAL_FILE,
    LOGS_DIR,
    NOTICIAS_CLASIFICADAS,
    NOTICIAS_RESUMIDAS,
)


# ----------------------------------------------------------------------
# Utilidades generales
# ----------------------------------------------------------------------

def cargar_json(ruta: Path, valor_defecto):
    """Carga un JSON. Si no existe o falla la lectura, devuelve valor_defecto."""
    if not ruta.exists():
        return valor_defecto

    try:
        with ruta.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR leyendo {ruta}: {e}")
        return valor_defecto


def contar_por(lista, campo: str) -> Counter:
    """Cuenta ocurrencias de un campo en una lista de diccionarios."""
    return Counter((item.get(campo) or "(vacío)") for item in lista)


def contar_booleano(lista, campo: str) -> int:
    """Cuenta elementos cuyo campo es exactamente True."""
    return sum(1 for item in lista if item.get(campo) is True)


def contar_vacios(lista, campo: str) -> int:
    """Cuenta elementos sin valor en un campo."""
    return sum(1 for item in lista if not item.get(campo))


def contar_listas_vacias(lista, campo: str) -> int:
    """Cuenta elementos cuyo campo lista está vacío o no existe."""
    return sum(1 for item in lista if not item.get(campo))


def listar_ficheros(carpeta: Path, patron: str) -> list[Path]:
    """Lista ficheros de una carpeta si existe."""
    if not carpeta.exists():
        return []
    return sorted(carpeta.glob(patron))


def generar_lineas_counter(counter: Counter) -> list[str]:
    """Convierte un Counter en líneas Markdown."""
    if not counter:
        return ["- Sin datos"]

    return [f"- {clave}: {valor}" for clave, valor in counter.most_common()]


def clave_visible_fila(fila: dict) -> str:
    """Devuelve la clave de una fila de aportacion incluyendo alias."""
    clave = str(fila.get("clave", ""))
    aliases = [item for item in fila.get("aliases", []) if item]
    if aliases:
        clave += " / " + " / ".join(aliases)
    return clave


def relativo_o_absoluto(ruta: Path) -> str:
    """Devuelve una ruta relativa a BASE_DIR si es posible."""
    try:
        return str(ruta.relative_to(BASE_DIR))
    except ValueError:
        return str(ruta)


def nombre_fuente(feed: dict) -> str:
    """
    Devuelve un nombre legible para una fuente.

    Si en el futuro se añade un campo 'nombre' a feeds.json, se usará.
    Mientras tanto, se genera a partir de la URL.
    """
    if feed.get("nombre"):
        return str(feed["nombre"])

    url = feed.get("url", "")
    if not url:
        return "(sin URL)"

    parsed = urlparse(url)
    dominio = parsed.netloc.replace("www.", "")
    path = parsed.path.strip("/")

    if "wp-json" in url:
        return f"{dominio} · WordPress API"

    if path:
        return f"{dominio}/{path}"

    return dominio or url


def fuente_configurada(feed: dict) -> str:
    """
    Devuelve la clave de fuente esperada para cruzar feeds.json con fuente_detectada.

    Prioriza el campo source si existe. Si no, usa el dominio de la URL.
    """
    source = str(feed.get("source", "")).strip()
    if source:
        return source.replace("www.", "")

    url = feed.get("url", "")
    if not url:
        return "(sin URL)"

    parsed = urlparse(url)
    dominio = parsed.netloc.replace("www.", "").strip()

    return dominio or url


def claves_fuente_configurada(feed: dict) -> list[str]:
    """
    Devuelve claves posibles para cruzar feeds.json con fuente_detectada.

    Algunas fuentes con `source`, como WordPress API, se normalizan en la
    noticia por dominio. Mantener el alias evita falsos ceros en el informe.
    """
    claves = []
    primaria = fuente_configurada(feed)
    if primaria:
        claves.append(primaria)

    url = feed.get("url", "")
    if url:
        dominio = urlparse(url).netloc.replace("www.", "").strip()
        if dominio and dominio not in claves:
            claves.append(dominio)

    return claves


def normalizar_texto(valor) -> str:
    """Normaliza valores vacíos para informes."""
    if valor is None:
        return "(vacío)"
    valor = str(valor).strip()
    return valor if valor else "(vacío)"


def fecha_procesado(item: dict) -> str:
    """
    Devuelve la fecha YYYY-MM-DD de procesado_en.

    Se usa para separar el histórico acumulado de la última ejecución detectable.
    """
    valor = str(item.get("procesado_en", "")).strip()
    if len(valor) >= 10:
        return valor[:10]
    return ""


def obtener_ultima_fecha_procesado(lista: list[dict]) -> str:
    """Obtiene la fecha más reciente disponible en procesado_en."""
    fechas = sorted({fecha_procesado(item) for item in lista if fecha_procesado(item)})
    return fechas[-1] if fechas else ""


def filtrar_por_fecha_procesado(lista: list[dict], fecha: str) -> list[dict]:
    """Filtra elementos cuya fecha procesado_en coincide con fecha."""
    if not fecha:
        return []
    return [item for item in lista if fecha_procesado(item) == fecha]


# ----------------------------------------------------------------------
# Diagnóstico de fuentes
# ----------------------------------------------------------------------

def diagnosticar_fuentes(feeds) -> dict:
    """
    Genera diagnóstico básico desde feeds.json.

    No comprueba conexión externa.
    Solo analiza la configuración declarada.
    """
    if not isinstance(feeds, list):
        return {
            "disponible": False,
            "total": 0,
            "activas": [],
            "inactivas": [],
            "activas_sin_modulo": [],
            "por_tipo_activas": Counter(),
            "por_modulo_activas": Counter(),
            "con_nota": [],
            "con_source": [],
        }

    activas = [feed for feed in feeds if feed.get("activo") is True]
    inactivas = [feed for feed in feeds if feed.get("activo") is False]
    activas_sin_modulo = [
        feed for feed in activas
        if not str(feed.get("modulo", "")).strip()
    ]

    por_tipo_activas = Counter(
        normalizar_texto(feed.get("tipo"))
        for feed in activas
    )

    por_modulo_activas = Counter(
        normalizar_texto(feed.get("modulo"))
        for feed in activas
    )

    con_nota = [feed for feed in feeds if feed.get("nota")]
    con_source = [feed for feed in feeds if feed.get("source")]

    return {
        "disponible": True,
        "total": len(feeds),
        "activas": activas,
        "inactivas": inactivas,
        "activas_sin_modulo": activas_sin_modulo,
        "por_tipo_activas": por_tipo_activas,
        "por_modulo_activas": por_modulo_activas,
        "con_nota": con_nota,
        "con_source": con_source,
    }


def diagnosticar_aportacion_fuentes(feeds, por_fuente: Counter, por_fuente_ultima: Counter) -> dict:
    """
    Cruza fuentes activas declaradas en feeds.json con las fuentes detectadas en noticias.

    Sirve para detectar fuentes activas sin aportación histórica o sin aportación reciente.
    """
    if not isinstance(feeds, list):
        return {
            "disponible": False,
            "filas": [],
            "activas_sin_historico": [],
            "activas_sin_ultima": [],
        }

    activas = [feed for feed in feeds if feed.get("activo") is True]
    filas = []

    for feed in activas:
        claves = claves_fuente_configurada(feed)
        clave = claves[0] if claves else "(sin clave)"
        historico = max((por_fuente.get(item, 0) for item in claves), default=0)
        ultima = max((por_fuente_ultima.get(item, 0) for item in claves), default=0)

        filas.append({
            "nombre": nombre_fuente(feed),
            "clave": clave,
            "aliases": [item for item in claves[1:] if item],
            "modulo": normalizar_texto(feed.get("modulo")),
            "tipo": normalizar_texto(feed.get("tipo")),
            "peso": feed.get("peso", ""),
            "historico": historico,
            "ultima": ultima,
        })

    filas.sort(key=lambda item: (item["historico"], item["ultima"], item["nombre"]), reverse=True)

    activas_sin_historico = [fila for fila in filas if fila["historico"] == 0]
    activas_sin_ultima = [fila for fila in filas if fila["ultima"] == 0]

    return {
        "disponible": True,
        "filas": filas,
        "activas_sin_historico": activas_sin_historico,
        "activas_sin_ultima": activas_sin_ultima,
    }


# ----------------------------------------------------------------------
# Comprobaciones de estado
# ----------------------------------------------------------------------

def comprobar_archivos_clave() -> dict:
    """Comprueba la existencia de archivos clave de la web generada."""
    archivos = {
        "Portada": DOCS_DIR / "index.html",
        "Aula": DOCS_DIR / "aula.html",
        "Índice newsletter": DOCS_DIR / "newsletter" / "index.html",
        "CSS principal": DOCS_DIR / "assets" / "style.css",
    }

    return {
        nombre: {
            "ruta": ruta,
            "existe": ruta.exists(),
        }
        for nombre, ruta in archivos.items()
    }


def calcular_estado_general(alertas_criticas: list[str], avisos: list[str]) -> str:
    """Calcula el semáforo general del sistema."""
    if alertas_criticas:
        return "ROJO"

    if avisos:
        return "AMARILLO"

    return "VERDE"


def descripcion_estado(estado: str) -> str:
    """Devuelve una descripción breve del estado general."""
    if estado == "ROJO":
        return "Hay incidencias críticas. Conviene revisar antes de considerar correcta la publicación."
    if estado == "AMARILLO":
        return "El sistema funciona, pero hay avisos que conviene revisar."
    return "No se han detectado incidencias relevantes."


# ----------------------------------------------------------------------
# Informe principal
# ----------------------------------------------------------------------

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

    ultima_newsletter_html = newsletters_html[-1] if newsletters_html else None
    ultima_newsletter_md = newsletters_md[-1] if newsletters_md else None
    newsletter_index = newsletter_dir / "index.html"

    por_modulo_original = contar_por(noticias_clasificadas, "modulo")
    por_modulo_asignado = contar_por(noticias_clasificadas, "modulo_asignado")
    por_modulo_relacionado = contar_por(noticias_clasificadas, "modulo_relacionado")
    por_fuente = contar_por(noticias_clasificadas, "fuente_detectada")
    por_valor_docente = contar_por(noticias_clasificadas, "valor_docente")
    por_tipo_uso = contar_por(noticias_clasificadas, "tipo_uso")

    ultima_fecha_procesado = obtener_ultima_fecha_procesado(noticias_resumidas)
    noticias_resumidas_ultima = filtrar_por_fecha_procesado(noticias_resumidas, ultima_fecha_procesado)
    noticias_clasificadas_ultima = filtrar_por_fecha_procesado(noticias_clasificadas, ultima_fecha_procesado)

    por_modulo_original_ultima = contar_por(noticias_clasificadas_ultima, "modulo")
    por_modulo_relacionado_ultima = contar_por(noticias_clasificadas_ultima, "modulo_relacionado")
    por_fuente_ultima = contar_por(noticias_clasificadas_ultima, "fuente_detectada")
    por_valor_docente_ultima = contar_por(noticias_clasificadas_ultima, "valor_docente")
    por_tipo_uso_ultima = contar_por(noticias_clasificadas_ultima, "tipo_uso")

    total_clasificadas = len(noticias_clasificadas)

    sin_ra = contar_vacios(noticias_clasificadas, "ra_asignado")
    sin_conceptos = contar_listas_vacias(noticias_clasificadas, "conceptos_clave")
    sin_actividad = contar_vacios(noticias_clasificadas, "actividad_breve")
    sin_actividad_en_fichas = sum(
        1 for item in noticias_clasificadas
        if item.get("generar_ficha") is True and not item.get("actividad_breve")
    )

    generar_ficha = contar_booleano(noticias_clasificadas, "generar_ficha")
    seleccion_newsletter = contar_booleano(noticias_clasificadas, "seleccion_newsletter")

    generar_ficha_ultima = contar_booleano(noticias_clasificadas_ultima, "generar_ficha")
    seleccion_newsletter_ultima = contar_booleano(noticias_clasificadas_ultima, "seleccion_newsletter")

    diagnostico_fuentes = diagnosticar_fuentes(feeds)
    diagnostico_aportacion_fuentes = diagnosticar_aportacion_fuentes(
        feeds,
        por_fuente,
        por_fuente_ultima,
    )
    archivos_clave = comprobar_archivos_clave()

    alertas_criticas = []
    avisos = []
    recomendaciones = []

    # ------------------------------------------------------------------
    # Alertas críticas
    # ------------------------------------------------------------------

    if not NOTICIAS_RESUMIDAS.exists():
        alertas_criticas.append(f"No se encuentra {relativo_o_absoluto(NOTICIAS_RESUMIDAS)}.")

    if not NOTICIAS_CLASIFICADAS.exists():
        alertas_criticas.append(f"No se encuentra {relativo_o_absoluto(NOTICIAS_CLASIFICADAS)}.")

    if total_clasificadas == 0:
        alertas_criticas.append("No hay noticias clasificadas.")

    if not archivos_clave["Portada"]["existe"]:
        alertas_criticas.append("No se encuentra docs/index.html.")

    if not archivos_clave["Aula"]["existe"]:
        alertas_criticas.append("No se encuentra docs/aula.html.")

    # ------------------------------------------------------------------
    # Avisos
    # ------------------------------------------------------------------

    if sin_ra > 0:
        avisos.append(f"Hay {sin_ra} noticia(s) sin RA asignado.")

    if sin_conceptos > 0:
        avisos.append(f"Hay {sin_conceptos} noticia(s) sin conceptos clave.")

    if not archivos_clave["Índice newsletter"]["existe"]:
        avisos.append("No se encuentra docs/newsletter/index.html.")

    if not archivos_clave["CSS principal"]["existe"]:
        avisos.append("No se encuentra docs/assets/style.css.")

    categorias_minimas = {
        "Comercio Electrónico": 1,
        "Digitalización": 1,
        "IA": 1,
        "CDI": 1,
    }

    for categoria, minimo in categorias_minimas.items():
        if por_modulo_relacionado.get(categoria, 0) < minimo:
            avisos.append(f"La categoría {categoria} tiene presencia muy baja o nula.")

    if por_modulo_relacionado.get("CDI", 0) <= 2:
        avisos.append("CDI aparece con muy poca presencia.")

    if por_fuente:
        fuente_principal, total_fuente_principal = por_fuente.most_common(1)[0]
        if total_clasificadas and total_fuente_principal / total_clasificadas > 0.60:
            porcentaje = round((total_fuente_principal / total_clasificadas) * 100, 1)
            avisos.append(
                f"La fuente {fuente_principal} concentra el {porcentaje}% del histórico clasificado."
            )

    if por_fuente_ultima:
        fuente_principal_ultima, total_fuente_principal_ultima = por_fuente_ultima.most_common(1)[0]
        total_ultima = len(noticias_clasificadas_ultima)
        if total_ultima and total_fuente_principal_ultima / total_ultima > 0.80:
            porcentaje_ultima = round((total_fuente_principal_ultima / total_ultima) * 100, 1)
            avisos.append(
                f"La fuente {fuente_principal_ultima} concentra el {porcentaje_ultima}% de la última ejecución detectada."
            )

    if diagnostico_aportacion_fuentes["disponible"]:
        total_activas_sin_ultima = len(diagnostico_aportacion_fuentes["activas_sin_ultima"])
        total_activas = len(diagnostico_aportacion_fuentes["filas"])
        if total_activas and total_activas_sin_ultima == total_activas:
            avisos.append("Ninguna fuente activa aparece en la última ejecución detectada.")
        elif total_activas_sin_ultima >= 3:
            avisos.append(
                f"Hay {total_activas_sin_ultima} fuente(s) activa(s) sin aportación en la última ejecución detectada."
            )

    # ------------------------------------------------------------------
    # Recomendaciones
    # ------------------------------------------------------------------

    if por_modulo_relacionado.get("CDI", 0) <= 2:
        recomendaciones.append("Revisar fuentes específicas de comercio internacional, aduanas o logística internacional.")

    if sin_actividad_en_fichas > 0:
        recomendaciones.append(
            f"Revisar {sin_actividad_en_fichas} noticia(s) marcadas para ficha sin actividad breve."
        )

    if diagnostico_aportacion_fuentes["disponible"] and diagnostico_aportacion_fuentes["activas_sin_historico"]:
        recomendaciones.append(
            "Revisar fuentes activas sin aportación histórica: pueden estar mal configuradas, ser transversales o no haber generado noticias útiles todavía."
        )

    if not recomendaciones:
        recomendaciones.append("No se proponen recomendaciones adicionales.")

    estado_general = calcular_estado_general(alertas_criticas, avisos)

    # ------------------------------------------------------------------
    # Construcción del informe Markdown
    # ------------------------------------------------------------------

    informe = []

    informe.append(f"# Informe post-pipeline — {fecha_archivo}")
    informe.append("")
    informe.append(f"Generado: {ahora.strftime('%Y-%m-%d %H:%M:%S')}")
    informe.append("")

    informe.append("## Estado general del sistema")
    informe.append("")
    informe.append(f"- Estado: **{estado_general}**")
    informe.append(f"- Lectura: {descripcion_estado(estado_general)}")
    informe.append(f"- Alertas críticas: {len(alertas_criticas)}")
    informe.append(f"- Avisos: {len(avisos)}")
    informe.append(f"- Recomendaciones: {len(recomendaciones)}")
    informe.append("")

    informe.append("## Resumen general")
    informe.append("")
    informe.append(f"- Noticias resumidas: {len(noticias_resumidas)}")
    informe.append(f"- Noticias clasificadas: {len(noticias_clasificadas)}")
    informe.append(f"- Fuentes configuradas: {diagnostico_fuentes['total'] if diagnostico_fuentes['disponible'] else 'No disponible'}")
    informe.append(f"- Fuentes activas: {len(diagnostico_fuentes['activas']) if diagnostico_fuentes['disponible'] else 'No disponible'}")
    informe.append(f"- Fuentes inactivas: {len(diagnostico_fuentes['inactivas']) if diagnostico_fuentes['disponible'] else 'No disponible'}")
    informe.append(f"- Registros en historial: {len(historial) if hasattr(historial, '__len__') else 'No disponible'}")
    informe.append(f"- Fichas HTML generadas: {len(fichas_html)}")
    informe.append(f"- Fichas MD generadas: {len(fichas_md)}")
    informe.append(f"- Newsletters HTML disponibles: {len(newsletters_html)}")
    informe.append(f"- Newsletters MD disponibles: {len(newsletters_md)}")
    informe.append("")

    informe.append("## Última ejecución detectada")
    informe.append("")
    if ultima_fecha_procesado:
        informe.append(f"- Fecha detectada por `procesado_en`: {ultima_fecha_procesado}")
        informe.append(f"- Noticias resumidas en esa fecha: {len(noticias_resumidas_ultima)}")
        informe.append(f"- Noticias clasificadas en esa fecha: {len(noticias_clasificadas_ultima)}")
        informe.append(f"- Noticias marcadas para ficha en esa fecha: {generar_ficha_ultima}")
        informe.append(f"- Noticias marcadas para newsletter en esa fecha: {seleccion_newsletter_ultima}")
        informe.append("")
        informe.append("### Fuentes en la última ejecución")
        informe.append("")
        informe.extend(generar_lineas_counter(por_fuente_ultima))
        informe.append("")
        informe.append("### Módulo relacionado en la última ejecución")
        informe.append("")
        informe.extend(generar_lineas_counter(por_modulo_relacionado_ultima))
        informe.append("")
        informe.append("### Valor docente en la última ejecución")
        informe.append("")
        informe.extend(generar_lineas_counter(por_valor_docente_ultima))
        informe.append("")
        informe.append("### Tipo de uso en la última ejecución")
        informe.append("")
        informe.extend(generar_lineas_counter(por_tipo_uso_ultima))
    else:
        informe.append("- No se ha podido detectar una última ejecución mediante `procesado_en`.")
    informe.append("")

    informe.append("## Archivos clave de la web")
    informe.append("")
    for nombre, datos in archivos_clave.items():
        estado_archivo = "OK" if datos["existe"] else "NO ENCONTRADO"
        informe.append(f"- {nombre}: {estado_archivo} — `{relativo_o_absoluto(datos['ruta'])}`")
    informe.append("")

    informe.append("## Calidad docente")
    informe.append("")
    informe.append(f"- Noticias marcadas para ficha: {generar_ficha}")
    informe.append(f"- Noticias marcadas para newsletter: {seleccion_newsletter}")
    informe.append(f"- Noticias sin RA asignado: {sin_ra}")
    informe.append(f"- Noticias sin conceptos clave: {sin_conceptos}")
    informe.append(f"- Noticias sin actividad breve: {sin_actividad}")
    informe.append(f"- Noticias marcadas para ficha sin actividad breve: {sin_actividad_en_fichas}")
    informe.append("")

    informe.append("## Diagnóstico de fuentes")
    informe.append("")
    if diagnostico_fuentes["disponible"]:
        informe.append(f"- Fuentes configuradas: {diagnostico_fuentes['total']}")
        informe.append(f"- Fuentes activas: {len(diagnostico_fuentes['activas'])}")
        informe.append(f"- Fuentes inactivas: {len(diagnostico_fuentes['inactivas'])}")
        informe.append(f"- Fuentes activas sin módulo declarado: {len(diagnostico_fuentes['activas_sin_modulo'])}")
        informe.append(f"- Fuentes con nota: {len(diagnostico_fuentes['con_nota'])}")
        informe.append(f"- Fuentes con configuración `source`: {len(diagnostico_fuentes['con_source'])}")
        informe.append("")

        informe.append("### Fuentes activas por tipo")
        informe.append("")
        informe.extend(generar_lineas_counter(diagnostico_fuentes["por_tipo_activas"]))
        informe.append("")

        informe.append("### Fuentes activas por módulo declarado")
        informe.append("")
        informe.extend(generar_lineas_counter(diagnostico_fuentes["por_modulo_activas"]))
        informe.append("")

        informe.append("### Fuentes activas sin módulo declarado")
        informe.append("")
        if diagnostico_fuentes["activas_sin_modulo"]:
            informe.append("Estas fuentes se consideran transversales o pendientes de clasificación automática. No generan alerta por sí solas.")
            informe.append("")
            for feed in diagnostico_fuentes["activas_sin_modulo"]:
                informe.append(f"- {nombre_fuente(feed)}")
        else:
            informe.append("- No hay fuentes activas sin módulo declarado.")
        informe.append("")

        informe.append("### Fuentes inactivas")
        informe.append("")
        if diagnostico_fuentes["inactivas"]:
            for feed in diagnostico_fuentes["inactivas"]:
                linea = f"- {nombre_fuente(feed)}"
                if feed.get("nota"):
                    linea += f" — {feed.get('nota')}"
                informe.append(linea)
        else:
            informe.append("- No hay fuentes inactivas.")
        informe.append("")
    else:
        informe.append("- No se ha podido analizar feeds.json.")
        informe.append("")

    informe.append("## Aportación de fuentes activas")
    informe.append("")
    if diagnostico_aportacion_fuentes["disponible"]:
        informe.append("Cruce entre fuentes activas declaradas en `feeds.json` y noticias detectadas en el histórico y en la última ejecución.")
        informe.append("")
        informe.append("| Fuente activa | Clave | Módulo | Peso | Histórico | Última ejecución |")
        informe.append("|---|---|---|---:|---:|---:|")
        for fila in diagnostico_aportacion_fuentes["filas"]:
            informe.append(
                f"| {fila['nombre']} | `{clave_visible_fila(fila)}` | {fila['modulo']} | {fila['peso']} | {fila['historico']} | {fila['ultima']} |"
            )
        informe.append("")
        informe.append(f"- Fuentes activas sin aportación histórica: {len(diagnostico_aportacion_fuentes['activas_sin_historico'])}")
        informe.append(f"- Fuentes activas sin aportación en la última ejecución: {len(diagnostico_aportacion_fuentes['activas_sin_ultima'])}")
        informe.append("")

        informe.append("### Fuentes activas sin aportación histórica")
        informe.append("")
        if diagnostico_aportacion_fuentes["activas_sin_historico"]:
            for fila in diagnostico_aportacion_fuentes["activas_sin_historico"]:
                informe.append(f"- {fila['nombre']} — clave `{fila['clave']}`")
        else:
            informe.append("- No hay fuentes activas sin aportación histórica.")
        informe.append("")

        informe.append("### Fuentes activas sin aportación en la última ejecución")
        informe.append("")
        if diagnostico_aportacion_fuentes["activas_sin_ultima"]:
            for fila in diagnostico_aportacion_fuentes["activas_sin_ultima"]:
                informe.append(f"- {fila['nombre']} — clave `{fila['clave']}`")
        else:
            informe.append("- Todas las fuentes activas aportaron noticias en la última ejecución detectada.")
    else:
        informe.append("- No se ha podido cruzar la aportación de fuentes activas.")
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

    informe.append("## Observación sobre Marketing Digital")
    informe.append("")
    marketing_original = por_modulo_original.get("Marketing Digital", 0)
    marketing_relacionado = por_modulo_relacionado.get("Marketing Digital", 0)
    informe.append(f"- Noticias con módulo original Marketing Digital: {marketing_original}")
    informe.append(f"- Noticias con módulo relacionado Marketing Digital: {marketing_relacionado}")
    informe.append("- Marketing Digital se usa como fuente temática de entrada, pero no como módulo curricular final independiente.")
    informe.append("- Según las reglas actuales de clasificación, las noticias de origen Marketing Digital se reclasifican normalmente como Comercio Electrónico o IA para Marketing y Comercio.")
    informe.append("")

    informe.append("## Distribución por valor docente")
    informe.append("")
    informe.extend(generar_lineas_counter(por_valor_docente))
    informe.append("")

    informe.append("## Distribución por tipo de uso")
    informe.append("")
    informe.extend(generar_lineas_counter(por_tipo_uso))
    informe.append("")

    informe.append("## Distribución por fuente detectada en noticias")
    informe.append("")
    informe.extend(generar_lineas_counter(por_fuente))
    informe.append("")

    informe.append("## Última newsletter detectada")
    informe.append("")
    if ultima_newsletter_html:
        informe.append(f"- Última newsletter HTML: `{ultima_newsletter_html.name}`")
    else:
        informe.append("- Última newsletter HTML: no detectada.")

    if ultima_newsletter_md:
        informe.append(f"- Última newsletter MD: `{ultima_newsletter_md.name}`")
    else:
        informe.append("- Última newsletter MD: no detectada.")

    informe.append(f"- Índice newsletter: {'detectado' if newsletter_index.exists() else 'no detectado'}")
    informe.append("")

    informe.append("## Últimas newsletters HTML disponibles")
    informe.append("")
    if newsletters_html:
        for newsletter in newsletters_html[-5:]:
            informe.append(f"- {newsletter.name}")
    else:
        informe.append("- No se han encontrado newsletters HTML.")
    informe.append("")

    informe.append("## Alertas críticas")
    informe.append("")
    if alertas_criticas:
        for alerta in alertas_criticas:
            informe.append(f"- {alerta}")
    else:
        informe.append("- No se han detectado alertas críticas.")
    informe.append("")

    informe.append("## Avisos")
    informe.append("")
    if avisos:
        for aviso in avisos:
            informe.append(f"- {aviso}")
    else:
        informe.append("- No se han detectado avisos.")
    informe.append("")

    informe.append("## Recomendaciones")
    informe.append("")
    if recomendaciones:
        for recomendacion in recomendaciones:
            informe.append(f"- {recomendacion}")
    else:
        informe.append("- No se proponen recomendaciones adicionales.")
    informe.append("")

    informe.append("## Archivos revisados")
    informe.append("")
    informe.append(f"- {relativo_o_absoluto(NOTICIAS_RESUMIDAS)}")
    informe.append(f"- {relativo_o_absoluto(NOTICIAS_CLASIFICADAS)}")
    informe.append(f"- {relativo_o_absoluto(FEEDS_FILE)}")
    informe.append(f"- {relativo_o_absoluto(HISTORIAL_FILE)}")
    informe.append(f"- {relativo_o_absoluto(DOCS_DIR / 'fichas-aula')}")
    informe.append(f"- {relativo_o_absoluto(DOCS_DIR / 'newsletter')}")
    informe.append("")

    ruta_informe = LOGS_DIR / f"informe_pipeline_{fecha_archivo}.md"
    ruta_informe.write_text("\n".join(informe), encoding="utf-8")

    print(f"Informe generado correctamente: {ruta_informe}")
    print(f"Estado general del sistema: {estado_general}")


if __name__ == "__main__":
    generar_informe()
