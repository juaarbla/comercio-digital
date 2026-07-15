# Seguimiento de fuentes post-v0.8

Fecha base: 2026-07-09

## Resumen de v0.8

La v0.8 reviso fuentes, diversidad y aportacion editorial. El objetivo fue mejorar la robustez del agregador sin redisenar la web, sin tocar Schema.org y sin introducir scraping HTML.

Acciones principales:

```text
- corregir fuentes HTML a RSS/XML cuando existia alternativa valida;
- desactivar temporalmente fuentes no fiables;
- documentar candidatas sin RSS valido;
- incorporar fuentes nuevas con RSS valido y valor docente;
- mantener trazabilidad de cada decision en Markdown.
```

## Metricas del informe 2026-07-09

```text
Estado general: AMARILLO
Alertas criticas: 0
Avisos: 4
Recomendaciones: 1
Noticias resumidas: 295
Noticias clasificadas: 295
Fuentes configuradas: 22
Fuentes activas: 14
Fuentes inactivas: 8
Registros en historial: 254
Fichas HTML generadas: 10
Fichas MD generadas: 10
Newsletters HTML disponibles: 2
Newsletters MD disponibles: 2
```

Ultima ejecucion detectada:

```text
Fecha: 2026-07-09
Noticias resumidas: 13
Noticias clasificadas: 13
Noticias marcadas para ficha: 4
Noticias marcadas para newsletter: 1
```

Fuentes en la ultima ejecucion:

```text
ecommerce-news.es: 9
cyberclick.es: 3
camara.es: 1
```

## Fuentes corregidas

```text
https://es.wordpress.org/news/ -> https://es.wordpress.org/news/feed/
https://casares.blog/ -> https://casares.blog/feed/
https://prestashop.es/blog -> https://prestashop.es/blog/feed.xml
https://consultoresia.com/inteligencia-artificial/ -> https://consultoresia.com/inteligencia-artificial/feed/
https://www.cyberclick.es/numerical-blog -> https://www.cyberclick.es/numerical-blog/rss.xml
```

## Fuentes incorporadas

```text
https://www.camara.es/rss.xml
https://www.thinkwithgoogle.com/intl/es-es/rss.xml
https://es.semrush.com/blog/feed/
```

## Fuentes desactivadas o mantenidas inactivas

```text
https://marketing4ecommerce.net/ecommerce/feed
https://prestotimes.com
https://www.taric.es/noticias/
https://www.incibe.es/rss.xml
```

Motivos principales:

```text
- HTML anti-bot/captcha;
- ausencia de RSS claro;
- paginas HTML no procesables como feed;
- ruido tecnico o editorial si se activan sin filtros mas finos.
```

## Candidatas documentadas sin automatizar

```text
Emprendedores.es
ICEX
Red.es
Shopify Blog Espana
Doofinder Blog
```

No se incorporan al pipeline mientras no exista RSS/Atom valido, accesible y estable.

## Criterios de observacion v0.9

Durante las proximas 2 o 3 ejecuciones conviene observar:

```text
- aportacion real de Camara, Think with Google y Semrush;
- continuidad de Cyberclick tras la correccion a RSS;
- si Prestashop, WordPress.org, Consultores IA y Casares empiezan a aportar;
- si ecommerce-news.es reduce peso relativo en la ultima ejecucion;
- si aparecen noticias sin RA o sin conceptos clave;
- si alguna fuente nueva genera ruido comercial, institucional o evergreen excesivo.
```

## Decision editorial

No anadir mas fuentes hasta disponer de 2 o 3 ejecuciones adicionales. La prioridad de v0.9 es estabilizar, medir y mejorar la observabilidad editorial del informe post-pipeline.

## Fuentes en observacion

```text
cyberclick.es
camara.es
thinkwithgoogle.com
es.semrush.com
prestashop.es
es.wordpress.org
consultoresia.com
casares.blog
ontsi.es
marketingdirecto.com
juanarmada.com WordPress API
```

## Criterios de decision futura

```text
Mantener activa:
- aporta contenido util;
- RSS estable;
- valor docente medio o alto.

Mantener en observacion:
- RSS valido pero baja frecuencia;
- fuente institucional o evergreen con aportacion irregular.

Desactivar temporalmente:
- genera ruido;
- falla tecnicamente;
- devuelve HTML, captcha o contenido no procesable.
```

## Evaluacion rapida de nuevas candidatas v0.9

Decision operativa de este lote: no incorporar nuevas fuentes a `feeds.json` por ahora. Todas las candidatas tienen algun RSS valido, pero v0.9 esta en fase de estabilizacion y conviene observar primero las fuentes incorporadas en v0.8.

| Fuente | RSS evaluado | Estado | Decision | Accion |
|---|---|---|---|---|
| IAB Spain | `https://iabspain.es/feed/` | RSS valido | ACEPTAR CON FILTROS | Documentar como candidata; no incorporar todavia |
| IncoDocs Blog | `https://incodocs.com/blog/feed/` | RSS valido | ACEPTAR CON FILTROS | Documentar como candidata CDI; no incorporar todavia |
| AI Weekly | `https://aiweekly.co/feed/` / `https://aiweekly.co/rss.xml` | RSS valido | ACEPTAR CON FILTROS | Documentar como candidata IA; no incorporar todavia |
| LliureX / PortalEdu | `https://portal.edu.gva.es/blogs/s1/lliurex/es/feed/` | RSS valido | MANTENER COMO FUENTE MANUAL | Documentar para uso manual o baja prioridad |
| Lodgify Blog ES | `https://www.lodgify.com/blog/es/feed/` | RSS valido | ACEPTAR CON FILTROS | Documentar como candidata sectorial; no incorporar todavia |

### IAB Spain

- URL principal: https://iabspain.es/
- RSS valido localizado: https://iabspain.es/feed/
- Rutas probadas: `/feed/`, `/rss.xml`, `/category/noticias/feed/`, `/category/blog/feed/`, `/actualidad/feed/`
- Modulo sugerido: Marketing Digital
- Valor docente: alto para publicidad digital, medicion, retail media, redes sociales, IA aplicada al marketing y estudios sectoriales
- Riesgo: contenido corporativo, premios, eventos, comisiones y actualidad sectorial no siempre aplicable al aula
- Motivo de la decision: RSS valido y reciente, pero conviene filtrar para evitar agenda institucional o noticias internas
- Newsletter: solo si pasa filtro docente

### IncoDocs Blog

- URL principal: https://incodocs.com/blog/
- RSS valido localizado: https://incodocs.com/blog/feed/
- Rutas probadas: `/blog/feed/`, `/blog/rss.xml`, `/blog/atom.xml`, `/feed/`, `/rss.xml`
- Modulo sugerido: Comercio Digital Internacional
- Valor docente: medio-alto para documentacion comercial, exportacion, importacion, logistica, shipping e Incoterms
- Riesgo: contenido en ingles, enfoque de producto y articulos evergreen
- Motivo de la decision: RSS valido y muy alineado con CDI, pero se recomienda observar antes de incorporarlo porque puede requerir filtro idiomatico y editorial
- Newsletter: solo si pasa filtro docente y aporta aplicacion clara al aula

### AI Weekly

- URL principal: https://aiweekly.co/
- RSS valido localizado: https://aiweekly.co/feed/ y https://aiweekly.co/rss.xml
- Rutas probadas: `/feed/`, `/rss.xml`, `/atom.xml`, `/issues/feed/`, `/newsletter/feed/`
- Modulo sugerido: IA para Marketing y Comercio
- Valor docente: medio para tendencias de IA, automatizacion y aplicaciones empresariales
- Riesgo: exceso de contenido tecnico, investigacion, robotics, modelos, chips, benchmarks o financiacion poco conectada con Comercio y Marketing
- Motivo de la decision: RSS valido, pero requiere filtros fuertes para no introducir ruido tecnico
- Newsletter: no automatizar; solo uso manual o seleccion muy filtrada

### LliureX / PortalEdu

- URL principal: https://portal.edu.gva.es/blogs/s1/lliurex/es/
- RSS valido localizado: https://portal.edu.gva.es/blogs/s1/lliurex/es/feed/
- Rutas probadas: `/es/feed/`, `/feed/`, `/es/rss.xml`, `/rss.xml`
- Modulo sugerido: Digitalizacion GS o Digitalizacion GM
- Valor docente: medio para competencia digital, software libre, Linux educativo y herramientas publicas
- Riesgo: baja relacion directa con Comercio y Marketing; contenidos mas centrados en entorno educativo que en empresa
- Motivo de la decision: RSS valido, pero prioridad baja-media para el agregador principal; mejor como fuente manual o para actividades puntuales
- Newsletter: no automatizar

### Lodgify Blog ES

- URL principal: https://www.lodgify.com/blog/es/
- RSS valido localizado: https://www.lodgify.com/blog/es/feed/
- Rutas probadas: `/blog/es/feed/`, `/blog/es/rss.xml`, `/blog/es/atom.xml`, `/blog/es/feed.xml`, `/blog/feed/`
- Modulo sugerido: Comercio Electronico
- Valor docente: medio para ecommerce, webs de reserva, SEO local, canales de venta online y negocio digital turistico
- Riesgo: fuente comercial, nicho de alquiler vacacional, contenidos legales/fiscales o sectoriales demasiado estrechos
- Motivo de la decision: RSS valido y reciente, pero se recomienda no incorporarlo todavia por prioridad baja-media y riesgo de ruido sectorial
- Newsletter: solo si pasa filtro docente y no es contenido promocional

## Observacion de ejecuciones post-v0.8

Periodo revisado: 2026-07-09 a 2026-07-14.

| Informe | Noticias ultima ejecucion | Fuentes en ultima ejecucion | Fuentes activas sin historico | Fuentes activas sin ultima ejecucion | Lectura |
|---|---:|---|---:|---:|---|
| 2026-07-09 | 13 | ecommerce-news.es: 9; cyberclick.es: 3; camara.es: 1 | 7 | 11 | Primeras senales positivas de Cyberclick y Camara. |
| 2026-07-10 | 15 | ecommerce-news.es: 10; consultoresia.com: 2; cyberclick.es: 2; casares.blog: 1 | 5 | 10 | Mejor diversidad: aparecen Consultores IA y Casares. |
| 2026-07-11 | 11 | ecommerce-news.es: 9; casares.blog: 1; cyberclick.es: 1 | 5 | 11 | Ecommerce-news vuelve a concentrar la ultima ejecucion. |
| 2026-07-13 | 1 | casares.blog: 1 | 5 | 13 | Ejecucion de muy bajo volumen; no tomar decisiones con este dato aislado. |
| 2026-07-14 | 21 | ecommerce-news.es: 17; cyberclick.es: 4 | 5 | 12 | Buen volumen, pero ecommerce-news concentra el 81,0% de la ultima ejecucion. |

### Lectura editorial

La v0.8 empieza a dar senales utiles:

```text
- cyberclick.es aporta de forma recurrente;
- camara.es ya aporto contenido CDI;
- casares.blog y consultoresia.com han empezado a aportar historico;
- WordPress API queda trazada con alias wordpress_api / juanarmada.com.
```

La concentracion de `ecommerce-news.es` sigue siendo el principal punto de observacion:

```text
- 73,8% del historico clasificado en 2026-07-14;
- 81,0% de la ultima ejecucion detectada en 2026-07-14.
```

### Decision temporal

No anadir nuevas fuentes todavia. Mantener la observacion durante 2 o 3 ejecuciones mas antes de activar candidatas documentadas como IAB Spain, IncoDocs o AI Weekly.

Prioridad de observacion:

```text
1. Confirmar si cyberclick.es mantiene aportacion util.
2. Comprobar si camara.es vuelve a aportar CDI.
3. Esperar senales de thinkwithgoogle.com y es.semrush.com.
4. Vigilar si ecommerce-news.es sigue por encima del 80% en varias ultimas ejecuciones.
5. Mantener sin cambios fuentes de baja frecuencia si el RSS sigue siendo valido.
```
