# Hallazgos

## 1. El crecimiento está acompañado por presión sobre el margen

Entre enero y septiembre de 2023, los ingresos alcanzaron **USD 6,96 M**, un crecimiento de **30,9%** frente al mismo período de 2022. La ganancia bruta creció de USD 1,57 M a **USD 1,82 M**, aproximadamente **16,0%**.

El crecimiento de la ganancia fue menor que el de los ingresos. El margen bruto bajó de **29,6% a 26,2%**. La historia principal no es solo crecimiento: el mix vendido en 2023 generó menos ganancia por dólar de ingreso.

## 2. Toys lidera por escala; Electronics casi lo alcanza con mayor margen

En todo el período:

| Categoría | Ingresos | Ganancia bruta | Margen bruto |
|---|---:|---:|---:|
| Toys | USD 5,09 M | USD 1,08 M | 21,2% |
| Electronics | USD 2,25 M | USD 1,00 M | 44,6% |
| Art & Crafts | USD 2,71 M | USD 753 K | 27,9% |
| Games | USD 2,23 M | USD 674 K | 30,3% |
| Sports & Outdoors | USD 2,17 M | USD 506 K | 23,3% |

Toys produce la mayor ganancia absoluta por volumen. Electronics produce casi la misma ganancia con menos de la mitad de los ingresos gracias a su margen.

`Colorbuds`, de Electronics, genera **USD 835 K**, el **20,8% de toda la ganancia bruta**. Esta concentración hace que disponibilidad, precio y demanda de ese producto sean especialmente importantes.

En la comparación enero-septiembre, el mix de ventas se desplazó hacia `Magic Sand` y se alejó de `Colorbuds`: el primero creció mientras el segundo cayó. Los datos muestran un cambio simultáneo en el mix, pero no permiten afirmar que `Magic Sand` haya reemplazado o causado la caída de `Colorbuds`.

## 3. La categoría líder cambia según el tipo de ubicación

- Electronics lidera la ganancia en tiendas `Airport` y `Commercial`.
- Toys lidera en `Downtown` y `Residential`.

Downtown genera el mayor total porque reúne 29 de las 50 tiendas. Sin embargo, Airport es la ubicación más productiva: aproximadamente **USD 126 K de ganancia por tienda**, frente a unos USD 77 K en los otros tipos de ubicación.

Por eso el dashboard debe mostrar tanto totales como resultados por tienda. Usar únicamente totales haría que Downtown pareciera automáticamente superior.

## 4. El patrón semanal es más claro que una estacionalidad anual estable

Viernes y sábado presentan los mayores ingresos diarios promedio: aproximadamente **USD 30,2 K** y **USD 31,1 K**, respectivamente. El sábado supera al lunes en cerca de **85%**.

Diciembre de 2022 tuvo una subida importante y marzo de 2023 fue el mes de mayores ingresos del período. Sin embargo, solo existe un año completo y nueve meses adicionales. Esto permite describir patrones, pero no afirmar una estacionalidad anual estable.

Todos los meses de enero a septiembre de 2023 superaron al mismo mes de 2022. Los mayores crecimientos ocurrieron en marzo (**49,9%**) y julio (**49,0%**). Septiembre creció **12,4% interanual**, menos que los demás meses observados de 2023; un solo mes no permite concluir que exista una tendencia de desaceleración.

## 5. El inventario tiene faltantes y exceso al mismo tiempo

El inventario reportado contiene **29.742 unidades** con un valor al costo de **USD 300,2 K**. Usando la demanda de los 90 días calendario terminados el 30 de septiembre de 2023, representa aproximadamente **16,5 días de cobertura estimada** en conjunto. La cifra solo incluye combinaciones con registro de inventario y supone que la fotografía de stock es razonablemente comparable con esa fecha.

La cifra global oculta desequilibrios:

- 77 combinaciones tienda-producto tienen stock cero y demanda reciente.
- Esas combinaciones representaron **USD 87,2 K de ingresos en los últimos 90 días**, 4,2% del ingreso reciente.
- 289 combinaciones tienen menos de 7 días de cobertura.
- 267 tienen entre 7 y 13 días.
- 497 tienen más de 30 días y concentran **USD 133,8 K** de inventario al costo.
- 93 tienen stock pero ninguna venta reciente, con **USD 16,7 K** inmovilizados.

Esto sugiere una oportunidad de redistribución: revisar inventario de alta cobertura o sin ventas antes de comprar más unidades para tiendas con stockout o cobertura crítica.

## 6. Las ventas perdidas no pueden medirse directamente

El dataset no incluye historial diario de inventario, reposiciones, pedidos no atendidos ni fecha de la fotografía de stock. Por eso los USD 87,2 K no son ventas perdidas. Representan la demanda histórica reciente asociada con combinaciones que actualmente aparecen agotadas.

La recomendación correcta es priorizar revisión y reposición, no presentar una pérdida causal que los datos no pueden demostrar.
