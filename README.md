# CIVITAS — World Lab 0.1

Prototipo individual de un laboratorio de países y economías. Interfaz en español, globo Three.js, simulación mensual y comparación de agentes adaptativos contra reglas fijas. No requiere claves ni una API de IA.

## Ejecutar

Con Python 3 instalado, desde el directorio del proyecto:

    python -m http.server 8000 --directory dist

Abre http://localhost:8000. Se necesita HTTP para cargar módulos y datos. El mundo solo avanza mientras la pestaña está abierta. Exporta el experimento a JSON antes de cerrarla; no hay guardado automático ni multijugador.

## Pruebas

Con Node.js instalado:

    node tests/engine.test.mjs

Comprueban reproducibilidad, aprendizaje, límites numéricos, divergencia de controles y efectos de fiscalización.

## Arquitectura

- dist/engine.mjs: simulación determinista; no depende de DOM ni Three.js.
- dist/app.js: controles, comparación, registro, exportación y globo.
- dist/data.json: 211 países/economías geolocalizados en la clasificación del Banco Mundial.
- dist/countries.json, population.json, income.json: respuestas originales de la API.
- tests/engine.test.mjs: comprobaciones de comportamiento.

## Datos y límites

Datos de 2024 consultados el 08/09/2026: Banco Mundial, SP.POP.TOTL y NY.GDP.PCAP.CD; metadatos del endpoint country. Licencia CC BY 4.0. 14 economías sin PIB por habitante usan un índice inicial neutro de 50 y muestran dato no disponible. Cartografía Natural Earth 1:110m (177 entidades cartográficas), dominio público: costas y fronteras generalizadas, no una resolución de disputas. Los microestados siguen disponibles por punto/selector. Fuente: https://github.com/nvkelso/natural-earth-vector/blob/master/geojson/ne_110m_admin_0_countries.geojson . La cobertura no equivale a un listado de estados soberanos.

https://data.worldbank.org/indicator/SP.POP.TOTL
https://data.worldbank.org/indicator/NY.GDP.PCAP.CD

Índice productivo inicial: clamp(15 + log10(PIB/hab./500)*30,10,90), una transformación hipotética, no una magnitud económica validada. Los demás índices sociales iniciales son comunes: no representan instituciones reales.

Gobiernos: bandido contextual con 3 estados, 6 políticas y exploración epsilon=0.12 tras probar acciones sin visitas. Actualización exponencial con paso 0.28. Es aprendizaje de recompensas, no superinteligencia ni inferencia causal. El incentivo privado a la corrupción forma parte de la función objetivo elegida y condiciona los resultados.

Ciudadanos: 24 grupos con ingresos relativos heterogéneos; bienestar y confianza adaptan gradualmente a los índices. No hay todavía aprendizaje individual, demografía, empresas, instituciones políticas reales ni comercio bilateral. El escenario fijo usa prioridades explícitas, no inmovilidad total. Comparte perturbaciones exógenas y semilla con el escenario adaptativo, pero sus dinámicas comerciales endógenas pueden divergir.

Retención: últimas 400 decisiones/eventos y últimos 601 puntos mensuales; las estimaciones de aprendizaje permanecen. La exportación incluye esos registros retenidos, ambos estados y las intervenciones. No sustituye un archivo completo de acontecimientos. Índices agregados son medias no ponderadas por población. Los resultados no predicen países reales.

## GitHub

Proyecto preparado para un repositorio independiente llamado `civitas-world-lab`. No contiene secretos. Crear el repositorio en la cuenta elegida e importar estos archivos. El prototipo no depende de una cuenta de GitHub para ejecutarse. La publicación estática puede configurarse posteriormente; la simulación compartida requerirá backend.

## Evolución prevista

1. Replicaciones con semillas configurables e intervalos de resultados.
2. Memoria y aprendizaje individual; demografía con conservación de población.
3. Mejor calibración y métricas reales con fuentes y años explícitos.
4. Persistencia en servidor y participación humana identificada.
5. Adaptador opcional de decisiones para modelos de lenguaje.

Three.js se distribuye bajo licencia MIT (ver dist/THREE-LICENSE.txt).

## Interfaz geográfica 0.2
Globo con territorios seleccionables, coordenadas y capas de confianza y producción simuladas. Ejecutar también `node tests/geography.test.mjs`. Las capas no contienen datos de inteligencia en tiempo real.
