## v0.7 · Alta en buscadores y Bloque 7 · Schema para newsletter

Se confirma el alta de `comerciodigital.net` en herramientas de seguimiento de indexación:

- Google Search Console.
- Bing Webmaster Tools.

El objetivo es empezar a recoger datos reales de rastreo, indexación, cobertura y rendimiento orgánico tras la incorporación progresiva de datos estructurados Schema.org.

Sitemap principal:

```text
https://comerciodigital.net/sitemap.xml
```

Además, se prepara el Bloque 7 de la v0.7: añadir Schema.org a la newsletter.

El enfoque elegido es describir la newsletter como colección editorial mediante:

- `CollectionPage`;
- `ItemList`;
- `ListItem`.

Se mantiene la decisión de no usar `Article` ni `NewsArticle` para noticias externas. Las noticias enlazadas se tratan como elementos de una lista curada, no como artículos propios publicados por Comercio Digital.

Queda fuera de este bloque el sitemap recursivo, canonical en subcarpetas y Open Graph específico para newsletter.

---

## v0.7 · Cierre final · SEO semántico y Schema.org

Se cierra la fase **v0.7 · SEO semántico y datos estructurados Schema.org**.

Durante esta fase se ha incorporado una capa semántica JSON-LD al agregador sin rediseñar la web ni modificar la arquitectura principal del pipeline.

### Bloques completados

- Bloque 1 · Roadmap v0.7.
- Bloque 2 · Diagnóstico SEO actual.
- Bloque 3 · Creación de `schema_utils.py`.
- Bloque 4 · Schema básico en portada.
- Bloque 4b · Schema básico en páginas principales.
- Bloque 6 · Schema educativo `LearningResource` en fichas de aula.
- Tarea complementaria · Alta en Google Search Console y Bing Webmaster Tools.
- Bloque 7 · Schema para newsletter.
- Bloque final · Validación post-pipeline y cierre.

### Datos estructurados incorporados

En portada:

```text
Organization
WebSite
CollectionPage
```

En páginas principales:

```text
CollectionPage
WebPage
```

En fichas de aula:

```text
LearningResource
```

En newsletter:

```text
CollectionPage
ItemList
ListItem
```

### Decisión editorial importante

Se documenta la decisión de no usar `Article` ni `NewsArticle` para las noticias externas enlazadas por el agregador.

Motivo:

```text
Comercio Digital no publica la noticia original completa.
El sitio actúa como agregador educativo, curador y generador de contexto docente.
```

Por tanto, las noticias externas se representan como elementos de listados o colecciones, no como artículos propios.

### Alta en buscadores

Se confirma el alta del sitio en:

```text
Google Search Console
Bing Webmaster Tools
```

Sitemap principal:

```text
https://comerciodigital.net/sitemap.xml
```

### Informe post-pipeline

Informe generado:

```text
2026-07-07 21:56:24
```

Estado general:

```text
AMARILLO
```

Lectura:

```text
El sistema funciona correctamente, pero hay avisos que conviene revisar.
```

Resumen del informe:

```text
Noticias resumidas: 282
Noticias clasificadas: 282
Fuentes configuradas: 19
Fuentes activas: 14
Fuentes inactivas: 5
Registros en historial: 241
Fichas HTML generadas: 10
Fichas MD generadas: 10
Newsletters HTML disponibles: 2
Newsletters MD disponibles: 2
Alertas críticas: 0
Avisos: 5
Recomendaciones: 1
```

Archivos clave:

```text
Portada: OK
Aula: OK
Índice newsletter: OK
CSS principal: OK
```

### Avisos no bloqueantes

El informe mantiene avisos sobre:

- 2 noticias sin RA asignado.
- 2 noticias sin conceptos clave.
- Concentración histórica de `ecommerce-news.es`.
- Concentración de `ecommerce-news.es` en la última ejecución.
- Fuentes activas sin aportación en la última ejecución.
- Recomendación de revisar fuentes activas sin aportación histórica.

Estos avisos no bloquean el cierre de la v0.7 porque pertenecen a mantenimiento editorial y revisión de fuentes, no a errores de Schema.org ni del pipeline.

### Tarea trasladada

Se propone trasladar a la siguiente fase:

```text
v0.8 · Revisión de fuentes, diversidad y aportación editorial
```

### Estado final

```text
v0.7 cerrada con avisos no bloqueantes.
```
