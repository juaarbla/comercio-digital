from pathlib import Path

# Raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent

# Carpetas principales
DATA_DIR = BASE_DIR / "data"
CURRICULO_DIR = DATA_DIR / "curriculo"
PROCESSED_DIR = DATA_DIR / "processed"
CACHE_DIR = DATA_DIR / "cache"
BACKUPS_DIR = DATA_DIR / "backups"

DOCS_DIR = BASE_DIR / "docs"
LOGS_DIR = BASE_DIR / "logs"
OUTPUTS_DIR = BASE_DIR / "outputs"
AULA_OUTPUTS_DIR = OUTPUTS_DIR / "aula"

# Archivos de datos
FEEDS_FILE = BASE_DIR / "feeds.json"
HISTORIAL_FILE = BASE_DIR / "historial.json"

NOTICIAS_RESUMIDAS = PROCESSED_DIR / "noticias_resumidas.json"
NOTICIAS_CLASIFICADAS = PROCESSED_DIR / "noticias_clasificadas.json"

# Cachés
CACHE_CLASIFICACION = CACHE_DIR / "cache_clasificacion.json"
CACHE_IMAGENES = CACHE_DIR / "cache_imagenes.json"


RUNTIME_DIRS = (
    PROCESSED_DIR,
    CACHE_DIR,
    BACKUPS_DIR,
    LOGS_DIR,
    OUTPUTS_DIR,
    AULA_OUTPUTS_DIR,
)


def ensure_runtime_dirs() -> None:
    """Crea los directorios locales necesarios para ejecutar el pipeline."""
    for directory in RUNTIME_DIRS:
        directory.mkdir(parents=True, exist_ok=True)
