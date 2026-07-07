# ROADMAP v0.7 · Actualización Bloque 6

## Decisión previa · Article / NewsArticle

Estado: documentado.

Se decide no implementar `Article` ni `NewsArticle` sobre las noticias externas enlazadas por el agregador.

Motivo:

```text
Comercio Digital no es la fuente original de esas noticias.
El sitio actúa como agregador educativo, curador y generador de materiales docentes.
```

En su lugar, se prioriza:

```text
CollectionPage para páginas de listado
ItemList si más adelante se enriquecen listados
LearningResource para fichas de aula
```

---

## Bloque 6 · Schema educativo para fichas de aula

Estado: preparado para implementación.

### Objetivo

Añadir datos estructurados JSON-LD a las fichas docentes generadas en:

```text
docs/fichas-aula/*.html
```

### Tipo Schema principal

```text
LearningResource
```

### Justificación

Las fichas de aula sí son contenido educativo propio generado por el proyecto. Por tanto, es más adecuado describirlas como recursos de aprendizaje que marcar las noticias externas como artículos propios.

### Archivos implicados

```text
schema_utils.py
generar_fichas_aula.py
docs/fichas-aula/*.html
```

### Cambios previstos

En `schema_utils.py`:

```text
- Añadir schema_learning_resource()
- Añadir schema_ficha_aula_basico()
```

En `generar_fichas_aula.py`:

```text
- Importar insertar_jsonld y schema_ficha_aula_basico
- Pasar el nombre del HTML generado a render_html()
- Insertar JSON-LD antes de </head> en cada ficha
```

### Datos usados en LearningResource

```text
titulo
resumen
url de ficha
módulo relacionado
RA asignado
RA texto si existe
tipo de uso
actividad breve
pregunta detonadora
conceptos clave
fuente original como isBasedOn
nivel educativo: Formación Profesional
```

### Fuera de alcance en este bloque

```text
newsletter
sitemap recursivo
canonical en subcarpetas
Open Graph en fichas
NewsArticle
Article para noticias externas
```

### Validación

Ejecutar:

```powershell
python .\generar_fichas_aula.py
```

Comprobar:

```powershell
Select-String -Path .\docs\fichas-aula\*.html -Pattern "application/ld+json","LearningResource"
```

Comprobar una ficha concreta:

```powershell
Select-String -Path .\docs\fichas-aula\001*.html -Pattern "LearningResource","educationalLevel","learningResourceType","isBasedOn"
```

Resultado esperado:

```text
Cada ficha HTML contiene un bloque JSON-LD con LearningResource.
No se modifican newsletter ni páginas paginadas.
```
