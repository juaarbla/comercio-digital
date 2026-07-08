# Decision de fuentes v0.8

## Decision general

La v0.8 se mantiene centrada en fuentes, diversidad y aportacion editorial.

No se abordan en este bloque:

```text
- rediseno visual;
- cambios en Schema.org;
- cambios en el pipeline principal;
- sustitucion masiva de fuentes;
- modificacion de feeds.json sin aprobacion expresa.
```

## Principio aplicado

Antes de cambiar configuracion, se documenta cada decision. Las fuentes que no aportan se separan en tres grupos:

```text
1. fuentes bien configuradas pero de baja frecuencia;
2. fuentes mal configuradas como HTML en lugar de RSS/API;
3. fuentes no fiables para el pipeline por captcha, bloqueo o ausencia de feed claro.
```

## Decision por fuente activa

| Fuente | Decision | Accion recomendada | Justificacion |
|---|---|---|---|
| `juanarmada.com/podcast/feed` | A - Mantener sin cambios | Mantener activa. | RSS valido, fuente propia y aporta identidad editorial. |
| `juanarmada.com/wp-json/wp/v2/posts` | B - Mantener pero corregir configuracion | Mantener activa y revisar trazabilidad de `source`. | La API funciona y contiene posts recientes, pero el informe la cuenta como 0 por clave `wordpress_api`; las noticias se detectan como `juanarmada.com`. |
| `ecommerce-news.es/feed` | A - Mantener sin cambios | Mantener activa. | Fuente estable y productiva. Su concentracion aconseja equilibrar, no desactivar. |
| `marketing4ecommerce.net/ecommerce/feed` | D - Desactivar temporalmente | Pasar a `activo:false` con nota, salvo que se encuentre una URL RSS sin captcha. | La comprobacion devuelve HTML anti-bot; el pipeline no puede procesarla como feed fiable. |
| `marketingdirecto.com/feed` | C - Mantener como observacion | Mantener temporalmente y monitorizar. | Tiene aportacion historica, aunque la comprobacion viva devuelve anti-bot. No desactivar sin observar otra ejecucion. |
| `ontsi.es/es/rss.xml` | C - Mantener como observacion | Mantener activa con nota editorial de baja frecuencia. | RSS valido. Puede aportar indicadores institucionales utiles aunque no haya aportado al historico reciente. |
| `taric.es/noticias/` | E - Sustituir por fuente mejor | Buscar alternativa RSS sobre comercio internacional/aduanas o crear parser especifico solo si compensa. | La URL es HTML y no se ha localizado feed alternativo claro. |
| `es.wordpress.org/news/` | B - Mantener pero corregir configuracion | Cambiar a `https://es.wordpress.org/news/feed/`. | La URL actual es HTML; el feed alternativo es RSS valido. |
| `casares.blog/` | B - Mantener pero corregir configuracion | Cambiar a `https://casares.blog/feed/`. | La URL actual es HTML; el feed alternativo es RSS valido y frecuente. |
| `prestashop.es/blog` | B - Mantener pero corregir configuracion | Cambiar a `https://prestashop.es/blog/feed.xml`. | La URL actual es HTML; el feed XML alternativo existe y contiene entradas recientes. |
| `prestotimes.com` | D - Desactivar temporalmente | Pasar a `activo:false` con nota. | Devuelve HTML anti-bot; no es fiable para el pipeline actual. |
| `consultoresia.com/inteligencia-artificial/` | B - Mantener pero corregir configuracion | Cambiar a `https://consultoresia.com/inteligencia-artificial/feed/`. | La URL actual es HTML; el feed alternativo es RSS valido. |
| `blog.hubspot.es/marketing/rss.xml` | A - Mantener sin cambios | Mantener activa. | RSS valido, contenido evergreen y aportacion historica aunque no diaria. |
| `cyberclick.es/numerical-blog` | B - Mantener pero corregir configuracion | Cambiar a `https://www.cyberclick.es/numerical-blog/rss.xml`. | La URL actual es HTML; el feed alternativo es RSS valido con entradas recientes. |

## Cambios candidatos para feeds.json

No aplicados todavia.

Cuando se autorice modificar `feeds.json`, se recomienda:

```text
- es.wordpress.org/news/ -> es.wordpress.org/news/feed/
- casares.blog/ -> casares.blog/feed/
- prestashop.es/blog -> prestashop.es/blog/feed.xml
- consultoresia.com/inteligencia-artificial/ -> consultoresia.com/inteligencia-artificial/feed/
- www.cyberclick.es/numerical-blog -> www.cyberclick.es/numerical-blog/rss.xml
- marketing4ecommerce.net/ecommerce/feed -> activo:false + nota por captcha/anti-bot
- prestotimes.com -> activo:false + nota por captcha/anti-bot
- taric.es/noticias/ -> activo:false + nota o sustitucion documentada
```

## Fuentes transversales

Fuentes activas sin modulo declarado:

```text
juanarmada.com WordPress API
taric.es/noticias
casares.blog
cyberclick.es/numerical-blog
```

Decision editorial:

```text
- Juan Armada WordPress API puede seguir transversal porque el modulo se infiere desde categorias.
- Casares puede mantenerse como observacion WordPress/tecnologia si se corrige a RSS.
- Cyberclick deberia declararse como Marketing Digital si se corrige a RSS.
- Taric no deberia seguir como transversal activa si no hay feed o parser.
```

## Riesgos

```text
- Corregir varias fuentes a la vez puede aumentar volumen de noticias y coste LLM.
- Algunas fuentes RSS pueden traer contenido evergreen no siempre reciente.
- Las fuentes anti-bot pueden funcionar de forma intermitente, por lo que conviene documentar la fecha de comprobacion.
- El cruce de WordPress API en el informe puede seguir dando falso cero si no se ajusta la clave de fuente.
```

## Validacion requerida antes de commit

Cuando se apliquen cambios de configuracion:

```powershell
python .\run_pipeline.py
python .\generar_informe_pipeline.py
```

Indicadores a comparar:

```text
- fuentes activas;
- fuentes inactivas;
- fuentes activas sin aportacion historica;
- fuentes activas sin aportacion en ultima ejecucion;
- concentracion de ecommerce-news.es;
- noticias sin RA;
- noticias sin conceptos clave.
```

## Cierre del bloque 1

El bloque 1 queda documentado como auditoria y decision previa. La conclusion principal es que la baja diversidad no se debe solo a falta de fuentes, sino a varias fuentes activas configuradas como paginas HTML o bloqueadas por anti-bot.

La accion siguiente natural es pedir autorizacion para aplicar un ajuste controlado en `feeds.json`.
