# -*- coding: utf-8 -*-
"""
Pipeline principal del agregador Comercio Digital.

Orden general:
1. Agrega y resume noticias.
2. Limpia duplicados.
3. Clasifica por módulo, RA y CE.
4. Enriquece la utilidad docente.
5. Añade conceptos clave desde los contenidos básicos curriculares.
6. Mejora las actividades breves vinculándolas a RA y CE.
7. Genera imágenes, web, fichas, aula y SEO.

Nota:
La newsletter no se genera dentro del pipeline principal.
Se ejecuta manualmente con generar_newsletter.py cuando se quiera publicar
una edición semanal o quincenal.
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
        "nombre": "Limpieza de duplicados",
        "script": "limpiar_duplicados.py",
        "obligatorio": False,
    },
    {
        "nombre": "Clasificación curricular por RA y CE",
        "script": "clasificador_ra.py",
        "obligatorio": True,
    },
    {
        "nombre": "Enriquecimiento docente",
        "script": "enriquecer_docente.py",
        "obligatorio": False,
        "args": ["--forzar"],
    },
    {
        "nombre": "Enriquecimiento de conceptos curriculares",
        "script": "enriquecer_conceptos.py",
        "obligatorio": True,
        "args": ["--sobrescribir"],
    },
    {
        "nombre": "Enriquecimiento de actividades de aula",
        "script": "enriquecer_actividades.py",
        "obligatorio": True,
        "args": ["--sobrescribir", "--solo-generar-ficha"],
    },
    {
        "nombre": "Imágenes destacadas",
        "script": "imagen_destacada.py",
        "obligatorio": False,
    },
    {
        "nombre": "Generación de la web principal",
        "script": "generar_web.py",
        "obligatorio": True,
    },
    {
        "nombre": "Generación de fichas docentes de aula",
        "script": "generar_fichas_aula.py",
        "obligatorio": True,
        "args": ["--max-fichas", "10", "--limpiar"],
    },
    {
        "nombre": "Generación de la página de aula",
        "script": "generar_aula.py",
        "obligatorio": True,
        "args": ["--max-noticias", "25"],
    },
    {
        "nombre": "SEO técnico",
        "script": "generar_seo.py",
        "obligatorio": True,
    },
]


def ejecutar_paso(paso: dict) -> bool:
    script = paso["script"]
    nombre = paso["nombre"]
    obligatorio = paso.get("obligatorio", True)
    args = paso.get("args", [])

    print("\n" + "=" * 70)
    print(f"▶ {nombre}")
    print(f"   Script: {script}")
    if args:
        print(f"   Args: {' '.join(args)}")
    print("=" * 70)

    if not Path(script).exists():
        mensaje = f"⚠ No se encuentra el archivo {script}"
        if obligatorio:
            print(mensaje)
            return False
        print(mensaje + " — paso omitido")
        return True

    resultado = subprocess.run([sys.executable, script, *args])

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
        if not ejecutar_paso(paso):
            sys.exit(1)

    fin = datetime.now()
    print("\n" + "=" * 70)
    print("🎉 Pipeline completado correctamente")
    print(f"Duración aproximada: {fin - inicio}")
    print("Revisa docs/index.html, docs/aula.html y docs/fichas-aula/.")
    print("Newsletter: ejecutar generar_newsletter.py manualmente cuando toque publicar edición.")
    print("=" * 70)


if __name__ == "__main__":
    main()
