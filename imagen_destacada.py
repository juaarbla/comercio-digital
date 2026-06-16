"""
Generador de imagen destacada para cada noticia
Opciones: rss (extraer del feed) | openai (DALL-E)
"""

import os
import json
import re
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ─── CONFIG ───────────────────────────────────────────────────────────────────

IMAGE_PROVIDER  = os.getenv("IMAGE_PROVIDER", "rss").lower()   # "rss" | "openai"
OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY", "")
OPENAI_IMG_SIZE = os.getenv("OPENAI_IMG_SIZE", "1024x1024")    # 1024x1024 | 1792x1024
OPENAI_IMG_MODEL = os.getenv("OPENAI_IMG_MODEL", "dall-e-3")

from paths import NOTICIAS_CLASIFICADAS, CACHE_IMAGENES

INPUT_FILE = NOTICIAS_CLASIFICADAS
OUTPUT_FILE = NOTICIAS_CLASIFICADAS   # Actualiza el mismo archivo
CACHE_FILE = CACHE_IMAGENES           # url_noticia -> imagen_url (solo éxitos)

# ─── CACHÉ DE IMÁGENES ─────────────────────────────────────────────────────

def cargar_cache() -> dict:
    if not CACHE_FILE.exists():
        return {}
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Aviso: no se pudo leer la caché de imágenes ({e}). Se empieza vacía.")
        return {}


def guardar_cache(cache: dict) -> None:
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

# ─── OPCIÓN C: EXTRAER IMAGEN DEL RSS ─────────────────────────────────────────

def extraer_imagen_rss(noticia: dict) -> str:
    """
    Intenta obtener la imagen directamente del feed RSS de la noticia.
    Hace una petición al feed de origen y busca la imagen del artículo concreto.
    """
    url_noticia = noticia.get("url", "")
    if not url_noticia:
        return ""

    # Intentar extraer imagen desde la URL de la noticia con og:image
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; FPNewsBot/1.0)"}
        r = requests.get(url_noticia, headers=headers, timeout=10)
        r.raise_for_status()
        html = r.text

        # Buscar og:image (la más fiable)
        match = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\'](https?://[^"\']+)["\']', html)
        if match:
            return match.group(1)

        # Fallback: twitter:image
        match = re.search(r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\'](https?://[^"\']+)["\']', html)
        if match:
            return match.group(1)

    except Exception as e:
        print(f"    RSS fetch error: {e}")

    return ""


# ─── OPCIÓN A: OPENAI DALL-E ──────────────────────────────────────────────────

def construir_prompt_imagen(noticia: dict) -> str:
    """Genera un prompt para DALL-E basado en la noticia."""
    modulo  = noticia.get("modulo_asignado") or noticia.get("modulo", "")
    titulo  = noticia.get("titulo", "")
    resumen = noticia.get("resumen", "")[:200]

    return (
        f"Create a clean, professional editorial illustration for an educational article. "
        f"Topic: {titulo}. Context: {resumen}. "
        f"Style: flat design, modern, suitable for a vocational education blog about {modulo}. "
        f"No text, no logos, no people's faces. Warm colors, professional look."
    )


def generar_imagen_openai(noticia: dict) -> str:
    """Llama a DALL-E y devuelve la URL de la imagen generada."""
    if not OPENAI_API_KEY:
        print("    Sin OPENAI_API_KEY en .env")
        return ""

    prompt = construir_prompt_imagen(noticia)

    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": OPENAI_IMG_MODEL,
            "prompt": prompt,
            "n": 1,
            "size": OPENAI_IMG_SIZE,
            "response_format": "url",
        }
        r = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers=headers,
            json=payload,
            timeout=60,
        )
        r.raise_for_status()
        url = r.json()["data"][0]["url"]
        return url

    except Exception as e:
        print(f"    DALL-E error: {e}")
        return ""


# ─── DISPATCHER ───────────────────────────────────────────────────────────────

def obtener_imagen(noticia: dict) -> str:
    if IMAGE_PROVIDER == "openai":
        return generar_imagen_openai(noticia)
    else:
        # rss: intenta og:image, si falla devuelve vacío
        return extraer_imagen_rss(noticia)


# ─── PRINCIPAL ────────────────────────────────────────────────────────────────

def procesar_imagenes():
    if not INPUT_FILE.exists():
        print(f"No se encontro {INPUT_FILE}. Ejecuta primero el clasificador.")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        noticias = json.load(f)

    cache = cargar_cache()
    print(f"Caché de imágenes: {len(cache)} URLs ya resueltas\n")

    pendientes     = [n for n in noticias if not n.get("imagen_url")]
    ya_procesadas  = [n for n in noticias if n.get("imagen_url")]

    print(f"Proveedor imagen: {IMAGE_PROVIDER.upper()}")
    print(f"Total noticias : {len(noticias)}")
    print(f"Con imagen     : {len(ya_procesadas)}")
    print(f"Sin imagen     : {len(pendientes)}\n")

    if not pendientes:
        print("Todas las noticias ya tienen imagen.")
        return

    actualizadas = []
    desde_cache = 0
    nuevas_en_cache = 0

    for i, noticia in enumerate(pendientes, 1):
        titulo_corto = noticia["titulo"][:55]
        url_noticia = noticia.get("url", "")
        print(f"[{i}/{len(pendientes)}] {titulo_corto}...")

        # 1. Comprobar caché primero (solo éxitos quedan cacheados)
        if url_noticia and url_noticia in cache:
            url_imagen = cache[url_noticia]
            print(f"           Caché: {url_imagen[:70]}...")
            desde_cache += 1
        else:
            url_imagen = obtener_imagen(noticia)
            if url_imagen:
                print(f"           OK: {url_imagen[:70]}...")
                if url_noticia:
                    cache[url_noticia] = url_imagen
                    nuevas_en_cache += 1
            else:
                print(f"           Sin imagen")

        noticia["imagen_url"] = url_imagen
        actualizadas.append(noticia)

    todos = actualizadas + ya_procesadas

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)

    if nuevas_en_cache:
        guardar_cache(cache)

    con_imagen = sum(1 for n in todos if n.get("imagen_url"))
    print(f"\nListo! {con_imagen}/{len(todos)} noticias con imagen")
    print(f"Desde caché: {desde_cache} · Nuevas peticiones con éxito: {nuevas_en_cache}")
    print(f"Guardado en: {OUTPUT_FILE}")
    print(f"Caché actualizada en: {CACHE_FILE} ({len(cache)} URLs totales)")


# ─── ENTRADA ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    procesar_imagenes()
