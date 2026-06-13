# -*- coding: utf-8 -*-
"""
enriquecer_docente.py — versión 3

Objetivo:
- Convertir el enriquecimiento docente en una capa editorial útil.
- Evitar que casi todas las noticias sean "alto".
- Separar:
  - valor_docente: alto | medio | bajo
  - generar_ficha: solo noticias realmente útiles
  - seleccion_newsletter: selección limitada y ordenada

Uso recomendado:
    python enriquecer_docente.py --forzar --no-sobrescribir

Después:
    python generar_aula.py --entrada noticias_clasificadas_v3.json

Si el resultado gusta:
    python enriquecer_docente.py --forzar
    python generar_aula.py
"""

from __future__ import annotations

import argparse
import json
import shutil
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple
from urllib.parse import urlparse


PESOS_POSITIVOS = {
    # IA / automatización
    "inteligencia artificial": 3,
    "ia generativa": 3,
    "agente de ia": 3,
    "agentes de ia": 3,
    "chatgpt": 2,
    "openai": 2,
    "claude": 2,
    "gemini": 2,
    "automatización": 2,
    "automatizacion": 2,
    "robot": 2,
    "robots": 2,

    # Comercio electrónico y negocio digital
    "comercio electrónico": 3,
    "comercio electronico": 3,
    "ecommerce": 3,
    "e-commerce": 3,
    "tienda online": 3,
    "marketplace": 3,
    "marketplaces": 3,
    "tiktok shop": 3,
    "social commerce": 3,
    "retail media": 3,
    "commerce media": 3,

    # Logística / operaciones
    "logística": 2,
    "logistica": 2,
    "última milla": 3,
    "ultima milla": 3,
    "fulfillment": 3,
    "cadena de suministro": 2,
    "supply chain": 2,

    # Marketing
    "marketing digital": 3,
    "seo": 2,
    "sem": 2,
    "paid media": 2,
    "publicidad": 2,
    "campaña": 1,
    "campana": 1,
    "redes sociales": 2,
    "branding": 2,
    "conversiones": 2,
    "roi": 2,

    # Digitalización / ciberseguridad
    "digitalización": 2,
    "digitalizacion": 2,
    "transformación digital": 3,
    "transformacion digital": 3,
    "crm": 2,
    "erp": 2,
    "ciberseguridad": 3,
    "vulnerabilidad": 2,
    "vulnerabilidades": 2,
    "datos": 1,
    "backups": 2,
    "copias de seguridad": 2,

    # Internacional
    "aduanas": 3,
    "aranceles": 3,
    "comercio transfronterizo": 3,
    "exportación": 3,
    "exportacion": 3,
    "importación": 3,
    "importacion": 3,
}

PENALIZACIONES = {
    "demo day": 3,
    "webinar": 3,
    "evento": 2,
    "jornada": 2,
    "premios": 2,
    "ganadores": 2,
    "convocatoria": 2,
    "boletín": 2,
    "boletin": 2,
    "aviso de seguridad": 1,
    "avisos de seguridad": 1,
}

EMPRESAS_CASO = [
    "amazon", "google", "meta", "apple", "openai", "anthropic", "tiktok",
    "dhl", "makro", "shein", "temu", "aliexpress", "just eat", "mediaset",
    "shopify", "instagram", "whatsapp", "reddit"
]

PREGUNTAS_AULA = {
    "Comercio Electrónico": "¿Cómo puede afectar esta noticia a una pequeña tienda online?",
    "CDI": "¿Qué impacto podría tener esta noticia en una empresa que vende en mercados internacionales?",
    "Digitalización": "¿Qué proceso empresarial podría mejorar una pyme aplicando esta tecnología o tendencia?",
    "Marketing Digital": "¿Cómo podría aprovechar esta noticia una empresa para mejorar su comunicación o sus ventas?",
    "IA": "¿Qué ventajas, riesgos y límites plantea el uso de IA en este caso?",
    "General": "¿Qué relación tiene esta noticia con la evolución actual de las empresas?"
}


def normalizar_texto(valor: Any) -> str:
    if valor is None:
        return ""
    if isinstance(valor, list):
        return " ".join(normalizar_texto(v) for v in valor)
    return str(valor)


def texto_noticia(noticia: Dict[str, Any]) -> str:
    campos = [
        "titulo", "title", "resumen", "summary", "descripcion", "description",
        "categoria", "category", "modulo", "modulo_asignado",
        "ra_asignado", "ra_justificacion", "conceptos_clave", "actividad_breve",
    ]
    return " ".join(normalizar_texto(noticia.get(c)) for c in campos).lower()


def normalizar_modulo(valor: str) -> str | None:
    v = valor.lower()

    if "comercio digital internacional" in v or v.strip() == "cdi":
        return "CDI"
    if "ia para marketing" in v or "inteligencia artificial" in v:
        return "IA"
    if "digitalización" in v or "digitalizacion" in v:
        return "Digitalización"
    if "marketing digital" in v:
        return "Marketing Digital"
    if "comercio electrónico" in v or "comercio electronico" in v or "ecommerce" in v:
        return "Comercio Electrónico"

    return None


def detectar_modulo(noticia: Dict[str, Any]) -> str:
    # Primero respetamos lo que ya ha calculado Ollama.
    for campo in ["modulo_asignado", "modulo", "categoria"]:
        modulo = normalizar_modulo(normalizar_texto(noticia.get(campo)))
        if modulo:
            return modulo

    texto = texto_noticia(noticia)

    if any(p in texto for p in ["aduanas", "arancel", "exportación", "exportacion", "importación", "importacion", "transfronterizo"]):
        return "CDI"
    if any(p in texto for p in ["chatgpt", "openai", "claude", "gemini", "ia generativa", "agentes de ia", "inteligencia artificial"]):
        return "IA"
    if any(p in texto for p in ["ciberseguridad", "erp", "crm", "digitalización", "digitalizacion", "transformación digital", "transformacion digital"]):
        return "Digitalización"
    if any(p in texto for p in ["seo", "sem", "redes sociales", "retail media", "publicidad", "branding", "paid media"]):
        return "Marketing Digital"
    if any(p in texto for p in ["ecommerce", "e-commerce", "comercio electrónico", "comercio electronico", "tienda online", "marketplace", "logística", "logistica"]):
        return "Comercio Electrónico"

    return "General"


def calcular_score(noticia: Dict[str, Any], modulo: str) -> int:
    texto = texto_noticia(noticia)
    titulo = normalizar_texto(noticia.get("titulo") or noticia.get("title")).lower()

    score = 0

    for palabra, peso in PESOS_POSITIVOS.items():
        if palabra in texto:
            score += peso

    for palabra, peso in PENALIZACIONES.items():
        if palabra in titulo:
            score -= peso

    # Potencial didáctico real: tiene pregunta + actividad + conceptos.
    if noticia.get("pregunta_aula") and noticia.get("actividad_breve") and noticia.get("conceptos_clave"):
        score += 2

    # Relación curricular existente.
    if noticia.get("ra_asignado"):
        score += 1

    # Caso empresarial reconocible.
    if any(empresa in texto for empresa in EMPRESAS_CASO):
        score += 1

    # Si hay imagen es más útil para web/ficha, pero con poco peso.
    if noticia.get("imagen_url"):
        score += 1

    # Módulo general no suma.
    if modulo != "General":
        score += 1

    return score


def valor_desde_score(score: int) -> str:
    # Umbrales más estrictos que v2.
    if score >= 13:
        return "alto"
    if score >= 7:
        return "medio"
    return "bajo"


def detectar_tipo_uso(noticia: Dict[str, Any], valor: str) -> str:
    texto = texto_noticia(noticia)

    if any(p in texto for p in ["bruselas", "regulación", "regulacion", "competencia", "privacidad", "riesgo", "fraude", "ética", "etica"]):
        return "debate"

    if any(e in texto for e in EMPRESAS_CASO):
        return "caso_empresa"

    if valor == "alto":
        return "actividad"

    if valor == "medio":
        return "lectura"

    return "archivo"


def detectar_fuente(noticia: Dict[str, Any]) -> str:
    if noticia.get("fuente"):
        return str(noticia["fuente"])
    if noticia.get("source"):
        return str(noticia["source"])

    url = noticia.get("url") or noticia.get("link") or ""
    dominio = urlparse(url).netloc.replace("www.", "")
    return dominio or "Fuente no indicada"


def detectar_fecha(noticia: Dict[str, Any]) -> str:
    return str(
        noticia.get("fecha_publicacion")
        or noticia.get("fecha")
        or noticia.get("date")
        or ""
    )


def enriquecer_uso_docente(noticia: Dict[str, Any], forzar: bool = False) -> Dict[str, Any]:
    n = dict(noticia)

    modulo = detectar_modulo(n)
    score = calcular_score(n, modulo)
    valor = valor_desde_score(score)
    tipo = detectar_tipo_uso(n, valor)

    nuevos = {
        "score_docente": score,
        "valor_docente": valor,
        "modulo_relacionado": modulo,
        "tipo_uso": tipo,
        "pregunta_aula": n.get("pregunta_aula") or PREGUNTAS_AULA.get(modulo, PREGUNTAS_AULA["General"]),
        "generar_ficha": valor == "alto",
        # Se recalcula luego con límite.
        "seleccion_newsletter": False,
        "fuente_detectada": detectar_fuente(n),
        "fecha_detectada": detectar_fecha(n),
    }

    for campo, valor_campo in nuevos.items():
        if forzar or campo not in n or n.get(campo) in [None, ""]:
            n[campo] = valor_campo

    return n


def seleccionar_newsletter(noticias: List[Dict[str, Any]], limite: int = 10) -> List[Dict[str, Any]]:
    """
    Marca como newsletter solo las mejores noticias.
    Intenta evitar que todas sean del mismo módulo.
    """
    for n in noticias:
        n["seleccion_newsletter"] = False

    candidatas = [n for n in noticias if n.get("valor_docente") == "alto"]

    candidatas.sort(
        key=lambda n: (
            int(n.get("score_docente", 0)),
            1 if n.get("imagen_url") else 0,
            str(n.get("fecha_detectada", "")),
        ),
        reverse=True,
    )

    seleccionadas = []
    conteo_modulos = Counter()

    # Primera pasada: diversidad de módulos.
    for n in candidatas:
        modulo = n.get("modulo_relacionado", "General")
        if len(seleccionadas) >= limite:
            break
        if conteo_modulos[modulo] < 4:
            seleccionadas.append(n)
            conteo_modulos[modulo] += 1

    # Segunda pasada: rellenar si faltan.
    if len(seleccionadas) < limite:
        ya = {id(n) for n in seleccionadas}
        for n in candidatas:
            if len(seleccionadas) >= limite:
                break
            if id(n) not in ya:
                seleccionadas.append(n)

    for n in seleccionadas:
        n["seleccion_newsletter"] = True

    return noticias


def cargar_json(ruta: Path) -> Any:
    if not ruta.exists():
        raise FileNotFoundError(f"No se encuentra el archivo: {ruta}")
    with ruta.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def extraer_lista(datos: Any) -> Tuple[List[Dict[str, Any]], str]:
    if isinstance(datos, list):
        return datos, "lista"
    if isinstance(datos, dict) and isinstance(datos.get("noticias"), list):
        return datos["noticias"], "dict_noticias"
    raise ValueError("Estructura JSON no reconocida. Se esperaba lista o clave 'noticias'.")


def insertar_lista(datos: Any, noticias: List[Dict[str, Any]], estructura: str) -> Any:
    if estructura == "lista":
        return noticias
    nuevo = dict(datos)
    nuevo["noticias"] = noticias
    return nuevo


def crear_backup(ruta: Path) -> Path:
    marca = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = ruta.with_name(f"{ruta.stem}.backup_{marca}{ruta.suffix}")
    shutil.copy2(ruta, backup)
    return backup


def guardar_json(ruta: Path, datos: Any) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


def resolver_entrada(ruta: str | None) -> Path:
    if ruta:
        return Path(ruta)

    for candidato in [
        Path("noticias_clasificadas.json"),
        Path("data/noticias_clasificadas.json"),
        Path("datos/noticias_clasificadas.json"),
        Path("noticias_clasificadas_docente.json"),
    ]:
        if candidato.exists():
            return candidato

    return Path("noticias_clasificadas.json")


def imprimir_resumen(noticias: List[Dict[str, Any]]) -> None:
    print("\nResumen del enriquecimiento docente v3")
    print("=" * 44)

    for campo in ["valor_docente", "modulo_relacionado", "tipo_uso", "generar_ficha", "seleccion_newsletter"]:
        contador = Counter(str(n.get(campo)) for n in noticias)
        print(f"\n{campo}:")
        for valor, total in contador.most_common():
            print(f"  - {valor}: {total}")

    scores = sorted(int(n.get("score_docente", 0)) for n in noticias)
    if scores:
        print("\nscore_docente:")
        print(f"  - mínimo: {scores[0]}")
        print(f"  - máximo: {scores[-1]}")
        print(f"  - mediana aproximada: {scores[len(scores)//2]}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Añade o recalcula capa docente/editorial.")
    parser.add_argument("--entrada", help="Ruta del JSON de entrada.")
    parser.add_argument("--salida", help="Ruta del JSON de salida.")
    parser.add_argument("--no-sobrescribir", action="store_true", help="Crea un JSON nuevo sin tocar el original.")
    parser.add_argument("--forzar", action="store_true", help="Recalcula campos aunque ya existan.")
    parser.add_argument("--limite-newsletter", type=int, default=10, help="Número máximo de noticias para newsletter.")

    args = parser.parse_args()

    entrada = resolver_entrada(args.entrada)
    datos = cargar_json(entrada)
    noticias, estructura = extraer_lista(datos)

    enriquecidas = [enriquecer_uso_docente(n, forzar=args.forzar) for n in noticias]
    enriquecidas = seleccionar_newsletter(enriquecidas, limite=args.limite_newsletter)

    datos_salida = insertar_lista(datos, enriquecidas, estructura)

    if args.salida:
        salida = Path(args.salida)
    elif args.no_sobrescribir:
        salida = entrada.with_name(f"{entrada.stem}_v3{entrada.suffix}")
    else:
        salida = entrada

    if salida == entrada:
        backup = crear_backup(entrada)
        print(f"Copia de seguridad creada: {backup}")

    guardar_json(salida, datos_salida)
    print(f"Archivo guardado en: {salida}")
    imprimir_resumen(enriquecidas)


if __name__ == "__main__":
    main()
