#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Enriquece noticias clasificadas con actividades de aula más contextualizadas.

Lee:
    data/processed/noticias_clasificadas.json

Actualiza:
    actividad_breve
    actividad_origen

Uso:
    python enriquecer_actividades.py
    python enriquecer_actividades.py --sobrescribir
    python enriquecer_actividades.py --solo-generar-ficha
"""

import argparse
import json
import re
import unicodedata
from pathlib import Path

try:
    from paths import NOTICIAS_CLASIFICADAS
except Exception:
    NOTICIAS_CLASIFICADAS = Path("data/processed/noticias_clasificadas.json")


def cargar_json(ruta: Path):
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_json(ruta: Path, data):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def normalizar(texto: str) -> str:
    texto = str(texto or "").strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = re.sub(r"[^a-z0-9]+", " ", texto)
    return re.sub(r"\s+", " ", texto).strip()


def campo(n, *keys):
    for k in keys:
        if n.get(k):
            return n.get(k)
    return ""


def modulo(n):
    return campo(n, "modulo_asignado", "modulo_relacionado", "modulo") or "General"


def conceptos(n, max_items=5):
    cs = n.get("conceptos_clave") or []
    if isinstance(cs, str):
        cs = [c.strip() for c in cs.split(",") if c.strip()]
    elif isinstance(cs, list):
        cs = [str(c).strip() for c in cs if str(c).strip()]
    else:
        cs = []
    return cs[:max_items]


def ce_codigos(n):
    ce = n.get("ce_textos") or []
    codigos = []
    if isinstance(ce, list):
        for item in ce:
            if isinstance(item, dict):
                codigo = item.get("codigo") or item.get("letra")
                if codigo:
                    codigos.append(str(codigo).strip())
            elif isinstance(item, str) and item.strip():
                codigos.append(item.strip())

    if not codigos:
        ce_asignados = n.get("ce_asignados") or []
        if isinstance(ce_asignados, str):
            ce_asignados = [x.strip() for x in ce_asignados.split(",") if x.strip()]
        if isinstance(ce_asignados, list):
            ra = n.get("ra_asignado") or "RA"
            codigos = [f"{ra}{x}" for x in ce_asignados if str(x).strip()]

    return codigos[:4]


def texto_base_noticia(n):
    titulo = str(n.get("titulo") or "la noticia").strip()
    return titulo.rstrip(".")


def actividad_por_modulo_y_ra(n):
    mod = normalizar(modulo(n))
    ra = str(n.get("ra_asignado") or "").upper().strip()
    tipo = normalizar(n.get("tipo_uso") or "")
    titulo = texto_base_noticia(n)
    conceptos_txt = ", ".join(conceptos(n, 5))
    ces_txt = ", ".join(ce_codigos(n)) or "los criterios de evaluación relacionados"

    if "comercio electronico" in mod:
        if ra == "RA1":
            return (f"Analiza la noticia «{titulo}» como ejemplo de decisión de marketing digital. "
                    f"Identifica el público objetivo, el canal digital utilizado y la propuesta de valor. "
                    f"Relaciona el caso con {ces_txt} y concluye qué mejora aplicarías en una empresa de comercio electrónico.")
        if ra == "RA2":
            return (f"Estudia la noticia «{titulo}» desde el punto de vista de la compraventa online. "
                    f"Describe el flujo comercial afectado —captación, pedido, pago, entrega o devolución— y localiza dos riesgos o mejoras. "
                    f"Conecta tus conclusiones con {ces_txt}.")
        if ra == "RA3":
            return (f"Revisa la noticia «{titulo}» pensando en una tienda online o página web comercial. "
                    f"Propón tres ajustes de catálogo, contenidos, navegación o posicionamiento que podrían aplicarse. "
                    f"Justifica cada ajuste con relación a {ces_txt}.")
        if ra == "RA4":
            return (f"Analiza la noticia «{titulo}» como caso de comunicación digital en redes sociales. "
                    f"Identifica el mensaje principal, el formato de contenido y la interacción esperada con los usuarios. "
                    f"Después, diseña una publicación alternativa y relaciónala con {ces_txt}.")
        if ra == "RA5":
            return (f"Valora la noticia «{titulo}» desde la perspectiva de reputación online y participación en entornos web 2.0. "
                    f"Detecta oportunidades, riesgos de imagen y posibles respuestas de la empresa. "
                    f"Relaciona el análisis con {ces_txt}.")

    if "comercio digital internacional" in mod:
        if ra == "RA1":
            return (f"Analiza la noticia «{titulo}» como posible acción dentro de un plan de marketing digital internacional. "
                    f"Define mercado objetivo, canal de entrada y adaptación del mensaje. Relaciona la propuesta con {ces_txt}.")
        if ra == "RA2":
            return (f"Estudia la noticia «{titulo}» como ejemplo de uso de Internet para la promoción internacional. "
                    f"Identifica fuentes de información, canales digitales y criterios para valorar la oportunidad exterior. "
                    f"Conecta el análisis con {ces_txt}.")
        if ra == "RA3":
            return (f"Revisa la noticia «{titulo}» desde los servicios y herramientas de Internet que facilitan la actividad internacional. "
                    f"Explica qué servicios digitales intervienen y cómo mejoran comunicación, búsqueda de información o gestión comercial. "
                    f"Relaciona la respuesta con {ces_txt}.")
        if ra == "RA4":
            return (f"Analiza la noticia «{titulo}» desde una política de comercio electrónico internacional. "
                    f"Identifica decisiones sobre plataforma, logística, pagos, cliente o normativa. "
                    f"Propón una acción concreta y vincúlala con {ces_txt}.")
        if ra == "RA5":
            return (f"Estudia la noticia «{titulo}» desde la administración telemática, documentación o facturación electrónica internacional. "
                    f"Señala qué trámites o documentos podrían verse afectados y qué ventajas tendría digitalizarlos. "
                    f"Relaciona el análisis con {ces_txt}.")

    if "digitalizacion" in mod:
        if ra == "RA1":
            return (f"Analiza la noticia «{titulo}» para explicar qué cambio digital refleja en el sector. "
                    f"Compara la situación tradicional con la digitalizada y señala beneficios, riesgos y efectos sobre la organización. "
                    f"Relaciona tus conclusiones con {ces_txt}.")
        if ra == "RA2":
            return (f"Identifica en la noticia «{titulo}» qué tecnologías habilitadoras aparecen o podrían aplicarse. "
                    f"Elabora una tabla con tecnología, uso empresarial, ventaja y posible limitación. "
                    f"Vincula la tabla con {ces_txt}.")
        if ra == "RA3":
            return (f"Estudia la noticia «{titulo}» desde el uso de sistemas conectados, cloud, edge o servicios digitales. "
                    f"Explica qué datos circularían, dónde se procesarían y qué impacto tendría en la empresa. "
                    f"Relaciona la explicación con {ces_txt}.")
        if ra == "RA4":
            return (f"Analiza la noticia «{titulo}» como ejemplo de tecnología aplicada al sector productivo o comercial. "
                    f"Describe el proceso que se transforma, la tecnología utilizada y el beneficio esperado. "
                    f"Después, plantea una mejora adicional vinculada con {ces_txt}.")
        if ra == "RA5":
            return (f"Revisa la noticia «{titulo}» desde la gestión del dato y la ciberseguridad. "
                    f"Identifica activos digitales, datos implicados, amenazas o medidas de protección. "
                    f"Relaciona el análisis con {ces_txt}.")
        if ra == "RA6":
            return (f"Utiliza la noticia «{titulo}» como punto de partida para un mini plan de transformación digital. "
                    f"Define objetivo, proceso afectado, tecnología, responsables, indicador de éxito y riesgo principal. "
                    f"Conecta el plan con {ces_txt}.")

    if "ia para marketing" in mod or mod == "ia" or "inteligencia artificial" in mod:
        if ra == "RA1":
            return (f"Analiza la noticia «{titulo}» para identificar qué herramienta o uso de IA aparece. "
                    f"Explica qué tarea mejora, qué datos necesita y qué limitaciones tendría en una empresa real. "
                    f"Relaciona el análisis con {ces_txt}.")
        if ra == "RA2":
            return (f"Usa la noticia «{titulo}» para crear una propuesta de texto comercial con IA. "
                    f"Define objetivo, público, tono y canal; después redacta una versión inicial y una versión mejorada. "
                    f"Conecta el trabajo con {ces_txt}.")
        if ra == "RA3":
            return (f"Analiza la noticia «{titulo}» desde la creación visual, diseño o branding con IA. "
                    f"Propón un recurso visual para una campaña y justifica prompt, estilo, público y coherencia de marca. "
                    f"Relaciona la propuesta con {ces_txt}.")
        if ra == "RA4":
            return (f"Estudia la noticia «{titulo}» como caso de contenido para redes sociales. "
                    f"Diseña una mini campaña de tres publicaciones indicando objetivo, formato, mensaje y métrica de seguimiento. "
                    f"Vincula la campaña con {ces_txt}.")
        if ra == "RA5":
            return (f"Analiza la noticia «{titulo}» desde una estrategia de marketing digital apoyada en IA. "
                    f"Identifica objetivo, segmento, canal, automatización posible y métrica principal. "
                    f"Relaciona la estrategia con {ces_txt}.")
        if ra == "RA6":
            return (f"Revisa la noticia «{titulo}» como caso de atención al cliente con IA. "
                    f"Diseña un pequeño flujo de conversación: consulta inicial, respuesta del asistente, derivación y cierre. "
                    f"Relaciona el flujo con {ces_txt}.")
        if ra == "RA7":
            return (f"Analiza la noticia «{titulo}» desde el punto de vista ético y legal del uso de IA. "
                    f"Detecta riesgos sobre transparencia, privacidad, sesgos o derechos de autor y propone medidas preventivas. "
                    f"Conecta el análisis con {ces_txt}.")

    if "debate" in tipo:
        return (f"Lee la noticia «{titulo}» y prepara dos argumentos a favor y dos en contra de la decisión o tendencia que presenta. "
                f"Relaciona el debate con {ces_txt} y usa al menos tres conceptos clave: {conceptos_txt}.")

    if "caso" in tipo:
        return (f"Analiza la noticia «{titulo}» como caso de empresa. Identifica problema, decisión tomada, impacto previsto y alternativa posible. "
                f"Relaciona la respuesta con {ces_txt} y con los conceptos clave: {conceptos_txt}.")

    return (f"Analiza la noticia «{titulo}» y elabora una ficha breve con: idea principal, relación con el módulo, conceptos clave, "
            f"impacto en una empresa y conclusión personal. Conecta la respuesta con {ces_txt}.")


def debe_actualizar(n, sobrescribir: bool, solo_generar_ficha: bool) -> bool:
    if solo_generar_ficha and not n.get("generar_ficha"):
        return False

    actual = str(n.get("actividad_breve") or "").strip()
    if sobrescribir:
        return True
    if not actual:
        return True

    actual_norm = normalizar(actual)
    genericas = [
        "analiza la noticia",
        "identifica el problema principal",
        "explica como afecta",
        "relaciona la noticia",
    ]
    return sum(1 for g in genericas if g in actual_norm) >= 2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--entrada", default=str(NOTICIAS_CLASIFICADAS))
    parser.add_argument("--salida", default="")
    parser.add_argument("--sobrescribir", action="store_true")
    parser.add_argument("--solo-generar-ficha", action="store_true")
    args = parser.parse_args()

    entrada = Path(args.entrada)
    salida = Path(args.salida) if args.salida else entrada

    noticias = cargar_json(entrada)
    if not isinstance(noticias, list):
        raise ValueError("El JSON no contiene una lista de noticias.")

    actualizadas = 0
    omitidas = 0

    for n in noticias:
        if debe_actualizar(n, args.sobrescribir, args.solo_generar_ficha):
            n["actividad_breve"] = actividad_por_modulo_y_ra(n)
            n["actividad_origen"] = "plantilla_ra_ce"
            actualizadas += 1
        else:
            omitidas += 1

    guardar_json(salida, noticias)

    print("Enriquecimiento de actividades")
    print("==============================")
    print(f"Noticias totales: {len(noticias)}")
    print(f"Actividades actualizadas: {actualizadas}")
    print(f"Noticias omitidas: {omitidas}")
    print(f"Guardado en: {salida}")


if __name__ == "__main__":
    main()
