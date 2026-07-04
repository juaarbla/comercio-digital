# ROADMAP v0.6 · Observabilidad, diagnóstico de fuentes y preparación para despliegue permanente

## 1. Contexto

La versión **v0.5** del proyecto Comercio Digital / Agregador educativo se centró en mejorar el control de calidad, la coherencia visual y el seguimiento básico del sistema.

Al cierre de v0.5 el proyecto se encuentra en un estado estable:

* pipeline diario funcionando desde Windows mediante el Programador de tareas;
* newsletter quincenal funcionando;
* web publicada correctamente en GitHub Pages;
* documentación actualizada;
* repositorio limpio;
* generación de informe de pipeline operativa;
* cabecera, navegación y footer unificados mediante `web_ui_common.py`;
* integración visual coherente entre portada, aula y newsletter.

La siguiente fase no debe centrarse todavía en ampliar funcionalidades visibles, sino en mejorar la capacidad del sistema para **explicar qué ocurre en cada ejecución**.

---

## 2. Objetivo general de la v0.6

El objetivo de la v0.6 es convertir el agregador en un sistema más transparente, fiable y fácil de mantener.

La fase se centrará en:

* diagnosticar el estado de las fuentes;
* mejorar el informe diario del pipeline;
* detectar errores o anomalías de forma más clara;
* resumir el estado global del sistema mediante un semáforo;
* preparar la futura migración a Raspberry Pi o despliegue permanente, sin ejecutarla todavía.

La idea principal es pasar de:

> “El pipeline se ha ejecutado.”

a:

> “El pipeline se ha ejecutado, sabemos qué ha pasado, qué fuentes han funcionado, qué contenido se ha generado y si el sistema está listo para publicar.”

---

## 3. Nombre de la fase

**v0.6 · Observabilidad, diagnóstico de fuentes y preparación para despliegue permanente**

---

## 4. Principios de trabajo

Durante esta fase se seguirán estos criterios:

1. No tocar código sin revisar antes el objetivo concreto.
2. Evitar cambios grandes de arquitectura.
3. No introducir nuevas funcionalidades visuales importantes.
4. No migrar todavía a Raspberry Pi.
5. Priorizar diagnóstico, trazabilidad y mantenimiento.
6. Documentar cada cambio relevante.
7. Mantener el proyecto siempre en estado ejecutable.

---

## 5. Líneas de trabajo

### 5.1. Diagnóstico avanzado de fuentes

Crear o mejorar un sistema que permita conocer el estado de cada fuente del agregador.

El diagnóstico debería mostrar, como mínimo:

* nombre de la fuente;
* URL o feed asociado;
* estado de la última consulta;
* número de noticias obtenidas;
* fecha de última ejecución correcta;
* posibles errores;
* fuentes sin novedades;
* fuentes caídas o problemáticas.

Ejemplo orientativo:

```text
Fuente                    Estado     Noticias     Observación
HubSpot Marketing          OK         4            Nueva fuente activa
Marketing4eCommerce        OK         6            Funcionando correctamente
Fuente X                   ERROR      0            Timeout
Fuente Y                   OK         0            Sin novedades
```

Posibles entregables:

* `diagnosticar_fuentes.py`
* sección específica en el informe diario
* log histórico de fuentes

Prioridad: **alta**

---

### 5.2. Mejora del informe diario del pipeline

Ampliar `generar_informe_pipeline.py` para que el informe diario sea más útil como herramienta de supervisión.

El informe podría incluir:

* fecha y hora de ejecución;
* duración aproximada;
* estado general;
* número total de noticias;
* número de noticias nuevas;
* número de noticias clasificadas;
* número de noticias para aula;
* número de fichas generadas;
* estado de la newsletter;
* fuentes activas;
* fuentes con error;
* fuentes sin novedades;
* resumen Git;
* archivos modificados;
* avisos o recomendaciones.

Posible salida:

```text
Estado general: VERDE

Noticias totales: 174
Noticias nuevas: 8
Noticias para aula: 25
Fichas generadas: 10
Newsletter activa: Sí
Fuentes con error: 0
Repo Git: limpio
```

Prioridad: **alta**

---

### 5.3. Semáforo de salud del sistema

Definir un estado global del sistema con tres niveles:

#### Verde

El sistema funciona correctamente.

Condiciones posibles:

* pipeline completado;
* web generada;
* fuentes principales funcionando;
* sin errores críticos;
* repo limpio o con cambios esperados;
* newsletter localizada correctamente.

#### Amarillo

El sistema funciona, pero requiere revisión.

Condiciones posibles:

* alguna fuente falla;
* hay fuentes sin novedades durante varios días;
* se generan menos noticias de lo esperado;
* hay cambios Git pendientes;
* alguna sección secundaria no se actualiza correctamente.

#### Rojo

El sistema no debería considerarse correcto.

Condiciones posibles:

* falla el pipeline;
* no se genera `index.html`;
* no se genera `aula.html`;
* error crítico en newsletter;
* no se puede acceder a los datos base;
* fallo de publicación.

Prioridad: **alta**

---

### 5.4. Revisión del valor docente generado

Analizar si el sistema está generando contenido útil para el objetivo docente.

Indicadores posibles:

* noticias con RA asignado;
* noticias con conceptos clave;
* noticias candidatas a ficha de aula;
* noticias candidatas a newsletter;
* distribución por módulo:

  * Comercio Electrónico;
  * Comercio Digital Internacional;
  * Digitalización;
  * IA para Marketing y Comercio;
* equilibrio entre tipos de uso:

  * actividad;
  * debate;
  * caso de empresa;
  * seguimiento;
  * ejemplo de aula.

El objetivo no es cambiar todavía el clasificador, sino observar si los resultados tienen sentido.

Prioridad: **media-alta**

---

### 5.5. Preparación para Raspberry Pi / despliegue permanente

Preparar la documentación previa para una futura migración a Raspberry Pi o servidor permanente.

No se realizará todavía la migración.

Se documentará:

* requisitos del entorno;
* instalación de Python;
* creación de entorno virtual;
* dependencias;
* variables `.env`;
* rutas que habría que adaptar de Windows a Linux;
* equivalentes de los `.bat` en `.sh`;
* uso de `cron`;
* gestión de logs;
* estrategia de publicación;
* pruebas mínimas;
* rollback.

Posible entregable:

```text
_documentacion/README_DESPLIEGUE_RASPBERRY.md
```

Prioridad: **media**

---

## 6. Fuera de alcance en v0.6

Para evitar dispersión, quedan fuera de esta fase:

* migración real a Raspberry Pi;
* rediseño visual completo;
* panel de control local;
* integración MCP;
* cambios profundos en newsletter;
* automatización nueva de envío por correo;
* refactor masivo del proyecto;
* cambios importantes en el modelo de clasificación;
* cambios grandes en SEO;
* nuevas secciones públicas de la web.

Estas líneas podrán abordarse en fases posteriores.

---

## 7. Entregables previstos

### Entregables principales

* `_documentacion/ROADMAP_v0.6.md`
* mejora de `generar_informe_pipeline.py`
* posible creación de `diagnosticar_fuentes.py`
* informe diario más completo en `logs/`
* bloque de estado general del sistema
* resumen de diagnóstico de fuentes
* actualización de `DIARIO_PROYECTO.md`

### Entregables secundarios

* `_documentacion/README_DESPLIEGUE_RASPBERRY.md`
* checklist previa de migración
* criterios de semáforo documentados

---

## 8. Orden de trabajo propuesto

### Paso 1 · Cierre formal de v0.5

Comprobar que el repositorio sigue limpio:

```powershell
git status
```

Crear etiqueta:

```powershell
git tag v0.5
git push origin v0.5
```

---

### Paso 2 · Crear la hoja de ruta v0.6

Crear:

```text
_documentacion/ROADMAP_v0.6.md
```

Añadir este documento como punto de partida.

---

### Paso 3 · Revisar archivos existentes

Antes de tocar código, revisar:

```text
generar_informe_pipeline.py
run_pipeline.py
publicar_web_diaria.bat
feeds.json
news_aggregator.py
noticias.json / noticias_clasificadas.json
DIARIO_PROYECTO.md
```

Objetivo: entender qué datos ya existen y cuáles se pueden reutilizar.

---

### Paso 4 · Diseñar el informe mejorado

Definir qué información debe aparecer en el informe diario.

No programar todavía hasta decidir:

* campos obligatorios;
* campos opcionales;
* formato del informe;
* ubicación;
* si habrá histórico;
* si se mostrará estado verde/amarillo/rojo.

---

### Paso 5 · Diagnóstico de fuentes

Diseñar el sistema de diagnóstico.

Preguntas a resolver:

* ¿se analiza desde `feeds.json`?
* ¿se guarda histórico de errores?
* ¿se integra en el pipeline?
* ¿se genera como informe independiente?
* ¿se muestra en el informe general?

---

### Paso 6 · Implementación progresiva

Implementar solo cuando los pasos anteriores estén claros.

Orden recomendado:

1. mejorar informe actual;
2. añadir semáforo;
3. añadir diagnóstico básico de fuentes;
4. documentar resultados;
5. probar pipeline completo;
6. revisar Git;
7. cerrar fase si procede.

---

## 9. Criterios de cierre de v0.6

La fase podrá considerarse cerrada cuando:

* exista una hoja de ruta documentada;
* el informe diario sea más completo;
* el sistema indique estado general;
* las fuentes puedan revisarse de forma clara;
* se identifiquen errores o anomalías sin revisar manualmente todo el proyecto;
* exista una checklist previa para Raspberry;
* el pipeline siga funcionando correctamente;
* la documentación esté actualizada;
* el repositorio quede limpio.

---

## 10. Posible fase siguiente

Si la v0.6 queda cerrada correctamente, la siguiente fase natural sería:

**v0.7 · Despliegue permanente en Raspberry Pi o servidor**

Esa fase abordaría:

* migración real del entorno;
* adaptación de rutas;
* scripts `.sh`;
* programación con `cron`;
* ejecución desatendida;
* logs persistentes;
* recuperación ante fallos;
* publicación automática desde entorno permanente.

---

## 11. Decisión inicial

La v0.6 queda orientada a:

```text
Observabilidad + diagnóstico + preparación para despliegue permanente
```

No se tocará código hasta revisar y validar esta hoja de ruta.

## 17. Primera mejora implementada: informe post-pipeline v0.6

Se implementa la primera mejora funcional de la v0.6 sobre `generar_informe_pipeline.py`.

La mejora convierte el informe post-pipeline en una herramienta más clara de observabilidad del sistema, sin modificar el funcionamiento del pipeline principal ni la publicación diaria.

### Cambios realizados

- Se añade un estado general del sistema mediante semáforo:
  - VERDE;
  - AMARILLO;
  - ROJO.

- Se separan las incidencias en tres niveles:
  - alertas críticas;
  - avisos;
  - recomendaciones.

- Se añade comprobación de archivos clave de la web:
  - `docs/index.html`;
  - `docs/aula.html`;
  - `docs/newsletter/index.html`;
  - `docs/assets/style.css`.

- Se añade diagnóstico básico de fuentes desde `feeds.json`:
  - fuentes configuradas;
  - fuentes activas;
  - fuentes inactivas;
  - fuentes activas por tipo;
  - fuentes activas por módulo declarado;
  - fuentes activas sin módulo declarado;
  - fuentes inactivas;
  - fuentes con nota;
  - fuentes con configuración `source`.

- Se mejora el bloque de última newsletter detectada.

- Se añade un control específico de noticias marcadas para ficha sin actividad breve.

- Se elimina la recomendación automática sobre fuentes activas sin módulo declarado, ya que se consideran fuentes transversales o pendientes de clasificación automática y no un problema por sí mismas.

### Resultado de la prueba

Tras ejecutar:

```powershell
python .\generar_informe_pipeline.py

---

## 18. Segunda mejora implementada: diagnóstico de equilibrio de fuentes y módulos

Se revisa el aviso detectado en el informe post-pipeline sobre baja presencia de Marketing Digital y concentración de noticias procedentes de `ecommerce-news.es`.

Esta mejora forma parte del segundo bloque de la v0.6, centrado en interpretar mejor los datos del informe antes de modificar clasificadores, fuentes o lógica del pipeline.

### Diagnóstico realizado

Se revisan los archivos:

- `noticias_clasificadas.json`;
- `clasificador_ra.py`;
- `news_aggregator.py`;
- `generar_informe_pipeline.py`.

La revisión confirma que Marketing Digital aparece como módulo original en algunas fuentes, pero no funciona como módulo curricular final independiente.

Según las reglas actuales de clasificación, las noticias de origen Marketing Digital se reclasifican normalmente como:

- Comercio Electrónico;
- IA para Marketing y Comercio.

Por tanto, la baja presencia final de Marketing Digital no es un error técnico ni un problema de clasificación, sino una consecuencia esperada del diseño curricular actual.

También se confirma que la concentración de `ecommerce-news.es` se calcula sobre el histórico clasificado acumulado, no solo sobre la ejecución diaria.

### Interpretación de Marketing Digital

Marketing Digital se mantiene como fuente temática de entrada.

No se considera un módulo curricular final independiente dentro de la clasificación actual.

El informe debe reflejar esta diferencia para evitar falsos avisos.

La lectura correcta es:

```text
Marketing Digital aporta noticias al sistema.
Después, esas noticias se asignan curricularmente a Comercio Electrónico o IA para Marketing y Comercio.
```

### Interpretación de la concentración de fuentes

El aviso sobre `ecommerce-news.es` no indica necesariamente que la última ejecución haya estado desequilibrada.

Indica que, en el histórico acumulado de noticias clasificadas, esa fuente tiene un peso elevado.

Por tanto, el texto del informe debe aclarar que el porcentaje se calcula sobre el histórico clasificado.

### Cambios realizados

Se ajusta `generar_informe_pipeline.py` para:

- eliminar el aviso automático sobre baja presencia de Marketing Digital;
- eliminar la recomendación automática de revisar fuentes de Marketing Digital;
- aclarar que la concentración de una fuente se mide sobre el histórico clasificado;
- añadir una sección específica titulada `Observación sobre Marketing Digital`.

### Criterio adoptado

Marketing Digital se mantiene como fuente temática de entrada, pero no como módulo curricular final independiente.

La baja presencia de Marketing Digital como módulo relacionado no debe generar aviso automático.

La concentración de una fuente debe mantenerse como aviso, pero indicando que se refiere al histórico clasificado.

### Archivos modificados

Se modifica:

- `generar_informe_pipeline.py`.

No se modifican:

- `clasificador_ra.py`;
- `news_aggregator.py`;
- `noticias_clasificadas.json`;
- `feeds.json`.

### Resultado esperado en el informe

El informe post-pipeline debe incluir una sección específica:

```md
## Observación sobre Marketing Digital
```

Y debe dejar de mostrar como aviso o recomendación:

```text
Marketing Digital aparece con muy poca presencia.
Revisar fuentes específicas de marketing digital si se mantiene baja presencia.
```

El aviso de concentración de fuente debe quedar formulado como:

```text
La fuente ecommerce-news.es concentra el 71.7% del histórico clasificado.
```

### Conclusión

El bloque 2 de v0.6 queda orientado a mejorar la interpretación del informe, no a modificar el clasificador.

La conclusión principal es que no hay fallo técnico:

1. Marketing Digital actúa como fuente temática, no como módulo curricular final.
2. La concentración de `ecommerce-news.es` afecta al histórico acumulado, no necesariamente a la última ejecución diaria.

La siguiente línea de trabajo recomendada será decidir si conviene crear un diagnóstico temporal que separe:

- histórico acumulado;
- últimas noticias añadidas;
- distribución por fuente en la última ejecución;
- distribución por módulo en la última ejecución.

---

## 19. Tercera mejora implementada: separación entre histórico acumulado y última ejecución

Se implementa una mejora en `generar_informe_pipeline.py` para diferenciar los datos acumulados del histórico completo y los datos correspondientes a la última ejecución detectada.

Hasta este punto, el informe post-pipeline mostraba correctamente la distribución general de noticias, fuentes y módulos, pero todos los porcentajes se calculaban sobre el histórico completo de `noticias_clasificadas.json`.

Esto podía generar una duda importante:

```text
¿La concentración de una fuente es un problema actual o solo arrastre histórico?
```

### Diagnóstico realizado

Se revisan los archivos:

- `noticias_resumidas.json`;
- `noticias_clasificadas.json`;
- `historial.json`;
- `generar_informe_pipeline.py`.

Los archivos de noticias incluyen el campo `procesado_en`, que permite identificar la fecha en la que una noticia fue resumida y clasificada.

Ese campo se utiliza para detectar la última fecha de ejecución disponible y separar las noticias correspondientes a esa fecha.

### Cambios realizados

Se añaden funciones auxiliares a `generar_informe_pipeline.py`:

```python
fecha_procesado()
obtener_ultima_fecha_procesado()
filtrar_por_fecha_procesado()
```

Estas funciones permiten:

- extraer la fecha `YYYY-MM-DD` del campo `procesado_en`;
- detectar la fecha más reciente disponible;
- filtrar noticias resumidas y clasificadas de esa última fecha.

### Nueva sección del informe

Se añade una nueva sección al informe:

```md
## Última ejecución detectada
```

Esta sección muestra:

- fecha detectada mediante `procesado_en`;
- noticias resumidas en esa fecha;
- noticias clasificadas en esa fecha;
- noticias marcadas para ficha en esa fecha;
- noticias marcadas para newsletter en esa fecha;
- fuentes presentes en la última ejecución;
- módulos relacionados en la última ejecución;
- valor docente de las noticias de la última ejecución;
- tipo de uso de las noticias de la última ejecución.

### Nuevo aviso de concentración reciente

Además del aviso sobre concentración en el histórico acumulado, se añade un aviso específico para la última ejecución.

Si una fuente concentra más del 80 % de las noticias de la última ejecución, el informe genera un aviso como:

```text
La fuente ecommerce-news.es concentra el 90.0% de la última ejecución detectada.
```

### Resultado observado

En la prueba realizada, la última ejecución detectada corresponde a:

```text
2026-07-03
```

Resultado observado:

- noticias resumidas en la última ejecución: 10;
- noticias clasificadas en la última ejecución: 10;
- fuente principal: `ecommerce-news.es`;
- concentración de `ecommerce-news.es` en la última ejecución: 90 %;
- segunda fuente detectada: `blog.hubspot.es`.

### Interpretación

La concentración de `ecommerce-news.es` no es solo un efecto del histórico acumulado.

También aparece en la última ejecución detectada.

Esto no implica necesariamente un fallo técnico, pero sí confirma que el sistema depende mucho de esa fuente para generar volumen diario de noticias.

### Criterio adoptado

Se mantiene el aviso de concentración histórica.

Se añade un aviso separado de concentración en la última ejecución.

De este modo el informe permite distinguir entre:

- desequilibrio acumulado;
- desequilibrio reciente;
- funcionamiento técnico correcto.

### Archivos modificados

Se modifica:

- `generar_informe_pipeline.py`.

No se modifican:

- `news_aggregator.py`;
- `clasificador_ra.py`;
- `noticias_resumidas.json`;
- `noticias_clasificadas.json`;
- `historial.json`;
- `feeds.json`.

### Conclusión

El bloque 3 de v0.6 mejora la capacidad de diagnóstico temporal del sistema.

A partir de ahora el informe permite saber no solo cómo está el histórico completo, sino también qué ha ocurrido en la última ejecución detectada.

La siguiente línea de trabajo recomendada será revisar si conviene equilibrar las fuentes mediante:

- nuevas fuentes activas;
- revisión de fuentes inactivas;
- límites por fuente;
- diagnóstico diario de fuentes con cero noticias;
- separación entre fuentes principales y fuentes complementarias.

---

## 20. Cuarta mejora implementada: diagnóstico de aportación de fuentes activas

Se implementa una mejora en `generar_informe_pipeline.py` para analizar la aportación real de las fuentes activas configuradas en `feeds.json`.

Hasta este punto, el informe permitía saber qué fuente concentraba más noticias en el histórico y en la última ejecución detectada.

Sin embargo, todavía faltaba responder una pregunta importante:

```text
¿Qué fuentes activas están aportando noticias y cuáles no?
```

Esta mejora cruza la configuración de fuentes activas con las noticias realmente detectadas.

### Diagnóstico realizado

Se revisan los archivos:

- `feeds.json`;
- `noticias_clasificadas.json`;
- `generar_informe_pipeline.py`.

La revisión confirma que el informe ya podía contar noticias por `fuente_detectada`, pero no cruzaba esa información con las fuentes declaradas como activas en `feeds.json`.

Por tanto, una fuente podía estar activa en configuración pero no aparecer en el histórico ni en la última ejecución.

### Cambios realizados

Se añaden nuevas funciones auxiliares a `generar_informe_pipeline.py`:

```python
fuente_configurada()
diagnosticar_aportacion_fuentes()
```

La función `fuente_configurada()` obtiene una clave de fuente esperada a partir de:

1. el campo `source`, si existe;
2. el dominio de la URL, si no existe `source`.

La función `diagnosticar_aportacion_fuentes()` cruza:

- fuentes activas declaradas en `feeds.json`;
- noticias detectadas en el histórico;
- noticias detectadas en la última ejecución.

### Nueva sección del informe

Se añade una nueva sección:

```md
## Aportación de fuentes activas
```

Esta sección muestra una tabla con:

- fuente activa;
- clave utilizada para el cruce;
- módulo declarado;
- número de noticias aportadas al histórico;
- número de noticias aportadas en la última ejecución detectada.

Ejemplo de lectura esperada:

```md
| Fuente activa | Clave | Módulo | Histórico | Última ejecución |
|---|---|---|---:|---:|
| ecommerce-news.es/... | ecommerce-news.es | Comercio Electrónico | 177 | 9 |
| blog.hubspot.es/... | blog.hubspot.es | Marketing Digital | 4 | 1 |
```

### Nuevos indicadores

El informe añade dos indicadores:

```text
Fuentes activas sin aportación histórica
Fuentes activas sin aportación en la última ejecución
```

Estos indicadores permiten diferenciar entre:

- fuentes que no han aportado nunca;
- fuentes que sí han aportado históricamente, pero no en la última ejecución;
- fuentes que aportan de forma regular;
- fuentes activas configuradas pero posiblemente mal enlazadas.

### Nuevos avisos

Si varias fuentes activas no aportan noticias en la última ejecución, el informe genera un aviso:

```text
Hay X fuente(s) activa(s) sin aportación en la última ejecución detectada.
```

Si ninguna fuente activa aparece en la última ejecución detectada, el informe genera un aviso más fuerte:

```text
Ninguna fuente activa aparece en la última ejecución detectada.
```

### Nueva recomendación

Si existen fuentes activas sin aportación histórica, el informe añade una recomendación:

```text
Revisar fuentes activas sin aportación histórica: pueden estar mal configuradas, ser transversales o no haber generado noticias útiles todavía.
```

### Criterio adoptado

Una fuente activa sin aportación en una ejecución concreta no se considera automáticamente un error.

Puede deberse a:

- ausencia de novedades;
- poca frecuencia de publicación;
- fuente transversal;
- feed activo pero sin entradas recientes;
- configuración pendiente de ajuste.

Una fuente activa sin aportación histórica sí merece revisión, porque puede indicar:

- problema de configuración;
- clave `source` no alineada con `fuente_detectada`;
- feed inactivo aunque esté marcado como activo;
- fuente poco útil para el objetivo docente.

### Archivos modificados

Se modifica:

- `generar_informe_pipeline.py`.

No se modifican:

- `feeds.json`;
- `news_aggregator.py`;
- `clasificador_ra.py`;
- `noticias_resumidas.json`;
- `noticias_clasificadas.json`;
- `historial.json`.

### Conclusión

El bloque 4 de v0.6 mejora el diagnóstico de fuentes.

A partir de ahora el informe no solo indica qué fuente domina el histórico o la última ejecución, sino también qué fuentes activas están aportando realmente noticias al sistema.

Esto permitirá decidir con más criterio si conviene:

- añadir nuevas fuentes;
- reactivar fuentes inactivas;
- corregir fuentes activas sin aportación;
- ajustar claves `source`;
- aceptar que algunas fuentes sean complementarias;
- equilibrar mejor el origen de las noticias.

La siguiente línea de trabajo recomendada será revisar el resultado del informe tras ejecutar el pipeline y decidir si se interviene sobre `feeds.json` o si se mantiene la configuración actual.
