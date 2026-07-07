## v0.7 · Bloque 6 · Schema educativo para fichas de aula

Se documenta la decisión de no usar `Article` ni `NewsArticle` para las noticias externas enlazadas por el agregador.

El motivo es que `Comercio Digital` no publica la noticia original completa, sino que actúa como agregador educativo: selecciona, resume, clasifica y propone usos docentes a partir de fuentes externas.

Se prioriza el schema educativo `LearningResource` para las fichas de aula, ya que estas sí son contenido propio del proyecto y tienen una finalidad didáctica clara.

Cambios preparados:

- ampliación de `schema_utils.py` con funciones para `LearningResource`;
- integración prevista en `generar_fichas_aula.py`;
- inserción de JSON-LD en `docs/fichas-aula/*.html`;
- validación mediante búsqueda de `application/ld+json` y `LearningResource`.

Queda fuera de este bloque la newsletter, el sitemap recursivo y el marcado de noticias externas como artículos propios.
