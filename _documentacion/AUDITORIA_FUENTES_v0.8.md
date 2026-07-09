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

## Recomendacion documentada en el bloque 1

En el bloque 1 se recomendo no modificar `feeds.json` sin aprobacion expresa.

Cambios candidatos documentados entonces y aplicados de forma controlada en el bloque 2:

```text
1. Corregir URLs HTML con feed alternativo confirmado.
2. Anadir notas a fuentes transversales.
3. Desactivar temporalmente fuentes con captcha o sin RSS claro.
4. Revisar el cruce de WordPress API para que no aparezca como fuente sin aportacion.
5. Ejecutar pipeline e informe post-ajustes en el bloque 3.
```

## Bloque 2 · Aplicación controlada de ajustes

Estado: aplicado en feeds.json.

Se han corregido URLs HTML a feeds RSS/XML cuando existia alternativa clara y se han desactivado temporalmente fuentes no fiables para el pipeline actual.

Correcciones aplicadas:

| Fuente anterior | Fuente nueva | Estado |
|---|---|---|
| `https://es.wordpress.org/news/` | `https://es.wordpress.org/news/feed/` | Activa |
| `https://casares.blog/` | `https://casares.blog/feed/` | Activa |
| `https://prestashop.es/blog` | `https://prestashop.es/blog/feed.xml` | Activa |
| `https://consultoresia.com/inteligencia-artificial/` | `https://consultoresia.com/inteligencia-artificial/feed/` | Activa |
| `https://www.cyberclick.es/numerical-blog` | `https://www.cyberclick.es/numerical-blog/rss.xml` | Activa |

Desactivaciones temporales aplicadas:

| Fuente | Estado | Motivo |
|---|---|---|
| `https://marketing4ecommerce.net/ecommerce/feed` | Inactiva | HTML anti-bot/captcha. |
| `https://prestotimes.com` | Inactiva | HTML anti-bot/captcha. |
| `https://www.taric.es/noticias/` | Inactiva | Pagina HTML sin RSS alternativo claro. |

## Emprendedores.es

- URL: https://emprendedores.es/
- Estado: pendiente / no incorporada
- Decision: no incorporar al pipeline por ahora
- Motivo: no se ha encontrado RSS valido aprovechable
- Valor editorial: alto para emprendimiento, pymes, marketing, ventas, franquicias, startups y casos de empresa
- Valor docente: alto como fuente manual o inspiracion para actividades de aula
- Riesgo: contenido patrocinado, branded content y ruido comercial
- Newsletter: no automatizar; solo uso manual si procede

### Justificacion

Emprendedores.es es una fuente interesante para contenidos de emprendimiento, pymes, ventas, marketing, franquicias y casos de empresa. Puede aportar ejemplos utiles para Formacion Profesional de Comercio y Marketing.

Sin embargo, al no disponer de un RSS valido aprovechable, no se incorpora al pipeline automatico del agregador. No se recomienda implementar scraping HTML en esta fase para evitar complejidad, fragilidad y ruido editorial.

La fuente queda documentada como candidata para revision manual o para una posible reevaluacion futura si publica un feed RSS valido.

## ICEX

- URL: https://www.icex.es/
- Area: Comercio Digital Internacional
- Tipo: institucional
- Estado: pendiente / no incorporada
- Decision: no incorporar al pipeline por ahora
- Motivo: no se ha encontrado RSS valido aprovechable
- Valor editorial: alto para internacionalizacion, exportacion, mercados exteriores, ayudas, financiacion y programas de apoyo a empresas espanolas
- Valor docente: alto para Comercio Digital Internacional y casos de aula
- Riesgo: ausencia de RSS y exceso de contenido institucional o agenda
- Newsletter: no automatizar; solo uso manual si procede

### Comprobacion tecnica

Se revisaron las paginas principales de sala de prensa, notas de prensa y Radar ICEX, junto con rutas RSS habituales:

```text
https://www.icex.es/es/sala-prensa
https://www.icex.es/es/sala-prensa/notas-de-prensa
https://www.icex.es/es/radar-icex/todo-en-el-radar-icex
https://www.icex.es/feed/
https://www.icex.es/rss.xml
https://www.icex.es/es/rss.xml
https://www.icex.es/es/sala-prensa/rss.xml
https://www.icex.es/es/sala-prensa/notas-de-prensa/rss.xml
https://www.icex.es/es/radar-icex/rss.xml
```

Las paginas editoriales devuelven HTML y no declaran RSS/Atom detectable. Las rutas RSS comprobadas devuelven 404.

### Justificacion

ICEX es una fuente oficial muy relevante para internacionalizacion, exportacion, mercados exteriores y programas de apoyo a empresas espanolas. Encaja especialmente con el modulo de Comercio Digital Internacional.

Sin embargo, al no disponer de un RSS valido aprovechable, no se incorpora al pipeline automatico del agregador. No se recomienda implementar scraping HTML en esta fase para evitar complejidad, fragilidad y ruido institucional.

La fuente queda documentada como candidata para revision manual o para reevaluacion futura si ICEX publica un feed RSS valido.

## Auditoria rapida de fuentes v0.8

### INCIBE

- URL principal: https://www.incibe.es/
- RSS evaluado: https://www.incibe.es/rss.xml
- Estado: Inactiva por prudencia
- Decision: mantener en `feeds.json` como inactiva con nota
- Modulo sugerido: Digitalizacion GS
- Valor docente: medio-alto si se seleccionan casos aplicados a pymes, fraude online, phishing o comercio electronico seguro
- Riesgo: avisos tecnicos, boletines de vulnerabilidades y alertas demasiado especificas
- Motivo: el RSS es valido y reciente, pero los titulos revisados se concentran en vulnerabilidades, SCI y avisos de seguridad. Puede generar ruido si se activa sin filtros mas finos.
- Newsletter: no automatizar; solo uso manual o si pasa filtro docente

### Red.es

- URL principal: https://www.red.es/
- RSS evaluado: https://www.red.es/rss.xml
- Estado: Rechazada para pipeline
- Decision: no incorporar
- Modulo sugerido: Digitalizacion GS
- Valor docente: medio potencial para digitalizacion de pymes y programas publicos
- Riesgo: RSS no util para automatizacion
- Motivo: existe RSS, pero solo devuelve un item antiguo/de prueba de 2021 y no representa la actualidad util de Red.es.
- Newsletter: no automatizar

### Camara de Comercio de Espana

- URL principal: https://www.camara.es/
- RSS evaluado: https://www.camara.es/rss.xml
- Estado: Aceptada con filtros
- Decision: incorporar a `feeds.json`
- Modulo sugerido: Comercio Digital Internacional
- Valor docente: alto
- Riesgo: contenido institucional, agenda o notas corporativas con valor docente desigual
- Motivo: RSS valido y reciente, con contenidos sobre internacionalizacion, pymes, emprendimiento, oficinas Acelera pyme y programas empresariales.
- Newsletter: solo si pasa filtro docente

### Think with Google Espana

- URL principal: https://www.thinkwithgoogle.com/intl/es-es/
- RSS evaluado: https://www.thinkwithgoogle.com/intl/es-es/rss.xml
- Estado: Aceptada con filtros
- Decision: incorporar a `feeds.json`
- Modulo sugerido: Marketing Digital
- Valor docente: alto
- Riesgo: sesgo de plataforma y contenido de tendencia no siempre aplicable al aula
- Motivo: RSS valido con articulos recientes sobre marketing digital, IA, analitica, comportamiento del consumidor y tendencias.
- Newsletter: solo si pasa filtro docente

### Semrush Blog Espana

- URL principal: https://es.semrush.com/blog/
- RSS evaluado: https://es.semrush.com/blog/feed/
- Estado: Aceptada con filtros
- Decision: incorporar a `feeds.json`
- Modulo sugerido: Marketing Digital
- Valor docente: medio-alto
- Riesgo: fuente comercial, contenido evergreen y posible promocion de herramienta
- Motivo: RSS valido sobre SEO, SEM, analitica, contenidos, redes sociales y busqueda local. Aporta utilidad docente si se filtra por aplicacion practica.
- Newsletter: solo si pasa filtro docente

### Shopify Blog Espana

- URL principal: https://www.shopify.com/es/blog
- RSS evaluado: https://www.shopify.com/es/blog.atom, https://www.shopify.com/es/blog/rss.xml, https://www.shopify.com/es/blog/feed
- Estado: Pendiente por falta de RSS
- Decision: no incorporar
- Modulo sugerido: Comercio Electronico
- Valor docente: alto potencial
- Riesgo: contenido comercial de plataforma
- Motivo: la pagina principal responde como HTML y las rutas RSS/Atom evaluadas devuelven 404. No se crea scraping HTML.
- Newsletter: no automatizar

### Doofinder Blog

- URL principal: https://www.doofinder.com/es/blog
- RSS evaluado: https://www.doofinder.com/es/blog/feed, https://www.doofinder.com/es/blog/rss.xml
- Estado: Rechazada para pipeline
- Decision: no incorporar
- Modulo sugerido: Comercio Electronico
- Valor docente: medio potencial para buscador interno, conversion y UX ecommerce
- Riesgo: fuente comercial y bloqueo tecnico
- Motivo: la pagina principal devuelve 403, `/feed` devuelve HTML y `/rss.xml` no ofrece un RSS valido estable. No se crea scraping HTML.
- Newsletter: no automatizar
