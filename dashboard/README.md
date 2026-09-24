# Tableau dashboard

The completed workbook is `mexico_toys_tableau.twb` and contains two dashboards:

- **Overview:** commercial performance, revenue trend, margin, product mix, store-location productivity and weekday demand.
- **Inventory Action:** inventory value, estimated coverage, stockout exposure, status distribution and replenishment priorities.

This workbook is the authoritative dashboard deliverable. The PNG mockups in this folder are early visual concepts, not Tableau exports; see `../docs/visual_concept_audit.md` for the validation boundary.

Data sources:

- `../data/export/dashboard_sales.csv`
- `../data/export/inventory_analysis.csv`
- `../data/export/weekday_performance.csv`

The sources intentionally remain separate because they use different grains. If Tableau cannot resolve the original local paths, use **Data → Replace Data Source** or edit each text connection and select the corresponding file above.

Supporting files include the color palette, gradient card assets, design guideline, dashboard specification and build guide.
