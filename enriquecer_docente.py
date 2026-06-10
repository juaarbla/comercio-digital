# -*- coding: utf-8 -*-
"""
Enriquecedor docente de noticias.

Lee noticias_clasificadas.json y añade, para cada noticia:
- pregunta_aula
- conceptos_clave
- actividad_breve

Uso:
    python enriquecer_docente.py

El script intenta usar el mismo proveedor LLM del resto del proyecto:
- LLM_PROVIDER=ollama
- LLM_PROVIDER=anthropic

Si el LLM falla, aplica un fallback sencillo para no romper el pipeline.
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

INPUT_FILE = Path("noticias_clasificadas.json")
OUTPUT_FILE = Path("noticias_clasificadas.json")

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()
CHAT_MODEL = os.getenv("CHAT_MODEL", "gemma4:latest")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# 0 significa sin límite. Puede ser útil en pruebas: MAX_ENRIQUECER_DOCENTE=5
MAX_ENRIQUECER_DOCENTE = int(os.getenv("MAX_ENRIQUECER_DOCENTE", "0"))


def tiene_enriquecimiento(noticia: dict) -> bool:
    return bool(
        noticia.get("pregunta_aula")
        and noticia.get("conceptos_clave")
        and noticia.get("actividad_breve")
    )


def construir_prompt(noticia: dict) -> str:
    titulo = noticia.get("titulo", "")
    resumen = noticia.get("resumen", "")
    modulo = noticia.get("modulo_asignado") or noticia.get("modulo", "")
    ra = noticia.get("ra_asignado", "")
    justificacion = noticia.get("ra_justificacion", "")

    return f"""Eres un docente de Formación Profesional de la familia de Comercio y Marketing.

A partir de esta noticia ya resumida, genera una pequeña capa didáctica útil para clase.

Noticia:
- Título: {titulo}
- Resumen: {resumen}
- Módulo asignado: {modulo}
- RA asignado: {ra}
- Justificación RA: {justificacion}

Devuelve ÚNICAMENTE un objeto JSON válido con esta estructura exacta:

{{
  "pregunta_aula": "una pregunta breve para iniciar debate o reflexión en clase",
  "conceptos_clave": ["concepto 1", "concepto 2", "concepto 3"],
  "actividad_breve": "una microactividad práctica de 10-15 minutos para alumnado de FP"
}}

Criterios:
- Siempre en español.
- Lenguaje claro para alumnado de FP.
- No inventes datos que no estén en la noticia.
- La actividad debe poder hacerse en clase sin herramientas complejas.
- Los conceptos clave deben ser concretos y útiles.
"""


def enriquecer_con_ollama(noticia: dict) -> dict | None:
    import requests

    url = f"{OLLAMA_BASE_URL}/api/chat"
    payload = {
        "model": CHAT_MODEL,
        "stream": False,
        "format": "json",
        "messages": [{"role": "user", "content": construir_prompt(noticia)}],
    }

    try:
        r = requests.post(url, json=payload, timeout=90)
        r.raise_for_status()
        texto = r.json()["message"]["content"].strip()
        return json.loads(texto)
    except Exception as e:
        print(f"  Error Ollama: {e}")
        return None


def enriquecer_con_anthropic(noticia: dict) -> dict | None:
    try:
        import anthropic

        client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=400,
            messages=[{"role": "user", "content": construir_prompt(noticia)}],
        )
        texto = response.content[0].text.strip()
        return json.loads(texto)
    except Exception as e:
        print(f"  Error Anthropic: {e}")
        return None


def fallback_docente(noticia: dict) -> dict:
    modulo = noticia.get("modulo_asignado") or noticia.get("modulo") or "el módulo"
    ra = noticia.get("ra_asignado", "")

    conceptos = []
    texto_base = " ".join([
        noticia.get("titulo", ""),
        noticia.get("resumen", ""),
        modulo,
        ra,
    ]).lower()

    candidatos = [
        ("comercio electrónico", ["comercio electrónico", "venta online", "e-commerce"]),
        ("logística", ["logística", "entrega", "última milla", "almacén"]),
        ("marketing digital", ["marketing", "campaña", "publicidad", "seo", "redes sociales"]),
        ("inteligencia artificial", ["ia", "inteligencia artificial", "chatbot", "agente"]),
        ("ciberseguridad", ["ciberseguridad", "vulnerabilidad", "phishing", "seguridad"]),
        ("transformación digital", ["digitalización", "transformación digital", "automatización"]),
        ("experiencia de cliente", ["cliente", "experiencia", "usuario", "ux"]),
    ]

    for concepto, palabras in candidatos:
        if any(p in texto_base for p in palabras):
            conceptos.append(concepto)

    if not conceptos:
        conceptos = ["actualidad del sector", "empresa digital", "toma de decisiones"]

    conceptos = conceptos[:3]

    return {
        "pregunta_aula": f"¿Qué relación tiene esta noticia con los contenidos de {modulo}?",
        "conceptos_clave": conceptos,
        "actividad_breve": "Resume la noticia en tres ideas clave y explica en parejas cómo podría afectar a una empresa real del sector.",
    }


def normalizar_enriquecimiento(data: dict, noticia: dict) -> dict:
    if not isinstance(data, dict):
        return fallback_docente(noticia)

    pregunta = str(data.get("pregunta_aula", "")).strip()
    actividad = str(data.get("actividad_breve", "")).strip()
    conceptos = data.get("conceptos_clave", [])

    if isinstance(conceptos, str):
        conceptos = [c.strip() for c in conceptos.split(",") if c.strip()]
    elif isinstance(conceptos, list):
        conceptos = [str(c).strip() for c in conceptos if str(c).strip()]
    else:
        conceptos = []

    if not pregunta or not actividad or not conceptos:
        return fallback_docente(noticia)

    return {
        "pregunta_aula": pregunta,
        "conceptos_clave": conceptos[:5],
        "actividad_breve": actividad,
    }


def enriquecer(noticia: dict) -> dict:
    if LLM_PROVIDER == "anthropic":
        resultado = enriquecer_con_anthropic(noticia)
    else:
        resultado = enriquecer_con_ollama(noticia)

    if not resultado:
        resultado = fallback_docente(noticia)

    return normalizar_enriquecimiento(resultado, noticia)


def enriquecer_noticias():
    if not INPUT_FILE.exists():
        print(f"No se encontro {INPUT_FILE}. Ejecuta primero clasificador_ra.py")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        noticias = json.load(f)

    pendientes = [n for n in noticias if not tiene_enriquecimiento(n)]

    if MAX_ENRIQUECER_DOCENTE > 0:
        pendientes = pendientes[:MAX_ENRIQUECER_DOCENTE]

    print(f"Proveedor: {LLM_PROVIDER.upper()} | Modelo: {CHAT_MODEL}")
    print(f"Total noticias: {len(noticias)}")
    print(f"Pendientes de enriquecimiento docente: {len(pendientes)}\n")

    if not pendientes:
        print("Todas las noticias ya tienen enriquecimiento docente.")
        return

    pendientes_ids = {id(n) for n in pendientes}

    for i, noticia in enumerate(noticias, 1):
        if id(noticia) not in pendientes_ids:
            continue

        titulo_corto = noticia.get("titulo", "")[:70]
        print(f"[{i}/{len(noticias)}] {titulo_corto}...")

        capa = enriquecer(noticia)

        noticia["pregunta_aula"] = capa["pregunta_aula"]
        noticia["conceptos_clave"] = capa["conceptos_clave"]
        noticia["actividad_breve"] = capa["actividad_breve"]

        print(f"         -> Pregunta y actividad añadidas")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(noticias, f, ensure_ascii=False, indent=2)

    total_enriquecidas = sum(1 for n in noticias if tiene_enriquecimiento(n))
    print(f"\nListo. {total_enriquecidas}/{len(noticias)} noticias con capa docente")
    print(f"Guardado en: {OUTPUT_FILE}")


if __name__ == "__main__":
    enriquecer_noticias()
