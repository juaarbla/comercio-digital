# Actualización ROADMAP v0.7 · Bloque 4b

## Bloque 4b · Schema básico en páginas principales

Estado: preparado para implementación.

### Objetivo

Extender la integración de datos estructurados JSON-LD, iniciada en la portada, a las páginas principales de primer nivel del agregador.

Esta ampliación mantiene el enfoque controlado de la v0.7:

```text
no modifica la arquitectura del pipeline
no rediseña la web
no cambia feeds.json
no toca clasificación RA/CE
no procesa todavía subcarpetas
```

### Páginas incluidas

```text
docs/index.html
docs/comercio-electronico.html
docs/internacional.html
docs/digitalizacion.html
docs/ia-marketing.html
docs/aula.html
docs/del-autor.html
docs/otros.html si existe
docs/marketing.html si existe
```

### Páginas excluidas en este bloque

```text
docs/comercio-electronico-p*.html
docs/digitalizacion-p*.html
docs/ia-marketing-p*.html
docs/newsletter/
docs/fichas-aula/
```

Motivo:

```text
las páginas paginadas, newsletter y fichas requieren decisiones específicas sobre canonical, sitemap, rutas relativas y tipo de schema.
```

### Schemas aplicados

En portada:

```text
Organization
WebSite
CollectionPage
```

En páginas principales de sección y Aula:

```text
Organization
WebSite
CollectionPage
```

En Del Autor:

```text
Organization
WebSite
WebPage
```

### Archivos modificados

```text
schema_utils.py
generar_seo.py
```

### Cambios previstos en schema_utils.py

Se añade la función:

```python
def schema_pagina_principal_basico(title, description, url, page_type="CollectionPage"):
    ...
```

Esta función devuelve un conjunto de schemas compuesto por:

```text
Organization
WebSite
WebPage o CollectionPage
```

### Cambios previstos en generar_seo.py

Se añade un conjunto controlado de páginas principales:

```python
PAGINAS_SCHEMA_PRINCIPALES = {
    "index.html": "CollectionPage",
    "comercio-electronico.html": "CollectionPage",
    "internacional.html": "CollectionPage",
    "digitalizacion.html": "CollectionPage",
    "ia-marketing.html": "CollectionPage",
    "marketing.html": "CollectionPage",
    "aula.html": "CollectionPage",
    "del-autor.html": "WebPage",
    "otros.html": "CollectionPage",
}
```

También se añade una función auxiliar:

```python
def schema_para_html(nombre, title, description, canonical):
    ...
```

### Validación prevista

Ejecutar:

```powershell
python .\generar_seo.py
```

Verificar JSON-LD en portada:

```powershell
Select-String -Path .\docs\index.html -Pattern "application/ld+json","Organization","WebSite","CollectionPage"
```

Verificar JSON-LD en páginas principales:

```powershell
Select-String -Path .\docs\comercio-electronico.html -Pattern "application/ld+json","CollectionPage"
Select-String -Path .\docs\internacional.html -Pattern "application/ld+json","CollectionPage"
Select-String -Path .\docs\digitalizacion.html -Pattern "application/ld+json","CollectionPage"
Select-String -Path .\docs\ia-marketing.html -Pattern "application/ld+json","CollectionPage"
Select-String -Path .\docs\aula.html -Pattern "application/ld+json","CollectionPage"
Select-String -Path .\docs\del-autor.html -Pattern "application/ld+json","WebPage"
```

Comprobar que no se ha aplicado a paginadas:

```powershell
Select-String -Path .\docs\comercio-electronico-p2.html -Pattern "application/ld+json"
```

Resultado esperado:

```text
sin resultados en páginas paginadas
```

### Criterios de cierre del bloque

```text
- generar_seo.py ejecuta sin errores.
- docs/index.html mantiene Organization, WebSite y CollectionPage.
- páginas principales contienen JSON-LD básico.
- páginas paginadas no reciben JSON-LD todavía.
- newsletter y fichas quedan fuera del bloque.
- pipeline sigue ejecutable.
- repositorio queda limpio tras commit.
```
