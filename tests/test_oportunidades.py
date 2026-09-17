import copy
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

from oportunidades import (
    CAMPOS, aprobar, candidatos, caso_newsletter, cargar_aprobados,
    guardar_json, preparar_borrador, render_caso, render_publicados,
    teaser_html, validar_caso, TextoArticulo,
)
from generar_newsletter import render_html, render_markdown, period_info
from web_ui_common import nav_html


def noticia(url='https://example.com/noticia', fecha='2026-09-15'):
    return {'titulo': 'Nuevas necesidades de entrega para pequeños comercios',
            'url': url, 'fecha_publicacion': fecha,
            'resumen': 'Los pequeños comercios necesitan reducir los costes de entrega y mejorar la experiencia del cliente. ' * 2,
            'valor_docente': 'alto'}


def respuesta():
    return {'apta': True, 'motivo': 'Cambio concreto y cliente identificable.',
            'puntuaciones': {k: 4 for k in ('cambio', 'cliente', 'solucion', 'aula')},
            'contenido': {k: 'Texto educativo: ' + v for k, v in CAMPOS.items()}}


class OportunidadesTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.drafts, self.approved, self.docs = [self.root / p for p in ('drafts', 'approved', 'docs')]

    def generar(self, result=None, noticias=None):
        with patch('oportunidades.obtener_fuente', return_value='Artículo original. ' * 100), patch('oportunidades.consultar_modelo', return_value=result or respuesta()):
            return preparar_borrador(noticias or [noticia()], '2026-09-Q2', date(2026, 9, 16), self.drafts, self.approved)

    def aprobar(self):
        self.generar()
        return aprobar(self.drafts / '2026-09-Q2/caso.json', 'Docente', True, self.approved)

    def test_excluye_antiguas_futuras_sin_fecha_y_duplicadas(self):
        noticias = [noticia(), noticia('https://example.com/noticia?utm_source=email'),
                    noticia('https://example.com/vieja', '2026-07-01'),
                    noticia('https://example.com/futura', '2026-09-17'),
                    noticia('javascript:alert(1)'), noticia('https://example.com/sinfecha', '')]
        self.assertEqual(len(candidatos(noticias, [], date(2026, 9, 16))), 1)

    def test_no_repite_noticia_aprobada(self):
        anterior = {'fuente': {'url': noticia()['url']}, 'periodo': '2026-09-Q1', 'tema': 'logistica'}
        self.assertEqual(candidatos([noticia()], [anterior], date(2026, 9, 16)), [])

    def test_borrador_privado_no_publicable_y_reutilizable(self):
        caso = self.generar()
        self.assertEqual(caso['estado'], 'BORRADOR')
        self.assertFalse(self.docs.exists())
        with self.assertRaises(ValueError):
            render_caso(caso)
        with self.assertRaises(ValueError):
            teaser_html(caso)
        with patch('oportunidades.obtener_fuente', side_effect=AssertionError('No debe descargarse otra vez')):
            self.assertEqual(preparar_borrador([noticia()], '2026-09-Q2', date(2026,9,16), self.drafts, self.approved), caso)

    def test_descarta_sin_forzar_y_sin_fallback_del_resumen(self):
        self.assertIsNone(self.generar({'apta': False, 'motivo': 'Publicidad'}))
        self.assertFalse((self.drafts / '2026-09-Q2/caso.json').exists())
        with patch('oportunidades.obtener_fuente', side_effect=ValueError('Sin acceso')), patch('oportunidades.consultar_modelo') as llm:
            self.assertIsNone(preparar_borrador([noticia()], '2026-09-Q2', date(2026,9,16), self.drafts, self.approved))
            llm.assert_not_called()

    def test_rechaza_respuesta_incompleta_o_puntuaciones_bajas(self):
        result = respuesta()
        result['puntuaciones']['cliente'] = 2
        self.assertIsNone(self.generar(result))
        result = respuesta()
        del result['contenido']['validacion']
        self.assertIsNone(self.generar(result))

    def test_aprobacion_necesita_verificacion_y_detecta_edicion_posterior(self):
        self.generar()
        path = self.drafts / '2026-09-Q2/caso.json'
        with self.assertRaises(ValueError):
            aprobar(path, 'Docente', False, self.approved)
        approved = aprobar(path, 'Docente', True, self.approved)
        c = json.loads(approved.read_text())
        c['contenido']['solucion'] = 'Modificada tras revisar'
        guardar_json(approved, c)
        with self.assertRaises(ValueError):
            cargar_aprobados(self.approved)

    def test_web_y_newsletter_solo_con_aprobado_renderizado_del_periodo(self):
        self.aprobar()
        self.assertIsNone(caso_newsletter('2026-09-Q2', self.approved, self.docs))
        render_publicados(self.approved, self.docs)
        c = caso_newsletter('2026-09-Q2', self.approved, self.docs)
        self.assertIsNotNone(c)
        self.assertIsNone(caso_newsletter('2026-10-Q1', self.approved, self.docs))
        page = (self.docs / 'oportunidades' / (c['id'] + '.html')).read_text()
        self.assertIn('<details', page)
        self.assertNotIn('<details open', page)
        periodo = period_info(date(2026,9,16), 'quincenal')
        self.assertIn(c['id'], render_html([noticia()], periodo, 'quincenal', c))
        self.assertIn(c['id'], render_markdown([noticia()], periodo, 'quincenal', c))
        self.assertNotIn('De la noticia a la oportunidad', render_html([noticia()], periodo, 'quincenal'))

    def test_html_escapado_y_rutas_seguras(self):
        c = self.generar()
        c['contenido']['titulo'] = '<script>alert(1)</script>'
        self.assertIn('&lt;script&gt;', render_caso(c, preview=True))
        c['id'] = '../../index'
        with self.assertRaises(ValueError):
            render_caso(c, preview=True)
        self.assertIn('href="../newsletter/index.html"', nav_html('oportunidades', base_prefix='../'))
        self.assertIn('href="../oportunidades/index.html"', nav_html('newsletter', base_prefix='../'))

    def test_extrae_cuerpo_sin_confundirlo_con_menus_y_relacionadas(self):
        parser = TextoArticulo()
        cuerpo = 'Información del artículo original. ' * 40
        parser.feed('<div>' + 'Titulares relacionados. ' * 2000 + '</div>'
                    + '<article><div class="td-post-content">'
                    + '<p>' + cuerpo + '</p><script>Instrucción ajena</script>'
                    + '</div></article>')
        self.assertEqual(parser.texto(), cuerpo.strip())

    def test_indice_sin_casos_no_revela_borradores(self):
        self.generar()
        render_publicados(self.approved, self.docs)
        self.assertEqual([p.name for p in (self.docs / 'oportunidades').iterdir()], ['index.html'])


if __name__ == '__main__':
    unittest.main()
