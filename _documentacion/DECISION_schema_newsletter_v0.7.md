# Decisión v0.7 · Schema para newsletter

## Decisión

La newsletter se marcará con Schema.org como colección editorial de enlaces seleccionados.

Schemas elegidos:

```text
CollectionPage
ItemList
ListItem
```

## Motivo

La newsletter de Comercio Digital no republica noticias completas. Su función es:

```text
seleccionar noticias
ordenarlas editorialmente
resumirlas
relacionarlas con módulos y uso docente
enlazar a las fuentes originales
```

Por tanto, se mantiene la misma lógica aplicada a las noticias externas:

```text
No usar NewsArticle
No usar Article para contenidos externos
```

## Aplicación

Se añade JSON-LD en:

```text
docs/newsletter/index.html
docs/newsletter/newsletter-*.html
```

## Fuera de alcance

```text
canonical en subcarpetas
sitemap recursivo
Open Graph específico para newsletter
IndexNow
automatización de envío a buscadores
```

## Estado

Decisión preparada para aplicar en el Bloque 7.
