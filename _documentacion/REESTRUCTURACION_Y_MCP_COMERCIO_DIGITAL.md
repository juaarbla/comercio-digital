# Reestructuración del agregador y creación del MCP Comercio Digital

## 1. Objetivo

Preparar el proyecto `00_CDI_press` para futuras integraciones con IA mediante MCP, manteniendo el pipeline actual funcionando y evitando publicar datos internos.

Trabajos realizados:

1. Reorganizar archivos internos del agregador.
2. Crear y probar un servidor MCP local para consultar noticias clasificadas.
3. Añadir una herramienta MCP para generar fichas Markdown de trabajo en `outputs/aula/`.

## 2. Estructura final

```text
00_CDI_press/
├─ data/
│  ├─ processed/
│  │  ├─ noticias_clasificadas.json
│  │  └─ noticias_resumidas.json
│  ├─ cache/
│  │  ├─ cache_clasificacion.json
│  │  └─ cache_imagenes.json
│  └─ backups/
│     └─ noticias_clasificadas.backup_*.json
│
├─ docs/
├─ logs/
├─ mcp_servers/
│  └─ comercio_digital/
│     ├─ server.py
│     ├─ requirements.txt
│     └─ README.md
│
├─ outputs/
│  └─ aula/
├─ paths.py
├─ run_pipeline.py
└─ README.md
```

## 3. Centralización de rutas

Se creó `paths.py` para evitar rutas dispersas.

Rutas clave:

```python
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"
CACHE_DIR = DATA_DIR / "cache"
BACKUPS_DIR = DATA_DIR / "backups"
OUTPUTS_DIR = BASE_DIR / "outputs"
AULA_OUTPUTS_DIR = OUTPUTS_DIR / "aula"

NOTICIAS_RESUMIDAS = PROCESSED_DIR / "noticias_resumidas.json"
NOTICIAS_CLASIFICADAS = PROCESSED_DIR / "noticias_clasificadas.json"

CACHE_CLASIFICACION = CACHE_DIR / "cache_clasificacion.json"
CACHE_IMAGENES = CACHE_DIR / "cache_imagenes.json"
```

## 4. Scripts actualizados

Scripts adaptados a la nueva estructura:

```text
clasificador_ra.py
generar_web.py
imagen_destacada.py
generar_aula.py
generar_fichas_aula.py
limpiar_duplicados.py
news_aggregator.py
enriquecer_docente.py
```

Cambios principales:

- `noticias_resumidas.json` pasa a `data/processed/noticias_resumidas.json`.
- `noticias_clasificadas.json` pasa a `data/processed/noticias_clasificadas.json`.
- `cache_clasificacion.json` pasa a `data/cache/cache_clasificacion.json`.
- `cache_imagenes.json` pasa a `data/cache/cache_imagenes.json`.
- Los backups de `enriquecer_docente.py` pasan a `data/backups/`.

## 5. Validación

Se ejecutó:

```powershell
python run_pipeline.py
```

Resultado:

```text
Pipeline completado correctamente.
```

También se comprobó que los JSON no reaparecen en la raíz.

## 6. MCP Comercio Digital v0.1

Ruta:

```text
mcp_servers/comercio_digital/
```

El MCP lee:

```text
data/processed/noticias_clasificadas.json
```

Herramientas v0.1:

```text
estado_agregador()
buscar_noticias(texto, limite)
noticias_por_modulo(modulo, limite)
noticias_por_valor_docente(valor, limite)
noticias_newsletter(limite)
ficha_aula_basica(url_o_titulo)
```

Estado:

```text
MCP Comercio Digital v0.1 operativo.
```

## 7. MCP Comercio Digital v0.2

Se añade:

```text
generar_ficha_md(url_o_titulo)
```

La herramienta:

1. Lee `data/processed/noticias_clasificadas.json`.
2. Busca una noticia por título o URL.
3. Genera una ficha de aula en Markdown.
4. Guarda el archivo en `outputs/aula/`.
5. Devuelve la ruta del archivo creado.

Estado:

```text
MCP Comercio Digital v0.2 operativo.
```

## 8. Configuración que funcionó en MCP Inspector

Durante las pruebas se usaron dos formas de iniciar el MCP:

1. Arrancar directamente el servidor MCP.
2. Probarlo desde MCP Inspector.

### 8.1. Inicio directo del servidor MCP

Se creó un archivo BAT para iniciar el servidor MCP desde la raíz del proyecto:

```text
iniciar_mcp.bat
```

Este BAT usa el Python del entorno virtual externo, ubicado fuera de Google Drive:

```text
%LOCALAPPDATA%\PythonVenvs\comercio-digital\Scripts\python.exe
```

Ruta real en el equipo principal:

```text
C:\Users\Juan\AppData\Local\PythonVenvs\comercio-digital\Scripts\python.exe
```

El servidor MCP que se ejecuta es:

```text
mcp_servers\comercio_digital\server.py
```

Resultado esperado al ejecutar:

```powershell
.\iniciar_mcp.bat
```

```text
MCP Comercio Digital
Iniciando servidor MCP...
Para detenerlo: CTRL + C
```

Esto indica que el servidor MCP está arrancado y esperando conexiones.

### 8.2. Prueba con MCP Inspector

Se creó también:

```text
probar_mcp_inspector.bat
```

El objetivo de este BAT es abrir MCP Inspector y mostrar las rutas correctas que deben usarse si la conexión automática falla.

Durante la prueba apareció el error:

```text
"mcp" no se reconoce como un comando interno o externo,
programa o archivo por lotes ejecutable.
```

### 8.3. Causa del error

El comando `mcp` no está disponible globalmente en Windows porque el entorno virtual del proyecto no está en el `PATH` global.

El entorno correcto está en:

```text
%LOCALAPPDATA%\PythonVenvs\comercio-digital\
```

Por eso no conviene depender de:

```text
mcp dev ...
```

como comando global.

### 8.4. Configuración manual correcta en MCP Inspector

La solución aplicada fue configurar manualmente el transporte `STDIO` en MCP Inspector.

Configuración correcta:

```text
Transport Type:
STDIO
```

```text
Command:
C:\Users\Juan\AppData\Local\PythonVenvs\comercio-digital\Scripts\python.exe
```

```text
Arguments:
"C:/Users/Juan/Google Drive/00_CDI_press/mcp_servers/comercio_digital/server.py"
```

Con esta configuración, MCP Inspector conecta correctamente con el servidor.

### 8.5. Resultado de la prueba

Se confirmó que:

```text
- el servidor MCP conecta desde Inspector;
- aparecen las herramientas MCP;
- se puede ejecutar buscar_noticias;
- se puede ejecutar generar_ficha_md;
- generar_ficha_md crea fichas Markdown en outputs/aula/.
```

### 8.6. Decisión

No se añade por ahora `mcp` al `PATH` global de Windows.

Motivo:

```text
Es más seguro y portable usar siempre el Python del entorno virtual específico del proyecto.
```

Riesgo:

```text
Hay que recordar configurar manualmente Command y Arguments en MCP Inspector si el acceso automático falla.
```

Siguiente paso:

```text
Mantener iniciar_mcp.bat y probar_mcp_inspector.bat como accesos rápidos documentados.
```

## 9. Seguridad

La versión actual:

```text
- no publica en WordPress;
- no modifica JSON;
- no borra archivos;
- no ejecuta el pipeline;
- no hace push a GitHub;
- no modifica docs/.
```

Sí puede crear archivos en:

```text
outputs/aula/
```

## 10. Decisión sobre `outputs/aula/`

`outputs/aula/` es una carpeta de salida local generada por MCP.

Recomendación:

```text
No versionar todas las fichas generadas automáticamente.
```

Añadir a `.gitignore`:

```gitignore
outputs/aula/
```

## 11. Próximos pasos

### Newsletter docente

Se ha creado `generar_newsletter.py` como salida del pipeline, no como herramienta MCP.

Genera:

```text
docs/newsletter/index.html
docs/newsletter/newsletter-AAAA-WSS.html
docs/newsletter/newsletter-AAAA-WSS.md
```

Decisión:

```text
El agregador genera la edición, pero no gestiona suscriptores ni envíos.
```

Posible evolución MCP futura:

```text
consultar_ultima_newsletter()
proponer_newsletter_docente()
```

### v0.4 — WordPress

Crear borradores, sugerir categorías, etiquetas y enlaces internos. No publicar automáticamente.

### v0.5 — Tutor IA

Relacionar noticias con módulos, RA, CE, unidades didácticas y actividades de aula.
