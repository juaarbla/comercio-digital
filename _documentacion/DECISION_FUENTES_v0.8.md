# Decision de fuentes v0.8

## Decision general

La v0.8 se mantiene centrada en fuentes, diversidad y aportacion editorial.

No se abordan en este bloque:

```text
- rediseno visual;
- cambios en Schema.org;
- cambios en el pipeline principal;
- sustitucion masiva de fuentes;
- modificacion de feeds.json sin aprobacion expresa.
```

## Principio aplicado

Antes de cambiar configuracion, se documenta cada decision. Las fuentes que no aportan se separan en tres grupos:

```text
1. fuentes bien configuradas pero de baja frecuencia;
2. fuentes mal configuradas como HTML en lugar de RSS/API;
3. fuentes no fiables para el pipeline por captcha, bloqueo o ausencia de feed claro.
```

## Decision por fuente activa

| Fuente | Decision | Accion recomendada | Justificacion |
|---|---|---|---|
| `juanarmada.com/podcast/feed` | A - Mantener sin cambios | Mantener activa. | RSS valido, fuente propia y aporta identidad editorial. |
| `juanarmada.com/wp-json/wp/v2/posts` | B - Mantener pero corregir configuracion | Mantener activa y revisar trazabilidad de `source`. | La API funciona y contiene posts recientes, pero el informe la cuenta como 0 por clave `wordpress_api`; las noticias se detectan como `juanarmada.com`. |
| `ecommerce-news.es/feed` | A - Mantener sin cambios | Mantener activa. | Fuente estable y productiva. Su concentracion aconseja equilibrar, no desactivar. |
| `marketing4ecommerce.net/ecommerce/feed` | D - Desactivar temporalmente | Pasar a `activo:false` con nota, salvo que se encuentre una URL RSS sin captcha. | La comprobacion devuelve HTML anti-bot; el pipeline no puede procesarla como feed fiable. |
| `marketingdirecto.com/feed` | C - Mantener como observacion | Mantener temporalmente y monitorizar. | Tiene aportacion historica, aunque la comprobacion viva devuelve anti-bot. No desactivar sin observar otra ejecucion. |
| `ontsi.es/es/rss.xml` | C - Mantener como observacion | Mantener activa con nota editorial de baja frecuencia. | RSS valido. Puede aportar indicadores institucionales utiles aunque no haya aportado al historico reciente. |
| `taric.es/noticias/` | E - Sustituir por fuente mejor | Buscar alternativa RSS sobre comercio internacional/aduanas o crear parser especifico solo si compensa. | La URL es HTML y no se ha localizado feed alternativo claro. |
| `es.wordpress.org/news/` | B - Mantener pero corregir configuracion | Cambiar a `https://es.wordpress.org/news/feed/`. | La URL actual es HTML; el feed alternativo es RSS valido. |
| `casares.blog/` | B - Mantener pero corregir configuracion | Cambiar a `https://casares.blog/feed/`. | La URL actual es HTML; el feed alternativo es RSS valido y frecuente. |
| `prestashop.es/blog` | B - Mantener pero corregir configuracion | Cambiar a `https://prestashop.es/blog/feed.xml`. | La URL actual es HTML; el feed XML alternativo existe y contiene entradas recientes. |
| `prestotimes.com` | D - Desactivar temporalmente | Pasar a `activo:false` con nota. | Devuelve HTML anti-bot; no es fiable para el pipeline actual. |
| `consultoresia.com/inteligencia-artificial/` | B - Mantener pero corregir configuracion | Cambiar a `https://consultoresia.com/inteligencia-artificial/feed/`. | La URL actual es HTML; el feed alternativo es RSS valido. |
| `blog.hubspot.es/marketing/rss.xml` | A - Mantener sin cambios | Mantener activa. | RSS valido, contenido evergreen y aportacion historica aunque no diaria. |
| `cyberclick.es/numerical-blog` | B - Mantener pero corregir configuracion | Cambiar a `https://www.cyberclick.es/numerical-blog/rss.xml`. | La URL actual es HTML; el feed alternativo es RSS valido con entradas recientes. |

## Cambios candidatos para feeds.json

Aplicados en el bloque 2.

Cambios aplicados en este bloque:

```text
- es.wordpress.org/news/ -> es.wordpress.org/news/feed/
- casares.blog/ -> casares.blog/feed/
- prestashop.es/blog -> prestashop.es/blog/feed.xml
- consultoresia.com/inteligencia-artificial/ -> consultoresia.com/inteligencia-artificial/feed/
- www.cyberclick.es/numerical-blog -> www.cyberclick.es/numerical-blog/rss.xml
- marketing4ecommerce.net/ecommerce/feed -> activo:false + nota por captcha/anti-bot
- prestotimes.com -> activo:false + nota por captcha/anti-bot
- taric.es/noticias/ -> activo:false + nota o sustitucion documentada
```

## Fuentes transversales

Fuentes activas sin modulo declarado:

```text
juanarmada.com WordPress API
taric.es/noticias
casares.blog
cyberclick.es/numerical-blog
```

Decision editorial:

```text
- Juan Armada WordPress API puede seguir transversal porque el modulo se infiere desde categorias.
- Casares puede mantenerse como observacion WordPress/tecnologia si se corrige a RSS.
- Cyberclick deberia declararse como Marketing Digital si se corrige a RSS.
- Taric no deberia seguir como transversal activa si no hay feed o parser.
```

## Riesgos

```text
- Corregir varias fuentes a la vez puede aumentar volumen de noticias y coste LLM.
- Algunas fuentes RSS pueden traer contenido evergreen no siempre reciente.
- Las fuentes anti-bot pueden funcionar de forma intermitente, por lo que conviene documentar la fecha de comprobacion.
- El cruce de WordPress API en el informe puede seguir dando falso cero si no se ajusta la clave de fuente.
```

## Bloque 2 · Ajustes aplicados en feeds.json

Estado: aplicado.

Cambios realizados:

| Fuente | Acción | Motivo |
|---|---|---|
| `https://es.wordpress.org/news/` | Corregida a `https://es.wordpress.org/news/feed/` y se mantiene activa. | La URL anterior era HTML; se usa RSS oficial. |
| `https://casares.blog/` | Corregida a `https://casares.blog/feed/`, modulo `WordPress`, y se mantiene activa. | La URL anterior era HTML; se usa RSS. Fuente tecnica de observacion sobre WordPress, hosting y servidor. |
| `https://prestashop.es/blog` | Corregida a `https://prestashop.es/blog/feed.xml` y se mantiene activa. | La URL anterior era HTML; se usa feed XML del blog. |
| `https://consultoresia.com/inteligencia-artificial/` | Corregida a `https://consultoresia.com/inteligencia-artificial/feed/` y se mantiene activa. | La URL anterior era HTML; se usa RSS de la categoria. |
| `https://www.cyberclick.es/numerical-blog` | Corregida a `https://www.cyberclick.es/numerical-blog/rss.xml`, modulo `Marketing Digital`, y se mantiene activa. | La URL anterior era HTML; se usa RSS. Fuente de marketing digital y analitica. |
| `https://marketing4ecommerce.net/ecommerce/feed` | Desactivada temporalmente con `activo:false`. | La comprobacion tecnica detecto HTML anti-bot/captcha; no es fiable para el pipeline como RSS. |
| `https://prestotimes.com` | Desactivada temporalmente con `activo:false`. | La comprobacion tecnica detecto HTML anti-bot/captcha; no es fiable para el pipeline actual. |
| `https://www.taric.es/noticias/` | Modulo asignado `Comercio Digital Internacional` y desactivada temporalmente con `activo:false`. | La URL es una pagina HTML y no se localizo RSS alternativo claro. Requiere sustitucion o parser especifico si compensa. |

## Validacion requerida antes de commit

En el bloque 2 solo se valida estructura y alcance. El pipeline completo queda para el bloque 3.

```powershell
python -m json.tool .\feeds.json > $null
git status
```

Cuando se ejecute el bloque 3, comparar:

```text
- fuentes activas;
- fuentes inactivas;
- fuentes activas sin aportacion historica;
- fuentes activas sin aportacion en ultima ejecucion;
- concentracion de ecommerce-news.es;
- noticias sin RA;
- noticias sin conceptos clave.
```

## Cierre del bloque 1

El bloque 1 queda documentado como auditoria y decision previa. La conclusion principal es que la baja diversidad no se debe solo a falta de fuentes, sino a varias fuentes activas configuradas como paginas HTML o bloqueadas por anti-bot.

La accion siguiente natural es pedir autorizacion para aplicar un ajuste controlado en `feeds.json`.

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

### Justificacion

ICEX es una fuente oficial sobre internacionalizacion, exportacion, mercados exteriores y apoyo a empresas espanolas. Tiene alto valor docente para Comercio Digital Internacional.

La evaluacion tecnica no ha localizado RSS valido aprovechable. Las paginas revisadas responden como HTML y las rutas RSS habituales devuelven 404. Por tanto, no se incorpora a `feeds.json` y no se implementa scraping HTML en esta fase.

Queda como fuente candidata para revision manual o para una posible reevaluacion futura si publica un feed RSS valido.

## Auditoria rapida de fuentes v0.8

| Fuente | RSS evaluado | Estado | Decision | Motivo |
|---|---|---|---|---|
| INCIBE | `https://www.incibe.es/rss.xml` | Inactiva por prudencia | Mantener inactiva con nota en `feeds.json` | RSS valido y reciente, pero muy centrado en vulnerabilidades, SCI y avisos tecnicos. |
| Red.es | `https://www.red.es/rss.xml` | Rechazada para pipeline | No incorporar | RSS existente pero no util: devuelve solo un item antiguo/de prueba de 2021. |
| Camara de Comercio de Espana | `https://www.camara.es/rss.xml` | Aceptada con filtros | Incorporar a `feeds.json` | RSS valido y reciente sobre internacionalizacion, pymes, emprendimiento y programas empresariales. |
| Think with Google Espana | `https://www.thinkwithgoogle.com/intl/es-es/rss.xml` | Aceptada con filtros | Incorporar a `feeds.json` | RSS valido sobre marketing digital, IA, analitica, consumidor y tendencias. |
| Semrush Blog Espana | `https://es.semrush.com/blog/feed/` | Aceptada con filtros | Incorporar a `feeds.json` | RSS valido sobre SEO, SEM, contenidos, analitica y redes sociales; fuente comercial/evergreen. |
| Shopify Blog Espana | rutas `/blog.atom`, `/blog/rss.xml`, `/blog/feed` | Pendiente por falta de RSS | No incorporar | La pagina es HTML y las rutas RSS/Atom evaluadas devuelven 404. |
| Doofinder Blog | `/es/blog/feed`, `/es/blog/rss.xml` | Rechazada para pipeline | No incorporar | La pagina principal devuelve 403 y no hay RSS valido estable. |

### Decisiones aplicadas

Se incorporan a `feeds.json`:

```text
https://www.camara.es/rss.xml
https://www.thinkwithgoogle.com/intl/es-es/rss.xml
https://es.semrush.com/blog/feed/
```

Se mantiene en `feeds.json` pero inactiva:

```text
https://www.incibe.es/rss.xml
```

No se incorporan por falta de RSS util o estable:

```text
https://www.red.es/
https://www.shopify.com/es/blog
https://www.doofinder.com/es/blog
```

No se crea scraping HTML para ninguna fuente de este lote.
