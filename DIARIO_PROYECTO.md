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
