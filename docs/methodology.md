# Metodología

## Modelo

`sales` es la tabla de hechos principal. Se relaciona con `products`, `stores` y `calendar`. `inventory` es una fotografía separada al nivel tienda-producto.

La vista `vw_sales_enriched` calcula:

- `revenue = units × product_price`
- `cogs = units × product_cost`
- `gross_profit = units × (product_price - product_cost)`
- `gross_margin = gross_profit / revenue`

Se usa el término **ganancia bruta** porque no existen datos de alquiler, salarios, logística, impuestos u otros gastos operativos.

## Períodos comparables

Las ventas cubren del 1 de enero de 2022 al 30 de septiembre de 2023. Para comparar años se usa enero-septiembre en ambos años. No se compara el total completo de 2022 contra el parcial de 2023.

## Inventario

El archivo de inventario no contiene fecha. Para calcular velocidad reciente se usa el último día disponible en ventas, 30 de septiembre de 2023, como fecha de referencia analítica. Esto no demuestra que el inventario haya sido medido exactamente ese día.

La cobertura se calcula al nivel tienda-producto. La ventana contiene exactamente 90 días calendario, desde el **3 de julio de 2023 hasta el 30 de septiembre de 2023**, ambos inclusive:

`days_cover_90d = stock_on_hand / (units_sold_last_90_days / 90)`

Ejemplo: si una tienda vendió 180 unidades de un producto en esos 90 días, su demanda diaria estimada es 2 unidades. Con 20 unidades disponibles, la cobertura estimada es 10 días. Si no hubo ventas recientes, la cobertura no se calcula como infinita: se clasifica como `No recent sales`.

La cobertura total ponderada se calcula únicamente sobre combinaciones que sí tienen registro de inventario:

`total_stock_reported / (units_last_90_days_for_reported_pairs / 90)`

No es una predicción ni una política de reposición. Es una estimación basada en el ritmo histórico reciente, sin ajustes por estacionalidad, lead time o ventas frustradas.

Estados operativos utilizados:

- `Missing inventory record`: no existe fila para esa combinación tienda-producto.
- `Stockout with recent demand`: stock reportado igual a cero y ventas en los últimos 90 días.
- `Critical cover under 7 days`.
- `Low cover 7-13 days`.
- `Balanced cover 14-30 days`.
- `High cover over 30 days`.
- `No recent sales`: existe inventario, pero no ventas durante los últimos 90 días.

Los umbrales son reglas analíticas para priorizar revisión. No provienen de una política de abastecimiento proporcionada por Maven Toys.

## Tratamiento de registros faltantes

Existen 1.750 combinaciones matemáticamente posibles entre 50 tiendas y 35 productos. El archivo de inventario incluye 1.593. Esto no significa que todas las tiendas deban vender todos los productos. Las 157 combinaciones ausentes permanecen como desconocidas y no se convierten en stock cero. Veintitrés tuvieron ventas durante los últimos 90 días, por lo que conviene confirmar si falta su registro de inventario o si el surtido cambió.
