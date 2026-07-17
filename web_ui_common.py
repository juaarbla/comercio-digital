# -*- coding: utf-8 -*-
"""
Funciones comunes de interfaz para Comercio Digital.

v0.5 — Consistencia visual

Centraliza cabecera, navegación, head, barra de subtítulo y pie para evitar
que portada, Aula y Newsletter evolucionen con estructuras distintas.
"""

from __future__ import annotations

from datetime import datetime
import html

SITE_TITLE = "Comercio Digital"
SITE_SUBTITLE = "La actualidad del sector para el aula de FP"
SITE_URL = "https://comerciodigital.net"

MATOMO_TRACKING_CODE = """
  <!-- Matomo -->
  <script>
    var _paq = window._paq = window._paq || [];
    /* tracker methods like "setCustomDimension" should be called before "trackPageView" */
    _paq.push(['trackPageView']);
    _paq.push(['enableLinkTracking']);
    (function() {
      var u="https://a.manitasdigital.com/";
      _paq.push(['setTrackerUrl', u+'matomo.php']);
      _paq.push(['setSiteId', '4']);
      var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
      g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
    })();
  </script>
  <noscript>
    <img referrerpolicy="no-referrer-when-downgrade"
         src="https://a.manitasdigital.com/matomo.php?idsite=4&amp;rec=1"
         style="border:0"
         alt="" />
  </noscript>
  <!-- End Matomo Code -->
"""

DEFAULT_SECTIONS = [
    {"id": "comercio-electronico", "label": "E-Commerce", "file": "comercio-electronico.html"},
    {"id": "internacional", "label": "Internacional", "file": "internacional.html"},
    {"id": "digitalizacion", "label": "Digitalización", "file": "digitalizacion.html"},
    {"id": "ia-marketing", "label": "IA & Marketing", "file": "ia-marketing.html"},
    {"id": "del-autor", "label": "Del Autor", "file": "del-autor.html"},
]


def esc_attr(value: str) -> str:
    return html.escape(str(value or ""), quote=True)


def fecha_hoy_larga() -> str:
    hoy = datetime.now()
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    meses = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
    ]
    return f"{dias[hoy.weekday()]}, {hoy.day} de {meses[hoy.month - 1]} de {hoy.year}"


def head_html(
    titulo: str,
    canonical_path: str = "/",
    *,
    descripcion: str = SITE_SUBTITLE,
    assets_prefix: str = "",
    body_class: str = "",
) -> str:
    canonical_url = (
        f"{SITE_URL.rstrip('/')}/{canonical_path.lstrip('/')}"
        if canonical_path != "/"
        else f"{SITE_URL.rstrip('/')}/"
    )
    body_attr = f' class="{esc_attr(body_class)}"' if body_class else ""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{titulo} &mdash; {SITE_TITLE}</title>
  <meta name="description" content="{esc_attr(descripcion)}">
  <link rel="canonical" href="{esc_attr(canonical_url)}">
  <link rel="icon" type="image/svg+xml" href="{assets_prefix}assets/favicon.svg">
  <link rel="stylesheet" href="{assets_prefix}assets/style.css">
{MATOMO_TRACKING_CODE}
</head>
<body{body_attr}>"""


def masthead_html(*, home_href: str = "index.html") -> str:
    return f"""
  <header>
    <div class="masthead">
      <div class="masthead-side">Formaci&oacute;n Profesional<br>Comercio y Marketing</div>
      <div class="site-title"><a href="{esc_attr(home_href)}">{SITE_TITLE}</a></div>
      <div class="masthead-side right">{fecha_hoy_larga()}<br>{SITE_URL.replace('https://', '')}</div>
    </div>
  </header>"""


def nav_html(
    active: str = "",
    *,
    base_prefix: str = "",
    secciones: list[dict] | None = None,
    secciones_con_noticias: set[str] | None = None,
) -> str:
    """Menú principal común con rutas adaptables.

    base_prefix="" para páginas en docs/.
    base_prefix="../" para páginas dentro de docs/newsletter/.
    """
    secciones = secciones or DEFAULT_SECTIONS
    salto = chr(10)

    def active_class(name: str) -> str:
        if name == "portada" and active in ("", "index", "portada"):
            return ' class="active"'
        return ' class="active"' if name == active else ""

    def href_for(file_name: str) -> str:
        return f"{base_prefix}{file_name}"

    items = f'<li><a href="{href_for("index.html")}"{active_class("portada")}>Portada</a></li>' + salto

    for seccion in secciones:
        sid = seccion.get("id", "")
        if sid in {"otros", "del-autor"}:
            continue
        if secciones_con_noticias is not None and sid not in secciones_con_noticias:
            continue
        href = href_for(seccion["file"])
        items += f'    <li><a href="{href}"{active_class(sid)}>{seccion["label"]}</a></li>' + salto

    items += f'    <li><a href="{href_for("aula.html")}"{active_class("aula")}>Aula</a></li>' + salto

    newsletter_href = "index.html" if base_prefix else "newsletter/index.html"
    items += f'    <li><a href="{newsletter_href}"{active_class("newsletter")}>Newsletter</a></li>' + salto

    del_autor = next((s for s in secciones if s.get("id") == "del-autor"), None)
    if del_autor:
        if secciones_con_noticias is None or "del-autor" in secciones_con_noticias:
            items += f'    <li><a href="{href_for(del_autor["file"])}"{active_class("del-autor")}>{del_autor["label"]}</a></li>' + salto

    return f"""
  <nav class="site-nav" aria-label="Menú principal">
    <input type="checkbox" id="nav-toggle" class="nav-toggle">
    <label for="nav-toggle" class="nav-toggle-label" aria-label="Abrir o cerrar menú">
      <span></span>
      <span></span>
      <span></span>
      <strong>Menú</strong>
    </label>
    <ul class="nav-menu">
      {items}    </ul>
  </nav>"""


def subtitle_bar_html(left: str, right: str) -> str:
    return f'<div class="subtitle-bar"><span>{left}</span><span>{right}</span></div>\n'


def footer_html() -> str:
    return f"""
  <footer>
    <strong>{SITE_TITLE}</strong> &middot; Generado el {fecha_hoy_larga()} &middot;
    Res&uacute;menes generados con IA a partir de fuentes p&uacute;blicas &middot;
    Uso educativo &mdash; FP Comercio y Marketing CV &middot;
    <a href="/privacidad.html">Privacidad</a>
  </footer>"""
