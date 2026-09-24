# Diseño del dashboard final

## Historia

El dashboard debe responder una secuencia:

1. **El negocio está creciendo.**
2. **El margen no crece al mismo ritmo.**
3. **El mix se desplazó hacia Magic Sand y se alejó de Colorbuds, sin atribuir causalidad.**
4. **El resultado depende de categorías y productos distintos según la ubicación.**
5. **El inventario no está alineado con esa demanda: la acción es proteger disponibilidad rentable y redistribuir exceso.**

## Página 1: Performance overview

### Filtros

- Date
- Store Location
- Store
- Product Category

### KPI

- Revenue
- Gross Profit
- Gross Margin
- Units Sold
- YoY Revenue Growth, enero-septiembre

### Visuales

1. **Monthly revenue and gross profit**  
   Línea cronológica de 21 meses. Usar dos paneles o escala claramente diferenciada; evitar un doble eje confuso.

2. **Gross profit by category**  
   Barras horizontales ordenadas. Tooltip: ingresos, margen y participación en la ganancia.

3. **Profit per store by location**  
   Barras con ganancia promedio por tienda. Incluir el número de tiendas en tooltip.

4. **Category leader by location**  
   Matriz o heatmap con `Store Location × Product Category`, usando ganancia por tienda.

5. **Average daily revenue by weekday**  
   Columnas de lunes a domingo para mostrar el pico de viernes y sábado.

### Anotaciones

- Revenue Jan-Sep 2023: +30,9% interanual.
- Gross margin: 29,6% → 26,2%.
- Colorbuds aporta 20,8% de la ganancia bruta total.
- El mix se desplazó hacia Magic Sand y se alejó de Colorbuds; no se presenta como sustitución causal.
- Septiembre creció 12,4% interanual; un mes aislado no demuestra desaceleración.

## Página 2: Inventory action

### KPI

- Inventory Cost Value
- Inventory Units
- Estimated Weighted Days of Cover (90-day demand)
- Stockouts with Recent Demand
- 90-Day Revenue Associated with Current Stockouts

### Visuales

1. **Store-product pairs by inventory status**  
   Barras horizontales por estado de cobertura.

2. **Inventory value by status**  
   Barras para identificar capital en cobertura alta y productos sin ventas recientes.

3. **Demand versus days of cover**  
   Scatter: `Revenue 90d` en Y y `Days Cover 90d` en X. Color por estado; tamaño por valor del inventario.

4. **Priority replenishment table**  
   Store, Product, Category, Stock, Units 30d, Units 90d, Revenue 90d, Days Cover y Status.

### Anotaciones

- 77 stockouts con demanda reciente.
- USD 87,2 K de ingresos recientes asociados con esas combinaciones.
- USD 150,4 K al costo en cobertura alta o sin ventas recientes.
- Cobertura = stock / demanda diaria promedio de los 90 días terminados el 30/09/2023. La fecha del inventario no está informada.

## Reglas visuales

- Azul oscuro para desempeño general.
- Verde para ganancia y margen saludables.
- Rojo solo para stockout y cobertura crítica.
- Ámbar para cobertura baja o datos faltantes.
- Gris para cobertura alta y productos sin ventas recientes.
- Mantener los mismos colores de estado en toda la página.
- No utilizar gráficos de torta ni medidores.

## Fuentes de datos

- `data/export/dashboard_sales.csv` para todos los KPI, filtros y visuales de Performance Overview.
- `data/export/inventory_analysis.csv`
- `data/export/inventory_status_summary.csv`

No relacionar los exports agregados entre sí. Tienen granos diferentes y un
join produciría duplicaciones. `dashboard_sales.csv` ya está agregado al nivel
mes-tienda-producto y permite que fecha, ubicación, tienda y categoría filtren
coherentemente toda la primera página.
