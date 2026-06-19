# Imágenes destacadas

`imagen_destacada.py` completa el campo `imagen_url` de las noticias clasificadas.

## Objetivo

Mejorar la presentación visual de:

- portada;
- páginas de sección;
- página Aula;
- fichas docentes.

## Archivo de entrada y salida

```text
data/processed/noticias_clasificadas.json
```

El script actualiza el mismo archivo.

## Caché

Para evitar repetir peticiones, usa:

```text
data/cache/cache_imagenes.json
```

La caché guarda únicamente éxitos:

```text
url_noticia → imagen_url
```

## Proveedores

El proveedor se configura en `.env`:

```env
IMAGE_PROVIDER=rss
```

o:

```env
IMAGE_PROVIDER=openai
```

### Modo RSS

Intenta obtener imagen desde la página original mediante:

- `og:image`;
- `twitter:image`.

### Modo OpenAI

Usa generación de imagen mediante API.

Variables:

```env
OPENAI_API_KEY=...
OPENAI_IMG_MODEL=dall-e-3
OPENAI_IMG_SIZE=1024x1024
```

## Ejecución

```powershell
python imagen_destacada.py
```

## Lugar en el pipeline

Debe ejecutarse después de clasificar y enriquecer noticias, y antes de generar HTML:

```text
enriquecer_docente.py
   ↓
imagen_destacada.py
   ↓
generar_web.py
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

También se puede revisar visualmente:

```powershell
start docs\index.html
start docs\aula.html
```
