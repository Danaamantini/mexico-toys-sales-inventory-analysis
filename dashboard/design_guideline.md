# Mexico Toys dashboard design guideline

Current visual reference: `dashboard/mexico_toys_dashboard_mockup_v2.png`

The mockup defines hierarchy, spacing, color, and storytelling. Exact chart marks must be rebuilt from the project exports in Tableau; the illustrated monthly line is not a substitute for the data.

## Story order

1. Growth outpaced profit.
2. The sales mix shifted toward Magic Sand and away from Colorbuds.
3. Location changes which category and store type performs best.
4. Current inventory is simultaneously scarce and excessive.
5. Demand is strongest late in the week.
6. Finish with three operational actions.

## Palette

| Role | Hex | Use |
|---|---|---|
| Canvas start | `#0B6B5C` | Upper-left dashboard background |
| Canvas end | `#063B49` | Lower-right dashboard background |
| Sidebar | `#063747` | Title and filter rail |
| Card | `#E7F0EC` | Analytical worksheet containers |
| Primary text | `#173E3F` | Titles, labels, main bars |
| Pink | `#EB2F69` | Revenue and principal highlight |
| Orange | `#F47C38` | Electronics / secondary series |
| Yellow | `#F6B51F` | Games / caution |
| Teal | `#22AA9A` | Profit, positive performance, in stock |
| Blue | `#2B88B8` | Margin / comparison series |
| Coral | `#F47478` | Soft negative comparison |
| Neutral | `#667777` | Secondary text and inactive marks |
| Grid | `#D5D6D2` | Dividers and gridlines |

KPI cards use gradients: pink/coral for Revenue, amber/orange for Units,
turquoise/green for Gross Profit, and blue/violet for Gross Margin. Red and
amber inside analytical charts still communicate an exception and should not
be reused decoratively.

## Canvas and spacing

- Fixed desktop size: `1600 × 900`.
- Outer padding: 20 px.
- Gap between containers: 12–16 px.
- Card corner radius: approximately 12 px if simulated with dashboard objects.
- A narrow left rail contains the title and global filters.
- The main area contains one KPI row, two analytical rows, and one inventory alert strip.

## Typography

- Editorial serif for the title and section headings; a readable sans serif for metrics, labels, and tooltips.
- Dashboard title: 26–30 pt.
- Section heading: 15–18 pt.
- KPI value: 24–30 pt.
- Axis and supporting text: 9–11 pt.

If the chosen Tableau environment cannot embed the preferred fonts reliably, use Georgia for headings and Tableau Book or Arial for the rest.

## Visual rules

- Use bars and lines with direct labels; avoid legends when the label can sit next to the mark.
- Use pale mint cards over the deep green background so chart areas remain readable.
- Tableau does not provide native gradient fills for ordinary dashboard containers. Use a gradient image as the background of each KPI card and float a worksheet with transparent shading above it.
- Avoid dual axes, maps, pie charts, gauges, gradients, and decorative images.
- Keep the five numbered sections visible so the reading order is obvious.
- Use coral only for negative movement, stockout, or critical cover.
- Display caveats near the claim they qualify, not only in a hidden tooltip.
- The inventory footer must state the 90-day formula and the missing snapshot date.

## Approved wording

- `Mix shifted toward Magic Sand and away from Colorbuds; no causal claim.`
- `Sep +12.4% YoY — one month, not a trend.`
- `Estimated days of cover` rather than an unqualified `days of supply`.

## Filters

- Date
- Store Location
- Category

Store can remain a detail-level filter or appear only on the inventory action view to prevent the header from becoming crowded.
