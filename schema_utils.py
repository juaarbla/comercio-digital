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


if __name__ == "__main__":
    print(jsonld_script(schema_portada_basico()))
