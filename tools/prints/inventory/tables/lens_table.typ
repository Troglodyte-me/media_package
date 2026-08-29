#import "_styles.typ": table_fill, table_stroke, table_align

#let lens_field(row, key) = {
  row.at(key, default: row.at(" " + key, default: "")).trim()
}

#let lens_missing(value) = {
  if value == "" { "—" } else { value }
}

#let lens_stack(lines) = {
  let filtered = lines.filter(line => line != "")
  if filtered.len() == 0 { "—" } else { filtered.join("\n") }
}

#let lens_columns = (
  "ID",
  "Brand\nModel",
  "Focal\nLength",
  "Aperture",
  "Focus\nSystem / Mount",
  "Filter\nThread",
  "Hood",
  "Serial ID",
  "Location",
  "Notes",
)

#let render_lens_table(data, theme, columns, font_size: 7.2pt) = table(
  columns: columns,
  fill: table_fill(theme),
  stroke: table_stroke(theme),
  align: table_align,
  ..lens_columns.map(header =>
    text(fill: theme.header_text_fill, weight: "bold", size: font_size)[#header]
  ),
  ..data.map(row => (
    text(size: font_size)[#lens_missing(lens_field(row, "id"))],
    text(size: font_size)[
      #lens_stack((
        lens_field(row, "brand"),
        text(weight: "bold")[#lens_field(row, "model")],
      ))
    ],
    text(size: font_size)[#lens_missing(lens_field(row, "focal_length"))],
    text(size: font_size)[#lens_missing(lens_field(row, "aperture"))],
    text(size: font_size)[
      #lens_stack((
        lens_field(row, "focus"),
        lens_field(row, "system"),
        lens_field(row, "mount"),
      ))
    ],
    text(size: font_size)[#lens_missing(lens_field(row, "filter_thread"))],
    text(size: font_size)[#lens_missing(lens_field(row, "hood"))],
    text(size: font_size)[#lens_missing(lens_field(row, "serial_id"))],
    text(size: font_size)[#lens_missing(lens_field(row, "location"))],
    text(size: font_size)[#lens_missing(lens_field(row, "notes"))],
  )).flatten(),
)