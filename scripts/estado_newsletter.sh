#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_DIR="$(cd -- "${SCRIPT_DIR}/.." && pwd -P)"
PYTHON="${PROJECT_DIR}/.venv/bin/python"
PENDING_DIR="${PROJECT_DIR}/data/private/newsletter_pendiente"
METADATA_FILE="${PENDING_DIR}/metadata.json"

if [[ ! -d "${PENDING_DIR}" ]]; then
    printf 'Newsletter pendiente: NO\n'
    exit 0
fi

if [[ ! -f "${METADATA_FILE}" ]]; then
    printf 'Newsletter pendiente: ESTADO INCOMPLETO\n'
    printf 'Ruta: %s\n' "${PENDING_DIR#${PROJECT_DIR}/}"
    exit 2
fi

if [[ ! -x "${PYTHON}" ]]; then
    printf 'ERROR: no existe .venv/bin/python ejecutable.\n' >&2
    exit 1
fi

"${PYTHON}" - "${METADATA_FILE}" "${PENDING_DIR#${PROJECT_DIR}/}" <<'PY'
import json
import sys
from pathlib import Path

metadata_path = Path(sys.argv[1])
display_path = sys.argv[2]
metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

print(f"Newsletter pendiente: {'SÍ' if metadata.get('estado') == 'PENDIENTE' else 'NO'}")
print(f"Estado: {metadata.get('estado', 'DESCONOCIDO')}")
print(f"Fecha de generación: {metadata.get('fecha_generacion', 'DESCONOCIDA')}")
print(f"Periodo: {metadata.get('periodo', 'DESCONOCIDO')}")
print(f"Código de salida: {metadata.get('codigo_salida', 'DESCONOCIDO')}")
print(f"Ruta: {display_path}")
print("Archivos:")
for filename in metadata.get("archivos", []):
    print(f"- {filename}")
PY
