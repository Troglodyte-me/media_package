#let inventory_table_theme = (
  header_fill: rgb("#2b6cb0"),
  header_text_fill: white,
  row_even_fill: rgb("#f1f5f9"),
  row_odd_fill: white,
  body_stroke: 0.4pt + rgb("#cbd5e1"),
)

#let inventory_table_font_sizes = (
  camera: 7pt,
  lens: 8pt,
  filter: 8.5pt,
)

#let inventory_table_columns = (
  camera: (auto, 2.2fr, 2fr, 1.8fr, 1.2fr, 1fr, 1fr, 1.2fr, 2fr, 3fr),
  lens: (auto, 1.8fr, 1.2fr, 1.2fr, 0.8fr, 1fr, 1fr, 1fr, 0.9fr, 0.9fr, 1.2fr, 1.2fr, 1.8fr),
  filter: (auto, 1.8fr, 1.4fr, 1.2fr, 1.8fr, 2.4fr),
)

#let table_fill(theme) = (x, y) =>
  if y == 0 { theme.header_fill }
  else if calc.even(y) { theme.row_even_fill }
  else { theme.row_odd_fill }

#let table_stroke(theme) = (x, y) =>
  if y == 0 { none } else { theme.body_stroke }

#let table_align = (col, row) =>
  if row == 0 { center + horizon } else { left + horizon }