# Inventory Print Procedure

This folder contains Typst sources and CSV data for the inventory printouts.

## Files and Responsibilities
- `inventory_overview.typ`: Main document orchestration (sections, imports, page setup).
- `inventory_cards.typ`: Card sheet generation with front/back imposition.
- `tables/_styles.typ`: Shared table theme, font sizes, and column layouts.
- `tables/camera_table.typ`: Reusable camera table renderer.
- `tables/lens_table.typ`: Reusable lens table renderer.
- `tables/filter_table.typ`: Reusable filter table renderer.
- `cameras_inventory.csv`, `lenses_inventory.csv`, `filters_inventory.csv`: Source data.

## Update Workflow
1. Edit CSV data first.
2. Keep CSV column names stable whenever possible.
3. If layout changes are needed, update `tables/_styles.typ` for widths/font sizes.
4. Keep section-specific formatting logic inside table modules, not in `inventory_overview.typ`.
5. Re-run Typst diagnostics/build and verify no missing fields render as blanks.

## Data Handling Rules
- Renderers use trimmed dictionary access so CSV headers/values with leading spaces still resolve.
- Missing values should display as an em dash (`—`) instead of empty content.
- Multi-part cells (for example Brand + Model) should stack lines and collapse empty parts.

## Section Wiring Pattern
In `inventory_overview.typ`, each section should follow this pattern:
1. Import a `render_*_table` function from `tables/*.typ`.
2. Load CSV with `csv(..., row-type: dictionary)`.
3. Call renderer with:
   - data
   - `inventory_table_theme`
   - matching `inventory_table_columns.*`
   - matching `inventory_table_font_sizes.*`

This keeps the main file clean and makes each table independently reusable.
