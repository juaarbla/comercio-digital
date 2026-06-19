# MCP Comercio Digital

Servidor MCP local para consultar y reutilizar las noticias clasificadas del agregador **Comercio Digital**.

Ruta del servidor:

```text
mcp_servers/comercio_digital/
```

Este MCP permite que un asistente compatible con Model Context Protocol consulte el archivo interno:

```text
data/processed/noticias_clasificadas.json
```

## Estado

Versión actual:

```text
v0.2
```

Estado:

```text
Operativo y probado con MCP Inspector.
```

## Objetivo

Exponer herramientas simples para consultar el agregador desde una IA:

- ver el estado general del agregador;
- buscar noticias por texto;
- filtrar noticias por módulo;
- filtrar por valor docente;
- consultar noticias seleccionadas para newsletter;
- generar una ficha básica en memoria;
- generar una ficha Markdown de trabajo en `outputs/aula/`.

## Estructura

```text
00_CDI_press/
├─ data/
│  └─ processed/
│     └─ noticias_clasificadas.json
│
├─ outputs/
│  └─ aula/
│
└─ mcp_servers/
   └─ comercio_digital/
      ├─ server.py
      ├─ requirements.txt
      └─ README.md
```

## Instalación

Desde la raíz del proyecto:

```powershell
pip install -r mcp_servers\comercio_digital\requirements.txt
```

El archivo `requirements.txt` contiene:

```text
mcp[cli]
```

## Ejecución básica

Desde la raíz del proyecto:

```powershell
python mcp_servers\comercio_digital\server.py
```

Si arranca sin errores, el servidor queda esperando conexión desde un cliente MCP.

Para detenerlo:

```text
CTRL + C
```

## Prueba con MCP Inspector

Ejecutar:

```powershell
mcp dev mcp_servers\comercio_digital\server.py
```

Si el Inspector intenta usar `uv` y falla con:

```text
Error: spawn uv ENOENT
```

configurar manualmente:

```text
Transport Type:
STDIO

Command:
C:\Users\Juan\Google Drive\00_CDI_press\.venv\Scripts\python.exe

Arguments:
"C:/Users/Juan/Google Drive/00_CDI_press/mcp_servers/comercio_digital/server.py"
```

Después pulsar:

```text
Connect
```

## Herramientas disponibles

```text
estado_agregador()
buscar_noticias(texto, limite)
noticias_por_modulo(modulo, limite)
noticias_por_valor_docente(valor, limite)
noticias_newsletter(limite)
ficha_aula_basica(url_o_titulo)
generar_ficha_md(url_o_titulo)
```

## `generar_ficha_md`

Genera una ficha de aula en Markdown y la guarda en:

```text
outputs/aula/
```

Ejemplo:

```json
{
  "url_o_titulo": "Reino Unido aprueba el veto a redes sociales"
}
```

Salida esperada:

```json
{
  "creada": true,
  "archivo": "C:\\Users\\Juan\\Google Drive\\00_CDI_press\\outputs\\aula\\reino-unido-aprueba-el-veto-a-redes-sociales.md",
  "titulo": "...",
  "url": "...",
  "modulo_relacionado": "Comercio Electrónico",
  "valor_docente": "alto"
}
```

## Seguridad

Permitido:

- leer `data/processed/noticias_clasificadas.json`;
- devolver resultados filtrados;
- generar propuestas de ficha en memoria;
- crear archivos Markdown en `outputs/aula/`.

No permitido:

- publicar en WordPress;
- modificar el JSON;
- borrar archivos;
- ejecutar el pipeline;
- subir contenido a GitHub Pages;
- hacer `git push`;
- modificar `docs/`.

## Decisión sobre `outputs/aula/`

`outputs/aula/` es una carpeta de salida local.

Recomendación:

```text
No versionar todas las fichas generadas automáticamente.
```

Añadir a `.gitignore`:

```gitignore
outputs/aula/
```

## Próximas mejoras posibles

### v0.3 — Newsletter docente

Crear:

```text
generar_newsletter_docente()
```

### v0.4 — WordPress

Crear o conectar una herramienta para crear borradores y proponer categorías, etiquetas y enlaces internos.

### v0.5 — Tutor IA

Relacionar noticias con módulos, RA, CE, unidades didácticas y actividades de aula.
