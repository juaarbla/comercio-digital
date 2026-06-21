"""
Clasificador de noticias por RA/CE v2

Mejora principal:
- Los RA/CE oficiales ya no están hardcodeados en este archivo.
- Se leen desde archivos Markdown ubicados en data/curriculo/.
- La clasificación añade módulo, RA, CE relacionados y textos oficiales para que
  generar_fichas_aula.py pueda mostrarlos directamente.

Estructura esperada recomendada:

data/
  curriculo/
    00_CE_RA_CE_oficial.md
    00_CDI_RA_CE_oficial.md
    00_Digitalizacion-GM_RA_CE_oficial.md
    00_Digitalizacion-GS_RA_CE_oficial.md
    00_IAMC_RA_CE_oficial.md
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

# ─── CONFIG ───────────────────────────────────────────────────────────────────

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()
CHAT_MODEL = os.getenv("CHAT_MODEL", "gemma4:latest")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY", "")

from paths import NOTICIAS_RESUMIDAS, NOTICIAS_CLASIFICADAS, CACHE_CLASIFICACION

INPUT_FILE = NOTICIAS_RESUMIDAS
OUTPUT_FILE = NOTICIAS_CLASIFICADAS
CACHE_FILE = CACHE_CLASIFICACION

# Puedes sobrescribir esta ruta en .env:
# CURRICULO_DIR=data/curriculo
PROJECT_ROOT = Path(__file__).resolve().parent
CURRICULO_DIR = Path(os.getenv("CURRICULO_DIR", PROJECT_ROOT / "data" / "curriculo"))

CURRICULO_FILES = {
    "Comercio Electrónico": "00_CE_RA_CE_oficial.md",
    "Comercio Digital Internacional": "00_CDI_RA_CE_oficial.md",
    "Digitalización GM": "00_Digitalizacion-GM_RA_CE_oficial.md",
    "Digitalización GS": "00_Digitalizacion-GS_RA_CE_oficial.md",
    "IA para Marketing y Comercio": "00_IAMC_RA_CE_oficial.md",
}


# ─── CACHÉ DE CLASIFICACIÓN ───────────────────────────────────────────────────

def clave_cache(noticia: dict[str, Any]) -> str:
    """Hash de título+resumen: si el resumen cambia, se reclasifica."""
    base = (noticia.get("titulo", "") + "|" + noticia.get("resumen", "")).encode("utf-8")
    return hashlib.sha256(base).hexdigest()


def cargar_cache() -> dict[str, Any]:
    if not CACHE_FILE.exists():
        return {}
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Aviso: no se pudo leer la caché de clasificación ({e}). Se empieza vacía.")
        return {}


def guardar_cache(cache: dict[str, Any]) -> None:
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


# ─── LECTURA DE RA/CE OFICIALES DESDE MARKDOWN ────────────────────────────────

def extraer_frontmatter(texto: str) -> tuple[dict[str, str], str]:
    """Extrae frontmatter YAML simple si existe. No requiere PyYAML."""
    if not texto.startswith("---"):
        return {}, texto

    partes = texto.split("---", 2)
    if len(partes) < 3:
        return {}, texto

    frontmatter_raw = partes[1]
    cuerpo = partes[2]
    meta: dict[str, str] = {}

    for linea in frontmatter_raw.splitlines():
        if ":" not in linea or linea.strip().startswith("-"):
            continue
        clave, valor = linea.split(":", 1)
        meta[clave.strip()] = valor.strip().strip('"').strip("'")

    return meta, cuerpo


def limpiar_linea(linea: str) -> str:
    return re.sub(r"\s+", " ", linea.strip()).strip()


def parsear_curriculo_md(path: Path, modulo_por_defecto: str) -> dict[str, Any]:
    """
    Convierte un Markdown oficial en una estructura:
    {
      "modulo": "Comercio Electrónico",
      "ras": {
        "RA1": {
          "texto": "...",
          "criterios": {"a": "...", "b": "..."}
        }
      }
    }
    """
    texto = path.read_text(encoding="utf-8")
    meta, cuerpo = extraer_frontmatter(texto)

    modulo = meta.get("titulo", modulo_por_defecto)
    # Si el título incluye " - RA y CE oficiales", nos quedamos con el nombre limpio.
    modulo = modulo.replace(" - RA y CE oficiales", "").strip() or modulo_por_defecto

    ras: dict[str, Any] = {}
    patron_ra = re.compile(r"^###\s+(RA\d+)\s*$", re.MULTILINE)
    coincidencias = list(patron_ra.finditer(cuerpo))

    for idx, match in enumerate(coincidencias):
        codigo_ra = match.group(1).strip()
        inicio = match.end()
        fin = coincidencias[idx + 1].start() if idx + 1 < len(coincidencias) else len(cuerpo)
        bloque = cuerpo[inicio:fin].strip()

        partes = re.split(r"Criterios de evaluaci[oó]n\s*:", bloque, maxsplit=1, flags=re.IGNORECASE)
        texto_ra = limpiar_linea(partes[0])
        criterios: dict[str, str] = {}

        if len(partes) > 1:
            criterios_raw = partes[1]
            for linea in criterios_raw.splitlines():
                linea = limpiar_linea(linea)
                m = re.match(r"^([a-z])\)\s+(.*)$", linea, flags=re.IGNORECASE)
                if m:
                    letra = m.group(1).lower()
                    criterios[letra] = m.group(2).strip()

        ras[codigo_ra] = {
            "texto": texto_ra,
            "criterios": criterios,
        }

    return {
        "modulo": modulo_por_defecto,
        "archivo": str(path),
        "ras": ras,
    }


def cargar_curriculos() -> dict[str, Any]:
    curriculos: dict[str, Any] = {}
    errores: list[str] = []

    for modulo, filename in CURRICULO_FILES.items():
        path = CURRICULO_DIR / filename
        if not path.exists():
            errores.append(f"- Falta {path}")
            continue
        try:
            curriculos[modulo] = parsear_curriculo_md(path, modulo)
        except Exception as e:
            errores.append(f"- Error leyendo {path}: {e}")

    if errores:
        print("Aviso: incidencias cargando currículos:")
        print("\n".join(errores))

    if not curriculos:
        raise RuntimeError(
            f"No se ha cargado ningún currículo. Comprueba CURRICULO_DIR={CURRICULO_DIR}"
        )

    return curriculos


CURRICULOS = cargar_curriculos()


def construir_lista_ra_ce_para_prompt() -> str:
    bloques: list[str] = []

    for modulo, data in CURRICULOS.items():
        bloques.append(f"MÓDULO: {modulo}")
        for codigo_ra, ra_data in data["ras"].items():
            bloques.append(f"- {codigo_ra}: {ra_data['texto']}")
            for letra, texto_ce in ra_data.get("criterios", {}).items():
                bloques.append(f"  CE {letra}) {texto_ce}")
        bloques.append("")

    return "\n".join(bloques)


# ─── VALIDACIÓN Y ENRIQUECIMIENTO DE LA RESPUESTA LLM ─────────────────────────

def normalizar_lista_ce(valor: Any) -> list[str]:
    """Acepta ['a','b'], ['CE a','CE1a'], 'a,b' y devuelve ['a','b']."""
    if valor is None:
        return []
    if isinstance(valor, str):
        partes = re.split(r"[,;]\s*", valor)
    elif isinstance(valor, list):
        partes = [str(v) for v in valor]
    else:
        return []

    ces: list[str] = []
    for item in partes:
        item = item.strip().lower()
        m = re.search(r"([a-z])$", item)
        if m:
            letra = m.group(1)
            if letra not in ces:
                ces.append(letra)
    return ces


def completar_con_textos_oficiales(clasificacion: dict[str, Any]) -> dict[str, Any] | None:
    modulo = clasificacion.get("modulo", "")
    ra = clasificacion.get("ra", "")

    if modulo not in CURRICULOS:
        return None
    if ra not in CURRICULOS[modulo]["ras"]:
        return None

    ra_data = CURRICULOS[modulo]["ras"][ra]
    criterios_disponibles = ra_data.get("criterios", {})
    ce_asignados = normalizar_lista_ce(clasificacion.get("ce", []))

    # Filtra CE inexistentes y limita a 3 para que la ficha no quede inflada.
    ce_asignados = [ce for ce in ce_asignados if ce in criterios_disponibles][:3]

    ce_textos = [
        {
            "codigo": f"{ra}{letra}",
            "letra": letra,
            "texto": criterios_disponibles[letra],
        }
        for letra in ce_asignados
    ]

    return {
        "modulo": modulo,
        "ra": ra,
        "ra_texto": ra_data["texto"],
        "ce": ce_asignados,
        "ce_textos": ce_textos,
        "justificacion": clasificacion.get("justificacion", ""),
    }


# ─── PROMPT ───────────────────────────────────────────────────────────────────

def construir_prompt_clasificacion(noticia: dict[str, Any]) -> str:
    ra_ce_texto = construir_lista_ra_ce_para_prompt()
    modulo_origen = noticia.get("modulo", "")

    return f"""Eres un docente experto en Formación Profesional de la familia de Comercio y Marketing.

Tienes esta noticia resumida:
- Título: {noticia['titulo']}
- Resumen: {noticia['resumen']}
- Módulo de origen (feed RSS): {modulo_origen}

Y esta base curricular oficial de Resultados de Aprendizaje y Criterios de Evaluación:
{ra_ce_texto}

INSTRUCCIONES DE CLASIFICACIÓN — SIGUE ESTE ORDEN:

REGLA 1 — Marketing Digital del feed → normalmente "Comercio Electrónico":
Si el módulo de origen es "Marketing Digital", clasifica en "Comercio Electrónico" RA1, RA4 o RA5 salvo que la noticia trate claramente de herramientas de IA generativa, chatbots, agentes IA o regulación/ética de IA.

REGLA 2 — Comercio Electrónico del feed → "Comercio Electrónico":
Logística, tiendas online, pagos, modelos de negocio → RA2. Marketing online → RA1. Web/catálogo → RA3. RRSS/comunidad/contenidos → RA4. Web 2.0/presencia digital/feedback → RA5.

REGLA 3 — "IA para Marketing y Comercio" SOLO para estos casos concretos:
Herramientas de IA generativa, creación de contenido con IA, diseño con IA, redes sociales con IA, email marketing con IA, chatbots, agentes IA autónomos, soporte predictivo o regulación/ética de IA.

REGLA 4 — "Digitalización GM/GS" para:
Cloud, IoT, ciberseguridad técnica, transformación digital empresarial, industria 4.0, Big Data como infraestructura, datos, IT/OT, tecnologías habilitadoras.

REGLA 5 — "Comercio Digital Internacional" para:
Comercio exterior, exportación digital, mercados internacionales, logística internacional, normativa aduanera UE, promoción internacional, facturación electrónica internacional.

Tu tarea:
1. Elige un único módulo.
2. Elige un único RA.
3. Elige entre 1 y 3 criterios de evaluación concretos de ese RA.
4. Redacta una justificación breve y docente.

Responde ÚNICAMENTE con un objeto JSON válido, sin texto adicional:
{{
  "modulo": "nombre exacto del módulo",
  "ra": "RA1",
  "ce": ["a", "b"],
  "justificacion": "una frase breve explicando la conexión curricular"
}}"""


# ─── LLM ──────────────────────────────────────────────────────────────────────

def clasificar_con_ollama(noticia: dict[str, Any]) -> dict[str, Any] | None:
    url = f"{OLLAMA_BASE_URL}/api/chat"
    payload = {
        "model": CHAT_MODEL,
        "stream": False,
        "format": "json",
        "messages": [{"role": "user", "content": construir_prompt_clasificacion(noticia)}],
    }
    try:
        r = requests.post(url, json=payload, timeout=90)
        r.raise_for_status()
        texto = r.json()["message"]["content"].strip()
        return json.loads(texto)
    except Exception as e:
        print(f"  Error Ollama: {e}")
        return None


def clasificar_con_anthropic(noticia: dict[str, Any]) -> dict[str, Any] | None:
    try:
        import anthropic

        client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            messages=[{"role": "user", "content": construir_prompt_clasificacion(noticia)}],
        )
        texto = response.content[0].text.strip()
        return json.loads(texto)
    except Exception as e:
        print(f"  Error Anthropic: {e}")
        return None


def clasificar(noticia: dict[str, Any]) -> dict[str, Any] | None:
    if LLM_PROVIDER == "anthropic":
        return clasificar_con_anthropic(noticia)
    return clasificar_con_ollama(noticia)


# ─── APLICAR CLASIFICACIÓN A NOTICIA ──────────────────────────────────────────

def aplicar_clasificacion(noticia: dict[str, Any], clasificacion: dict[str, Any]) -> dict[str, Any]:
    noticia["modulo_asignado"] = clasificacion.get("modulo", "")
    noticia["ra_asignado"] = clasificacion.get("ra", "")
    noticia["ra_texto"] = clasificacion.get("ra_texto", "")
    noticia["ce_asignados"] = clasificacion.get("ce", [])
    noticia["ce_textos"] = clasificacion.get("ce_textos", [])
    noticia["ra_justificacion"] = clasificacion.get("justificacion", "")
    return noticia


def marcar_sin_clasificar(noticia: dict[str, Any]) -> dict[str, Any]:
    noticia["ra_asignado"] = "Sin clasificar"
    noticia["modulo_asignado"] = noticia.get("modulo", "")
    noticia["ra_texto"] = ""
    noticia["ce_asignados"] = []
    noticia["ce_textos"] = []
    noticia["ra_justificacion"] = ""
    return noticia


# ─── PRINCIPAL ────────────────────────────────────────────────────────────────

def clasificar_noticias() -> None:
    if not INPUT_FILE.exists():
        print(f"No se encontró {INPUT_FILE}. Ejecuta primero news_aggregator.py")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        noticias = json.load(f)

    cache = cargar_cache()
    print(f"Currículos cargados desde: {CURRICULO_DIR}")
    for modulo, data in CURRICULOS.items():
        print(f"- {modulo}: {len(data['ras'])} RA")
    print(f"\nCaché de clasificación: {len(cache)} entradas\n")

    pendientes = [n for n in noticias if "ra_asignado" not in n]
    ya_clasificadas = [n for n in noticias if "ra_asignado" in n]

    print(f"Proveedor: {LLM_PROVIDER.upper()} | Modelo: {CHAT_MODEL}")
    print(f"Total noticias: {len(noticias)}")
    print(f"Ya clasificadas: {len(ya_clasificadas)}")
    print(f"Pendientes: {len(pendientes)}\n")

    if not pendientes:
        print("Todas las noticias ya están clasificadas.")
        return

    resultados_nuevos: list[dict[str, Any]] = []
    desde_cache = 0
    nuevas_en_cache = 0

    for i, noticia in enumerate(pendientes, 1):
        titulo_corto = noticia.get("titulo", "")[:60]
        print(f"[{i}/{len(pendientes)}] {titulo_corto}...")

        if noticia.get("modulo") == "Del Autor":
            noticia["ra_asignado"] = ""
            noticia["modulo_asignado"] = "Del Autor"
            noticia["ra_texto"] = ""
            noticia["ce_asignados"] = []
            noticia["ce_textos"] = []
            noticia["ra_justificacion"] = ""
            print("         -> Del Autor (sin clasificar por RA)")
            resultados_nuevos.append(noticia)
            continue

        clave = clave_cache(noticia)

        if clave in cache:
            clasificacion = completar_con_textos_oficiales(cache[clave]) or cache[clave]
            noticia = aplicar_clasificacion(noticia, clasificacion)
            print(f"         -> {noticia['modulo_asignado']} | {noticia['ra_asignado']} | CE {noticia['ce_asignados']} (caché)")
            desde_cache += 1
            resultados_nuevos.append(noticia)
            continue

        clasificacion_raw = clasificar(noticia)
        clasificacion = completar_con_textos_oficiales(clasificacion_raw or {})

        if clasificacion:
            noticia = aplicar_clasificacion(noticia, clasificacion)
            print(f"         -> {noticia['modulo_asignado']} | {noticia['ra_asignado']} | CE {noticia['ce_asignados']}")

            cache[clave] = {
                "modulo": clasificacion["modulo"],
                "ra": clasificacion["ra"],
                "ce": clasificacion["ce"],
                "justificacion": clasificacion["justificacion"],
            }
            nuevas_en_cache += 1
        else:
            noticia = marcar_sin_clasificar(noticia)
            print("         -> Sin clasificar")

        resultados_nuevos.append(noticia)

    todos = resultados_nuevos + ya_clasificadas

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)

    if nuevas_en_cache:
        guardar_cache(cache)

    print(f"\nListo. {len(resultados_nuevos)} noticias procesadas")
    print(f"Desde caché: {desde_cache} · Nuevas peticiones con éxito: {nuevas_en_cache}")
    print(f"Guardadas en: {OUTPUT_FILE}")
    print(f"Caché actualizada en: {CACHE_FILE} ({len(cache)} entradas totales)")


if __name__ == "__main__":
    clasificar_noticias()
