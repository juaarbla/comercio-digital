# Capa docente

La capa docente convierte cada noticia clasificada en un posible recurso de aula. Añade criterios didácticos, prioriza noticias útiles y prepara los datos que después usan Aula, fichas y newsletter.

## Script principal

```text
enriquecer_docente.py
```

## Archivo de trabajo

```text
data/processed/noticias_clasificadas.json
```

El script lee y actualiza este archivo.

## Campos añadidos

Ejemplo de campos docentes añadidos a cada noticia:

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

Para pruebas conservadoras:

```powershell
python enriquecer_docente.py --forzar --no-sobrescribir
```

## Criterios de uso

### Aula

Una noticia puede aparecer en `docs/aula.html` si cumple alguno de estos criterios:

```text
valor_docente = alto
generar_ficha = true
seleccion_newsletter = true
```

### Ficha docente

Una noticia puede generar ficha si:

```text
generar_ficha = true
```

o si cumple criterios de calidad didáctica suficientes:

```text
valor_docente = alto
score_docente >= 25
tiene pregunta_aula
tiene actividad_breve
tiene ra_asignado
```

### Newsletter

Una noticia puede entrar en la newsletter si:

```text
seleccion_newsletter = true
```

También pueden priorizarse noticias con alto valor docente, buena actividad breve y relación clara con módulo/RA.

## Campos internos

No se deben mostrar en la web pública:

```text
score_docente
valor_docente
seleccion_newsletter
```

Estos campos sirven para:

- ordenar noticias;
- limitar selección;
- decidir fichas;
- preparar newsletter;
- priorizar recursos para clase.

## Campos visibles recomendados

Sí pueden mostrarse en Aula, fichas y newsletter:

```text
módulo relacionado
resultado de aprendizaje
tipo de uso
pregunta_aula
actividad_breve
conceptos_clave
justificación curricular
resumen
enlace original
```

## Ejecución completa relacionada

```powershell
python enriquecer_docente.py --forzar
python imagen_destacada.py
python generar_fichas_aula.py --max-fichas 10 --limpiar
python generar_aula.py --max-noticias 25
python generar_newsletter.py --periodicidad quincenal --force
python generar_seo.py
```

## Nota sobre Git

Los datos procesados están en:

```text
data/processed/noticias_resumidas.json
data/processed/noticias_clasificadas.json
```

No se publican en GitHub Pages porque la web pública se sirve desde:

```text
docs/
```

Decisión actual:

```text
data/processed/ no se ignora de momento.
```

Sí conviene ignorar:

```text
data/cache/
data/backups/
outputs/aula/
historial.json
.env
```
