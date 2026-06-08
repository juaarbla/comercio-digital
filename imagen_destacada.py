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

INPUT_FILE  = Path("noticias_clasificadas.json")
OUTPUT_FILE = Path("noticias_clasificadas.json")   # Actualiza el mismo archivo

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
    for i, noticia in enumerate(pendientes, 1):
        titulo_corto = noticia["titulo"][:55]
        print(f"[{i}/{len(pendientes)}] {titulo_corto}...")

        url_imagen = obtener_imagen(noticia)

        if url_imagen:
            noticia["imagen_url"] = url_imagen
            print(f"           OK: {url_imagen[:70]}...")
        else:
            noticia["imagen_url"] = ""
            print(f"           Sin imagen")

        actualizadas.append(noticia)

    todos = actualizadas + ya_procesadas

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)

    con_imagen = sum(1 for n in todos if n.get("imagen_url"))
    print(f"\nListo! {con_imagen}/{len(todos)} noticias con imagen")
    print(f"Guardado en: {OUTPUT_FILE}")


# ─── ENTRADA ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    procesar_imagenes()
