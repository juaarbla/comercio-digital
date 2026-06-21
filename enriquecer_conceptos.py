#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Enriquece noticias clasificadas con conceptos clave curriculares.

Lee:
    data/processed/noticias_clasificadas.json
    data/curriculo/*_contenidos_basicos.md

Añade a cada noticia:
    conceptos_clave: [...]
    conceptos_origen: "contenidos_basicos"
    conceptos_modulo: ...
    conceptos_ra: ...

Uso:
    python enriquecer_conceptos.py
    python enriquecer_conceptos.py --sobrescribir
    python enriquecer_conceptos.py --max-conceptos 12
"""

import argparse
import json
import re
import unicodedata
from pathlib import Path

try:
    from paths import BASE_DIR, DATA_DIR, NOTICIAS_CLASIFICADAS
    try:
        from paths import CURRICULO_DIR
    except ImportError:
        CURRICULO_DIR = DATA_DIR / "curriculo"
except Exception:
    BASE_DIR = Path(__file__).resolve().parent
    DATA_DIR = BASE_DIR / "data"
    CURRICULO_DIR = DATA_DIR / "curriculo"
    NOTICIAS_CLASIFICADAS = DATA_DIR / "processed" / "noticias_clasificadas.json"


# ─────────────────────────────────────────────────────────────────────────────
# Utilidades
# ─────────────────────────────────────────────────────────────────────────────

def normalizar(texto: str) -> str:
    """Normaliza texto para comparar claves de módulo."""
    texto = str(texto or "").strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"[^a-z0-9]+", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def cargar_json(ruta: Path):
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_json(ruta: Path, data) -> None:
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def limpiar_bullet(linea: str) -> str:
    linea = linea.strip()
    linea = re.sub(r"^[-–—*•]\s+", "", linea)
    linea = linea.strip()
    return linea.rstrip(".").strip()


def deduplicar(lista):
    vistos = set()
    salida = []
    for item in lista:
        clave = normalizar(item)
        if not clave or clave in vistos:
            continue
        vistos.add(clave)
        salida.append(item)
    return salida


# ─────────────────────────────────────────────────────────────────────────────
# Detección de módulo a partir del nombre de archivo
# ─────────────────────────────────────────────────────────────────────────────

def modulo_desde_nombre_archivo(nombre: str) -> str | None:
    n = normalizar(nombre)

    if "cdi" in n or "comercio digital internacional" in n:
        return "Comercio Digital Internacional"

    # Importante: CE antes que genéricos.
    if re.search(r"\bce\b", n) or "comercio electronico" in n:
        return "Comercio Electrónico"

    if "digitalizacion gs" in n or "digitalizacion superior" in n:
        return "Digitalización GS"

    if "digitalizacion gm" in n or "digitalizacion medio" in n:
        return "Digitalización GM"

    if "iamc" in n or "ia marketing comercio" in n or "ia para el marketing" in n:
        return "IA para Marketing y Comercio"

    return None


# ─────────────────────────────────────────────────────────────────────────────
# Parser de conceptos mínimos por RA
# ─────────────────────────────────────────────────────────────────────────────

def extraer_conceptos_por_ra(texto: str) -> dict:
    """
    Extrae bloques tipo:

    ### RA1. ...
    Conceptos mínimos asociados:
    - Concepto A
    - Concepto B

    Devuelve:
    {
      "RA1": ["Concepto A", "Concepto B"],
      ...
    }
    """
    lineas = texto.splitlines()
    resultado = {}

    ra_actual = None
    recogiendo = False

    for linea in lineas:
        stripped = linea.strip()

        m_ra = re.match(r"^#{2,4}\s+(RA\d+)\b", stripped, flags=re.IGNORECASE)
        if m_ra:
            ra_actual = m_ra.group(1).upper()
            resultado.setdefault(ra_actual, [])
            recogiendo = False
            continue

        if ra_actual and normalizar(stripped).startswith("conceptos minimos asociados"):
            recogiendo = True
            continue

        if recogiendo:
            # Si empieza otro encabezado, paramos hasta el siguiente RA.
            if stripped.startswith("#"):
                recogiendo = False
                continue

            if re.match(r"^[-–—*•]\s+", stripped):
                concepto = limpiar_bullet(stripped)
                if concepto:
                    resultado.setdefault(ra_actual, []).append(concepto)

    return {ra: deduplicar(conceptos) for ra, conceptos in resultado.items()}


def cargar_curriculo_conceptos(curriculo_dir: Path) -> dict:
    """
    Devuelve:
    {
      "Comercio Electrónico": {"RA1": [...], ...},
      "Digitalización GS": {"RA1": [...], ...},
      ...
    }
    """
    conceptos = {}

    if not curriculo_dir.exists():
        print(f"ERROR: no existe la carpeta de currículo: {curriculo_dir}")
        return conceptos

    archivos = sorted(curriculo_dir.glob("*_contenidos_basicos*.md"))

    for archivo in archivos:
        modulo = modulo_desde_nombre_archivo(archivo.name)
        if not modulo:
            print(f"Aviso: no se reconoce el módulo del archivo {archivo.name}. Se omite.")
            continue

        texto = archivo.read_text(encoding="utf-8")
        por_ra = extraer_conceptos_por_ra(texto)

        if not por_ra:
            print(f"Aviso: no se han encontrado conceptos por RA en {archivo.name}.")
            continue

        conceptos[modulo] = por_ra

    return conceptos


# ─────────────────────────────────────────────────────────────────────────────
# Inferencia de módulo
# ─────────────────────────────────────────────────────────────────────────────

def inferir_modulo_digitalizacion(noticia: dict) -> str:
    """
    Si una noticia viene como 'Digitalización' sin GM/GS, intenta decidir.
    Se apoya en el texto del RA y en el propio RA.
    """
    ra = str(noticia.get("ra_asignado") or "").upper().strip()
    ra_texto = normalizar(noticia.get("ra_texto") or "")
    just = normalizar(noticia.get("ra_justificacion") or "")
    texto = f"{ra_texto} {just}"

    # Pistas claras de GS
    pistas_gs = [
        "it ot",
        "entornos it",
        "entornos ot",
        "tecnologias habilitadoras digitales necesarias",
        "aplicaciones de la ia",
        "importancia de los datos",
        "proteccion en una economia digital",
        "proyecto de transformacion digital",
        "objetivos estrategicos",
        "brechas de seguridad",
    ]

    # Pistas claras de GM
    pistas_gm = [
        "economia lineal",
        "economia circular",
        "cuarta revolucion industrial",
        "sistemas ciber fisicos",
        "sistemas de produccion digitalizados",
        "sistemas clasicos",
        "empresa clasica",
        "concepto 4 0",
    ]

    if any(p in texto for p in pistas_gs):
        return "Digitalización GS"

    if any(p in texto for p in pistas_gm):
        return "Digitalización GM"

    # Reglas por RA cuando el RA ayuda.
    if ra == "RA6":
        return "Digitalización GS"

    # RA5 es ambiguo: en GS es datos/ciberseguridad; en GM es plan de transformación.
    if ra == "RA5":
        if any(p in texto for p in ["datos", "ciberseguridad", "big data", "cloud", "seguridad"]):
            return "Digitalización GS"
        return "Digitalización GM"

    # RA4 también puede ser ambiguo; si habla de IA sectorial, suele ser GS.
    if ra == "RA4":
        if any(p in texto for p in ["inteligencia artificial", "big data", "lenguajes de programacion"]):
            return "Digitalización GS"
        return "Digitalización GM"

    # Por defecto, si no hay pista, usamos GS porque suele ser el más frecuente
    # en noticias de datos, IA, cloud y ciberseguridad.
    return "Digitalización GS"


def modulo_canonico(noticia: dict, conceptos_disponibles: dict) -> str:
    raw = (
        noticia.get("modulo_asignado")
        or noticia.get("modulo_relacionado")
        or noticia.get("modulo")
        or ""
    )

    n = normalizar(raw)

    if "comercio digital internacional" in n or n == "cdi":
        return "Comercio Digital Internacional"

    if "comercio electronico" in n or n in {"e commerce", "ecommerce", "ce"}:
        return "Comercio Electrónico"

    if "ia para marketing" in n or "ia para el marketing" in n or "marketing y comercio" in n:
        return "IA para Marketing y Comercio"

    # En algunas fichas aparece simplemente "IA".
    if n == "ia":
        return "IA para Marketing y Comercio"

    if "digitalizacion gs" in n:
        return "Digitalización GS"

    if "digitalizacion gm" in n:
        return "Digitalización GM"

    if n == "digitalizacion" or "digitalizacion" in n:
        return inferir_modulo_digitalizacion(noticia)

    # Si no se reconoce, intentamos una coincidencia aproximada.
    for modulo in conceptos_disponibles:
        if normalizar(modulo) in n or n in normalizar(modulo):
            return modulo

    return raw


def seleccionar_conceptos(conceptos: list[str], max_conceptos: int) -> list[str]:
    """
    Por ahora no usa IA: recorta conceptos para que la ficha no sea demasiado larga.
    Mantiene el orden del documento curricular.
    """
    conceptos = deduplicar(conceptos)
    if max_conceptos and max_conceptos > 0:
        return conceptos[:max_conceptos]
    return conceptos


# ─────────────────────────────────────────────────────────────────────────────
# Principal
# ─────────────────────────────────────────────────────────────────────────────

def enriquecer_conceptos(max_conceptos: int = 10, sobrescribir: bool = False, salida: Path | None = None) -> None:
    conceptos_curriculo = cargar_curriculo_conceptos(CURRICULO_DIR)

    print(f"Currículos de contenidos cargados desde: {CURRICULO_DIR}")
    for modulo, ras in conceptos_curriculo.items():
        total = sum(len(v) for v in ras.values())
        print(f"- {modulo}: {len(ras)} RA · {total} conceptos")

    if not conceptos_curriculo:
        print("No se han cargado conceptos. Revisa los archivos *_contenidos_basicos.md.")
        return

    if not NOTICIAS_CLASIFICADAS.exists():
        print(f"No se encontró {NOTICIAS_CLASIFICADAS}.")
        return

    noticias = cargar_json(NOTICIAS_CLASIFICADAS)
    if not isinstance(noticias, list):
        print("El JSON de noticias clasificadas no contiene una lista.")
        return

    enriquecidas = 0
    ya_tenian = 0
    sin_ra = 0
    sin_match = 0

    ejemplos_sin_match = []

    for noticia in noticias:
        if noticia.get("conceptos_clave") and not sobrescribir:
            ya_tenian += 1
            continue

        ra = str(noticia.get("ra_asignado") or "").upper().strip()
        if not ra:
            sin_ra += 1
            continue

        modulo = modulo_canonico(noticia, conceptos_curriculo)

        conceptos_ra = conceptos_curriculo.get(modulo, {}).get(ra, [])

        if not conceptos_ra:
            sin_match += 1
            if len(ejemplos_sin_match) < 8:
                ejemplos_sin_match.append({
                    "titulo": noticia.get("titulo", "")[:80],
                    "modulo": modulo,
                    "ra": ra,
                })
            continue

        noticia["conceptos_clave"] = seleccionar_conceptos(conceptos_ra, max_conceptos)
        noticia["conceptos_origen"] = "contenidos_basicos"
        noticia["conceptos_modulo"] = modulo
        noticia["conceptos_ra"] = ra

        enriquecidas += 1

    destino = salida or NOTICIAS_CLASIFICADAS
    guardar_json(destino, noticias)

    print("\nResultado")
    print(f"- Noticias totales: {len(noticias)}")
    print(f"- Enriquecidas con conceptos: {enriquecidas}")
    print(f"- Ya tenían conceptos y no se tocaron: {ya_tenian}")
    print(f"- Sin RA: {sin_ra}")
    print(f"- Sin coincidencia módulo/RA: {sin_match}")
    print(f"- Guardado en: {destino}")

    if ejemplos_sin_match:
        print("\nEjemplos sin coincidencia:")
        for e in ejemplos_sin_match:
            print(f"  · {e['modulo']} | {e['ra']} | {e['titulo']}...")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--max-conceptos",
        type=int,
        default=10,
        help="Número máximo de conceptos por noticia. Usa 0 para no limitar."
    )
    parser.add_argument(
        "--sobrescribir",
        action="store_true",
        help="Recalcula conceptos aunque la noticia ya tenga conceptos_clave."
    )
    parser.add_argument(
        "--salida",
        default="",
        help="Ruta alternativa de salida. Si se omite, sobrescribe NOTICIAS_CLASIFICADAS."
    )
    args = parser.parse_args()

    salida = Path(args.salida) if args.salida else None
    enriquecer_conceptos(
        max_conceptos=args.max_conceptos,
        sobrescribir=args.sobrescribir,
        salida=salida,
    )


if __name__ == "__main__":
    main()
