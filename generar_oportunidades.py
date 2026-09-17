"""Generación privada, aprobación editorial y renderizado de oportunidades."""
import argparse
from datetime import date
from pathlib import Path

from generar_newsletter import flatten_news, load_env_file, period_info
from oportunidades import aprobar, leer_json, preparar_borrador, render_publicados, render_caso
from paths import NOTICIAS_CLASIFICADAS, OPORTUNIDADES_BORRADORES


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    acciones = parser.add_mutually_exclusive_group()
    acciones.add_argument('--renderizar', action='store_true', help='Genera la web solo con casos aprobados.')
    acciones.add_argument('--vista-previa', type=Path, help='Regenera la vista previa de un JSON editado.')
    acciones.add_argument('--aprobar', type=Path, help='JSON revisado que se incorporará al archivo editorial.')
    parser.add_argument('--revisor', default='')
    parser.add_argument('--fuente-verificada', action='store_true')
    parser.add_argument('--entrada', type=Path, default=NOTICIAS_CLASIFICADAS)
    parser.add_argument('--fecha', type=date.fromisoformat, default=date.today())
    args = parser.parse_args()
    if args.vista_previa:
        destino = args.vista_previa.parent / 'vista-previa.html'
        destino.write_text(render_caso(leer_json(args.vista_previa), preview=True), encoding='utf-8')
        print(destino)
    elif args.aprobar:
        print(aprobar(args.aprobar, args.revisor, args.fuente_verificada))
        render_publicados()
    elif args.renderizar:
        render_publicados()
    else:
        load_env_file()
        periodo = period_info(args.fecha, 'quincenal')['slug']
        caso = preparar_borrador(flatten_news(leer_json(args.entrada)), periodo, args.fecha)
        print('Borrador disponible:' if caso else 'Sin nuevo caso apto; consulta el registro de selección:')
        print(OPORTUNIDADES_BORRADORES / periodo)


if __name__ == '__main__':
    main()
