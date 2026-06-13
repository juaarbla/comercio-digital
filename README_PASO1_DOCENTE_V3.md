# Paso 1 — Capa docente v3

Esta versión corrige dos problemas detectados en la v2:

1. Seguía marcando demasiadas noticias como `valor_docente = alto`.
2. La newsletter seguía siendo demasiado amplia.

## Qué cambia

- Añade `score_docente`.
- Usa umbrales más exigentes.
- `seleccion_newsletter` se limita por defecto a 10 noticias.
- `generar_aula.py` muestra como máximo 40 noticias por defecto.
- El HTML muestra:
  - fuente
  - fecha
  - imagen
  - score
  - etiqueta de newsletter
  - actividad breve

## Prueba recomendada

```powershell
python enriquecer_docente.py --forzar --no-sobrescribir
```

Ojo: el archivo generado se llamará:

```text
noticias_clasificadas_v3.json
```

No `noticias_clasificadas_docente_v3.json`.

Después:

```powershell
python generar_aula.py --entrada noticias_clasificadas_v3.json
```

## Si quieres limitar más la página de aula

```powershell
python generar_aula.py --entrada noticias_clasificadas_v3.json --max-noticias 25
```

## Si te gusta el resultado definitivo

```powershell
python enriquecer_docente.py --forzar
python generar_aula.py
```

## Ajuste de newsletter

Por defecto selecciona 10 noticias:

```powershell
python enriquecer_docente.py --forzar --limite-newsletter 10
```

También puedes probar con 5:

```powershell
python enriquecer_docente.py --forzar --no-sobrescribir --limite-newsletter 5
```
