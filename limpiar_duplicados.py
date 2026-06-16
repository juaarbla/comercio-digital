#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Limpia duplicados en noticias_resumidas.json y noticias_clasificadas.json.

Uso:
    python limpiar_duplicados.py
"""

import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode


from paths import NOTICIAS_RESUMIDAS, NOTICIAS_CLASIFICADAS

ARCHIVOS = [NOTICIAS_RESUMIDAS, NOTICIAS_CLASIFICADAS]


def normalizar_url(url: str) -> str:
    url = str(url or "").strip()
    if not url:
        return ""
    try:
        p = urlsplit(url)
        query = []
        for k, v in parse_qsl(p.query, keep_blank_values=True):
            kl = k.lower()
            if kl.startswith("utm_") or kl in {"fbclid", "gclid"}:
                continue
            query.append((k, v))
        return urlunsplit((p.scheme.lower(), p.netloc.lower().replace("www.", ""), p.path.rstrip("/"), urlencode(query), ""))
    except Exception:
        return url.rstrip("/").lower()


def normalizar_titulo(titulo: str) -> str:
    texto = str(titulo or "").strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"[^a-z0-9]+", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def puntuacion(n: dict) -> int:
    score = 0
    for campo, puntos in [
        ("imagen_url", 20),
        ("pregunta_aula", 10),
        ("actividad_breve", 10),
        ("conceptos_clave", 10),
        ("ra_justificacion", 10),
        ("ra_asignado", 5),
        ("modulo_asignado", 5),
    ]:
        if n.get(campo):
            score += puntos
    score += min(len(str(n.get("resumen") or "")), 500) // 20
    score += len([k for k, v in n.items() if v not in ("", None, [], {})])
    return score


def cargar(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data, None
    for key in ("noticias", "items", "data"):
        if isinstance(data.get(key), list):
            return data[key], key
    raise ValueError(f"No se encontró lista en {path}")


def guardar(path: Path, noticias, key):
    if key is None:
        data = noticias
    else:
        data = json.loads(path.read_text(encoding="utf-8"))
        data[key] = noticias
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def deduplicar(noticias):
    vistas = {}
    eliminadas = 0
    for n in noticias:
        url = normalizar_url(n.get("url", ""))
        titulo = normalizar_titulo(n.get("titulo", ""))
        clave = ("url", url) if url else ("titulo", titulo)

        if not clave[1]:
            clave = ("id", id(n))

        if clave not in vistas:
            vistas[clave] = n
            continue

        if puntuacion(n) > puntuacion(vistas[clave]):
            vistas[clave] = n
        eliminadas += 1

    return list(vistas.values()), eliminadas


def main():
    total = 0
    for path in ARCHIVOS:
        if not path.exists():
            print(f"No existe {path}, omitido.")
            continue

        noticias, key = cargar(path)
        limpias, eliminadas = deduplicar(noticias)

        if eliminadas:
            backup = path.with_suffix(path.suffix + ".backup_duplicados")
            backup.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
            guardar(path, limpias, key)

        print(f"{path}: {len(noticias)} → {len(limpias)} ({eliminadas} duplicados eliminados)")
        total += eliminadas

    print(f"\nDuplicados eliminados en total: {total}")


if __name__ == "__main__":
    main()
