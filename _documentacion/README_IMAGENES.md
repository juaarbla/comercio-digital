# Imágenes destacadas

`imagen_destacada.py` completa el campo `imagen_url` de las noticias clasificadas para mejorar la presentación visual de la web.

## Objetivo

Añadir imagen destacada a:

- portada;
- páginas de sección;
- página Aula;
- fichas docentes;
- newsletter, si el diseño la utiliza.

## Archivo de entrada y salida

```text
data/processed/noticias_clasificadas.json
```

El script actualiza el mismo archivo.

## Caché

Para evitar repetir peticiones usa:

```text
data/cache/cache_imagenes.json
```

La caché guarda únicamente resultados válidos:

```text
url_noticia → imagen_url
```

## Proveedores

El proveedor se configura en `.env`.

### Modo RSS/OG

```env
IMAGE_PROVIDER=rss
```

Intenta obtener imagen desde la página original mediante:

- `og:image`;
- `twitter:image`;
- metadatos disponibles en la fuente.

### Modo OpenAI

```env
IMAGE_PROVIDER=openai
OPENAI_API_KEY=...
OPENAI_IMG_MODEL=dall-e-3
OPENAI_IMG_SIZE=1024x1024
```

Este modo puede generar costes y debe usarse solo si interesa crear imágenes propias.

## Ejecución

```powershell
python imagen_destacada.py
```

## Lugar en el pipeline

Debe ejecutarse después de clasificar/enriquecer y antes de generar HTML:

```text
enriquecer_docente.py
   ↓
imagen_destacada.py
   ↓
generar_web.py
   ↓
generar_fichas_aula.py
   ↓
generar_aula.py
```

## Archivos que no conviene subir

```text
data/cache/cache_imagenes.json
data/backups/
.env
```

## Validación rápida

```powershell
Select-String -Path data\processed\noticias_clasificadas.json -Pattern "imagen_url"
```

Revisión visual:

```powershell
start docs\index.html
start docs\aula.html
start docs\newsletter\index.html
```

## Criterio actual

El modo preferente es `rss`, porque aprovecha imágenes reales de las fuentes y evita costes.

El modo `openai` queda como opción futura o puntual.
