# -*- coding: utf-8 -*-
"""
Pipeline principal del agregador Comercio Digital.

Ejecuta, en orden:
1. Agregación y resumen de noticias
2. Clasificación por módulo y RA
3. Obtención de imágenes destacadas
4. Generación de la web estática

Uso:
    python run_pipeline.py
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path


PASOS = [
    {
        "nombre": "Agregación y resumen de noticias",
        "script": "news_aggregator.py",
        "obligatorio": True,
    },
    {
        "nombre": "Clasificación por RA",
        "script": "clasificador_ra.py",
        "obligatorio": True,
    },
    {
        "nombre": "Enriquecimiento docente",
        "script": "enriquecer_docente.py",
        "obligatorio": False,
    },
    {
        "nombre": "Imágenes destacadas",
        "script": "imagen_destacada.py",
        "obligatorio": False,
    },
    {
        "nombre": "Generación de la web",
        "script": "generar_web.py",
        "obligatorio": True,
    },
]


def ejecutar_paso(paso: dict) -> bool:
    """Ejecuta un script del pipeline y devuelve True si termina correctamente."""
    script = paso["script"]
    nombre = paso["nombre"]
    obligatorio = paso.get("obligatorio", True)

    print("\n" + "=" * 70)
    print(f"▶ {nombre}")
    print(f"   Script: {script}")
    print("=" * 70)

    if not Path(script).exists():
        mensaje = f"⚠ No se encuentra el archivo {script}"
        if obligatorio:
            print(mensaje)
            return False
        print(mensaje + " — paso omitido")
        return True

    resultado = subprocess.run([sys.executable, script])

    if resultado.returncode == 0:
        print(f"✅ Paso completado: {nombre}")
        return True

    print(f"❌ Error en: {nombre}")

    if obligatorio:
        print("Pipeline detenido porque este paso es obligatorio.")
        return False

    print("El paso no es obligatorio. El pipeline continuará.")
    return True


def main():
    inicio = datetime.now()

    print("\n🚀 Iniciando pipeline Comercio Digital")
    print(f"Fecha/hora: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")

    for paso in PASOS:
        ok = ejecutar_paso(paso)
        if not ok:
            sys.exit(1)

    fin = datetime.now()
    duracion = fin - inicio

    print("\n" + "=" * 70)
    print("🎉 Pipeline completado correctamente")
    print(f"Duración aproximada: {duracion}")
    print("Revisa la carpeta docs/ y publica los cambios en GitHub.")
    print("=" * 70)


if __name__ == "__main__":
    main()
