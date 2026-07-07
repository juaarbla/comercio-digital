## v0.7 · SEO semántico y Schema.org · Cierre Bloque 4

Se ha completado y validado la primera integración funcional de datos estructurados Schema.org en el agregador.

### Trabajo realizado

```text
- Se ha creado `schema_utils.py` como módulo común para generar JSON-LD.
- Se ha integrado el módulo en `generar_seo.py`.
- Se ha añadido JSON-LD en la portada `docs/index.html`.
- La portada incorpora los schemas `Organization`, `WebSite` y `CollectionPage`.
```

### Validación

```text
- El pipeline se ha ejecutado correctamente con `python .\run_pipeline.py`.
- El informe se ha generado correctamente con `python .\generar_informe_pipeline.py`.
- Se ha comprobado que la portada contiene el bloque `application/ld+json`.
- El proyecto sigue ejecutable y estable.
```

### Decisiones tomadas

```text
- No se amplía todavía `generar_seo.py` a `docs/**/*.html`.
- No se modifican todavía newsletter ni fichas de aula.
- No se toca clasificación RA/CE.
- No se modifica `feeds.json`.
- La revisión de fuentes sin aportación histórica queda aplazada a una fase posterior de mantenimiento.
```

### Próximo paso

El siguiente paso será extender el schema básico a páginas principales de primer nivel mediante un bloque controlado:

```text
Bloque 4b · Schema básico en páginas principales
```

Páginas candidatas:

```text
docs/comercio-electronico.html
docs/internacional.html
docs/digitalizacion.html
docs/ia-marketing.html
docs/aula.html
docs/del-autor.html
```
