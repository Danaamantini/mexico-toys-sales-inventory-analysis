# Data layers

- `raw/`: original Maven Analytics files. Never modify these files.
- `processed/`: cleaned dimensions and the reported inventory snapshot.
- `export/`: small analysis tables used by Excel and the future dashboard.

For Tableau, use `dashboard_sales.csv` for the performance page and
`inventory_analysis.csv` for the inventory page. Each page then has one
consistent data source and its filters apply to every visual on that page.

The 829,262-row sales table remains in SQLite instead of being duplicated into Excel. Rebuild all generated files with `python3 scripts/build_project.py`.
