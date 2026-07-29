import unittest

from enriquecer_docente import enriquecer_uso_docente, generar_pregunta_aula


class EnriquecerDocenteTest(unittest.TestCase):
    def test_preguntas_del_mismo_modulo_se_contextualizan_con_el_titular(self):
        primera = {"titulo": "Suben las devoluciones en las tiendas online", "modulo": "Comercio Electrónico", "ra_asignado": "RA2"}
        segunda = {"titulo": "Un marketplace cambia sus métodos de pago", "modulo": "Comercio Electrónico", "ra_asignado": "RA2"}

        self.assertNotEqual(
            generar_pregunta_aula(primera, "Comercio Electrónico"),
            generar_pregunta_aula(segunda, "Comercio Electrónico"),
        )
        self.assertIn("devoluciones", generar_pregunta_aula(primera, "Comercio Electrónico"))

    def test_reemplaza_una_pregunta_legacy_aunque_no_se_fuerce(self):
        noticia = {
            "titulo": "La última milla incorpora puntos de recogida",
            "modulo": "Comercio Electrónico",
            "ra_asignado": "RA2",
            "pregunta_aula": "¿Cómo puede afectar esta noticia a una pequeña tienda online?",
        }

        enriquecida = enriquecer_uso_docente(noticia)
        self.assertNotEqual(enriquecida["pregunta_aula"], noticia["pregunta_aula"])
        self.assertIn("última milla", enriquecida["pregunta_aula"])

    def test_conserva_una_pregunta_editorial_si_no_se_fuerza(self):
        personalizada = "¿Debe asumir la plataforma el coste de esta devolución?"
        noticia = {
            "titulo": "Cambios en las devoluciones",
            "modulo": "Comercio Electrónico",
            "pregunta_aula": personalizada,
        }

        self.assertEqual(enriquecer_uso_docente(noticia)["pregunta_aula"], personalizada)


if __name__ == "__main__":
    unittest.main()
