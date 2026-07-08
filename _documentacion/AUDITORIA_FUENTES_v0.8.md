# Auditoria de fuentes v0.8

## Base de trabajo

Fecha de revision: 2026-07-08

Archivos revisados:

```text
feeds.json
historial.json
data/processed/noticias_resumidas.json
data/processed/noticias_clasificadas.json
logs/informe_pipeline_2026-07-08.md
news_aggregator.py
```

Comprobaciones realizadas:

```text
- cruce entre fuentes activas de feeds.json y fuente_detectada en noticias_clasificadas.json;
- revision del informe post-pipeline de 2026-07-08;
- comprobacion tecnica de URLs activas: estado HTTP, tipo de contenido y muestra inicial;
- busqueda de feeds alternativos comunes para fuentes configuradas como paginas HTML.
```

No se ha modificado `feeds.json` en este bloque.

## Resumen operativo

```text
Fuentes configuradas: 19
Fuentes activas: 14
Fuentes inactivas: 5
Noticias clasificadas: 282
Ultima ejecucion detectada: 2026-07-07
Noticias clasificadas en la ultima ejecucion: 23
```

Distribucion por fuente detectada en el historico:

| Fuente detectada | Noticias |
|---|---:|
| ecommerce-news.es | 208 |
| incibe.es | 39 |
| marketingdirecto.com | 22 |
| juanarmada.com | 8 |
| blog.hubspot.es | 5 |

La concentracion de `ecommerce-news.es` es real: aporta el 73,8% del historico clasificado y 21 de las 23 noticias de la ultima ejecucion.

## Criterios de clasificacion

| Codigo | Significado |
|---|---|
| A | Mantener sin cambios |
| B | Mantener pero corregir configuracion |
| C | Mantener como fuente transversal/de observacion |
| D | Desactivar temporalmente |
| E | Sustituir por una fuente mejor |

## Auditoria de fuentes activas

| Fuente activa | Tipo tecnico comprobado | Aportacion historica | Ultima ejecucion | Decision | Motivo |
|---|---|---:|---:|---|---|
| `https://juanarmada.com/podcast/feed/` | RSS valido | 8* | 2* | A | Fuente propia, estable y con RSS correcto. Aporta contenido editorial de autor. |
| `https://juanarmada.com/wp-json/wp/v2/posts?...` | JSON API valida | 0 segun clave `wordpress_api` | 0 segun clave `wordpress_api` | B | La API responde y contiene posts recientes, pero el informe no la cruza con `fuente_detectada` porque las noticias quedan como `juanarmada.com`. Requiere ajustar trazabilidad, no desactivar. |
| `https://ecommerce-news.es/feed/` | RSS valido | 208 | 21 | A | Fuente principal y funcional. Debe mantenerse, aunque conviene equilibrar su peso con otras fuentes. |
| `https://marketing4ecommerce.net/ecommerce/feed` | HTML anti-bot / captcha, no RSS efectivo | 0 | 0 | D | Devuelve `202 text/html` con redireccion a captcha. El pipeline no puede procesarla de forma fiable como RSS. |
| `https://www.marketingdirecto.com/feed` | HTML anti-bot en comprobacion viva | 22 | 0 | C | Tiene aportacion historica, pero en la comprobacion actual devuelve pantalla anti-bot. Mantener en observacion antes de desactivar. |
| `https://www.ontsi.es/es/rss.xml` | RSS valido | 0 | 0 | C | RSS correcto con entradas, algunas recientes. Puede aportar informes e indicadores de baja frecuencia; no parece mal configurada. |
| `https://www.taric.es/noticias/` | HTML, no RSS | 0 | 0 | E | Pagina de noticias, no feed. No se ha localizado RSS alternativo claro. Requiere sustitucion o parser especifico. |
| `https://es.wordpress.org/news/` | HTML, no RSS | 0 | 0 | B | La fuente correcta parece `https://es.wordpress.org/news/feed/`, RSS valido con entradas recientes. |
| `https://casares.blog/` | HTML, no RSS | 0 | 0 | B | La fuente correcta parece `https://casares.blog/feed/`, RSS valido y con alta frecuencia. |
| `https://prestashop.es/blog` | HTML, no RSS | 0 | 0 | B | La fuente correcta parece `https://prestashop.es/blog/feed.xml`, XML valido con entradas recientes. |
| `https://prestotimes.com` | HTML anti-bot / captcha | 0 | 0 | D | Devuelve `202 text/html` con captcha. No es fiable para el pipeline actual. |
| `https://consultoresia.com/inteligencia-artificial/` | HTML, no RSS | 0 | 0 | B | La fuente correcta parece `https://consultoresia.com/inteligencia-artificial/feed/`, RSS valido con entradas recientes. |
| `https://blog.hubspot.es/marketing/rss.xml` | RSS valido | 5 | 0 | A | RSS correcto y con contenido evergreen. Baja aportacion reciente, pero no hay indicio de fallo tecnico. |
| `https://www.cyberclick.es/numerical-blog` | HTML, no RSS | 0 | 0 | B | La fuente correcta parece `https://www.cyberclick.es/numerical-blog/rss.xml`, RSS valido con entradas recientes. |

`*` Nota sobre `juanarmada.com`: el procesado actual detecta la fuente por dominio. Por eso podcast y WordPress API pueden mezclarse en metricas basadas solo en `fuente_detectada`.

## Hallazgos tecnicos

Fuentes activas con configuracion correcta:

```text
juanarmada.com/podcast/feed
juanarmada.com/wp-json/wp/v2/posts
ecommerce-news.es/feed
ontsi.es/es/rss.xml
blog.hubspot.es/marketing/rss.xml
```

Fuentes activas que son HTML y deberian cambiar a feed real:

```text
es.wordpress.org/news -> es.wordpress.org/news/feed/
casares.blog -> casares.blog/feed/
prestashop.es/blog -> prestashop.es/blog/feed.xml
consultoresia.com/inteligencia-artificial/ -> consultoresia.com/inteligencia-artificial/feed/
www.cyberclick.es/numerical-blog -> www.cyberclick.es/numerical-blog/rss.xml
```

Fuentes activas bloqueadas o no fiables para RSS:

```text
marketing4ecommerce.net/ecommerce/feed
prestotimes.com
```

Fuente activa sin RSS alternativo claro:

```text
taric.es/noticias/
```

Fuente activa con comportamiento mixto:

```text
marketingdirecto.com/feed
```

Aunque tiene aportacion historica, la comprobacion viva devolvio una respuesta anti-bot. Conviene observarla antes de decidir su desactivacion.

## Lectura editorial

`ecommerce-news.es` no debe penalizarse: funciona y aporta volumen util. El problema no es su calidad, sino la dependencia excesiva del sistema respecto a una sola fuente.

La prioridad de v0.8 deberia ser recuperar diversidad mediante correcciones de configuracion de fuentes ya existentes antes de buscar sustituciones externas. Hay cinco fuentes activas con feed alternativo claro y contenido reciente; corregirlas probablemente reducira avisos sin tocar el pipeline principal.

## Recomendacion para el siguiente bloque

No modificar todavia `feeds.json` sin aprobacion expresa.

Cambios candidatos, cuando se autorice el bloque de ajustes:

```text
1. Corregir URLs HTML con feed alternativo confirmado.
2. Anadir notas a fuentes transversales.
3. Desactivar temporalmente fuentes con captcha o sin RSS claro.
4. Revisar el cruce de WordPress API para que no aparezca como fuente sin aportacion.
5. Ejecutar pipeline e informe post-ajustes.
```
