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
