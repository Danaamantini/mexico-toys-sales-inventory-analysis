# Manual Tableau build guide

## Data sources

Use two independent data sources:

1. `dashboard_sales.csv`: one row per month, store, and product.
2. `inventory_analysis.csv`: one row per possible store-product combination.

Do not join them. Each source owns a separate dashboard page.

## Performance Overview calculated fields

### Gross Margin

```text
SUM([gross_profit]) / SUM([revenue])
```

### Profit per Store

```text
SUM([gross_profit]) / COUNTD([store_id])
```

### Comparable Revenue 2022

```text
SUM(
    IF [year] = 2022 AND [month_number] <= 9
    THEN [revenue]
    END
)
```

### Comparable Revenue 2023

```text
SUM(
    IF [year] = 2023
    THEN [revenue]
    END
)
```

### Revenue YoY

```text
([Comparable Revenue 2023] / [Comparable Revenue 2022]) - 1
```

Format Gross Margin and Revenue YoY as percentages with one decimal.

## Performance Overview sheets

1. KPI Revenue: `SUM(revenue)` as Text.
2. KPI Gross Profit: `SUM(gross_profit)` as Text.
3. KPI Gross Margin: calculated field as Text.
4. KPI Units: `SUM(units_sold)` as Text.
5. KPI Revenue YoY: calculated field as Text.
6. Monthly trend: `month_start` on Columns; `SUM(revenue)` and `SUM(gross_profit)` on Rows.
7. Category profit: `product_category` on Rows; `SUM(gross_profit)` on Columns; descending sort.
8. Location productivity: `store_location` on Rows; `Profit per Store` on Columns.
9. Weekday analysis is optional on the final page because the dashboard sales export is monthly. Use `weekday_performance.csv` as a separate source only for that isolated chart.

Apply `store_location`, `store_name`, and `product_category` filters to every worksheet using the `dashboard_sales` source.

## Inventory Action sheets

1. KPI Inventory Cost: `SUM(inventory_cost_value)`.
2. KPI Inventory Units: `SUM(stock_on_hand)`.
3. KPI Stockouts: count rows where `inventory_status = Stockout with recent demand`.
4. Status bars: `inventory_status` on Rows and Number of Records on Columns.
5. Priority table: store, product, category, stock, units 30d, units 90d, revenue 90d, days cover, and status.
6. Demand versus cover: `days_cover_90d` on Columns, `revenue_90d` on Rows, status on Color, and inventory cost on Size.

Use red only for stockouts and critical cover, amber for low cover or missing
records, blue for balanced cover, and gray for high cover or no recent sales.

Add this visible methodology note to the inventory dashboard:

```text
Estimated days of cover = stock on hand / (units sold from Jul 3 to Sep 30, 2023 / 90).
The inventory snapshot date is not provided; thresholds are analytical flags, not company policy.
```

Use the phrase `Sales mix shifted toward Magic Sand and away from Colorbuds`.
Do not label the change as a replacement or substitution. Describe September as
`12.4% YoY growth, lower than the other observed 2023 months`; do not describe
one month as a slowing trend.
