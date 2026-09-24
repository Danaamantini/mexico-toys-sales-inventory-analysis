PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS vw_dashboard_kpis;
DROP VIEW IF EXISTS vw_inventory_analysis;
DROP VIEW IF EXISTS vw_sales_enriched;

DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS calendar;
DROP TABLE IF EXISTS stores;
DROP TABLE IF EXISTS products;

CREATE TABLE products (
    product_id       INTEGER PRIMARY KEY,
    product_name     TEXT NOT NULL,
    product_category TEXT NOT NULL,
    product_cost     REAL NOT NULL CHECK (product_cost >= 0),
    product_price    REAL NOT NULL CHECK (product_price >= product_cost)
);

CREATE TABLE stores (
    store_id        INTEGER PRIMARY KEY,
    store_name      TEXT NOT NULL UNIQUE,
    store_city      TEXT NOT NULL,
    store_location  TEXT NOT NULL,
    store_open_date TEXT NOT NULL
);

CREATE TABLE calendar (
    date_key       TEXT PRIMARY KEY,
    year           INTEGER NOT NULL,
    quarter        INTEGER NOT NULL,
    month_number   INTEGER NOT NULL,
    month_name     TEXT NOT NULL,
    year_month     TEXT NOT NULL,
    weekday_number INTEGER NOT NULL,
    weekday_name   TEXT NOT NULL
);

CREATE TABLE inventory (
    store_id      INTEGER NOT NULL,
    product_id    INTEGER NOT NULL,
    stock_on_hand INTEGER NOT NULL CHECK (stock_on_hand >= 0),
    PRIMARY KEY (store_id, product_id),
    FOREIGN KEY (store_id) REFERENCES stores(store_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE sales (
    sale_id    INTEGER PRIMARY KEY,
    sale_date  TEXT NOT NULL,
    store_id   INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    units      INTEGER NOT NULL CHECK (units > 0),
    FOREIGN KEY (sale_date) REFERENCES calendar(date_key),
    FOREIGN KEY (store_id) REFERENCES stores(store_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE INDEX idx_sales_date ON sales(sale_date);
CREATE INDEX idx_sales_store_product_date ON sales(store_id, product_id, sale_date);
CREATE INDEX idx_sales_product ON sales(product_id);

