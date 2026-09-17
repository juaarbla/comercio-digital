# De la noticia a la oportunidad

Sección quincenal para Comercio Electrónico y Comercio Digital Internacional.
La noticia procede exclusivamente de `data/processed/noticias_clasificadas.json`.

## Flujo

1. `generar_newsletter.py` prepara, además de la newsletter, un caso privado
   para la quincena. No modifica los tres archivos esperados por el lanzador.
2. La preselección considera noticias de los últimos 30 días (fecha de publicación,
   nunca fecha de procesamiento), valor docente, necesidades comerciales y variedad.
   Excluye URLs ya utilizadas en casos aprobados. Examina hasta tres candidatas.
3. Descarga la fuente original y consulta el Ollama existente. El modelo puede
   descartar la noticia. Se exige puntuación mínima 3/5 en cambio, cliente,
   solución y utilidad para el aula, y todos los campos de la ficha.
4. Los borradores y el texto consultado quedan en
   `data/private/oportunidades/AAAA-MM-QN/`, ignorados por Git. Un borrador
   existente se conserva. Si no hay candidata apta, se guarda `seleccion.json`
   y la newsletter continúa sin esta sección. Una nueva ejecución puede reintentar.
5. El docente revisa `caso.json`, la fuente enlazada y `vista-previa.html`.
   Comprueba hechos, fechas y promesas; distingue hipótesis de demanda real;
   revisa el nivel del alumnado, las alternativas y la prueba de validación.
6. La aprobación explícita guarda el caso en `data/editorial/oportunidades/`.
   Se registra revisor, fecha y huella del contenido. Una edición posterior
   invalida la aprobación. El renderizado falla si un archivo editorial es inválido.
7. El pipeline diario renderiza exclusivamente ese archivo aprobado en
   `docs/oportunidades/`. Incluye índice, navegación y sitemap. No llama al LLM.
8. La newsletter HTML/Markdown incluye un enlace únicamente si existe un caso
   aprobado para su quincena y la página correspondiente ya está renderizada.
   Se debe publicar esa página antes de distribuir el enlace.

No se añaden dependencias, timers ni envíos. La configuración de Ollama se lee
como en el resto del proyecto. Esta primera versión solo admite ese proveedor.
La llamada limita la salida y desactiva el razonamiento separado para acotar
la latencia, mediante los parámetros de la [API de Ollama](https://docs.ollama.com/api/chat).

## Uso manual

Preparar un borrador sin ejecutar el agregador ni enviar la newsletter:

```bash
.venv/bin/python generar_oportunidades.py --fecha 2026-09-16
```

Si editas el JSON, actualiza su vista previa antes de aprobar:

```bash
.venv/bin/python generar_oportunidades.py \
  --vista-previa data/private/oportunidades/2026-09-Q2/caso.json
```

Tras revisar y, si procede, editar el JSON:

```bash
.venv/bin/python generar_oportunidades.py \
  --aprobar data/private/oportunidades/2026-09-Q2/caso.json \
  --revisor 'Nombre del docente' --fuente-verificada
```

Esto crea el JSON editorial y las páginas locales; no hace commit, push ni envío.
Las páginas públicas no incluyen la copia íntegra del artículo original.
La respuesta resuelta está dentro de un desplegable cerrado por defecto.

Regenerar el borrador existente de newsletter para incorporar el caso aprobado:

```bash
.venv/bin/python generar_newsletter.py --fecha 2026-09-16 \
  --periodicidad quincenal --force --sin-oportunidad \
  --output-dir data/private/newsletter_pendiente/archivos \
  --metadata-file data/private/newsletter_pendiente/metadata.json
```

Usar la fecha de la edición pendiente, no necesariamente la fecha actual.
Conservar el circuito habitual de revisión y publicación de la newsletter.
Versionar código, JSON editorial aprobado y HTML generado; no subir borradores.

Para renderizar únicamente los casos aprobados:

```bash
.venv/bin/python generar_oportunidades.py --renderizar
```

`--sin-oportunidad` omite la generación de nuevos casos, pero mantiene el enlace
al caso ya aprobado. Las newsletters semanales conservan su comportamiento.

## Límites y comprobaciones

La puntuación es una ayuda editorial, no una validación comercial. La diversidad
es una preferencia de selección, no una garantía temática. Una fuente bloqueada,
un error del modelo o una respuesta incompleta hacen pasar a otra candidata;
no se inventa un caso usando únicamente el resumen. Revisar `seleccion.json`
si no aparece una propuesta (solo registra tipos de error, no endpoints privados).

La vista previa incorpora la misma hoja CSS del sitio y abre la respuesta para
facilitar su revisión. No necesita conexión para cargar el diseño; las fuentes
web usan las mismas alternativas locales que el sitio si no hay conexión.
La página pública mantiene la respuesta plegada para el alumnado.

```bash
python3 -m unittest discover -s tests -v
```
