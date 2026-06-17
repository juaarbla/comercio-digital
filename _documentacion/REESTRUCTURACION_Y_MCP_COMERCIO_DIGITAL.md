# Reestructuración del agregador y creación del MCP Comercio Digital

## 1. Objetivo

El objetivo de esta intervención ha sido preparar el proyecto `00_CDI_press` para futuras integraciones con IA mediante MCP, manteniendo el pipeline actual funcionando y evitando publicar datos internos.

Se han realizado dos trabajos principales:

1. Reorganizar archivos internos del agregador.
2. Crear y probar un servidor MCP local de solo lectura para consultar las noticias clasificadas.

---

## 2. Situación inicial

El proyecto tenía en la raíz tanto scripts como archivos de datos, cachés y backups.

Ejemplo de archivos mezclados en la raíz:

```text
noticias_clasificadas.json
noticias_resumidas.json
cache_clasificacion.json
cache_imagenes.json
noticias_clasificadas.backup_*.json
generar_web.py
generar_aula.py
run_pipeline.py
```

Esto funcionaba, pero no era lo más adecuado para añadir un MCP, porque las rutas quedaban dispersas y había riesgo de publicar o versionar archivos internos por error.

---

## 3. Nueva estructura creada

Se crearon estas carpetas:

```powershell
New-Item -ItemType Directory -Force -Path data
New-Item -ItemType Directory -Force -Path data\processed
New-Item -ItemType Directory -Force -Path data\cache
New-Item -ItemType Directory -Force -Path data\backups
New-Item -ItemType Directory -Force -Path outputs
New-Item -ItemType Directory -Force -Path outputs\aula
New-Item -ItemType Directory -Force -Path outputs\newsletter
New-Item -ItemType Directory -Force -Path mcp
New-Item -ItemType Directory -Force -Path mcp\comercio_digital
```

La estructura final queda así:

```text
00_CDI_press/
├─ data/
│  ├─ processed/
│  │  ├─ noticias_clasificadas.json
│  │  └─ noticias_resumidas.json
│  │
│  ├─ cache/
│  │  ├─ cache_clasificacion.json
│  │  └─ cache_imagenes.json
│  │
│  └─ backups/
│     └─ noticias_clasificadas.backup_*.json
│
├─ docs/
├─ logs/
├─ mcp/
│  └─ comercio_digital/
│     ├─ server.py
│     ├─ requirements.txt
│     └─ README.md
│
├─ outputs/
├─ paths.py
├─ run_pipeline.py
├─ generar_web.py
├─ generar_aula.py
├─ generar_fichas_aula.py
├─ enriquecer_docente.py
├─ clasificador_ra.py
├─ imagen_destacada.py
├─ limpiar_duplicados.py
├─ news_aggregator.py
└─ README.md
```

De momento los scripts principales se mantienen en la raíz para no romper el flujo de trabajo, `arrancar.bat` ni `run_pipeline.py`.

---

## 4. Movimiento de archivos

### 4.1. Backups

Se movieron los backups antiguos a:

```text
data/backups/
```

Comando usado:

```powershell
Move-Item "noticias_clasificadas.backup_*.json" "data\backups\"
```

### 4.2. Cachés

Se movieron las cachés a:

```text
data/cache/
```

Comandos usados:

```powershell
Move-Item "cache_clasificacion.json" "data\cache\"
Move-Item "cache_imagenes.json" "data\cache\"
```

### 4.3. Datos procesados

Se movieron los JSON principales a:

```text
data/processed/
```

Comandos usados:

```powershell
Move-Item "noticias_clasificadas.json" "data\processed\"
Move-Item "noticias_resumidas.json" "data\processed\"
```

---

## 5. Centralización de rutas

Se creó un archivo `paths.py` en la raíz del proyecto.

Contenido:

```python
from pathlib import Path

# Raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent

# Carpetas principales
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"
CACHE_DIR = DATA_DIR / "cache"
BACKUPS_DIR = DATA_DIR / "backups"

DOCS_DIR = BASE_DIR / "docs"
LOGS_DIR = BASE_DIR / "logs"
OUTPUTS_DIR = BASE_DIR / "outputs"

# Archivos de datos
FEEDS_FILE = BASE_DIR / "feeds.json"
HISTORIAL_FILE = BASE_DIR / "historial.json"

NOTICIAS_RESUMIDAS = PROCESSED_DIR / "noticias_resumidas.json"
NOTICIAS_CLASIFICADAS = PROCESSED_DIR / "noticias_clasificadas.json"

# Cachés
CACHE_CLASIFICACION = CACHE_DIR / "cache_clasificacion.json"
CACHE_IMAGENES = CACHE_DIR / "cache_imagenes.json"
```

Este archivo evita tener rutas escritas manualmente en cada script.

---

## 6. Scripts actualizados

Se actualizaron los scripts para usar `paths.py`.

### 6.1. `clasificador_ra.py`

Antes usaba:

```python
INPUT_FILE  = Path("noticias_resumidas.json")
OUTPUT_FILE = Path("noticias_clasificadas.json")
CACHE_FILE  = Path("cache_clasificacion.json")
```

Ahora usa:

```python
from paths import NOTICIAS_RESUMIDAS, NOTICIAS_CLASIFICADAS, CACHE_CLASIFICACION

INPUT_FILE = NOTICIAS_RESUMIDAS
OUTPUT_FILE = NOTICIAS_CLASIFICADAS
CACHE_FILE = CACHE_CLASIFICACION
```

### 6.2. `generar_web.py`

Ahora usa:

```python
from paths import NOTICIAS_CLASIFICADAS

INPUT_FILE = NOTICIAS_CLASIFICADAS
```

### 6.3. `imagen_destacada.py`

Ahora usa:

```python
from paths import NOTICIAS_CLASIFICADAS, CACHE_IMAGENES

INPUT_FILE = NOTICIAS_CLASIFICADAS
OUTPUT_FILE = NOTICIAS_CLASIFICADAS
CACHE_FILE = CACHE_IMAGENES
```

### 6.4. `generar_aula.py`

El argumento de entrada por defecto pasó a:

```python
from paths import NOTICIAS_CLASIFICADAS

parser.add_argument("--entrada", default=str(NOTICIAS_CLASIFICADAS))
```

### 6.5. `generar_fichas_aula.py`

El argumento de entrada por defecto pasó a:

```python
from paths import NOTICIAS_CLASIFICADAS

p.add_argument("--entrada", default=str(NOTICIAS_CLASIFICADAS))
```

### 6.6. `limpiar_duplicados.py`

Antes:

```python
ARCHIVOS = [Path("noticias_resumidas.json"), Path("noticias_clasificadas.json")]
```

Ahora:

```python
from paths import NOTICIAS_RESUMIDAS, NOTICIAS_CLASIFICADAS

ARCHIVOS = [NOTICIAS_RESUMIDAS, NOTICIAS_CLASIFICADAS]
```

### 6.7. `news_aggregator.py`

Antes generaba:

```python
OUTPUT_FILE = Path("noticias_resumidas.json")
```

Ahora genera:

```python
from paths import FEEDS_FILE, HISTORIAL_FILE, NOTICIAS_RESUMIDAS

OUTPUT_FILE = NOTICIAS_RESUMIDAS
```

Se mantienen en la raíz:

```text
feeds.json
historial.json
```

### 6.8. `enriquecer_docente.py`

Se añadió:

```python
from paths import NOTICIAS_CLASIFICADAS, BACKUPS_DIR
```

La función de localización de entrada prioriza ahora:

```python
NOTICIAS_CLASIFICADAS
```

Es decir:

```text
data/processed/noticias_clasificadas.json
```

También se modificó la función de backups para que guarde en `data/backups/`:

```python
def crear_backup(ruta: Path) -> Path:
    marca = datetime.now().strftime("%Y%m%d_%H%M%S")
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
    backup = BACKUPS_DIR / f"{ruta.stem}.backup_{marca}{ruta.suffix}"
    shutil.copy2(ruta, backup)
    return backup
```

---

## 7. Comprobaciones realizadas

### 7.1. Comprobar referencias antiguas

Se usó:

```powershell
Select-String -Path *.py,*.bat -Pattern "noticias_clasificadas|noticias_resumidas|cache_clasificacion|cache_imagenes"
```

Sirvió para localizar scripts que seguían apuntando a rutas antiguas.

### 7.2. Probar scripts individuales

Se probaron sin errores:

```powershell
python clasificador_ra.py
python imagen_destacada.py
python generar_web.py
python generar_aula.py
python generar_fichas_aula.py
python limpiar_duplicados.py
python news_aggregator.py
python enriquecer_docente.py
```

### 7.3. Probar pipeline completo

Se ejecutó:

```powershell
python run_pipeline.py
```

Resultado:

```text
Pipeline completado correctamente
Duración aproximada: 0:05:03
```

### 7.4. Comprobar que los JSON no reaparecen en la raíz

Se usó:

```powershell
Get-ChildItem -File | Select-Object Name
```

La raíz quedó sin:

```text
noticias_clasificadas.json
noticias_resumidas.json
cache_clasificacion.json
cache_imagenes.json
```

---

## 8. `.gitignore`

Se actualizó `.gitignore` para evitar subir archivos sensibles o internos.

Contenido recomendado:

```gitignore
# Credenciales — NUNCA subir
.env

# Entorno local
entorno.bat

# Python
__pycache__/
*.pyc
*.pyo
.venv/
venv/

# VSCode
.vscode/

# Logs
logs/
*.log

# Datos internos del agregador
data/cache/
data/backups/

# Backups sueltos
*.backup.json
*.backup_*.json

# Antiguos JSON en raíz, por si reaparecen
noticias_resumidas.json
noticias_clasificadas.json
cache_clasificacion.json
cache_imagenes.json

# Historial local
historial.json

# Carpeta deprecated
_deprecated/

# Windows
Thumbs.db
desktop.ini
```

Decisión tomada:

```text
data/processed/ no se ignora de momento.
```

Motivo:

```text
Ahí están los JSON procesados principales del proyecto. No se publican en GitHub Pages si GitHub Pages sirve desde docs/, pero sí pueden quedar versionados en el repositorio.
```

---

## 9. Commit de reestructuración

Tras comprobar que el pipeline funcionaba, se guardó el estado en Git.

Comandos usados:

```powershell
git add .gitignore paths.py clasificador_ra.py enriquecer_docente.py generar_aula.py generar_fichas_aula.py generar_web.py imagen_destacada.py limpiar_duplicados.py news_aggregator.py
git add docs/
git commit -m "Reorganiza datos internos y centraliza rutas del agregador"
git push
```

---

# MCP Comercio Digital

## 10. Objetivo del MCP

Se creó un servidor MCP local para consultar el agregador desde herramientas compatibles con Model Context Protocol.

Nombre:

```text
MCP Comercio Digital
```

Ruta:

```text
mcp/comercio_digital/
```

Objetivo inicial:

```text
Consultar noticias clasificadas desde una IA sin modificar archivos ni publicar nada.
```

Esta primera versión es de solo lectura.

---

## 11. Archivos creados

```text
mcp/comercio_digital/
├─ server.py
├─ requirements.txt
└─ README.md
```

### 11.1. `requirements.txt`

Contenido:

```text
mcp[cli]
```

---

## 12. Ruta de datos usada por el MCP

El MCP lee este archivo:

```text
data/processed/noticias_clasificadas.json
```

En `server.py` se define así:

```python
BASE_DIR = Path(__file__).resolve().parents[2]
JSON_PATH = BASE_DIR / "data" / "processed" / "noticias_clasificadas.json"
```

---

## 13. Herramientas MCP creadas

El servidor expone estas herramientas:

```text
estado_agregador()
buscar_noticias(texto, limite)
noticias_por_modulo(modulo, limite)
noticias_por_valor_docente(valor, limite)
noticias_newsletter(limite)
ficha_aula_basica(url_o_titulo)
```

### 13.1. `estado_agregador`

Devuelve:

```text
- ruta del archivo JSON
- total de noticias
- distribución por módulo
- distribución por valor docente
- número de noticias seleccionadas para newsletter
- número de noticias marcadas para ficha
```

### 13.2. `buscar_noticias`

Busca texto en:

```text
- título
- resumen
- fuente
- módulo
- RA
- CE
```

### 13.3. `noticias_por_modulo`

Filtra por módulo relacionado.

Ejemplos:

```text
Comercio Electrónico
IA
CDI
Digitalización
```

### 13.4. `noticias_por_valor_docente`

Filtra por:

```text
alto
medio
bajo
```

### 13.5. `noticias_newsletter`

Devuelve noticias marcadas con:

```text
seleccion_newsletter = True
```

### 13.6. `ficha_aula_basica`

Genera una ficha básica en memoria a partir de una noticia localizada por URL o título.

No guarda archivos todavía.

---

## 14. Instalación del MCP

Desde la raíz del proyecto:

```powershell
pip install -r mcp\comercio_digital\requirements.txt
```

---

## 15. Prueba básica del servidor

Desde la raíz del proyecto:

```powershell
python mcp\comercio_digital\server.py
```

Si no muestra errores y queda esperando, el servidor arranca correctamente.

Para detener:

```text
CTRL + C
```

---

## 16. Prueba con MCP Inspector

Se ejecutó:

```powershell
mcp dev mcp\comercio_digital\server.py
```

El Inspector pidió instalar:

```text
@modelcontextprotocol/inspector
```

Se aceptó con:

```text
y
```

Inicialmente apareció un error:

```text
Error: spawn uv ENOENT
```

Motivo:

```text
El Inspector intentaba usar uv, pero uv no estaba instalado o no estaba disponible en PATH.
```

Solución:

Se configuró manualmente el Inspector con transporte `STDIO`.

### 16.1. Configuración que funcionó

En el MCP Inspector:

```text
Transport Type:
STDIO
```

En `Command` se puso el Python del entorno virtual:

```text
C:\Users\Juan\Google Drive\00_CDI_press\.venv\Scripts\python.exe
```

En `Arguments` se puso la ruta absoluta del servidor, usando barras `/`:

```text
"C:/Users/Juan/Google Drive/00_CDI_press/mcp/comercio_digital/server.py"
```

Después se pulsó:

```text
Connect
```

El Inspector conectó correctamente y mostró:

```text
Connected
comercio-digital
```

---

## 17. Pruebas realizadas en el Inspector

Se accedió a la pestaña:

```text
Tools
```

Se listaron las herramientas y se ejecutaron llamadas MCP.

Se comprobó que el servidor devolvía noticias reales desde:

```text
data/processed/noticias_clasificadas.json
```

Ejemplo de resultado devuelto:

```text
titulo
url
resumen
modulo_relacionado
valor_docente
tipo_uso
seleccion_newsletter
generar_ficha
score_docente
```

El Inspector mostró:

```text
Valid according to output schema
```

Conclusión:

```text
MCP Comercio Digital v0.1 operativo.
```

---

## 18. Seguridad de la versión v0.1

Esta versión es segura porque es de solo lectura.

Permitido:

```text
- leer data/processed/noticias_clasificadas.json
- devolver noticias filtradas
- generar fichas básicas en memoria
```

No permitido:

```text
- publicar en WordPress
- modificar JSON
- borrar archivos
- ejecutar el pipeline
- hacer push a GitHub
- modificar docs/
```

---

## 19. Commit del MCP

Para guardar el MCP en Git:

```powershell
git add mcp/
git commit -m "Añade MCP local para consultar el agregador"
git push
```

---

## 20. Estado final

El proyecto queda con:

```text
✅ Datos internos organizados
✅ Rutas centralizadas en paths.py
✅ Pipeline funcionando
✅ Git limpio tras commit
✅ MCP local creado
✅ MCP probado con Inspector
✅ Servidor MCP conectado correctamente
✅ Herramientas MCP devolviendo noticias reales
```

---

## 21. Próximos pasos posibles

### v0.2 — Generación de fichas Markdown

Crear una herramienta MCP:

```text
generar_ficha_md(url_o_titulo)
```

Que guarde la ficha en:

```text
outputs/aula/
```

### v0.3 — Newsletter docente

Crear una herramienta:

```text
generar_newsletter_docente()
```

Que prepare una propuesta semanal o quincenal.

### v0.4 — Conexión con WordPress

Más adelante, crear un MCP o integración adicional para:

```text
- crear borradores
- sugerir categorías
- sugerir etiquetas
- proponer enlaces internos
```

No publicar automáticamente.

### v0.5 — Conexión con Tutor IA

Relacionar noticias con:

```text
- módulos
- RA
- CE
- unidades didácticas
- actividades de aula
```

---

## 22. Decisiones importantes

### Decisión 1

Mantener los scripts en la raíz.

Motivo:

```text
Evita romper run_pipeline.py, arrancar.bat y publicar_web_diaria.bat.
```

Riesgo:

```text
La raíz sigue teniendo bastantes scripts.
```

Siguiente paso futuro:

```text
Mover scripts a scripts/ solo cuando el MCP y el pipeline estén consolidados.
```

### Decisión 2

No publicar JSON en GitHub Pages.

Motivo:

```text
GitHub Pages sirve desde docs/. Los JSON internos están fuera de docs/.
```

Riesgo:

```text
data/processed/ podría quedar versionado en el repositorio si no se ignora.
```

Siguiente paso futuro:

```text
Decidir si data/processed/ debe versionarse o ignorarse.
```

### Decisión 3

MCP solo lectura.

Motivo:

```text
Permite probar MCP sin riesgo.
```

Riesgo:

```text
Todavía no genera archivos persistentes.
```

Siguiente paso:

```text
Añadir generación de fichas Markdown en outputs/aula/.
```
