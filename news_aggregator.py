"""
Agregador de noticias para FP Comercio
Lee feeds RSS, resume con LLM (Ollama o Claude) y guarda en JSON
"""

import os
import re
import json
import hashlib
import requests
from datetime import datetime, timezone
from pathlib import Path

import feedparser
from dotenv import load_dotenv

load_dotenv()

# ─── CONFIGURACIÓN ────────────────────────────────────────────────────────────

FEEDS_FILE = Path("feeds.json")

def cargar_feeds() -> list:
    if not FEEDS_FILE.exists():
        print(f"AVISO: No se encontro {FEEDS_FILE}. Crea el archivo con los feeds.")
        return []
    with open(FEEDS_FILE, "r", encoding="utf-8") as f:
        feeds = json.load(f)
    activos = [f for f in feeds if f.get("activo", True)]
    print(f"Feeds cargados: {len(activos)} activos de {len(feeds)} totales")
    return activos

FEEDS = cargar_feeds()

WP_CATEGORY_TO_MODULE = {
    "Inteligencia Artificial": "IA para Marketing y Comercio",
    "Marketing Digital": "Marketing Digital",
    "Comercio Electrónico": "Comercio Electrónico",
    "Comercio Digital Internacional": "Comercio Digital Internacional",
    "Digitalización": "Digitalización GS",
}

WP_CATEGORY_CACHE: dict[int, str] = {}

# Horas hacia atrás para considerar una noticia "nueva"
HORAS_RECIENTES = int(os.getenv("HORAS_RECIENTES", 48))

# Palabras clave en el título que descartan la noticia automáticamente
PALABRAS_DESCARTADAS = [
    "vulnerabilidad", "vulnerabilidades",
    "cve-", "boletín de vulnerabilidades",
    "actualización de seguridad", "parche crítico",
    "advisory", "exploit",
]

# Archivos de datos
from paths import FEEDS_FILE, HISTORIAL_FILE, NOTICIAS_RESUMIDAS

OUTPUT_FILE = NOTICIAS_RESUMIDAS

# ─── LLM: detección automática de proveedor ───────────────────────────────────

LLM_PROVIDER    = os.getenv("LLM_PROVIDER", "ollama").lower()   # "ollama" | "anthropic"
CHAT_MODEL      = os.getenv("CHAT_MODEL", "gemma4:latest")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
ANTHROPIC_KEY   = os.getenv("ANTHROPIC_API_KEY", "")

# ─── FUNCIONES DE HISTORIAL ───────────────────────────────────────────────────

def cargar_historial() -> set:
    if HISTORIAL_FILE.exists():
        with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def guardar_historial(historial: set):
    with open(HISTORIAL_FILE, "w", encoding="utf-8") as f:
        json.dump(list(historial), f, ensure_ascii=False, indent=2)

# ─── FUNCIONES DE FEED ────────────────────────────────────────────────────────

def id_noticia(entry) -> str:
    clave = entry.get("link") or entry.get("id") or entry.get("title", "")
    return hashlib.md5(clave.encode()).hexdigest()

def es_reciente(entry) -> bool:
    published = entry.get("published_parsed") or entry.get("updated_parsed")
    if not published:
        fecha_iso = entry.get("published") or entry.get("date") or entry.get("date_gmt") or entry.get("modified")
        if not fecha_iso:
            return True
        try:
            fecha = datetime.fromisoformat(str(fecha_iso).replace("Z", "+00:00"))
            if fecha.tzinfo is None:
                fecha = fecha.replace(tzinfo=timezone.utc)
        except Exception:
            return True
    else:
        fecha = datetime(*published[:6], tzinfo=timezone.utc)
    horas_diff = (datetime.now(timezone.utc) - fecha).total_seconds() / 3600
    return horas_diff <= HORAS_RECIENTES

def es_relevante(entry) -> bool:
    """Descarta noticias cuyo título contiene palabras de ruido."""
    titulo = entry.get("title", "").lower()
    descartada = any(p in titulo for p in PALABRAS_DESCARTADAS)
    if descartada:
        print(f"  [filtro] Descartada: {entry.get('title','')[:60]}")
    return not descartada


HEADERS_RSS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
    "Accept-Language": "es-ES,es;q=0.9",
}


def limpiar_html(texto: str) -> str:
    return re.sub(r"<[^>]+>", " ", texto or "").strip()


def obtener_nombre_categoria_wp(category_id: int) -> str:
    if category_id in WP_CATEGORY_CACHE:
        return WP_CATEGORY_CACHE[category_id]

    try:
        r = requests.get(
            f"https://juanarmada.com/wp-json/wp/v2/categories/{category_id}",
            headers=HEADERS_RSS,
            timeout=15,
        )
        r.raise_for_status()
        nombre = r.json().get("name", "")
    except Exception:
        nombre = ""

    WP_CATEGORY_CACHE[category_id] = nombre
    return nombre


def inferir_modulo_wp(post: dict, modulo_default: str = "") -> str:
    for category_id in post.get("categories", []):
        categoria = obtener_nombre_categoria_wp(category_id)
        if categoria in WP_CATEGORY_TO_MODULE:
            return WP_CATEGORY_TO_MODULE[categoria]
    return modulo_default


def normalizar_post_wp(post: dict, feed_config: dict) -> dict:
    titulo = post.get("title", {}).get("rendered", "Sin título")
    url = post.get("link", "")
    contenido = post.get("content", {}).get("rendered") or post.get("excerpt", {}).get("rendered") or titulo
    modulo = inferir_modulo_wp(post, feed_config.get("modulo", ""))
    return {
        "id": id_noticia({"link": url, "id": post.get("id", ""), "title": titulo}),
        "titulo": titulo,
        "url": url,
        "contenido_original": limpiar_html(contenido)[:2000],
        "modulo": modulo,
        "tipo": feed_config.get("tipo", "articulo"),
        "fecha_publicacion": post.get("date_gmt") or post.get("date") or "",
        "date": post.get("date_gmt") or post.get("date") or "",
        "published": post.get("date_gmt") or post.get("date") or "",
    }

def obtener_noticias_nuevas(historial: set) -> list[dict]:
    noticias = []
    for feed_config in FEEDS:
        url    = feed_config["url"]
        modulo = feed_config.get("modulo", "")
        source = feed_config.get("source", "rss")
        print(f"Leyendo: {url}")
        try:
            r = requests.get(url, headers=HEADERS_RSS, timeout=15)
            r.raise_for_status()

            if source == "wordpress_api":
                posts = r.json()
                for post in posts:
                    noticia = normalizar_post_wp(post, feed_config)
                    if noticia["id"] in historial or not es_reciente(noticia) or not es_relevante(noticia):
                        continue
                    noticias.append(noticia)
                continue

            feed = feedparser.parse(r.content)
            for entry in feed.entries:
                nid = id_noticia(entry)
                if nid in historial or not es_reciente(entry) or not es_relevante(entry):
                    continue
                contenido = (
                    entry.get("summary")
                    or entry.get("description")
                    or entry.get("title", "")
                )
                contenido_limpio = limpiar_html(contenido)
                noticias.append({
                    "id":                nid,
                    "titulo":            entry.get("title", "Sin título"),
                    "url":               entry.get("link", ""),
                    "contenido_original": contenido_limpio[:2000],
                    "modulo":            modulo,
                    "tipo":              feed_config.get("tipo", "noticia"),
                    "fecha_publicacion": entry.get("published", ""),
                })
        except Exception as e:
            print(f"  ⚠️  Error leyendo {url}: {e}")
    print(f"\n✅ {len(noticias)} noticias nuevas encontradas\n")
    return noticias

# ─── FUNCIONES LLM ────────────────────────────────────────────────────────────

def construir_prompt(noticia: dict) -> str:
    tipo = noticia.get("tipo", "noticia")

    if tipo == "podcast":
        return f"""Eres el asistente editorial de Juan Armada, docente de FP Comercio y Marketing.
Resume este episodio de podcast en 2-3 frases que inviten a escucharlo.
Mantén un tono cercano y práctico. Menciona que es un podcast.
No uses frases genéricas como "en este episodio".

Título: {noticia['titulo']}
Contenido: {noticia['contenido_original']}

Solo el resumen, sin introducción ni explicaciones adicionales."""

    if tipo == "articulo" and noticia.get("modulo") == "Del Autor":
        return f"""Eres el asistente editorial de Juan Armada, docente de FP Comercio y Marketing.
Resume este artículo de su blog en 2-3 frases que inviten a leerlo.
Mantén su tono práctico y directo, orientado a docentes y alumnos de FP.
No uses frases genéricas como "en este artículo".

Título: {noticia['titulo']}
Contenido: {noticia['contenido_original']}

Solo el resumen, sin introducción ni explicaciones adicionales."""

    # Prompt estándar para noticias externas
    return f"""Eres un docente de Formación Profesional especializado en Comercio y Marketing.
Tu tarea es resumir noticias de actualidad para que sean útiles en el aula, especialmente para el módulo de "{noticia['modulo']}".

Noticia:
Título: {noticia['titulo']}
Contenido: {noticia['contenido_original']}

Escribe un resumen de 3-4 frases SIEMPRE EN ESPAÑOL (aunque la noticia esté en inglés) que:
1. Explique qué ha pasado de forma clara y directa
2. Conecte con conceptos del módulo cuando sea relevante
3. Use lenguaje accesible para alumnos de FP (no jerga excesiva)

Solo el resumen en español, sin introducción ni explicaciones adicionales."""


def resumir_con_ollama(noticia: dict) -> str:
    url = f"{OLLAMA_BASE_URL}/api/chat"
    payload = {
        "model": CHAT_MODEL,
        "stream": False,
        "messages": [{"role": "user", "content": construir_prompt(noticia)}]
    }
    try:
        r = requests.post(url, json=payload, timeout=60)
        r.raise_for_status()
        return r.json()["message"]["content"].strip()
    except Exception as e:
        print(f"  ⚠️  Error Ollama para '{noticia['titulo']}': {e}")
        return ""


def resumir_con_anthropic(noticia: dict) -> str:
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": construir_prompt(noticia)}]
        )
        return response.content[0].text.strip()
    except Exception as e:
        print(f"  ⚠️  Error Anthropic para '{noticia['titulo']}': {e}")
        return ""


def resumir(noticia: dict) -> str:
    if LLM_PROVIDER == "anthropic":
        return resumir_con_anthropic(noticia)
    return resumir_con_ollama(noticia)

# ─── FUNCIÓN PRINCIPAL ────────────────────────────────────────────────────────

def procesar_noticias():
    print(f"🧠 Proveedor LLM: {LLM_PROVIDER.upper()}"
          + (f" → {OLLAMA_BASE_URL}" if LLM_PROVIDER == "ollama" else "")
          + f"  |  Modelo: {CHAT_MODEL if LLM_PROVIDER == 'ollama' else 'claude-sonnet-4'}\n")

    if LLM_PROVIDER == "anthropic" and not ANTHROPIC_KEY:
        raise ValueError("LLM_PROVIDER=anthropic pero ANTHROPIC_API_KEY no está definida en .env")

    historial = cargar_historial()
    print(f"📚 Historial: {len(historial)} noticias ya procesadas\n")

    noticias = obtener_noticias_nuevas(historial)
    if not noticias:
        print("No hay noticias nuevas. Prueba a ampliar HORAS_RECIENTES en .env")
        return

    resultados = []
    for i, noticia in enumerate(noticias, 1):
        print(f"🤖 Resumiendo {i}/{len(noticias)}: {noticia['titulo'][:60]}...")
        resumen = resumir(noticia)
        if resumen:
            resultados.append({
                "titulo":            noticia["titulo"],
                "url":               noticia["url"],
                "modulo":            noticia["modulo"],
                "tipo":              noticia.get("tipo", "noticia"),
                "fecha_publicacion": noticia["fecha_publicacion"],
                "resumen":           resumen,
                "procesado_en":      datetime.now().isoformat(),
                "llm":               f"{LLM_PROVIDER}/{CHAT_MODEL}",
            })
            historial.add(noticia["id"])

    existentes = []
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            existentes = json.load(f)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(resultados + existentes, f, ensure_ascii=False, indent=2)

    guardar_historial(historial)
    print(f"\n🎉 Listo! {len(resultados)} noticias resumidas → {OUTPUT_FILE}")

# ─── ENTRADA ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    procesar_noticias()
