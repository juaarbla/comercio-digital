# Paso 1 — Capa docente v3

Esta versión corrige dos problemas detectados en las primeras pruebas:

1. Se marcaban demasiadas noticias como `valor_docente = alto`.
2. La selección para newsletter era demasiado amplia.

## Qué cambia

- Añade `score_docente`.
- Usa umbrales más exigentes.
- `seleccion_newsletter` se limita por defecto a 10 noticias.
- `generar_aula.py` permite limitar el número de noticias mostradas.
- El HTML muestra fuente, fecha, imagen, score, etiqueta de newsletter, RA, justificación, conceptos clave, pregunta para el aula y actividad breve.

## Prueba sin sobrescribir el JSON principal

```powershell
python enriquecer_docente.py --forzar --no-sobrescribir
python generar_aula.py --entrada noticias_clasificadas_v3.json --max-noticias 25
```

## Uso definitivo

```powershell
python enriquecer_docente.py --forzar
python generar_aula.py --max-noticias 25
```

## Ajuste de newsletter

```powershell
python enriquecer_docente.py --forzar --limite-newsletter 10
```

## Nota sobre Git

`noticias_clasificadas.json` es un archivo generado localmente y normalmente está ignorado por Git. Lo que debe publicarse es la salida de `docs/`.
