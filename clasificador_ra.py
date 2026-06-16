"""
Clasificador de noticias por RA/CE
Lee noticias_resumidas.json y añade módulo, RA y CE a cada noticia
"""

import os
import json
import hashlib
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ─── CONFIG ───────────────────────────────────────────────────────────────────

LLM_PROVIDER    = os.getenv("LLM_PROVIDER", "ollama").lower()
CHAT_MODEL      = os.getenv("CHAT_MODEL", "gemma4:latest")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
ANTHROPIC_KEY   = os.getenv("ANTHROPIC_API_KEY", "")

INPUT_FILE  = Path("noticias_resumidas.json")
OUTPUT_FILE = Path("noticias_clasificadas.json")
CACHE_FILE  = Path("cache_clasificacion.json")  # hash(titulo+resumen) -> clasificación (solo éxitos)

# ─── CACHÉ DE CLASIFICACIÓN ────────────────────────────────────────────────

def clave_cache(noticia: dict) -> str:
    """Hash de título+resumen: si el resumen cambia, se reclasifica."""
    base = (noticia.get("titulo", "") + "|" + noticia.get("resumen", "")).encode("utf-8")
    return hashlib.sha256(base).hexdigest()


def cargar_cache() -> dict:
    if not CACHE_FILE.exists():
        return {}
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Aviso: no se pudo leer la caché de clasificación ({e}). Se empieza vacía.")
        return {}


def guardar_cache(cache: dict) -> None:
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

# ─── BASE DE CONOCIMIENTO: RA/CE POR MÓDULO ───────────────────────────────────

MODULOS_RA_CE = {
    "Comercio Electrónico": {
        "RA1": "Aplica las directrices del plan de marketing digital: posicionamiento, SEO/SEM, publicidad online, fidelización, CRM, tendencias marketing digital.",
        "RA2": "Realiza ventas online: crear negocio online, captación clientes, modelos de negocio, tienda virtual, logística, medios de pago, seguridad.",
        "RA3": "Mantiene página web, tienda electrónica y catálogo online: HTML, registro dominio, publicación web, diseño.",
        "RA4": "Establece foros y comunicación: redes sociales empresariales, blogs, mensajería, contenidos audiovisuales, publicidad en RRSS.",
        "RA5": "Utiliza entornos Web 2.0: reputación online, herramientas SMM, RSS, comparadores, prosumidor, seguridad informática.",
    },
    "Comercio Digital Internacional": {
        "RA1": "Elabora plan de marketing digital internacional: posicionamiento internacional, publicidad online internacional, marketing buscadores, fidelización clientes internacionales, mobile marketing.",
        "RA2": "Utiliza Internet como canal de promoción internacional: navegadores, búsquedas, conexión red, intranets/extranets.",
        "RA3": "Gestiona servicios y protocolos de Internet: correo electrónico, FTP, foros internacionales, redes sociales internacionales, blogs profesionales.",
        "RA4": "Define política de comercio electrónico internacional: tienda virtual internacional, modelos de negocio, logística internacional, medios de pago internacionales, seguridad.",
        "RA5": "Realiza facturación electrónica y tareas administrativas telemáticas: EDIFACT, XML, firma electrónica, organismos públicos online, seguridad datos.",
    },
    "Digitalización GM": {
        "RA1": "Economía Lineal vs Economía Circular: sostenibilidad, reciclaje, ODS, impacto medioambiental.",
        "RA2": "4ª Revolución Industrial: sistemas ciber-físicos, automatización, IoT, entornos 4.0, ventajas para empresas y clientes.",
        "RA3": "Sistemas cloud/nube: niveles cloud, edge computing, fog, mist, ventajas nube.",
        "RA4": "Tecnologías habilitadoras digitales: IoT, IA, Big Data, 5G, robótica colaborativa, Blockchain, ciberseguridad, realidad virtual, gemelos digitales.",
        "RA5": "Plan de transformación digital: diagrama empresa clásica, etapas digitalizables, tecnologías implicadas, informe de viabilidad.",
    },
    "Digitalización GS": {
        "RA1": "Digitalización y sectores productivos: entornos IT/OT, tecnologías digitales, conexión IT-OT, ventajas digitalización empresa.",
        "RA2": "Tecnologías habilitadoras digitales avanzadas: THD, economía sostenible, nuevos mercados, informe tecnologías.",
        "RA3": "Cloud/nube avanzado: niveles, edge computing, fog, mist, ventajas.",
        "RA4": "IA en sectores productivos: automatización procesos, Big Data, lenguajes programación IA, aplicaciones sectoriales.",
        "RA5": "Datos y ciberseguridad: ciclo vida del dato, Big Data, machine learning, almacenaje cloud, regulación seguridad datos.",
        "RA6": "Proyecto transformación digital: objetivos estratégicos, áreas digitalizables, tecnologías, brechas seguridad, gestión datos, recursos humanos.",
    },
    "IA para Marketing y Comercio": {
        "RA1": "Herramientas de IA para empresa, marketing y comercio: identificar herramientas IA, segmentación mercado con IA.",
        "RA2": "Elaborar textos y contenido con IA: copywriting, textos persuasivos, marketing de contenidos, SEO con IA.",
        "RA3": "Diseño, branding y creatividad con IA: herramientas diseño IA, branding asistido.",
        "RA4": "Redes sociales con IA: análisis tendencias, diseño publicaciones, automatización y personalización RRSS.",
        "RA5": "Marketing digital con IA: estrategias marketing digital IA, email marketing IA, segmentación público objetivo.",
        "RA6": "Atención al cliente con IA: chatbots, IA generativa, sistemas predictivos, soporte automatizado.",
        "RA7": "Ética y legalidad IA: riesgos legales, privacidad datos, cumplimiento normativo.",
    },
}

# ─── PROMPT ───────────────────────────────────────────────────────────────────

def construir_prompt_clasificacion(noticia: dict) -> str:
    # Construir lista de módulos/RA para el prompt
    lista_ra = []
    for modulo, ras in MODULOS_RA_CE.items():
        for ra, descripcion in ras.items():
            lista_ra.append(f'  {{"modulo": "{modulo}", "ra": "{ra}", "descripcion": "{descripcion}"}}')

    ra_texto = "\n".join(lista_ra)
    modulo_origen = noticia.get("modulo", "")

    return f"""Eres un docente experto en Formación Profesional de Comercio y Marketing.

Tienes esta noticia resumida:
- Título: {noticia['titulo']}
- Resumen: {noticia['resumen']}
- Módulo de origen (feed RSS): {modulo_origen}

Y esta lista de Resultados de Aprendizaje (RA) de diferentes módulos:
{ra_texto}

INSTRUCCIONES DE CLASIFICACIÓN — SIGUE ESTE ORDEN ESTRICTAMENTE:

REGLA 1 — Marketing Digital del feed → siempre "Comercio Electrónico":
Si el módulo de origen es "Marketing Digital", clasifica en "Comercio Electrónico" RA1 (campañas, SEO, branding, RRSS, publicidad) o RA4 (redes sociales, influencers, contenidos). NO uses "IA para Marketing y Comercio" aunque se mencione IA.

REGLA 2 — Comercio Electrónico del feed → "Comercio Electrónico":
Logística, tiendas online, pagos, modelos de negocio → RA2. Marketing online → RA1. RRSS → RA4.

REGLA 3 — "IA para Marketing y Comercio" SOLO para estos casos concretos:
Herramientas de IA generativa (ChatGPT, DALL-E, Midjourney), chatbots de atención al cliente, agentes IA autónomos, o regulación/ética de la IA. Si no es uno de estos casos exactos, NO uses este módulo.

REGLA 4 — "Digitalización GM/GS" para:
Cloud, IoT, ciberseguridad técnica, transformación digital empresarial, industria 4.0, Big Data como infraestructura.

REGLA 5 — "Comercio Digital Internacional" para:
Comercio exterior, exportación digital, mercados internacionales, logística internacional, normativa aduanera UE.

Responde ÚNICAMENTE con un objeto JSON válido, sin texto adicional, sin explicaciones, sin comillas extra:
{{
  "modulo": "nombre exacto del módulo de la lista",
  "ra": "RA1",
  "justificacion": "una frase breve explicando la conexión"
}}"""


# ─── LLM ──────────────────────────────────────────────────────────────────────

def clasificar_con_ollama(noticia: dict) -> dict | None:
    url = f"{OLLAMA_BASE_URL}/api/chat"
    payload = {
        "model": CHAT_MODEL,
        "stream": False,
        "format": "json",
        "messages": [{"role": "user", "content": construir_prompt_clasificacion(noticia)}]
    }
    try:
        r = requests.post(url, json=payload, timeout=90)
        r.raise_for_status()
        texto = r.json()["message"]["content"].strip()
        return json.loads(texto)
    except Exception as e:
        print(f"  Error Ollama: {e}")
        return None


def clasificar_con_anthropic(noticia: dict) -> dict | None:
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": construir_prompt_clasificacion(noticia)}]
        )
        texto = response.content[0].text.strip()
        return json.loads(texto)
    except Exception as e:
        print(f"  Error Anthropic: {e}")
        return None


def clasificar(noticia: dict) -> dict | None:
    if LLM_PROVIDER == "anthropic":
        return clasificar_con_anthropic(noticia)
    return clasificar_con_ollama(noticia)


# ─── PRINCIPAL ────────────────────────────────────────────────────────────────

def clasificar_noticias():
    if not INPUT_FILE.exists():
        print(f"No se encontro {INPUT_FILE}. Ejecuta primero news_aggregator.py")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        noticias = json.load(f)

    cache = cargar_cache()
    print(f"Caché de clasificación: {len(cache)} entradas\n")

    # Filtrar las que ya tienen clasificacion
    pendientes = [n for n in noticias if "ra_asignado" not in n]
    ya_clasificadas = [n for n in noticias if "ra_asignado" in n]

    print(f"Proveedor: {LLM_PROVIDER.upper()} | Modelo: {CHAT_MODEL}")
    print(f"Total noticias: {len(noticias)}")
    print(f"Ya clasificadas: {len(ya_clasificadas)}")
    print(f"Pendientes: {len(pendientes)}\n")

    if not pendientes:
        print("Todas las noticias ya estan clasificadas.")
        return

    resultados_nuevos = []
    desde_cache = 0
    nuevas_en_cache = 0

    for i, noticia in enumerate(pendientes, 1):
        titulo_corto = noticia['titulo'][:60]
        print(f"[{i}/{len(pendientes)}] {titulo_corto}...")

        # Contenido propio — no clasificar por RA, no pasa por caché
        if noticia.get("modulo") == "Del Autor":
            noticia["ra_asignado"]      = ""
            noticia["modulo_asignado"]  = "Del Autor"
            noticia["ra_justificacion"] = ""
            print(f"         -> Del Autor (sin clasificar por RA)")
            resultados_nuevos.append(noticia)
            continue

        clave = clave_cache(noticia)

        if clave in cache:
            clasificacion = cache[clave]
            noticia["ra_asignado"]      = clasificacion.get("ra", "")
            noticia["modulo_asignado"]  = clasificacion.get("modulo", "")
            noticia["ra_justificacion"] = clasificacion.get("justificacion", "")
            print(f"         -> {noticia['modulo_asignado']} | {noticia['ra_asignado']} (caché)")
            desde_cache += 1
            resultados_nuevos.append(noticia)
            continue

        clasificacion = clasificar(noticia)

        if clasificacion and "modulo" in clasificacion and "ra" in clasificacion:
            noticia["ra_asignado"]      = clasificacion.get("ra", "")
            noticia["modulo_asignado"]  = clasificacion.get("modulo", "")
            noticia["ra_justificacion"] = clasificacion.get("justificacion", "")
            print(f"         -> {noticia['modulo_asignado']} | {noticia['ra_asignado']}")

            # Solo éxitos van a caché
            cache[clave] = {
                "modulo": noticia["modulo_asignado"],
                "ra": noticia["ra_asignado"],
                "justificacion": noticia["ra_justificacion"],
            }
            nuevas_en_cache += 1
        else:
            noticia["ra_asignado"]      = "Sin clasificar"
            noticia["modulo_asignado"]  = noticia.get("modulo", "")
            noticia["ra_justificacion"] = ""
            print(f"         -> Sin clasificar")

        resultados_nuevos.append(noticia)

    # Combinar: nuevas clasificadas + las que ya lo estaban
    todos = resultados_nuevos + ya_clasificadas

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)

    if nuevas_en_cache:
        guardar_cache(cache)

    print(f"\nListo! {len(resultados_nuevos)} noticias clasificadas")
    print(f"Desde caché: {desde_cache} · Nuevas peticiones con éxito: {nuevas_en_cache}")
    print(f"Guardadas en: {OUTPUT_FILE}")
    print(f"Caché actualizada en: {CACHE_FILE} ({len(cache)} entradas totales)")


# ─── ENTRADA ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    clasificar_noticias()
