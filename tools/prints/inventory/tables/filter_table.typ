#import "_styles.typ": table_fill, table_stroke, table_align

#let filter_field(row, key) = {
  row.at(key, default: row.at(" " + key, default: "")).trim()
}

#let filter_missing(value) = {
  if value == "" { "—" } else { value }
}

#let filter_stack(lines) = {
  let filtered = lines.filter(line => line != "")
  if filtered.len() == 0 { "—" } else { filtered.join("\n") }
}

#let filter_columns = (
  "ID",
  "Brand\nModel / Type",
  "Thread\nSize",
  "Mount\nCompatibility",
  "Location",
  "Notes",
)

#let render_filter_table(data, theme, columns, font_size: 7.4pt) = table(
  columns: columns,
  fill: table_fill(theme),
  stroke: table_stroke(theme),
  align: table_align,
  ..filter_columns.map(header =>
    text(fill: theme.header_text_fill, weight: "bold", size: font_size)[#header]
  ),
  ..data.map(row => (
    text(size: font_size)[#filter_missing(filter_field(row, "id"))],
    text(size: font_size)[
      #filter_stack((
        filter_field(row, "brand"),
        filter_field(row, "model"),
        filter_field(row, "filter_type"),
      ))
    ],
    text(size: font_size)[#filter_missing(filter_field(row, "thread_size"))],
    text(size: font_size)[
      #filter_stack((
        filter_field(row, "mount"),
        filter_field(row, "system"),
      ))
    ],
    text(size: font_size)[#filter_missing(filter_field(row, "location"))],
    text(size: font_size)[#filter_missing(filter_field(row, "notes"))],
  )).flatten(),
)