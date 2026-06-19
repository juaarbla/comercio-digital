# Capa docente

La capa docente convierte cada noticia en un posible recurso de aula.

## Script principal

```text
enriquecer_docente.py
```

## Archivo principal de trabajo

```text
data/processed/noticias_clasificadas.json
```

## Campos añadidos

```json
{
  "score_docente": 25,
  "valor_docente": "alto",
  "tipo_uso": "actividad",
  "pregunta_aula": "...",
  "actividad_breve": "...",
  "conceptos_clave": ["..."],
  "generar_ficha": true,
  "seleccion_newsletter": true
}
```

## Uso recomendado

```powershell
python enriquecer_docente.py --forzar
```

## Criterios de uso

### Aula

Una noticia puede entrar en `aula.html` si:

```text
valor_docente = alto
o generar_ficha = true
o seleccion_newsletter = true
```

### Ficha docente

Una noticia genera ficha si:

```text
generar_ficha = true
```

o si cumple:

```text
valor_docente = alto
score_docente >= 25
tiene pregunta_aula
tiene actividad_breve
tiene ra_asignado
```

## Qué campos son internos

No se deben mostrar en la web pública:

```text
score_docente
valor_docente
seleccion_newsletter
```

Sí se pueden usar para:

- ordenar noticias;
- limitar selección;
- generar newsletter docente;
- decidir qué fichas crear;
- priorizar materiales de aula.


## Newsletter docente

La newsletter utiliza la capa docente como criterio de curación. Una noticia puede entrar en una edición si:

```text
seleccion_newsletter = true
```

o si tiene alto valor docente y cumple los criterios internos definidos por `generar_newsletter.py`.

La newsletter no muestra campos internos como `score_docente` o `seleccion_newsletter`; solo muestra información útil para el lector:

- título;
- resumen;
- módulo relacionado;
- tipo de uso;
- enlace a la noticia;
- enlace a ficha de aula si existe.

La generación se realiza con:

```powershell
python generar_newsletter.py --periodicidad quincenal --force
```

## Ejecución de prueba

```powershell
python enriquecer_docente.py --forzar --no-sobrescribir
python generar_aula.py --max-noticias 25
```

## Ejecución definitiva

```powershell
python enriquecer_docente.py --forzar
python generar_fichas_aula.py --max-fichas 10 --limpiar
python generar_aula.py --max-noticias 25
```

## Nota sobre Git

Los JSON de trabajo ya no están en la raíz del proyecto.

Ubicación actual:

```text
data/processed/noticias_resumidas.json
data/processed/noticias_clasificadas.json
```

Estos archivos son datos internos del agregador. No se publican en GitHub Pages porque la web pública se sirve desde:

```text
docs/
```

Decisión actual:

```text
data/processed/ no se ignora de momento.
```

Esto permite conservar una fotografía del estado procesado del agregador si se decide versionarlo.

Sí deben ignorarse:

```text
data/cache/
data/backups/
outputs/aula/
historial.json
.env
```
