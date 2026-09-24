# Mexico Toys Sales & Inventory Analysis

Proyecto de portafolio de análisis de ventas e inventario de Maven Toys en México. Integra SQL, Excel y Tableau para explicar el crecimiento, la presión sobre el margen y los desbalances entre inventario y demanda reciente.

El resultado principal es el workbook interactivo [`dashboard/mexico_toys_tableau.twb`](dashboard/mexico_toys_tableau.twb), con las vistas **Overview** e **Inventory Action**. Las imágenes conceptuales del repositorio son referencias de dirección visual y no capturas del dashboard terminado.

## Resultado ejecutivo

- **USD 14,4 M** de ingresos y **USD 4,0 M** de ganancia bruta en el período analizado.
- Entre enero y septiembre de 2023, los ingresos crecieron **30,9% interanual**, mientras el margen bruto bajó de **29,6% a 26,2%**.
- El inventario reportado representa **USD 300,2 K al costo** y aproximadamente **16,5 días de cobertura**.
- **77 combinaciones tienda-producto** aparecen sin stock pese a registrar demanda reciente.
- **USD 150,4 K** están concentrados en inventario con más de 30 días de cobertura o sin ventas recientes.

El workbook incluye dos vistas conectadas mediante navegación:

1. **Overview:** ingresos, unidades, ganancia, margen y evolución comercial.
2. **Inventory Action:** cobertura, riesgo de stockout, capital inmovilizado y prioridades de reposición.

## Stack

- **SQLite:** modelo relacional, métricas y consultas reproducibles.
- **Excel:** revisión ejecutiva, anotaciones de hallazgos y tablas listas para explorar.
- **Tableau:** dashboard ejecutivo con páginas de desempeño e inventario.

## Estructura

- `data/raw/`: archivos originales, sin modificaciones.
- `data/processed/`: dimensiones limpias e inventario reportado.
- `data/export/`: resultados pequeños listos para Excel y dashboard.
- `sql/`: esquema, vistas y consultas de negocio.
- `scripts/`: reconstrucción completa del proyecto.
- `docs/`: metodología, hallazgos, limitaciones y diseño del dashboard.
- `dashboard/mexico_toys_tableau.twb`: workbook final de Tableau.
- `dashboard/`: assets, especificación visual y guía de construcción.
- `outputs/`: workbook de análisis generado.

## Reproducir

Desde la raíz del proyecto:

```bash
python3 scripts/build_project.py
```

Esto vuelve a crear `sql/mexico_toys.db`, los archivos limpios y todos los exports analíticos.

Para abrir el dashboard, usa `dashboard/mexico_toys_tableau.twb`. Si Tableau solicita localizar las fuentes, apunta a:

- `data/export/dashboard_sales.csv`
- `data/export/inventory_analysis.csv`
- `data/export/weekday_performance.csv`

El análisis completo también está disponible en `outputs/01a0c449-42d0-7ea3-b248-27cdd5d48ea7/mexico_toys_analysis.xlsx`.

## Preguntas de negocio

1. ¿Qué categorías generan la mayor ganancia bruta? ¿Es igual según la ubicación de las tiendas?
2. ¿Qué tendencias temporales aparecen en ventas y rentabilidad?
3. ¿Qué combinaciones tienda-producto tienen stock cero pese a mostrar demanda reciente?
4. ¿Cuánto dinero está invertido en inventario y cuántos días puede durar?

La pregunta de ventas perdidas se presenta como **exposición de demanda**, no como ventas históricas perdidas, porque el dataset solo contiene una fotografía de inventario sin movimientos ni fechas de reposición.

## Documentación

- [Hallazgos](docs/findings.md)
- [Metodología](docs/methodology.md)
- [Limitaciones](docs/limitations.md)
- [Validación](docs/validation_report.md)
- [Especificación del dashboard](docs/dashboard_spec.md)
- [Auditoría del concepto visual](docs/visual_concept_audit.md)

## Concepto visual

La siguiente imagen fue una exploración estética temprana. Sirve como referencia para color, jerarquía y profundidad visual, pero **no es una exportación de Tableau**. Los KPI y llamados ejecutivos fueron validados; la geometría de algunos gráficos es ilustrativa y no debe leerse como una representación exacta de los datos.

![Concepto visual de Mexico Toys](dashboard/mexico_toys_dashboard_mockup_v2.png)
