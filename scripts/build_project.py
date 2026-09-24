#!/usr/bin/env python3
"""Build the SQLite database, cleaned dimensions, and dashboard exports."""

from __future__ import annotations

import csv
import sqlite3
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
EXPORT = ROOT / "data" / "export"
DB_PATH = ROOT / "sql" / "mexico_toys.db"


def read_csv(name: str):
    with (RAW / name).open(encoding="utf-8-sig", newline="") as handle:
        yield from csv.DictReader(handle)


def money(value: str) -> float:
    return float(value.replace("$", "").strip())


def write_csv(path: Path, headers: list[str], rows) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        writer.writerows(rows)


def query_to_csv(connection: sqlite3.Connection, filename: str, sql: str) -> None:
    cursor = connection.execute(sql)
    write_csv(EXPORT / filename, [item[0] for item in cursor.description], cursor.fetchall())


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    EXPORT.mkdir(parents=True, exist_ok=True)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()

    connection = sqlite3.connect(DB_PATH)
    connection.executescript((ROOT / "sql" / "00_schema.sql").read_text(encoding="utf-8"))
    connection.execute("PRAGMA journal_mode = MEMORY")
    connection.execute("PRAGMA synchronous = OFF")
    connection.execute("PRAGMA temp_store = MEMORY")

    products = [
        (
            int(row["Product_ID"]),
            row["Product_Name"].strip(),
            row["Product_Category"].strip(),
            money(row["Product_Cost"]),
            money(row["Product_Price"]),
        )
        for row in read_csv("products.csv")
    ]
    stores = [
        (
            int(row["Store_ID"]),
            row["Store_Name"].strip(),
            row["Store_City"].strip(),
            row["Store_Location"].strip(),
            row["Store_Open_Date"].strip(),
        )
        for row in read_csv("stores.csv")
    ]
    calendar = []
    for row in read_csv("calendar.csv"):
        date_value = datetime.strptime(row["Date"], "%m/%d/%Y").date()
        calendar.append(
            (
                date_value.isoformat(),
                date_value.year,
                (date_value.month - 1) // 3 + 1,
                date_value.month,
                date_value.strftime("%B"),
                date_value.strftime("%Y-%m"),
                date_value.isoweekday(),
                date_value.strftime("%A"),
            )
        )
    inventory = [
        (int(row["Store_ID"]), int(row["Product_ID"]), int(row["Stock_On_Hand"]))
        for row in read_csv("inventory.csv")
    ]

    connection.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?)", products)
    connection.executemany("INSERT INTO stores VALUES (?, ?, ?, ?, ?)", stores)
    connection.executemany("INSERT INTO calendar VALUES (?, ?, ?, ?, ?, ?, ?, ?)", calendar)
    connection.executemany("INSERT INTO inventory VALUES (?, ?, ?)", inventory)

    batch = []
    for row in read_csv("sales.csv"):
        batch.append(
            (
                int(row["Sale_ID"]),
                row["Date"],
                int(row["Store_ID"]),
                int(row["Product_ID"]),
                int(row["Units"]),
            )
        )
        if len(batch) == 25_000:
            connection.executemany("INSERT INTO sales VALUES (?, ?, ?, ?, ?)", batch)
            batch.clear()
    if batch:
        connection.executemany("INSERT INTO sales VALUES (?, ?, ?, ?, ?)", batch)
    connection.commit()

    connection.executescript((ROOT / "sql" / "01_core_views.sql").read_text(encoding="utf-8"))
    connection.commit()

    write_csv(PROCESSED / "products_clean.csv", ["product_id", "product_name", "product_category", "product_cost", "product_price"], products)
    write_csv(PROCESSED / "stores_clean.csv", ["store_id", "store_name", "store_city", "store_location", "store_open_date"], stores)
    write_csv(PROCESSED / "calendar_clean.csv", ["date", "year", "quarter", "month_number", "month_name", "year_month", "weekday_number", "weekday_name"], calendar)
    write_csv(PROCESSED / "inventory_clean.csv", ["store_id", "product_id", "stock_on_hand"], inventory)

    exports = {
        "dashboard_sales.csv": """
            SELECT year_month, MIN(sale_date) AS month_start, year, quarter,
                   month_number, month_name, store_id, store_name, store_city,
                   store_location, product_id, product_name, product_category,
                   COUNT(*) AS transactions, SUM(units) AS units_sold,
                   ROUND(SUM(revenue), 2) AS revenue,
                   ROUND(SUM(cogs), 2) AS cogs,
                   ROUND(SUM(gross_profit), 2) AS gross_profit
            FROM vw_sales_enriched
            GROUP BY year_month, year, quarter, month_number, month_name,
                     store_id, store_name, store_city, store_location,
                     product_id, product_name, product_category
            ORDER BY year_month, store_id, product_id
        """,
        "kpi_summary.csv": "SELECT * FROM vw_dashboard_kpis",
        "monthly_performance.csv": """
            SELECT year_month, MIN(sale_date) AS month_start, COUNT(*) AS transactions,
                   SUM(units) AS units_sold, ROUND(SUM(revenue), 2) AS revenue,
                   ROUND(SUM(gross_profit), 2) AS gross_profit,
                   ROUND(SUM(gross_profit) / SUM(revenue), 4) AS gross_margin
            FROM vw_sales_enriched GROUP BY year_month ORDER BY year_month
        """,
        "category_performance.csv": """
            SELECT product_category, SUM(units) AS units_sold,
                   ROUND(SUM(revenue), 2) AS revenue,
                   ROUND(SUM(gross_profit), 2) AS gross_profit,
                   ROUND(SUM(gross_profit) / SUM(revenue), 4) AS gross_margin,
                   ROUND(SUM(gross_profit) * 1.0 / SUM(SUM(gross_profit)) OVER (), 4) AS profit_share
            FROM vw_sales_enriched GROUP BY product_category ORDER BY gross_profit DESC
        """,
        "location_performance.csv": """
            SELECT store_location, COUNT(DISTINCT store_id) AS stores,
                   SUM(units) AS units_sold, ROUND(SUM(revenue), 2) AS revenue,
                   ROUND(SUM(gross_profit), 2) AS gross_profit,
                   ROUND(SUM(revenue) / COUNT(DISTINCT store_id), 2) AS revenue_per_store,
                   ROUND(SUM(gross_profit) / COUNT(DISTINCT store_id), 2) AS profit_per_store,
                   ROUND(SUM(gross_profit) / SUM(revenue), 4) AS gross_margin
            FROM vw_sales_enriched GROUP BY store_location ORDER BY gross_profit DESC
        """,
        "category_location.csv": """
            SELECT store_location, product_category, COUNT(DISTINCT store_id) AS stores,
                   SUM(units) AS units_sold, ROUND(SUM(revenue), 2) AS revenue,
                   ROUND(SUM(gross_profit), 2) AS gross_profit,
                   ROUND(SUM(gross_profit) / COUNT(DISTINCT store_id), 2) AS profit_per_store,
                   ROUND(SUM(gross_profit) / SUM(revenue), 4) AS gross_margin
            FROM vw_sales_enriched GROUP BY store_location, product_category
            ORDER BY store_location, gross_profit DESC
        """,
        "store_performance.csv": """
            SELECT store_id, store_name, store_city, store_location,
                   SUM(units) AS units_sold, ROUND(SUM(revenue), 2) AS revenue,
                   ROUND(SUM(gross_profit), 2) AS gross_profit,
                   ROUND(SUM(gross_profit) / SUM(revenue), 4) AS gross_margin
            FROM vw_sales_enriched GROUP BY store_id, store_name, store_city, store_location
            ORDER BY gross_profit DESC
        """,
        "product_performance.csv": """
            SELECT product_id, product_name, product_category,
                   SUM(units) AS units_sold, ROUND(SUM(revenue), 2) AS revenue,
                   ROUND(SUM(gross_profit), 2) AS gross_profit,
                   ROUND(SUM(gross_profit) / SUM(revenue), 4) AS gross_margin
            FROM vw_sales_enriched GROUP BY product_id, product_name, product_category
            ORDER BY gross_profit DESC
        """,
        "weekday_performance.csv": """
            SELECT weekday_number, weekday_name, COUNT(DISTINCT sale_date) AS observed_days,
                   ROUND(SUM(revenue), 2) AS revenue,
                   ROUND(SUM(revenue) / COUNT(DISTINCT sale_date), 2) AS avg_daily_revenue,
                   ROUND(SUM(gross_profit) / COUNT(DISTINCT sale_date), 2) AS avg_daily_gross_profit
            FROM vw_sales_enriched GROUP BY weekday_number, weekday_name ORDER BY weekday_number
        """,
        "matched_yoy.csv": """
            SELECT month_number, month_name,
                   ROUND(SUM(CASE WHEN year = 2022 THEN revenue END), 2) AS revenue_2022,
                   ROUND(SUM(CASE WHEN year = 2023 THEN revenue END), 2) AS revenue_2023,
                   ROUND(SUM(CASE WHEN year = 2023 THEN revenue END) /
                         SUM(CASE WHEN year = 2022 THEN revenue END) - 1, 4) AS revenue_yoy,
                   ROUND(SUM(CASE WHEN year = 2022 THEN gross_profit END), 2) AS profit_2022,
                   ROUND(SUM(CASE WHEN year = 2023 THEN gross_profit END), 2) AS profit_2023
            FROM vw_sales_enriched WHERE month_number <= 9
            GROUP BY month_number, month_name ORDER BY month_number
        """,
        "inventory_analysis.csv": """
            SELECT * FROM vw_inventory_analysis
            ORDER BY CASE inventory_status
                WHEN 'Stockout with recent demand' THEN 1
                WHEN 'Missing inventory record' THEN 2
                WHEN 'Critical cover under 7 days' THEN 3
                WHEN 'Low cover 7-13 days' THEN 4
                WHEN 'Balanced cover 14-30 days' THEN 5
                WHEN 'High cover over 30 days' THEN 6
                ELSE 7 END,
                revenue_90d DESC
        """,
        "inventory_status_summary.csv": """
            SELECT inventory_status, COUNT(*) AS store_product_pairs,
                   SUM(COALESCE(stock_on_hand, 0)) AS stock_units,
                   ROUND(SUM(COALESCE(inventory_cost_value, 0)), 2) AS inventory_cost_value,
                   SUM(units_90d) AS units_90d,
                   ROUND(SUM(revenue_90d), 2) AS revenue_90d
            FROM vw_inventory_analysis GROUP BY inventory_status
            ORDER BY store_product_pairs DESC
        """,
    }
    for filename, sql in exports.items():
        query_to_csv(connection, filename, sql)

    checks = {
        "sales_rows": connection.execute("SELECT COUNT(*) FROM sales").fetchone()[0],
        "distinct_sale_ids": connection.execute("SELECT COUNT(DISTINCT sale_id) FROM sales").fetchone()[0],
        "min_sale_date": connection.execute("SELECT MIN(sale_date) FROM sales").fetchone()[0],
        "max_sale_date": connection.execute("SELECT MAX(sale_date) FROM sales").fetchone()[0],
        "sales_without_product": connection.execute("SELECT COUNT(*) FROM sales s LEFT JOIN products p USING(product_id) WHERE p.product_id IS NULL").fetchone()[0],
        "sales_without_store": connection.execute("SELECT COUNT(*) FROM sales s LEFT JOIN stores st USING(store_id) WHERE st.store_id IS NULL").fetchone()[0],
        "inventory_records": connection.execute("SELECT COUNT(*) FROM inventory").fetchone()[0],
        "missing_inventory_records": connection.execute("SELECT COUNT(*) FROM vw_inventory_analysis WHERE has_inventory_record = 0").fetchone()[0],
    }
    write_csv(EXPORT / "validation_summary.csv", ["check", "value"], checks.items())
    connection.close()


if __name__ == "__main__":
    main()
