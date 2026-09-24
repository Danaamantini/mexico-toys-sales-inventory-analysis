DROP VIEW IF EXISTS vw_sales_enriched;
CREATE VIEW vw_sales_enriched AS
SELECT
    s.sale_id,
    s.sale_date,
    c.year,
    c.quarter,
    c.month_number,
    c.month_name,
    c.year_month,
    c.weekday_number,
    c.weekday_name,
    st.store_id,
    st.store_name,
    st.store_city,
    st.store_location,
    p.product_id,
    p.product_name,
    p.product_category,
    s.units,
    p.product_cost,
    p.product_price,
    ROUND(s.units * p.product_price, 2) AS revenue,
    ROUND(s.units * p.product_cost, 2) AS cogs,
    ROUND(s.units * (p.product_price - p.product_cost), 2) AS gross_profit
FROM sales s
JOIN calendar c ON c.date_key = s.sale_date
JOIN stores st ON st.store_id = s.store_id
JOIN products p ON p.product_id = s.product_id;

DROP VIEW IF EXISTS vw_inventory_analysis;
CREATE VIEW vw_inventory_analysis AS
WITH analysis_date AS (
    SELECT MAX(sale_date) AS max_sale_date FROM sales
),
recent_sales AS (
    SELECT
        s.store_id,
        s.product_id,
        SUM(CASE WHEN s.sale_date >= date(a.max_sale_date, '-29 days') THEN s.units ELSE 0 END) AS units_30d,
        SUM(CASE WHEN s.sale_date >= date(a.max_sale_date, '-59 days') THEN s.units ELSE 0 END) AS units_60d,
        SUM(CASE WHEN s.sale_date >= date(a.max_sale_date, '-89 days') THEN s.units ELSE 0 END) AS units_90d,
        ROUND(SUM(CASE WHEN s.sale_date >= date(a.max_sale_date, '-89 days') THEN s.units * p.product_price ELSE 0 END), 2) AS revenue_90d,
        ROUND(SUM(CASE WHEN s.sale_date >= date(a.max_sale_date, '-89 days') THEN s.units * (p.product_price - p.product_cost) ELSE 0 END), 2) AS gross_profit_90d
    FROM sales s
    CROSS JOIN analysis_date a
    JOIN products p ON p.product_id = s.product_id
    GROUP BY s.store_id, s.product_id
),
grid AS (
    SELECT
        st.store_id,
        st.store_name,
        st.store_city,
        st.store_location,
        p.product_id,
        p.product_name,
        p.product_category,
        p.product_cost,
        p.product_price
    FROM stores st
    CROSS JOIN products p
),
base AS (
    SELECT
        g.*,
        CASE WHEN i.store_id IS NULL THEN 0 ELSE 1 END AS has_inventory_record,
        i.stock_on_hand,
        COALESCE(r.units_30d, 0) AS units_30d,
        COALESCE(r.units_60d, 0) AS units_60d,
        COALESCE(r.units_90d, 0) AS units_90d,
        COALESCE(r.revenue_90d, 0) AS revenue_90d,
        COALESCE(r.gross_profit_90d, 0) AS gross_profit_90d
    FROM grid g
    LEFT JOIN inventory i
        ON i.store_id = g.store_id AND i.product_id = g.product_id
    LEFT JOIN recent_sales r
        ON r.store_id = g.store_id AND r.product_id = g.product_id
)
SELECT
    *,
    CASE
        WHEN has_inventory_record = 0 THEN 'Missing inventory record'
        WHEN stock_on_hand = 0 AND units_90d > 0 THEN 'Stockout with recent demand'
        WHEN stock_on_hand = 0 THEN 'Zero stock, no recent demand'
        WHEN units_90d = 0 THEN 'No recent sales'
        WHEN stock_on_hand / (units_90d / 90.0) < 7 THEN 'Critical cover under 7 days'
        WHEN stock_on_hand / (units_90d / 90.0) < 14 THEN 'Low cover 7-13 days'
        WHEN stock_on_hand / (units_90d / 90.0) <= 30 THEN 'Balanced cover 14-30 days'
        ELSE 'High cover over 30 days'
    END AS inventory_status,
    CASE
        WHEN has_inventory_record = 1 AND units_90d > 0
        THEN ROUND(stock_on_hand / (units_90d / 90.0), 1)
    END AS days_cover_90d,
    CASE WHEN has_inventory_record = 1 THEN ROUND(stock_on_hand * product_cost, 2) END AS inventory_cost_value,
    CASE WHEN has_inventory_record = 1 THEN ROUND(stock_on_hand * product_price, 2) END AS inventory_retail_value
FROM base;

DROP VIEW IF EXISTS vw_dashboard_kpis;
CREATE VIEW vw_dashboard_kpis AS
SELECT 'Revenue' AS metric, ROUND(SUM(revenue), 2) AS value FROM vw_sales_enriched
UNION ALL
SELECT 'Gross profit', ROUND(SUM(gross_profit), 2) FROM vw_sales_enriched
UNION ALL
SELECT 'Gross margin', ROUND(SUM(gross_profit) / SUM(revenue), 4) FROM vw_sales_enriched
UNION ALL
SELECT 'Units sold', SUM(units) FROM sales
UNION ALL
SELECT 'Transactions', COUNT(*) FROM sales
UNION ALL
SELECT 'Inventory at cost', ROUND(SUM(inventory_cost_value), 2) FROM vw_inventory_analysis
UNION ALL
SELECT 'Inventory units', SUM(stock_on_hand) FROM inventory
UNION ALL
SELECT 'Stockouts with recent demand', COUNT(*) FROM vw_inventory_analysis WHERE inventory_status = 'Stockout with recent demand'
UNION ALL
SELECT 'Missing inventory records', COUNT(*) FROM vw_inventory_analysis WHERE inventory_status = 'Missing inventory record';

