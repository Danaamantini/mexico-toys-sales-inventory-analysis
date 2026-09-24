-- Q4: Inventory value and duration by store and category.
SELECT
    store_name,
    store_location,
    product_category,
    SUM(stock_on_hand) AS stock_units,
    ROUND(SUM(inventory_cost_value), 2) AS inventory_cost_value,
    ROUND(SUM(inventory_retail_value), 2) AS inventory_retail_value,
    SUM(units_90d) AS units_90d,
    CASE
        WHEN SUM(units_90d) > 0
        THEN ROUND(SUM(stock_on_hand) / (SUM(units_90d) / 90.0), 1)
    END AS weighted_days_cover_90d
FROM vw_inventory_analysis
WHERE has_inventory_record = 1
GROUP BY store_name, store_location, product_category
ORDER BY inventory_cost_value DESC;

