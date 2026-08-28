#import "_styles.typ": table_fill, table_stroke, table_align

#let camera_columns = (
  "ID",
  "Brand\nModel",
  "Camera Type",
  "Sensor\n(pixel)",
  "Mount/Lens",
  "Battery",
  "Storage",
  "Serial ID",
  "Location",
  "Notes",
)

#let camera_field(row, key) = {
  row.at(key, default: row.at(" " + key, default: "")).trim()
}

#let stack_lines(lines) = {
  lines.filter(line => line != "").join("\n")
}

#let render_camera_table(data, theme, columns, font_size: 7pt) = table(
  columns: columns,
  fill: table_fill(theme),
  stroke: table_stroke(theme),
  align: table_align,
  ..camera_columns.map(header =>
    text(fill: theme.header_text_fill, weight: "bold", size: font_size)[#header]
  ),
  ..data.map(row => (
    text(size: font_size)[#camera_field(row, "id")],
    text(size: font_size)[#stack_lines((camera_field(row, "brand"), camera_field(row, "model")))],
    text(size: font_size)[#camera_field(row, "camera_type")],
    text(size: font_size)[#stack_lines((camera_field(row, "sensor"), camera_field(row, "pixel")))],
    text(size: font_size)[#stack_lines((camera_field(row, "mount"), camera_field(row, "lens_aperture"), camera_field(row, "lens_length")))],
    text(size: font_size)[#camera_field(row, "battery")],
    text(size: font_size)[#camera_field(row, "storage")],
    text(size: font_size)[#camera_field(row, "serial_id")],
    text(size: font_size)[#camera_field(row, "location")],
    text(size: font_size)[#camera_field(row, "notes")],
  )).flatten(),
)