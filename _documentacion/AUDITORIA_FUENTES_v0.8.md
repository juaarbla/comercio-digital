# Auditoría inicial de fuentes v0.8

## Base de trabajo

Archivos revisados:

```text
informe_pipeline_2026-07-08.md
feeds.json
historial.json
```

## Resumen de feeds.json

```text
Fuentes configuradas: 19
Fuentes activas: 14
Fuentes inactivas: 5
Fuentes activas sin módulo declarado: 4
```

## Fuentes activas por módulo declarado

| Módulo | Fuentes activas |
|---|---:|
| Del Autor | 1 |
| (vacío) | 4 |
| Comercio Electrónico | 2 |
| Marketing Digital | 2 |
| Digitalización GS | 1 |
| WordPress | 1 |
| PrestaShop | 1 |
| IA para Marketing y Comercio | 2 |

## Fuentes activas por tipo

| Tipo | Fuentes activas |
|---|---:|
| podcast | 1 |
| articulo | 2 |
| noticia | 11 |

## Fuentes activas

| URL | Módulo | Tipo | Decisión inicial |
|---|---|---|---|
| https://juanarmada.com/podcast/feed/ | Del Autor | podcast | Pendiente de revisar |
| https://juanarmada.com/wp-json/wp/v2/posts?per_page=20&orderby=date&order=desc&_fields=id,link,date,date_gmt,title,excerpt,content,categories | (vacío) | articulo | Pendiente de revisar |
| https://ecommerce-news.es/feed/ | Comercio Electrónico | noticia | Pendiente de revisar |
| https://marketing4ecommerce.net/ecommerce/feed | Comercio Electrónico | noticia | Pendiente de revisar |
| https://www.marketingdirecto.com/feed | Marketing Digital | noticia | Pendiente de revisar |
| https://www.ontsi.es/es/rss.xml | Digitalización GS | noticia | Pendiente de revisar |
| https://www.taric.es/noticias/ | (vacío) | noticia | Pendiente de revisar |
| https://es.wordpress.org/news/ | WordPress | noticia | Pendiente de revisar |
| https://casares.blog/ | (vacío) | noticia | Pendiente de revisar |
| https://prestashop.es/blog | PrestaShop | noticia | Pendiente de revisar |
| https://prestotimes.com | IA para Marketing y Comercio | noticia | Pendiente de revisar |
| https://consultoresia.com/inteligencia-artificial/ | IA para Marketing y Comercio | noticia | Pendiente de revisar |
| https://blog.hubspot.es/marketing/rss.xml | Marketing Digital | articulo | Pendiente de revisar |
| https://www.cyberclick.es/numerical-blog | (vacío) | noticia | Pendiente de revisar |

## Fuentes inactivas

| URL | Módulo | Tipo | Nota |
|---|---|---|---|
| https://juanarmada.com/inteligencia-artificial/feed/ | Del Autor | articulo | Desactivado para evitar duplicados con WordPress API. |
| https://juanarmada.com/marketing-digital/feed/ | Del Autor | articulo | Desactivado para evitar duplicados con WordPress API. |
| https://www.incibe.es/rss.xml | Digitalización GS | noticia |  |
| https://blog.hubspot.es/sales/rss.xml | Comercio Electrónico | articulo | Ventas, CRM, social selling y procesos comerciales. Activar si aporta noticias útiles para CE/CDI. |
| https://blog.hubspot.es/service/rss.xml | Marketing Digital | articulo | Atención al cliente, fidelización y experiencia de cliente. Útil pero menos prioritaria. |

## Fuentes activas sin módulo declarado

| URL | Tipo | Propuesta inicial |
|---|---|---|
| https://juanarmada.com/wp-json/wp/v2/posts?per_page=20&orderby=date&order=desc&_fields=id,link,date,date_gmt,title,excerpt,content,categories | articulo | Revisar si debe seguir como transversal o asignar módulo |
| https://www.taric.es/noticias/ | noticia | Revisar si debe seguir como transversal o asignar módulo |
| https://casares.blog/ | noticia | Revisar si debe seguir como transversal o asignar módulo |
| https://www.cyberclick.es/numerical-blog | noticia | Revisar si debe seguir como transversal o asignar módulo |

## Fuentes activas sin aportación histórica

| Fuente | Clave | Módulo | Propuesta inicial |
|---|---|---|---|
| taric.es/noticias | `taric.es` | (vacío) | Revisar configuración y utilidad editorial |
| prestotimes.com | `prestotimes.com` | IA para Marketing y Comercio | Revisar configuración y utilidad editorial |
| prestashop.es/blog | `prestashop.es` | PrestaShop | Revisar configuración y utilidad editorial |
| ontsi.es/es/rss.xml | `ontsi.es` | Digitalización GS | Revisar configuración y utilidad editorial |
| marketing4ecommerce.net/ecommerce/feed | `marketing4ecommerce.net` | Comercio Electrónico | Revisar configuración y utilidad editorial |
| juanarmada.com · WordPress API | `wordpress_api` | (vacío) | Revisar configuración y utilidad editorial |
| es.wordpress.org/news | `es.wordpress.org` | WordPress | Revisar configuración y utilidad editorial |
| cyberclick.es/numerical-blog | `cyberclick.es` | (vacío) | Revisar configuración y utilidad editorial |
| consultoresia.com/inteligencia-artificial | `consultoresia.com` | IA para Marketing y Comercio | Revisar configuración y utilidad editorial |
| casares.blog | `casares.blog` | (vacío) | Revisar configuración y utilidad editorial |

## Lectura inicial

La fuente `ecommerce-news.es` aporta gran parte del histórico y de la última ejecución. No conviene penalizarla, porque funciona y aporta noticias útiles, pero sí conviene equilibrar el sistema.

La revisión debe priorizar:

```text
- fuentes activas que realmente no son RSS;
- fuentes activas que requieren parser específico;
- fuentes transversales sin módulo declarado;
- fuentes que podrían mantenerse desactivadas con nota;
- posibles sustituciones de fuentes con mayor aportación educativa.
```
