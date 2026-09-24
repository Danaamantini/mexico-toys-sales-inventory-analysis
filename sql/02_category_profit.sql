-- Q1: Which product categories drive the biggest gross profits?
SELECT
    product_category,
    SUM(units) AS units_sold,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(gross_profit), 2) AS gross_profit,
    ROUND(SUM(gross_profit) / SUM(revenue), 4) AS gross_margin,
    ROUND(SUM(gross_profit) * 1.0 / SUM(SUM(gross_profit)) OVER (), 4) AS profit_share
FROM vw_sales_enriched
GROUP BY product_category
ORDER BY gross_profit DESC;

-- Compare category performance by location type.
SELECT
    store_location,
    product_category,
    COUNT(DISTINCT store_id) AS stores,
    SUM(units) AS units_sold,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(gross_profit), 2) AS gross_profit,
    ROUND(SUM(gross_profit) / COUNT(DISTINCT store_id), 2) AS profit_per_store,
    ROUND(SUM(gross_profit) / SUM(revenue), 4) AS gross_margin
FROM vw_sales_enriched
GROUP BY store_location, product_category
ORDER BY store_location, gross_profit DESC;

