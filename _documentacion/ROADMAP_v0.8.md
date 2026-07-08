# ROADMAP v0.8 · Revisión de fuentes, diversidad y aportación editorial

## Estado inicial

La v0.8 parte del informe post-pipeline del **2026-07-08**.

Estado general detectado:

```text
Estado: AMARILLO
Alertas críticas: 0
Avisos: 5
Recomendaciones: 1
```

Resumen operativo:

```text
Noticias resumidas: 282
Noticias clasificadas: 282
Fuentes configuradas: 19
Fuentes activas: 14
Fuentes inactivas: 5
Fichas HTML generadas: 10
Fichas MD generadas: 10
Newsletters HTML disponibles: 2
Newsletters MD disponibles: 2
```

## Objetivo de la v0.8

Mejorar la calidad, diversidad y utilidad editorial de las fuentes del agregador sin rediseñar la web ni modificar la arquitectura principal del pipeline.

La fase se centra en:

```text
- revisar fuentes activas sin aportación histórica;
- reducir dependencia excesiva de una sola fuente;
- distinguir fuentes mal configuradas de fuentes simplemente poco frecuentes;
- mejorar la trazabilidad de fuentes transversales;
- documentar decisiones editoriales sobre activar, mantener, corregir o desactivar fuentes.
```

## Fuera de alcance

```text
- Rediseño visual.
- Nuevos schemas.
- Cambios en GitHub Pages.
- Envío automático de newsletter.
- Automatización IndexNow.
- Cambios grandes en el clasificador RA.
- Sustitución completa de fuentes.
```

## Diagnóstico inicial

### Concentración de fuente principal

```text
ecommerce-news.es concentra el 73.8% del histórico clasificado.
ecommerce-news.es concentra el 91.3% de la última ejecución detectada.
```

Lectura:

```text
La fuente funciona bien y aporta volumen, pero el agregador queda demasiado condicionado por una sola fuente.
```

### Fuentes activas sin aportación histórica

```text
Fuentes activas sin aportación histórica: 10
```

| Fuente | Clave | Módulo |
|---|---|---|
| taric.es/noticias | `taric.es` | (vacío) |
| prestotimes.com | `prestotimes.com` | IA para Marketing y Comercio |
| prestashop.es/blog | `prestashop.es` | PrestaShop |
| ontsi.es/es/rss.xml | `ontsi.es` | Digitalización GS |
| marketing4ecommerce.net/ecommerce/feed | `marketing4ecommerce.net` | Comercio Electrónico |
| juanarmada.com · WordPress API | `wordpress_api` | (vacío) |
| es.wordpress.org/news | `es.wordpress.org` | WordPress |
| cyberclick.es/numerical-blog | `cyberclick.es` | (vacío) |
| consultoresia.com/inteligencia-artificial | `consultoresia.com` | IA para Marketing y Comercio |
| casares.blog | `casares.blog` | (vacío) |

### Fuentes activas sin módulo declarado

Según `feeds.json`, hay 4 fuentes activas sin módulo declarado:

- https://juanarmada.com/wp-json/wp/v2/posts?per_page=20&orderby=date&order=desc&_fields=id,link,date,date_gmt,title,excerpt,content,categories
- https://www.taric.es/noticias/
- https://casares.blog/
- https://www.cyberclick.es/numerical-blog

Estas fuentes pueden ser transversales, pero conviene documentar su papel para evitar ambigüedad editorial.

## Bloques de trabajo

### Bloque 1 · Auditoría de fuentes activas

Objetivo:

```text
Revisar las 14 fuentes activas y clasificarlas según su estado real.
```

Clasificación propuesta:

```text
A · Mantener sin cambios
B · Mantener pero corregir configuración
C · Mantener como fuente transversal/de observación
D · Desactivar temporalmente
E · Sustituir por una fuente mejor
```

Resultado esperado:

```text
_documentacion/AUDITORIA_FUENTES_v0.8.md
```

### Bloque 2 · Diagnóstico técnico de fuentes sin aportación

Objetivo:

```text
Distinguir fuentes que no aportan porque están mal configuradas de fuentes que simplemente no han generado noticias nuevas.
```

Acciones:

```text
- revisar si cada URL es RSS real, HTML, API o página de listado;
- comprobar si el agregador actual puede leerla;
- marcar fuentes que requieren parser específico;
- evitar falsas alertas para fuentes de baja frecuencia.
```

Resultado esperado:

```text
_documentacion/DIAGNOSTICO_TECNICO_FUENTES_v0.8.md
```

### Bloque 3 · Decisión editorial por fuente

Objetivo:

```text
Tomar una decisión explícita sobre cada fuente sin aportación histórica.
```

Decisiones posibles:

```text
mantener
corregir
desactivar
sustituir
observar
```

Resultado esperado:

```text
_documentacion/DECISION_FUENTES_v0.8.md
```

### Bloque 4 · Ajustes controlados en feeds.json

Objetivo:

```text
Aplicar solo los cambios acordados en feeds.json.
```

Reglas:

```text
- No eliminar fuentes directamente.
- Preferir activo:false + nota antes que borrar.
- Añadir módulo cuando tenga sentido.
- Añadir nota editorial a fuentes transversales.
- Mantener trazabilidad de por qué se cambia cada fuente.
```

### Bloque 5 · Informe post-ajustes

Objetivo:

```text
Ejecutar pipeline y comparar indicadores antes/después.
```

Comandos:

```powershell
python .\run_pipeline.py
python .\generar_informe_pipeline.py
```

Indicadores a comparar:

```text
- fuentes activas;
- fuentes inactivas;
- fuentes activas sin aportación histórica;
- fuentes activas sin aportación en última ejecución;
- concentración de ecommerce-news.es;
- noticias sin RA;
- noticias sin conceptos clave.
```

### Bloque 6 · Cierre v0.8

Objetivo:

```text
Documentar el cierre de la fase y decidir si los avisos restantes son bloqueantes o no.
```

## Criterios de éxito

```text
✅ Todas las fuentes activas tienen una decisión editorial documentada.
✅ Las fuentes sin módulo declarado quedan justificadas o corregidas.
✅ Las fuentes sin aportación histórica quedan clasificadas.
✅ feeds.json queda más claro y trazable.
✅ El pipeline sigue funcionando.
✅ El informe post-pipeline no presenta alertas críticas.
✅ La revisión de fuentes queda separada de futuras mejoras de clasificación.
```

## Decisión inicial recomendada

No hacer cambios masivos. La primera acción debe ser una auditoría documentada.

Prioridad inicial:

```text
1. Revisar fuentes activas sin aportación histórica.
2. Identificar cuáles no son RSS reales.
3. Añadir notas editoriales.
4. Desactivar temporalmente solo las claramente problemáticas.
```
