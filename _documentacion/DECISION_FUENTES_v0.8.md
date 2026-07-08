# Decisión inicial v0.8 · Revisión de fuentes

## Decisión

La v0.8 se dedicará a revisar fuentes, diversidad y aportación editorial.

No se abordarán cambios visuales ni nuevos datos estructurados.

## Motivo

El informe post-pipeline mantiene el sistema en estado AMARILLO, sin alertas críticas, pero con avisos relacionados con:

```text
- concentración de ecommerce-news.es;
- fuentes activas sin aportación histórica;
- fuentes activas sin aportación en la última ejecución;
- algunas noticias sin RA o conceptos clave.
```

Estos avisos no son errores técnicos críticos, pero sí afectan a la calidad editorial del agregador.

## Principios de trabajo

```text
1. No borrar fuentes sin documentar.
2. Preferir activo:false + nota antes que eliminar.
3. Separar fallo técnico de baja frecuencia editorial.
4. Mantener fuentes transversales solo si tienen sentido docente.
5. No mezclar revisión de fuentes con cambios grandes de clasificación.
6. Validar siempre con pipeline e informe post-pipeline.
```

## Estados posibles por fuente

```text
mantener
mantener con nota
corregir URL/configuración
asignar módulo
mantener como transversal
desactivar temporalmente
sustituir
```

## Primer foco

Revisar estas fuentes activas sin aportación histórica:

```text
taric.es/noticias
prestotimes.com
prestashop.es/blog
ontsi.es/es/rss.xml
marketing4ecommerce.net/ecommerce/feed
wordpress_api
es.wordpress.org/news
cyberclick.es/numerical-blog
consultoresia.com/inteligencia-artificial
casares.blog
```

## Resultado esperado

Un `feeds.json` más claro, con fuentes activas justificadas, fuentes inactivas documentadas y menor ruido en los informes.
