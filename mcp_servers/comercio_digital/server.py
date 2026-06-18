from pathlib import Path
import json
from typing import Any

from mcp.server.fastmcp import FastMCP

import re
from datetime import datetime


mcp = FastMCP("comercio-digital")


BASE_DIR = Path(__file__).resolve().parents[2]
JSON_PATH = BASE_DIR / "data" / "processed" / "noticias_clasificadas.json"
AULA_OUTPUTS_DIR = BASE_DIR / "outputs" / "aula"

def cargar_noticias() -> list[dict[str, Any]]:
    if not JSON_PATH.exists():
        raise FileNotFoundError(f"No se encuentra el archivo: {JSON_PATH}")

    with JSON_PATH.open("r", encoding="utf-8") as f:
        datos = json.load(f)

    if isinstance(datos, list):
        return datos

    if isinstance(datos, dict):
        for clave in ["noticias", "items", "data"]:
            if clave in datos and isinstance(datos[clave], list):
                return datos[clave]

    raise ValueError("El JSON no tiene una estructura de lista de noticias reconocible.")


def simplificar_noticia(noticia: dict[str, Any]) -> dict[str, Any]:
    return {
        "titulo": noticia.get("titulo") or noticia.get("title"),
        "url": noticia.get("url") or noticia.get("link"),
        "fuente": noticia.get("fuente") or noticia.get("source"),
        "fecha": noticia.get("fecha") or noticia.get("date"),
        "resumen": noticia.get("resumen") or noticia.get("summary"),
        "modulo_relacionado": noticia.get("modulo_relacionado"),
        "ra_relacionado": noticia.get("ra_relacionado") or noticia.get("ra"),
        "ce_relacionado": noticia.get("ce_relacionado") or noticia.get("ce"),
        "valor_docente": noticia.get("valor_docente"),
        "tipo_uso": noticia.get("tipo_uso"),
        "seleccion_newsletter": noticia.get("seleccion_newsletter"),
        "generar_ficha": noticia.get("generar_ficha"),
        "score_docente": noticia.get("score_docente"),
    }


@mcp.tool()
def estado_agregador() -> dict[str, Any]:
    """Devuelve un resumen del estado del agregador de noticias."""
    noticias = cargar_noticias()

    por_modulo: dict[str, int] = {}
    por_valor: dict[str, int] = {}
    newsletter = 0
    fichas = 0

    for noticia in noticias:
        modulo = noticia.get("modulo_relacionado") or "Sin módulo"
        valor = noticia.get("valor_docente") or "Sin valor"

        por_modulo[modulo] = por_modulo.get(modulo, 0) + 1
        por_valor[valor] = por_valor.get(valor, 0) + 1

        if noticia.get("seleccion_newsletter"):
            newsletter += 1

        if noticia.get("generar_ficha"):
            fichas += 1

    return {
        "archivo": str(JSON_PATH),
        "total_noticias": len(noticias),
        "por_modulo": por_modulo,
        "por_valor_docente": por_valor,
        "seleccion_newsletter": newsletter,
        "generar_ficha": fichas,
    }


@mcp.tool()
def buscar_noticias(texto: str, limite: int = 5) -> list[dict[str, Any]]:
    """Busca noticias por texto en título, resumen, fuente, módulo, RA o CE."""
    noticias = cargar_noticias()
    texto_normalizado = texto.lower().strip()
    resultados = []

    for noticia in noticias:
        campos = [
            noticia.get("titulo"),
            noticia.get("title"),
            noticia.get("resumen"),
            noticia.get("summary"),
            noticia.get("fuente"),
            noticia.get("source"),
            noticia.get("modulo_relacionado"),
            noticia.get("ra_relacionado"),
            noticia.get("ra"),
            noticia.get("ce_relacionado"),
            noticia.get("ce"),
        ]

        contenido = " ".join(str(c or "") for c in campos).lower()

        if texto_normalizado in contenido:
            resultados.append(simplificar_noticia(noticia))

    return resultados[:limite]


@mcp.tool()
def noticias_por_modulo(modulo: str, limite: int = 10) -> list[dict[str, Any]]:
    """Devuelve noticias filtradas por módulo relacionado."""
    noticias = cargar_noticias()
    modulo_normalizado = modulo.lower().strip()

    resultados = [
        simplificar_noticia(n)
        for n in noticias
        if modulo_normalizado in str(n.get("modulo_relacionado", "")).lower()
    ]

    return resultados[:limite]


@mcp.tool()
def noticias_por_valor_docente(valor: str = "alto", limite: int = 10) -> list[dict[str, Any]]:
    """Devuelve noticias filtradas por valor docente: alto, medio o bajo."""
    noticias = cargar_noticias()
    valor_normalizado = valor.lower().strip()

    resultados = [
        simplificar_noticia(n)
        for n in noticias
        if valor_normalizado == str(n.get("valor_docente", "")).lower()
    ]

    return resultados[:limite]


@mcp.tool()
def noticias_newsletter(limite: int = 10) -> list[dict[str, Any]]:
    """Devuelve noticias marcadas para selección de newsletter."""
    noticias = cargar_noticias()

    resultados = [
        simplificar_noticia(n)
        for n in noticias
        if n.get("seleccion_newsletter") is True
    ]

    return resultados[:limite]


@mcp.tool()
def ficha_aula_basica(url_o_titulo: str) -> dict[str, Any]:
    """Genera una ficha básica de aula a partir de una noticia localizada por URL o título."""
    noticias = cargar_noticias()
    q = url_o_titulo.lower().strip()

    encontrada = None

    for noticia in noticias:
        titulo = str(noticia.get("titulo") or noticia.get("title") or "").lower()
        url = str(noticia.get("url") or noticia.get("link") or "").lower()

        if q in titulo or q in url:
            encontrada = noticia
            break

    if not encontrada:
        return {
            "encontrada": False,
            "mensaje": "No se ha encontrado ninguna noticia con ese título o URL.",
        }

    n = simplificar_noticia(encontrada)

    return {
        "encontrada": True,
        "titulo": n["titulo"],
        "url": n["url"],
        "modulo_relacionado": n["modulo_relacionado"],
        "ra_relacionado": n["ra_relacionado"],
        "ce_relacionado": n["ce_relacionado"],
        "valor_docente": n["valor_docente"],
        "tipo_uso": n["tipo_uso"],
        "actividad_aula": {
            "titulo": f"Análisis aplicado: {n['titulo']}",
            "duracion": "30-45 minutos",
            "objetivo": "Relacionar una noticia actual con los contenidos del módulo y extraer aprendizajes aplicables.",
            "tarea_alumnado": [
                "Leer la noticia.",
                "Identificar el problema, tendencia o caso empresarial que plantea.",
                "Relacionarlo con el RA o contenido trabajado en clase.",
                "Proponer una aplicación práctica para una empresa real o simulada.",
            ],
            "producto_final": "Breve informe, debate guiado o entrega en Aules.",
        },
    }

def slugify(texto: str, max_length: int = 80) -> str:
    texto = texto.lower()
    texto = re.sub(r"[áàäâ]", "a", texto)
    texto = re.sub(r"[éèëê]", "e", texto)
    texto = re.sub(r"[íìïî]", "i", texto)
    texto = re.sub(r"[óòöô]", "o", texto)
    texto = re.sub(r"[úùüû]", "u", texto)
    texto = re.sub(r"ñ", "n", texto)
    texto = re.sub(r"[^a-z0-9]+", "-", texto)
    texto = texto.strip("-")
    return texto[:max_length].strip("-") or "ficha-aula"


def crear_markdown_ficha(n: dict[str, Any]) -> str:
    fecha_generacion = datetime.now().strftime("%Y-%m-%d %H:%M")

    return f"""# Ficha de aula: {n.get("titulo")}

## Datos de la noticia

- **Fuente:** {n.get("fuente") or "No indicada"}
- **Fecha:** {n.get("fecha") or "No indicada"}
- **URL:** {n.get("url") or "No indicada"}
- **Módulo relacionado:** {n.get("modulo_relacionado") or "Pendiente de revisar"}
- **RA relacionado:** {n.get("ra_relacionado") or "Pendiente de revisar"}
- **CE relacionado:** {n.get("ce_relacionado") or "Pendiente de revisar"}
- **Valor docente:** {n.get("valor_docente") or "Pendiente"}
- **Tipo de uso:** {n.get("tipo_uso") or "Pendiente"}

## Resumen

{n.get("resumen") or "Resumen no disponible."}

## Propuesta de actividad

**Duración estimada:** 30-45 minutos.

**Objetivo:**  
Relacionar una noticia actual con los contenidos del módulo y extraer aprendizajes aplicables al comercio, el marketing digital o la transformación digital.

## Tarea para el alumnado

1. Lee la noticia.
2. Identifica el problema, tendencia o caso empresarial que plantea.
3. Relaciona la noticia con los contenidos trabajados en clase.
4. Propón una aplicación práctica para una empresa real o simulada.
5. Redacta una conclusión breve.

## Preguntas guía

- ¿Qué hecho o tendencia destaca la noticia?
- ¿Qué relación tiene con el módulo?
- ¿Qué impacto puede tener en una empresa?
- ¿Qué decisiones debería tomar una empresa ante esta situación?
- ¿Qué aprendizaje práctico podemos extraer?

## Producto final

Entrega breve en Aules, debate guiado o comentario individual.

## Criterios de valoración

- Comprende la noticia y resume sus ideas principales.
- Relaciona la noticia con contenidos del módulo.
- Propone una aplicación práctica.
- Argumenta con claridad.
- Presenta una conclusión razonada.

---

Ficha generada automáticamente por MCP Comercio Digital.  
Fecha de generación: {fecha_generacion}
"""
@mcp.tool()
def generar_ficha_md(url_o_titulo: str) -> dict[str, Any]:
    """Genera una ficha de aula en Markdown y la guarda en outputs/aula/."""
    noticias = cargar_noticias()
    q = url_o_titulo.lower().strip()

    encontrada = None

    for noticia in noticias:
        titulo = str(noticia.get("titulo") or noticia.get("title") or "").lower()
        url = str(noticia.get("url") or noticia.get("link") or "").lower()

        if q in titulo or q in url:
            encontrada = noticia
            break

    if not encontrada:
        return {
            "creada": False,
            "mensaje": "No se ha encontrado ninguna noticia con ese título o URL.",
        }

    n = simplificar_noticia(encontrada)

    AULA_OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    titulo = n.get("titulo") or "ficha aula"
    slug = slugify(titulo)
    ruta = AULA_OUTPUTS_DIR / f"{slug}.md"

    contenido = crear_markdown_ficha(n)

    ruta.write_text(contenido, encoding="utf-8")

    return {
        "creada": True,
        "archivo": str(ruta),
        "titulo": titulo,
        "url": n.get("url"),
        "modulo_relacionado": n.get("modulo_relacionado"),
        "valor_docente": n.get("valor_docente"),
    }

if __name__ == "__main__":
    mcp.run()