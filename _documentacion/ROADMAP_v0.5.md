# ROADMAP v0.5 — Control de calidad y seguimiento del agregador

## Estado de partida

La versión v0.5 se inicia después del cierre de las versiones v0.3 y v0.4.

Estado actual del proyecto:

* Repositorio limpio.
* Rama principal sincronizada con `origin/main`.
* Etiquetas existentes:

  * `v0.3`
  * `v0.4`
* Pipeline diario funcionando en Windows mediante Programador de tareas.
* Newsletter docente automatizada mediante BAT quincenal.
* Raspberry Pi pospuesta como mejora futura de infraestructura.
* Documentación técnica organizada en `_documentacion`.
* Logs existentes:

  * `logs/publicacion_diaria.log`
  * `logs/newsletter_quincenal.log`

## Objetivo general de la v0.5

La versión v0.5 tiene como objetivo mejorar el control de calidad, seguimiento y revisión editorial del agregador educativo automatizado.

No se plantea como una fase de rediseño ni de cambio estructural profundo, sino como una fase de observabilidad, seguridad editorial y mejora del mantenimiento.

## Líneas de trabajo

### 1. Informe post-pipeline

Crear un informe diario legible que se genere al finalizar el pipeline.

El informe deberá permitir revisar rápidamente:

* Si el pipeline ha finalizado correctamente.
* Cuántas noticias se han procesado.
* Cuántas noticias nuevas se han incorporado.
* Cuántas fichas de aula se han generado.
* Qué categorías han tenido más o menos presencia.
* Si hay noticias sin clasificación docente.
* Si hay errores o alertas relevantes.

Posible salida:

```text
logs/informe_pipeline_YYYY-MM-DD.md
```

Contenido orientativo:

```md
# Informe pipeline diario

## Resumen
- Noticias procesadas:
- Noticias nuevas:
- Noticias clasificadas:
- Fichas de aula generadas:
- Noticias candidatas a newsletter:
- Errores detectados:

## Distribución por categoría
- Comercio Electrónico:
- Digitalización:
- IA:
- Comercio Digital Internacional:
- Marketing Digital:

## Alertas
- Fuentes sin noticias:
- Categorías con baja presencia:
- Noticias sin RA:
- Noticias sin conceptos clave:
```

### 2. Mejora de logs

Revisar la estructura actual de logs para hacerla más clara y útil.

Situación actual:

```text
logs/
├── publicacion_diaria.log
└── newsletter_quincenal.log
```

Estructura deseable:

```text
logs/
├── publicacion_diaria.log
├── newsletter_quincenal.log
├── errores.log
├── historico_pipeline.csv
└── informe_pipeline_YYYY-MM-DD.md
```

El objetivo no es generar más ruido, sino facilitar la revisión del sistema.

### 3. Revisión de cambios antes de publicar

Incorporar una revisión sencilla de cambios generados antes de publicar en GitHub Pages.

Opciones posibles:

#### Opción A — Revisión manual con Git

Usar comandos como:

```powershell
git status
git diff --stat
```

#### Opción B — Crear un BAT de revisión

Crear un archivo:

```text
revisar_cambios.bat
```

Que muestre el estado del repositorio y el resumen de cambios antes de publicar.

#### Opción C — Publicación en dos pasos

Separar generación y publicación:

```text
actualizar_diario.bat
publicar_cambios.bat
```

En v0.5 se recomienda empezar por una revisión sencilla, sin romper la automatización actual.

### 4. Bloque “Última newsletter” en portada

Añadir en la portada del agregador un bloque visible pero discreto que enlace a la última newsletter docente.

Primera versión recomendada:

* Enlazar a `docs/newsletter/index.html`.
* Evitar, de momento, detectar automáticamente el último archivo HTML.
* Mantener el bloque integrado en el diseño actual de la portada.

Texto orientativo:

```text
Última newsletter docente

Consulta la última selección quincenal de noticias y recursos para trabajar en el aula.

Leer newsletter
```

### 5. Revisión de fuentes y equilibrio temático

Analizar si las fuentes actuales alimentan de forma equilibrada las áreas del proyecto:

* Comercio Electrónico
* Digitalización
* Inteligencia Artificial
* Comercio Digital Internacional
* Marketing Digital

Antes de modificar `feeds.json`, se recomienda generar primero un diagnóstico.

Posible informe:

```text
logs/informe_fuentes_YYYY-MM-DD.md
```

Contenido orientativo:

```md
# Informe de fuentes

## Distribución por categoría
- Comercio Electrónico:
- Digitalización:
- IA:
- Comercio Digital Internacional:
- Marketing Digital:

## Distribución por fuente
- Fuente 1:
- Fuente 2:
- Fuente 3:

## Alertas
- Fuentes sin noticias recientes.
- Categorías con poca presencia.
- Categorías sobrerrepresentadas.
```

## Qué entra en v0.5

Entran en esta versión:

* Informe post-pipeline.
* Mejora razonable de logs.
* Revisión de cambios antes de publicar.
* Bloque “Última newsletter” en portada.
* Diagnóstico de fuentes y equilibrio temático.
* Actualización de documentación.
* Cierre con etiqueta `v0.5`.

## Qué no entra en v0.5

Queda fuera de esta versión:

* Raspberry Pi.
* Rediseño completo de la web.
* Base de datos.
* Panel web de administración.
* Envío masivo de newsletter.
* Integración MCP avanzada.
* Reestructuración profunda del pipeline.
* Cambios grandes en la arquitectura del proyecto.

## Orden de trabajo

### Paso 1 — Documentar la hoja de ruta

Crear este documento y validarlo antes de tocar código.

### Paso 2 — Revisar el pipeline actual

Revisar:

* `run_pipeline.py`
* `publicar_web_diaria.bat`
* `generar_newsletter.py`
* `generar_web.py`
* `paths.py`
* carpeta `logs`

### Paso 3 — Diseñar el informe post-pipeline

Definir qué datos se pueden obtener ya con la estructura actual.

### Paso 4 — Implementar informe post-pipeline

Crear o adaptar el script necesario para generar el informe.

### Paso 5 — Mejorar logs

Separar información operativa, errores e histórico si procede.

### Paso 6 — Añadir revisión de cambios

Crear un mecanismo sencillo para revisar qué ha cambiado antes de publicar.

### Paso 7 — Añadir bloque “Última newsletter”

Incorporar en portada un enlace claro a la newsletter docente.

### Paso 8 — Diagnóstico de fuentes

Generar un primer informe de equilibrio temático y fuentes.

### Paso 9 — Actualizar documentación

Actualizar:

* `DIARIO_PROYECTO.md`
* `_documentacion/INDICE_DOCUMENTACION.md`
* documentación específica si se crea algún nuevo script o BAT.

### Paso 10 — Cierre v0.5

Comprobar:

```powershell
git status
```

Hacer commit:

```powershell
git add .
git commit -m "Cierre v0.5 control de calidad del agregador"
git push
```

Crear etiqueta:

```powershell
git tag v0.5
git push origin v0.5
```

## Criterios de cierre

La versión v0.5 se considerará cerrada cuando:

* El pipeline genere un informe diario legible.
* Los logs permitan detectar errores y revisar la ejecución.
* Exista un mecanismo sencillo de revisión antes de publicar.
* La portada muestre acceso a la última newsletter.
* Exista un primer diagnóstico de fuentes y categorías.
* La documentación esté actualizada.
* El repositorio esté limpio.
* La etiqueta `v0.5` esté creada y subida a GitHub.
