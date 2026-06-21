# Aula y fichas docentes

La página `docs/aula.html` es la parte docente del agregador. Convierte noticias de actualidad en recursos rápidos para trabajar en clase en módulos de FP de Comercio y Marketing.

## Objetivo

Aula no es una página de noticias general. Su función es seleccionar noticias con valor didáctico y mostrarlas con información útil para el profesorado:

- módulo relacionado;
- resultado de aprendizaje;
- tipo de uso en clase;
- resumen;
- fuente;
- pregunta detonadora;
- actividad breve;
- conceptos clave;
- justificación curricular;
- enlace a la noticia original;
- enlace a ficha docente HTML;
- enlace a ficha Markdown.

## Archivos implicados

```text
generar_fichas_aula.py      → genera fichas HTML/Markdown
generar_aula.py             → genera docs/aula.html
docs/aula.html              → página pública de Aula
docs/fichas-aula/           → fichas públicas
docs/fichas-aula/index_fichas.json
docs/fichas-aula/material-aula.md
```

## Orden correcto de generación

Las fichas deben generarse antes que `aula.html`, porque Aula necesita saber qué noticias tienen ficha asociada.

```powershell
python generar_fichas_aula.py --max-fichas 10 --limpiar
python generar_aula.py --max-noticias 25
python generar_newsletter.py --periodicidad quincenal --force
python generar_seo.py
```

## Criterio para entrar en Aula

Una noticia puede entrar en `docs/aula.html` si cumple alguno de estos criterios:

```text
valor_docente = alto
generar_ficha = true
seleccion_newsletter = true
```

La selección final se limita con:

```powershell
python generar_aula.py --max-noticias 25
```

## Fichas docentes públicas

`generar_fichas_aula.py` crea fichas individuales en HTML y Markdown.

```text
docs/fichas-aula/001-titulo-noticia.html
docs/fichas-aula/001-titulo-noticia.md
docs/fichas-aula/material-aula.md
docs/fichas-aula/index_fichas.json
```

Uso de cada archivo:

| Archivo | Uso |
|---|---|
| `.html` | Ficha pública navegable desde la web. |
| `.md` | Material reutilizable en Aules/Moodle, Tutor IA o preparación docente. |
| `material-aula.md` | Recopilación conjunta de varias fichas. |
| `index_fichas.json` | Índice técnico para enlazar Aula con las fichas. |

## Material conjunto

`material-aula.md` agrupa varias fichas docentes en un único Markdown reutilizable.

Usos previstos:

- preparar una sesión de actualidad;
- copiar actividades a Aules/Moodle;
- alimentar Tutor IA/RAG;
- revisar semanal o quincenalmente noticias con valor docente.

## Campos internos que no deben mostrarse

Estos campos se usan para ordenar, filtrar o seleccionar, pero no deben aparecer en la interfaz pública:

```text
score_docente
valor_docente
seleccion_newsletter
```

Sí pueden utilizarse internamente para:

- ordenar noticias;
- limitar la selección;
- decidir qué fichas crear;
- preparar la newsletter;
- priorizar materiales de aula.

## Diferencia entre fichas públicas y fichas MCP

```text
docs/fichas-aula/  → fichas públicas generadas por el pipeline
outputs/aula/      → fichas locales de trabajo generadas desde MCP
```

Las fichas de `outputs/aula/` no se publican automáticamente y se recomienda ignorarlas en Git.

## Relación con la newsletter

La newsletter es una salida complementaria:

```text
Aula            → banco de noticias útiles para clase
Fichas docentes → material individual reutilizable
Newsletter      → selección periódica para compartir
```

Cuando existe una ficha docente, la newsletter puede enlazar a `docs/fichas-aula/`.

## Comprobaciones rápidas

```powershell
Test-Path docs\aula.html
Test-Path docs\fichas-aula\material-aula.md
Select-String -Path docs\aula.html -Pattern "Ficha docente"
Select-String -Path docs\aula.html -Pattern "Descargar Markdown"
Select-String -Path docs\aula.html -Pattern "Descargar material de aula MD"
```

## Estilos

`aula.html` debe usar la hoja de estilos común:

```html
<link rel="stylesheet" href="assets/style.css">
```

No conviene mantener estilos incrustados en la página.
