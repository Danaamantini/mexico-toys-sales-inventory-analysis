-- Compact evidence used to write the project findings.
SELECT 'CATEGORY' AS section, * FROM (
    SELECT product_category, SUM(units) AS units,
           ROUND(SUM(revenue), 2) AS revenue,
           ROUND(SUM(gross_profit), 2) AS profit,
           ROUND(SUM(gross_profit) / SUM(revenue), 4) AS margin
    FROM vw_sales_enriched
    GROUP BY product_category
    ORDER BY profit DESC
);

SELECT 'LOCATION' AS section, store_location, COUNT(DISTINCT store_id) AS stores,
       ROUND(SUM(revenue), 2) AS revenue,
       ROUND(SUM(gross_profit), 2) AS profit,
       ROUND(SUM(gross_profit) / COUNT(DISTINCT store_id), 2) AS profit_per_store
FROM vw_sales_enriched
GROUP BY store_location
ORDER BY profit DESC;

WITH monthly AS (
    SELECT year_month, ROUND(SUM(revenue), 2) AS revenue,
           ROUND(SUM(gross_profit), 2) AS profit
    FROM vw_sales_enriched
    GROUP BY year_month
)
SELECT 'MONTH_HIGH' AS section, * FROM monthly ORDER BY revenue DESC LIMIT 5;

WITH monthly AS (
    SELECT year_month, ROUND(SUM(revenue), 2) AS revenue,
           ROUND(SUM(gross_profit), 2) AS profit
    FROM vw_sales_enriched
    GROUP BY year_month
)
SELECT 'MONTH_LOW' AS section, * FROM monthly ORDER BY revenue LIMIT 5;

SELECT 'YOY_JAN_SEP' AS section, year,
       ROUND(SUM(revenue), 2) AS revenue,
       ROUND(SUM(gross_profit), 2) AS profit,
       SUM(units) AS units
FROM vw_sales_enriched
WHERE month_number <= 9
GROUP BY year
ORDER BY year;

SELECT 'WEEKDAY' AS section, weekday_name,
       COUNT(DISTINCT sale_date) AS observed_days,
       ROUND(SUM(revenue) / COUNT(DISTINCT sale_date), 2) AS avg_daily_revenue
FROM vw_sales_enriched
GROUP BY weekday_number, weekday_name
ORDER BY weekday_number;

SELECT 'TOP_PRODUCT' AS section, product_name, product_category,
       ROUND(SUM(revenue), 2) AS revenue,
       ROUND(SUM(gross_profit), 2) AS profit,
       SUM(units) AS units
FROM vw_sales_enriched
GROUP BY product_id, product_name, product_category
ORDER BY profit DESC
LIMIT 10;

SELECT 'TOP_STORE' AS section, store_name, store_location,
       ROUND(SUM(revenue), 2) AS revenue,
       ROUND(SUM(gross_profit), 2) AS profit
FROM vw_sales_enriched
GROUP BY store_id, store_name, store_location
ORDER BY profit DESC
LIMIT 10;

SELECT 'INV_STATUS' AS section, inventory_status, COUNT(*) AS pairs,
       SUM(COALESCE(stock_on_hand, 0)) AS stock,
       ROUND(SUM(COALESCE(inventory_cost_value, 0)), 2) AS cost_value,
       SUM(units_90d) AS units_90d,
       ROUND(SUM(revenue_90d), 2) AS revenue_90d
FROM vw_inventory_analysis
GROUP BY inventory_status
ORDER BY pairs DESC;

SELECT 'TOP_STOCKOUT' AS section, store_name, product_name, product_category,
       units_90d, revenue_90d, gross_profit_90d
FROM vw_inventory_analysis
WHERE inventory_status = 'Stockout with recent demand'
ORDER BY revenue_90d DESC
LIMIT 10;

