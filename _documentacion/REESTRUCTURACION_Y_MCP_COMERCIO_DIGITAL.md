# Reestructuración del agregador y MCP Comercio Digital

Este documento recoge la reestructuración interna del proyecto `00_CDI_press` y la creación del servidor MCP local para consultar y reutilizar noticias clasificadas.

## 1. Objetivo

Preparar el agregador para futuras integraciones con IA mediante MCP, manteniendo el pipeline actual funcionando y evitando publicar datos internos.

Trabajos realizados:

1. Reorganizar archivos internos del agregador.
2. Centralizar rutas en `paths.py`.
3. Crear y probar un servidor MCP local.
4. Añadir generación de fichas Markdown de trabajo en `outputs/aula/`.
5. Mantener separada la publicación web de las salidas locales de trabajo.

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
news_aggregator.py
clasificador_ra.py
enriquecer_docente.py
imagen_destacada.py
generar_web.py
generar_aula.py
generar_fichas_aula.py
generar_newsletter.py
generar_seo.py
limpiar_duplicados.py
run_pipeline.py
```

Cambios principales:

- `noticias_resumidas.json` pasa a `data/processed/noticias_resumidas.json`.
- `noticias_clasificadas.json` pasa a `data/processed/noticias_clasificadas.json`.
- `cache_clasificacion.json` pasa a `data/cache/cache_clasificacion.json`.
- `cache_imagenes.json` pasa a `data/cache/cache_imagenes.json`.
- Los backups pasan a `data/backups/`.

## 5. Validación

Se ejecutó:

```powershell
python run_pipeline.py
```

Resultado esperado:

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

## 8. Diferencia entre pipeline y MCP

```text
docs/fichas-aula/  → fichas públicas generadas por el pipeline
outputs/aula/      → fichas locales generadas desde MCP
```

El MCP se usa para consulta y trabajo local. El pipeline se usa para generar la web pública.

## 9. Configuración que funcionó en MCP Inspector

### Inicio directo del servidor MCP

Archivo BAT:

```text
iniciar_mcp.bat
```

Python recomendado:

```text
%LOCALAPPDATA%\PythonVenvs\comercio-digital\Scripts\python.exe
```

Ruta real en el equipo principal:

```text
C:\Users\Juan\AppData\Local\PythonVenvs\comercio-digital\Scripts\python.exe
```

Servidor:

```text
mcp_servers\comercio_digital\server.py
```

Ejecución:

```powershell
.\iniciar_mcp.bat
```

### Prueba con MCP Inspector

Archivo BAT:

```text
probar_mcp_inspector.bat
```

Si aparece:

```text
"mcp" no se reconoce como un comando interno o externo,
programa o archivo por lotes ejecutable.
```

la causa es que `mcp` no está disponible globalmente en Windows.

### Configuración manual correcta

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
"C:/Users/Juan/Google Drive/00. Proyectos/00_CDI_press/mcp_servers/comercio_digital/server.py"
```

Con esta configuración, MCP Inspector conecta correctamente.

## 10. Seguridad

La versión actual del MCP:

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

## 11. Decisión sobre `outputs/aula/`

`outputs/aula/` es una carpeta de salida local generada por MCP.

Recomendación:

```text
No versionar todas las fichas generadas automáticamente.
```

Añadir a `.gitignore`:

```gitignore
outputs/aula/
```

## 12. Próximos pasos posibles

### MCP v0.3 — Newsletter docente

Posibles herramientas:

```text
consultar_ultima_newsletter()
proponer_newsletter_docente()
```

### MCP v0.4 — WordPress

Objetivo futuro:

```text
crear borradores, sugerir categorías, etiquetas y enlaces internos.
```

No publicar automáticamente.

### MCP v0.5 — Tutor IA

Relacionar noticias con:

```text
módulos
RA
CE
unidades didácticas
actividades de aula
```

## 13. Decisión actual

```text
MCP se mantiene como herramienta local de consulta y generación de materiales de trabajo.
La publicación sigue dependiendo del pipeline y de GitHub Pages.
```
