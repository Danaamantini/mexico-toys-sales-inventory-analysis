# SQL analysis

The project uses SQLite. Run `python3 scripts/build_project.py` from the project root to recreate `sql/mexico_toys.db`, the cleaned dimension files, and every dashboard export.

Files:

- `00_schema.sql`: normalized tables, constraints, and indexes.
- `01_core_views.sql`: enriched sales, inventory analysis, and KPI views.
- `02_category_profit.sql`: category profitability and location comparison.
- `03_seasonality.sql`: monthly, matched-year, and weekday trends.
- `04_inventory_risk.sql`: current stockout and low-cover exposure.
- `05_inventory_value_cover.sql`: inventory value and weighted days of cover.

The database file is generated and excluded from version control.

