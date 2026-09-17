from __future__ import annotations

import unittest

from web_ui_common import nav_html


class NavigationTest(unittest.TestCase):
    def test_groups_main_navigation(self) -> None:
        html = nav_html("portada")
        self.assertEqual(html.count('class="nav-group"'), 2)
        self.assertIn("<summary>Actualidad</summary>", html)
        self.assertIn("<summary>Aula</summary>", html)
        self.assertIn(">E-Commerce</a>", html)
        self.assertIn(">Recursos de aula</a>", html)
        self.assertIn(">Oportunidades</a>", html)
        self.assertIn(">Newsletter</a>", html)

    def test_marks_and_opens_current_group(self) -> None:
        html = nav_html("oportunidades", base_prefix="../")
        self.assertIn('<details>\n        <summary class="active">Aula</summary>', html)
        self.assertIn('href="../oportunidades/index.html" class="active"', html)
        self.assertIn('href="../newsletter/index.html"', html)

    def test_opens_news_group_for_section(self) -> None:
        html = nav_html("internacional")
        self.assertIn('<details>\n        <summary class="active">Actualidad</summary>', html)
        self.assertIn('href="internacional.html" class="active"', html)


if __name__ == "__main__":
    unittest.main()
