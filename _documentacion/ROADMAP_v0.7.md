## Actualización · Cierre Bloque 4

### Bloque 4 · Schema básico global en portada

Estado: completado.

Acciones realizadas:

```text
- Creado `schema_utils.py` como módulo común para generar JSON-LD.
- Integrado `schema_utils.py` en `generar_seo.py`.
- Añadido JSON-LD en `docs/index.html`.
- Incorporados schemas básicos en portada:
  - `Organization`
  - `WebSite`
  - `CollectionPage`
- Mantenido `generar_seo.py` limitado a HTML de primer nivel en `docs/*.html`.
- No se han tocado subcarpetas `docs/newsletter/` ni `docs/fichas-aula/`.
- No se ha modificado la clasificación RA/CE.
- No se ha modificado `feeds.json`.
- No se ha cambiado la arquitectura del pipeline.
```

Validaciones realizadas:

```text
- Ejecutado `python .\run_pipeline.py` correctamente.
- Ejecutado `python .\generar_informe_pipeline.py` correctamente.
- Verificado visualmente que `docs/index.html` contiene un bloque `application/ld+json`.
- Comprobada la presencia de los tipos `Organization`, `WebSite` y `CollectionPage` en la portada generada.
```

Conclusión:

```text
La primera integración funcional de Schema.org queda validada.
La portada del agregador ya incorpora datos estructurados JSON-LD sin romper el SEO técnico existente ni el pipeline.
```

Observación detectada durante la validación:

```text
El informe mantiene una recomendación sobre revisión de fuentes sin aportación histórica.
Esta recomendación se considera una tarea de mantenimiento editorial/técnico de fuentes y no forma parte del alcance directo del Bloque 4 ni del objetivo principal de Schema.org.
```

Decisión:

```text
Aplazar la revisión de fuentes sin aportación histórica a una fase posterior o bloque independiente.
No mezclarla con la implementación de Schema.org para mantener la v0.7 acotada.
```

Siguiente paso propuesto:

```text
Bloque 4b · Extender Schema básico a páginas principales de primer nivel.
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

Quedan todavía fuera del siguiente paso:

```text
docs/newsletter/
docs/fichas-aula/
```

Motivo:

```text
Las subcarpetas requieren una revisión específica de canonical, sitemap, rutas relativas y tipo de schema antes de incorporarlas.
```
