-- Q3: Current stockouts or missing inventory records with recent demand.
-- This identifies demand exposure, not proven historical lost sales.
SELECT
    store_name,
    store_location,
    product_name,
    product_category,
    inventory_status,
    stock_on_hand,
    units_30d,
    units_90d,
    revenue_90d,
    gross_profit_90d,
    days_cover_90d
FROM vw_inventory_analysis
WHERE inventory_status IN (
    'Stockout with recent demand',
    'Missing inventory record',
    'Critical cover under 7 days',
    'Low cover 7-13 days'
)
ORDER BY
    CASE inventory_status
        WHEN 'Stockout with recent demand' THEN 1
        WHEN 'Missing inventory record' THEN 2
        WHEN 'Critical cover under 7 days' THEN 3
        ELSE 4
    END,
    revenue_90d DESC;

