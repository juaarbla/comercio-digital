# Aula y fichas docentes

La página `docs/aula.html` es la parte docente del agregador. Su objetivo es convertir la actualidad en recursos rápidos para trabajar en clase.

## Qué muestra Aula

Cada noticia seleccionada puede mostrar:

- módulo relacionado;
- resultado de aprendizaje;
- tipo de uso;
- resumen;
- fuente;
- pregunta detonadora;
- actividad breve;
- conceptos clave;
- justificación de encaje con el RA;
- enlace a ficha docente HTML;
- enlace a ficha Markdown;
- enlace a la noticia original.

## Qué no debe mostrar

Los siguientes campos son internos:

```text
score_docente
valor_docente
seleccion_newsletter
```

Pueden usarse para ordenar, filtrar y seleccionar, pero no deben aparecer en la interfaz pública.

## Criterio para entrar en Aula

Una noticia entra en `aula.html` si cumple alguno de estos criterios:

```text
valor_docente = alto
generar_ficha = true
seleccion_newsletter = true
```

La página se genera con:

```powershell
python generar_aula.py --max-noticias 25
```

## Fichas docentes públicas

Las fichas públicas se generan antes que Aula:

```powershell
python generar_fichas_aula.py --max-fichas 10 --limpiar
```

Genera:

```text
docs/fichas-aula/001-titulo.html
docs/fichas-aula/001-titulo.md
docs/fichas-aula/material-aula.md
docs/fichas-aula/index_fichas.json
```

`index_fichas.json` permite que `aula.html` sepa qué noticias tienen ficha y muestre los enlaces:

```text
Ver ficha docente →
Descargar Markdown →
```

## Material conjunto

`material-aula.md` agrupa varias fichas docentes en un único Markdown reutilizable.

Uso previsto:

- Aules/Moodle;
- preparación de clase;
- banco de actividades;
- material para Tutor IA/RAG;
- revisión semanal de actualidad.

## Fichas generadas por MCP

Además de las fichas públicas generadas por `generar_fichas_aula.py`, el servidor MCP puede generar fichas Markdown de trabajo mediante la herramienta:

```text
generar_ficha_md(url_o_titulo)
```

Estas fichas se guardan en:

```text
outputs/aula/
```

Diferencia importante:

```text
docs/fichas-aula/  → fichas públicas generadas por el pipeline
outputs/aula/      → fichas locales de trabajo generadas desde MCP
```

Las fichas de `outputs/aula/` no se publican automáticamente.

## Orden correcto de generación

```powershell
python generar_fichas_aula.py --max-fichas 10 --limpiar
python generar_aula.py --max-noticias 25
python generar_newsletter.py --periodicidad quincenal --force
python generar_seo.py
```


## Relación con la newsletter

La newsletter es una salida complementaria a Aula y fichas docentes.

```text
Aula                 → banco de noticias útiles para clase
Fichas docentes      → material individual reutilizable
Newsletter           → selección periódica para compartir
```

`generar_newsletter.py` puede utilizar noticias marcadas con:

```text
seleccion_newsletter = true
valor_docente = alto
```

La newsletter enlaza, cuando existe, con las fichas generadas en:

```text
docs/fichas-aula/
```

Por eso se recomienda generar primero las fichas y después la newsletter.

## Comprobaciones

```powershell
Select-String -Path docs\aula.html -Pattern "Ficha docente"
Select-String -Path docs\aula.html -Pattern "Descargar Markdown"
Select-String -Path docs\aula.html -Pattern "Descargar material de aula MD"
Test-Path docs\fichas-aula\material-aula.md
```

## Estilos

`aula.html` debe enlazar con:

```html
<link rel="stylesheet" href="assets/style.css">
```

No debe tener un bloque `<style>` incrustado.
