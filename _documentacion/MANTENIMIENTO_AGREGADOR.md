# Mantenimiento del agregador ComercioDigital.net

## 1. Objetivo del documento

Esta guia sirve para mantener el agregador sin romper el pipeline, combinando criterios tecnicos y editoriales. Esta pensada para el mantenimiento docente diario y para que Codex pueda intervenir con contexto claro.

El principio general es simple:

```text
Cambios pequenos, trazables y validados antes de publicar o cerrar version.
```

## 2. Estado actual del sistema

```text
v0.8 cerrada: fuentes y diversidad editorial.
v0.9 abierta: estabilizacion post-fuentes.
```

El informe post-pipeline de referencia es:

```text
logs/informe_pipeline_2026-07-09.md
```

Estado de referencia:

```text
Estado: AMARILLO
Alertas criticas: 0
Avisos: 4
Recomendaciones: 1
Fuentes configuradas: 22
Fuentes activas: 14
Fuentes inactivas: 8
```

AMARILLO sin alertas criticas significa que el sistema funciona, pero hay aspectos que conviene vigilar.

## 3. Ejecucion diaria normal

Comandos habituales en PowerShell:

```powershell
python .\run_pipeline.py
python .\generar_informe_pipeline.py
git status
```

Tambien existen scripts `.bat` en la raiz del proyecto:

```text
arrancar.bat
publicar_web_diaria.bat
generar_newsletter_quincenal.bat
generar_brief_podcast.bat
```

Usarlos solo cuando encajen con la tarea concreta. Para diagnostico fino, los comandos Python permiten ver mejor que ha ocurrido.

## 4. Revision del informe post-pipeline

Despues de generar el informe, revisar especialmente:

```text
- Estado general
- Alertas criticas
- Avisos
- Noticias nuevas de la ultima ejecucion
- Fuentes en la ultima ejecucion
- Noticias sin RA
- Noticias sin conceptos clave
- Fuentes activas sin aportacion
- Concentracion de ecommerce-news.es
```

El informe se guarda en `logs/` con fecha del dia.

## 5. Interpretacion de estados

```text
VERDE: sistema estable. No hay avisos relevantes.
AMARILLO: funciona, pero hay avisos revisables.
ROJO: hay alertas criticas o fallos que impiden confiar en la salida.
```

Un estado AMARILLO no bloquea por si solo. Lo importante es leer los avisos y decidir si son esperables o requieren accion.

## 6. Avisos normales

No todos los avisos implican error. Pueden ser aceptables temporalmente:

```text
- fuentes nuevas sin aportacion historica;
- fuentes institucionales de baja frecuencia;
- fuentes transversales como WordPress API;
- pocas noticias sin RA o sin conceptos clave;
- estado AMARILLO sin alertas criticas.
```

En v0.9 conviene observar varias ejecuciones antes de desactivar fuentes nuevas.

## 7. Avisos que requieren intervencion

Revisar con prioridad si aparece:

```text
- alertas criticas;
- muchas noticias sin RA;
- muchas noticias sin conceptos clave;
- una fuente activa devuelve HTML, captcha o error;
- una fuente domina casi toda la ultima ejecucion durante varios dias;
- caida de generacion de docs/index.html o docs/aula.html;
- newsletter vacia o con contenido poco util.
```

Si el problema afecta a publicacion web o a datos generados, validar antes de hacer commit.

## 8. Gestion de fuentes

Principio editorial:

```text
Solo incorporar fuentes con RSS, Atom o API estable.
No crear scraping HTML salvo decision futura muy justificada.
```

Criterios de decision:

```text
Aceptar:
- RSS valido;
- valor docente medio o alto;
- relacion clara con Comercio y Marketing;
- estabilidad tecnica.

Aceptar con filtros:
- fuente comercial pero util;
- contenido evergreen;
- posible ruido editorial.

Pendiente:
- valor editorial alto pero sin RSS.

Rechazar:
- sin RSS;
- captcha;
- bloqueo tecnico;
- contenido poco docente.
```

## 9. Como anadir una fuente nueva

Procedimiento recomendado:

```text
1. Verificar que el RSS/Atom/API responde y no es HTML.
2. Revisar titulos recientes y frecuencia.
3. Decidir modulo.
4. Anadir nota editorial en feeds.json.
5. Validar JSON.
6. Ejecutar el informe.
7. Observar 2 o 3 ejecuciones.
```

Validacion obligatoria:

```powershell
python -m json.tool feeds.json > $null
```

No anadir URLs HTML como si fueran fuentes RSS.

## 10. Como desactivar una fuente

No borrar una fuente salvo caso claro y documentado. Se prefiere:

```json
"activo": false,
"nota": "Motivo de desactivacion..."
```

Motivos habituales:

```text
- devuelve HTML o captcha;
- RSS roto o inestable;
- ruido editorial;
- baja utilidad docente;
- requiere scraping no previsto.
```

## 11. Fuentes en observacion post-v0.8

Observar durante varias ejecuciones:

```text
cyberclick.es
camara.es
thinkwithgoogle.com
es.semrush.com
prestashop.es
es.wordpress.org
consultoresia.com
casares.blog
ontsi.es
marketingdirecto.com
juanarmada.com WordPress API
```

Decision temporal: no anadir mas fuentes hasta tener 2 o 3 ejecuciones adicionales.

## 12. Calidad docente

Revisar en el informe:

```text
- noticias marcadas para ficha;
- noticias marcadas para newsletter;
- RA asignado;
- conceptos clave;
- actividad breve;
- valor docente;
- tipo de uso.
```

Pocas noticias sin RA o conceptos pueden ser aceptables. Si aumentan, revisar `clasificador_ra.py` o los datos de entrada antes de publicar.

## 13. Newsletter

No automatizar la newsletter a ciegas si hay ruido.

Antes de publicar, revisar:

```text
- seleccion de 10 noticias;
- diversidad de fuentes;
- valor docente;
- equilibrio entre CE, CDI, Digitalizacion e IA;
- ausencia de contenido patrocinado o demasiado comercial.
```

Comando relacionado:

```powershell
generar_newsletter_quincenal.bat
```

Usarlo cuando proceda generar la newsletter quincenal.

Salida complementaria para podcast:

```powershell
python .\generar_brief_newsletter.py --periodicidad quincenal
```

Tambien puede lanzarse con:

```powershell
generar_brief_podcast.bat
```

Este comando genera un brief Markdown en `outputs/podcast/` a partir de la misma seleccion editorial de la newsletter. No genera audio, no publica nada y debe revisarse manualmente antes de usarlo como entrada para `comercIAaliza.online`.

## 14. Fichas de aula

Las fichas deben tener utilidad docente clara.

Revisar:

```text
- actividad breve;
- pregunta de aula;
- RA y criterios;
- valor docente alto o medio;
- caso aplicable a FP Comercio y Marketing.
```

Una ficha sin actividad breve no deberia publicarse como material principal.

## 15. Checklist antes de commit

Antes de confirmar cambios:

```powershell
git status
python -m json.tool feeds.json > $null
git diff --stat
```

Si se ha ejecutado pipeline o cambiado diagnostico:

```powershell
python .\generar_informe_pipeline.py
```

Comprobar que no se han modificado archivos fuera de alcance.

## 16. Checklist de cierre de version

Solo etiquetar con `working tree clean`.

Comandos:

```powershell
git status
git log --oneline -5
git tag vX.Y
git push origin vX.Y
git ls-remote --tags origin
```

Antes de cerrar version:

```text
- feeds.json valido;
- informe generado;
- sin alertas criticas;
- documentacion actualizada;
- cambios subidos a GitHub;
- etiqueta creada y subida.
```

## 17. Criterios para v1.0

Considerar v1.0 cuando se cumplan estas condiciones:

```text
- varias ejecuciones sin alertas criticas;
- informes claros y accionables;
- fuentes nuevas observadas durante varias ejecuciones;
- baja incidencia de noticias sin RA o sin conceptos clave;
- documentacion de mantenimiento creada;
- pipeline reproducible;
- Git limpio;
- sitio publicado correctamente.
```

La prioridad para v1.0 no es crecer en numero de fuentes, sino confirmar estabilidad, calidad docente y mantenimiento sencillo.
