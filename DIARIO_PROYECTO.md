## v0.7 · Bloque 4b · Schema básico en páginas principales

Se prepara la extensión controlada de Schema.org desde la portada hacia las páginas principales del agregador.

El objetivo de este bloque es que las páginas principales de primer nivel incorporen JSON-LD básico sin entrar todavía en páginas paginadas, newsletter ni fichas de aula.

Páginas objetivo:

```text
docs/comercio-electronico.html
docs/internacional.html
docs/digitalizacion.html
docs/ia-marketing.html
docs/aula.html
docs/del-autor.html
```

Schemas previstos:

```text
Organization
WebSite
CollectionPage
WebPage en Del Autor
```

Se mantiene fuera de este bloque:

```text
docs/newsletter/
docs/fichas-aula/
páginas paginadas -pN.html
```

La decisión técnica es seguir usando `schema_utils.py` como módulo común y ampliar `generar_seo.py` con una lista explícita de páginas principales. De esta forma evitamos que el JSON-LD se aplique accidentalmente a páginas que todavía no han sido analizadas.

Este bloque continúa el criterio de cambios pequeños, verificables y reversibles.
