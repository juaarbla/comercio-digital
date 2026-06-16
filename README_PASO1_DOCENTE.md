# Capa docente

La capa docente convierte cada noticia en un posible recurso de aula.

## Script principal

```text
enriquecer_docente.py
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
- generar newsletter;
- decidir qué fichas crear;
- priorizar materiales de aula.

## Ejecución de prueba

```powershell
python enriquecer_docente.py --forzar --no-sobrescribir
python generar_aula.py --entrada noticias_clasificadas_v3.json --max-noticias 25
```

## Ejecución definitiva

```powershell
python enriquecer_docente.py --forzar
python generar_fichas_aula.py --max-fichas 10 --limpiar
python generar_aula.py --max-noticias 25
```

## Nota sobre Git

`noticias_clasificadas.json` es un archivo generado localmente y normalmente debe estar ignorado por Git. Lo que se publica es la salida estática en `docs/`.
