#import "_styles.typ": table_fill, table_stroke, table_align

#let filter_columns = (
  "id",
  "brand",
  "filter_type",
  "thread_size",
  "location",
  "notes",
)

#let render_filter_table(data, theme, columns, font_size: 8.5pt) = table(
  columns: columns,
  fill: table_fill(theme),
  stroke: table_stroke(theme),
  align: table_align,
  ..filter_columns.map(header =>
    text(fill: theme.header_text_fill, weight: "bold", size: font_size)[#header]
  ),
  ..data.map(row =>
    filter_columns.map(col => text(size: font_size)[#row.at(col, default: "")])
  ).flatten(),
)