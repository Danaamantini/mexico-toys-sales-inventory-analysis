-- Q2: Monthly trend. 2023 is partial through September.
SELECT
    year_month,
    MIN(sale_date) AS month_start,
    COUNT(*) AS transactions,
    SUM(units) AS units_sold,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(gross_profit), 2) AS gross_profit,
    ROUND(SUM(gross_profit) / SUM(revenue), 4) AS gross_margin
FROM vw_sales_enriched
GROUP BY year_month
ORDER BY year_month;

-- Matched-period year-over-year comparison: January-September only.
SELECT
    month_number,
    month_name,
    ROUND(SUM(CASE WHEN year = 2022 THEN revenue END), 2) AS revenue_2022,
    ROUND(SUM(CASE WHEN year = 2023 THEN revenue END), 2) AS revenue_2023,
    ROUND(
        SUM(CASE WHEN year = 2023 THEN revenue END)
        / SUM(CASE WHEN year = 2022 THEN revenue END) - 1,
        4
    ) AS revenue_yoy,
    ROUND(SUM(CASE WHEN year = 2022 THEN gross_profit END), 2) AS profit_2022,
    ROUND(SUM(CASE WHEN year = 2023 THEN gross_profit END), 2) AS profit_2023
FROM vw_sales_enriched
WHERE month_number <= 9
GROUP BY month_number, month_name
ORDER BY month_number;

-- Day-of-week pattern.
SELECT
    weekday_number,
    weekday_name,
    COUNT(DISTINCT sale_date) AS observed_days,
    ROUND(SUM(revenue), 2) AS revenue,
    ROUND(SUM(revenue) / COUNT(DISTINCT sale_date), 2) AS avg_daily_revenue,
    ROUND(SUM(gross_profit) / COUNT(DISTINCT sale_date), 2) AS avg_daily_gross_profit
FROM vw_sales_enriched
GROUP BY weekday_number, weekday_name
ORDER BY weekday_number;

