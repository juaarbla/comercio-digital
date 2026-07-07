# Decisión v0.7 · No usar Article/NewsArticle para noticias externas

## Contexto

Durante la fase v0.7 se valoró añadir Schema.org de tipo `Article` o `NewsArticle` a las noticias mostradas por el agregador.

## Decisión

Se decide **no marcar las noticias enlazadas como `NewsArticle` ni como `Article` propio** en esta fase.

## Motivo

El sitio `comerciodigital.net` no publica la noticia completa ni actúa como fuente original de esas noticias.

El agregador realiza:

- selección;
- curación;
- resumen;
- clasificación educativa;
- vinculación con módulos, RA y CE;
- propuesta de uso en el aula;
- enlace a la fuente original.

Por tanto, describir cada noticia externa como `NewsArticle` propio podría generar ambigüedad sobre autoría, publicación y entidad responsable del contenido original.

## Enfoque adoptado

Se mantiene el enfoque semántico ya implementado:

- `WebSite` para el sitio;
- `Organization` para el proyecto;
- `CollectionPage` para portada, secciones y Aula;
- `WebPage` para Del autor.

Para noticias externas se prioriza, si se aborda más adelante, un enfoque de listado:

- `ItemList`;
- `ListItem`;
- `name`;
- `url`;
- `description`;
- `position`.

## Alternativa priorizada

Se prioriza el schema educativo en fichas de aula, ya que ahí sí existe contenido educativo propio generado por el proyecto.

El siguiente bloque pasa a ser:

```text
Bloque 6 · Schema educativo para fichas de aula
```

## Estado

Decisión documentada.
