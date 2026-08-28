#import "_styles.typ": table_fill, table_stroke, table_align

#let lens_columns = (
  "id",
  "brand", "model",
  "focal_length",
  "aperture",
  "focus",
  "system",
  "mount",
  "filter_thread",
  "hood",
  "serial_id",
  "location",
  "notes",
)

#let render_lens_table(data, theme, columns, font_size: 8pt) = table(
  columns: columns,
  fill: table_fill(theme),
  stroke: table_stroke(theme),
  align: table_align,
  ..lens_columns.map(header =>
    text(fill: theme.header_text_fill, weight: "bold", size: font_size)[#header]
  ),
  ..data.map(row =>
    lens_columns.map(col => text(size: font_size)[#row.at(col, default: "")])
  ).flatten(),
)