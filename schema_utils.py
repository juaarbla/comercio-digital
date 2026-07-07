# -*- coding: utf-8 -*-
"""
Utilidades Schema.org para Comercio Digital.

v0.7 · SEO semántico y datos estructurados

Este módulo centraliza la generación de JSON-LD para evitar duplicar
schemas en los distintos generadores HTML del proyecto.

Incluye:
- limpieza de schemas
- generación de script JSON-LD
- inserción segura antes de </head>
- WebSite
- Organization
- Person
- WebPage
- CollectionPage
- ItemList
- conjuntos básicos para portada y páginas principales
- LearningResource para fichas de aula
- CollectionPage e ItemList para newsletter
"""

from __future__ import annotations

import json
import re
from typing import Any

SITE_URL = "https://comerciodigital.net"
SITE_NAME = "Comercio Digital"
SITE_DESCRIPTION = (
    "Actualidad de comercio, marketing, digitalización e inteligencia artificial "
    "seleccionada y preparada para trabajar en el aula de Formación Profesional."
)
AUTHOR_NAME = "Juan Armada"


def limpiar_schema(data: Any) -> Any:
    """Elimina valores vacíos de un schema antes de serializarlo.

    Elimina:
    - None
    - cadenas vacías
    - listas vacías
    - diccionarios vacíos

    Mantiene valores numéricos y booleanos válidos.
    """
    if isinstance(data, dict):
        limpio: dict[str, Any] = {}
        for key, value in data.items():
            value_limpio = limpiar_schema(value)
            if value_limpio in (None, ""):
                continue
            if isinstance(value_limpio, (list, dict)) and not value_limpio:
                continue
            limpio[key] = value_limpio
        return limpio

    if isinstance(data, list):
        limpio_lista = []
        for item in data:
            item_limpio = limpiar_schema(item)
            if item_limpio in (None, ""):
                continue
            if isinstance(item_limpio, (list, dict)) and not item_limpio:
                continue
            limpio_lista.append(item_limpio)
        return limpio_lista

    return data


def jsonld_script(data: dict[str, Any] | list[dict[str, Any]]) -> str:
    """Devuelve un bloque <script type="application/ld+json">."""
    limpio = limpiar_schema(data)
    contenido = json.dumps(limpio, ensure_ascii=False, indent=2)
    return (
        '<script type="application/ld+json">\n'
        f'{contenido}\n'
        '</script>'
    )


def contiene_jsonld(html: str) -> bool:
    """Indica si el HTML ya contiene algún bloque JSON-LD."""
    return bool(
        re.search(
            r'<script\s+type=["\']application/ld\+json["\']',
            html,
            flags=re.IGNORECASE,
        )
    )


def insertar_jsonld(
    html: str,
    schema: dict[str, Any] | list[dict[str, Any]],
    *,
    reemplazar_existente: bool = False,
) -> str:
    """Inserta JSON-LD antes de </head>.

    Por defecto no duplica si ya existe un bloque JSON-LD.
    Si reemplazar_existente=True, elimina los bloques JSON-LD existentes
    antes de insertar el nuevo bloque.
    """
    if not html:
        return html

    if contiene_jsonld(html):
        if not reemplazar_existente:
            return html
        html = re.sub(
            r'\s*<script\s+type=["\']application/ld\+json["\']>.*?</script>',
            "",
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )

    bloque = jsonld_script(schema)

    if re.search(r"</head>", html, flags=re.IGNORECASE):
        return re.sub(
            r"</head>",
            f"  {bloque}\n</head>",
            html,
            count=1,
            flags=re.IGNORECASE,
        )

    return html


def absolute_url(path: str = "/") -> str:
    """Construye una URL absoluta del sitio."""
    path = str(path or "/").strip()
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if path == "/":
        return f"{SITE_URL.rstrip('/')}/"
    return f"{SITE_URL.rstrip('/')}/{path.lstrip('/')}"


def schema_organization() -> dict[str, Any]:
    """Schema Organization para el proyecto Comercio Digital."""
    return limpiar_schema(
        {
            "@context": "https://schema.org",
            "@type": "Organization",
            "@id": absolute_url("/#organization"),
            "name": SITE_NAME,
            "url": absolute_url("/"),
            "description": SITE_DESCRIPTION,
        }
    )


def schema_person() -> dict[str, Any]:
    """Schema Person para la autoría/editor responsable."""
    return limpiar_schema(
        {
            "@context": "https://schema.org",
            "@type": "Person",
            "@id": absolute_url("/#juan-armada"),
            "name": AUTHOR_NAME,
            "url": "https://juanarmada.com",
            "affiliation": {
                "@type": "Organization",
                "name": SITE_NAME,
                "url": absolute_url("/"),
            },
        }
    )


def schema_website() -> dict[str, Any]:
    """Schema WebSite para el agregador."""
    return limpiar_schema(
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "@id": absolute_url("/#website"),
            "name": SITE_NAME,
            "url": absolute_url("/"),
            "description": SITE_DESCRIPTION,
            "publisher": {
                "@id": absolute_url("/#organization"),
            },
            "inLanguage": "es",
        }
    )


def schema_webpage(
    title: str,
    description: str,
    url: str,
    *,
    page_type: str = "WebPage",
) -> dict[str, Any]:
    """Schema WebPage genérico para una página concreta."""
    url_abs = absolute_url(url)
    return limpiar_schema(
        {
            "@context": "https://schema.org",
            "@type": page_type,
            "@id": f"{url_abs}#webpage",
            "name": title,
            "description": description,
            "url": url_abs,
            "isPartOf": {
                "@id": absolute_url("/#website"),
            },
            "publisher": {
                "@id": absolute_url("/#organization"),
            },
            "inLanguage": "es",
        }
    )


def schema_collection_page(
    title: str,
    description: str,
    url: str,
    items: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Schema CollectionPage para portada, secciones, Aula o newsletter."""
    schema = schema_webpage(
        title,
        description,
        url,
        page_type="CollectionPage",
    )

    if items:
        schema["mainEntity"] = schema_item_list(items)

    return limpiar_schema(schema)


def schema_item_list(items: list[dict[str, Any]]) -> dict[str, Any]:
    """Schema ItemList desde elementos con name, url y opcionalmente description."""
    elementos = []
    for pos, item in enumerate(items or [], start=1):
        name = item.get("name") or item.get("title") or item.get("titulo")
        url = item.get("url") or item.get("href")
        description = item.get("description") or item.get("resumen")

        elementos.append(
            limpiar_schema(
                {
                    "@type": "ListItem",
                    "position": pos,
                    "name": name,
                    "url": absolute_url(url) if url else "",
                    "description": description,
                }
            )
        )

    return limpiar_schema(
        {
            "@type": "ItemList",
            "itemListElement": elementos,
        }
    )


def schema_portada_basico() -> list[dict[str, Any]]:
    """Conjunto Schema.org básico para docs/index.html."""
    return [
        schema_organization(),
        schema_website(),
        schema_collection_page(
            "Comercio Digital | Actualidad para el aula de FP",
            "Noticias de comercio electrónico, marketing, digitalización e inteligencia artificial clasificadas por resultados de aprendizaje y preparadas para FP.",
            "/",
        ),
    ]


def schema_pagina_principal_basico(
    title: str,
    description: str,
    url: str,
    *,
    page_type: str = "CollectionPage",
) -> list[dict[str, Any]]:
    """Conjunto Schema.org básico para páginas principales del agregador.

    Mantiene Organization y WebSite como entidades de referencia y añade
    la página concreta como WebPage o CollectionPage.
    """
    if page_type == "CollectionPage":
        pagina = schema_collection_page(title, description, url)
    else:
        pagina = schema_webpage(title, description, url, page_type=page_type)

    return [
        schema_organization(),
        schema_website(),
        pagina,
    ]


def _conceptos_desde_valor(value: Any) -> list[str]:
    """Normaliza conceptos/keywords desde lista o cadena."""
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if isinstance(value, str):
        return [v.strip() for v in value.split(",") if v.strip()]
    return []


def schema_learning_resource(
    ficha: dict[str, Any],
    url: str,
    *,
    html_file: str | None = None,
) -> dict[str, Any]:
    """Schema LearningResource para una ficha de aula.

    Describe contenido educativo propio generado por Comercio Digital.
    No marca la noticia original como NewsArticle.
    """
    titulo = ficha.get("titulo") or ficha.get("title") or "Ficha docente"
    resumen = ficha.get("resumen") or ficha.get("resumen_docente") or ""
    modulo = (
        ficha.get("modulo_relacionado")
        or ficha.get("modulo_asignado")
        or ficha.get("modulo")
        or "Formación Profesional"
    )
    ra = ficha.get("ra_asignado") or ""
    ra_texto = ficha.get("ra_texto") or ""
    tipo = ficha.get("tipo_uso") or "Ficha docente"
    actividad = ficha.get("actividad_breve") or ""
    pregunta = ficha.get("pregunta_aula") or ""
    conceptos = _conceptos_desde_valor(ficha.get("conceptos_clave"))
    keywords = [modulo, ra, tipo] + conceptos

    is_based_on = ficha.get("url") or ficha.get("link") or ficha.get("enlace") or ""

    schema = {
        "@context": "https://schema.org",
        "@type": "LearningResource",
        "@id": f"{absolute_url(url)}#learningresource",
        "name": titulo,
        "headline": titulo,
        "description": resumen,
        "url": absolute_url(url),
        "inLanguage": "es",
        "isAccessibleForFree": True,
        "learningResourceType": tipo,
        "educationalLevel": "Formación Profesional",
        "educationalUse": "Uso en el aula",
        "audience": {
            "@type": "EducationalAudience",
            "educationalRole": "student",
        },
        "creator": {
            "@id": absolute_url("/#organization"),
        },
        "publisher": {
            "@id": absolute_url("/#organization"),
        },
        "isPartOf": {
            "@id": absolute_url("/aula.html#webpage"),
        },
        "about": conceptos[:10],
        "keywords": ", ".join([k for k in keywords if k]),
        "teaches": [x for x in [modulo, ra, ra_texto] if x],
        "abstract": resumen,
        "text": actividad,
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": f"{absolute_url(url)}#webpage",
        },
        "isBasedOn": is_based_on,
    }

    if pregunta:
        schema["educationalAlignment"] = {
            "@type": "AlignmentObject",
            "alignmentType": "educationalSubject",
            "targetName": pregunta,
        }

    return limpiar_schema(schema)


def schema_ficha_aula_basico(
    ficha: dict[str, Any],
    url: str,
) -> list[dict[str, Any]]:
    """Conjunto básico para una ficha de aula."""
    titulo = ficha.get("titulo") or ficha.get("title") or "Ficha docente"
    resumen = ficha.get("resumen") or ficha.get("resumen_docente") or "Ficha docente para trabajar una noticia de comercio digital en clase."

    return [
        schema_organization(),
        schema_website(),
        schema_webpage(
            f"{titulo} · Ficha docente · Comercio Digital",
            resumen,
            url,
            page_type="WebPage",
        ),
        schema_learning_resource(ficha, url),
    ]



def _newsletter_item(noticia: dict[str, Any], position: int) -> dict[str, Any]:
    """Elemento de listado para una noticia enlazada desde newsletter.

    No declara la noticia como Article/NewsArticle propio.
    """
    titulo = noticia.get("titulo") or noticia.get("title") or "Noticia seleccionada"
    url = noticia.get("url") or noticia.get("link") or noticia.get("enlace") or ""
    resumen = (
        noticia.get("resumen_docente")
        or noticia.get("resumen")
        or noticia.get("summary")
        or noticia.get("descripcion")
        or noticia.get("description")
        or ""
    )
    modulo = (
        noticia.get("modulo_relacionado")
        or noticia.get("módulo_relacionado")
        or noticia.get("modulo")
        or noticia.get("categoria")
        or ""
    )

    return limpiar_schema({
        "@type": "ListItem",
        "position": position,
        "name": titulo,
        "url": url,
        "description": resumen,
        "about": modulo,
    })


def schema_newsletter_index(ediciones: list[dict[str, Any]], url: str = "/newsletter/") -> list[dict[str, Any]]:
    """Schema básico para el índice de newsletters."""
    items = []
    for i, edicion in enumerate(ediciones, 1):
        name = edicion.get("name") or edicion.get("title") or "Newsletter"
        href = edicion.get("url") or edicion.get("href") or ""
        description = edicion.get("description") or "Edición de la newsletter docente de Comercio Digital."
        items.append(limpiar_schema({
            "@type": "ListItem",
            "position": i,
            "name": name,
            "url": absolute_url(href),
            "description": description,
        }))

    page_url = absolute_url(url)

    return [
        schema_organization(),
        schema_website(),
        schema_collection_page(
            "Newsletter · Comercio Digital",
            "Archivo de newsletters docentes de Comercio Digital.",
            page_url,
            items=items,
        ),
    ]


def schema_newsletter_issue(
    noticias: list[dict[str, Any]],
    periodo: dict[str, str],
    periodicidad: str,
    url: str,
) -> list[dict[str, Any]]:
    """Schema CollectionPage + ItemList para una edición de newsletter.

    La edición se describe como colección de enlaces seleccionados.
    Las noticias externas se describen como ListItem, no como NewsArticle propio.
    """
    label = periodo.get("label") or "Newsletter"
    title = f"Comercio Digital en el aula · {label}"
    description = (
        "Newsletter docente de Comercio Digital con noticias seleccionadas "
        "para trabajar comercio electrónico, digitalización, marketing e inteligencia artificial en FP."
    )
    page_url = absolute_url(url)

    items = [_newsletter_item(noticia, i) for i, noticia in enumerate(noticias, 1)]

    collection = schema_collection_page(title, description, page_url, items=items)
    collection["isPartOf"] = {"@id": absolute_url("/newsletter/#webpage")}
    collection["additionalProperty"] = [
        {"@type": "PropertyValue", "name": "Periodicidad", "value": periodicidad},
        {"@type": "PropertyValue", "name": "Periodo", "value": label},
    ]

    item_list = schema_item_list(items)
    item_list["@id"] = f"{page_url}#itemlist"
    item_list["name"] = f"Noticias seleccionadas · {label}"

    return [
        schema_organization(),
        schema_website(),
        limpiar_schema(collection),
        limpiar_schema(item_list),
    ]


if __name__ == "__main__":
    print(jsonld_script(schema_portada_basico()))
