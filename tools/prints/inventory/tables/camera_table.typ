#import "_styles.typ": table_fill, table_stroke, table_align

#let camera_columns = (
  "ID",
  "Kamera\nModel + S/N",
  "Typ",
  "Sensor",
  "Objektiv\n + Mount",
  "Energie",
  "Daten",
  "Ort",
  "Kommentare",
)

#let camera_field(row, key) = {
  row.at(key, default: row.at(" " + key, default: "")).trim()
}

#let camera_missing(value) = {
  if value == "" { "—" } else { value }
}

#let stack_lines(lines) = {
  let filtered = lines.filter(line => line != "")
  if filtered.len() == 0 { "—" } else { filtered.join("\n") }
}

#let camera_serial(value) = {
  if value == "" { "" } else { "[S/N: " + value + "]" }
}

#let camera_identity_cell(row, font_size) = {
  let brand = camera_field(row, "brand")
  let model = camera_field(row, "model")
  let serial = camera_serial(camera_field(row, "serial"))

  if brand == "" and model == "" and serial == "" {
    text(size: font_size)[—]
  } else [
    #if brand != "" { text(size: font_size, weight: "bold")[#brand] }
    #if brand != "" and (model != "" or serial != "") { linebreak() }
    #if model != "" { text(size: font_size, weight: "bold")[#model] }
    #if model != "" and serial != "" { linebreak() }
    #if serial != "" { text(size: font_size)[#serial] }
  ]
}

#let camera_notes_cell(row, font_size) = {
  let notes = camera_field(row, "notes")
  if notes == "" {
    text(size: font_size)[—]
  } else {
    let normalized = notes.replace(";", ",")
    let parts = normalized.split(",").map(part => part.trim()).filter(part => part != "")
    if parts.len() == 0 {
      text(size: font_size)[—]
    } else {
      text(size: font_size)[#parts.join("\n")]
    }
  }
}

#let render_camera_table(data, theme, columns, font_size: 7pt) = table(
  columns: columns,
  inset: (x: 3pt, y: 3pt),
  fill: table_fill(theme),
  stroke: table_stroke(theme),
  align: table_align,
  ..camera_columns.map(header =>
    text(fill: theme.header_text_fill, weight: "bold", size: font_size)[#header]
  ),
  ..data.map(row => (
    text(size: font_size)[#camera_missing(camera_field(row, "id"))],
    camera_identity_cell(row, font_size),
    text(size: font_size)[#camera_missing(camera_field(row, "camera_type"))],
    text(size: font_size)[#stack_lines((camera_field(row, "sensor"), camera_field(row, "pixel")))],
    text(size: font_size)[#stack_lines((camera_field(row, "mount"), camera_field(row, "lens_aperture"), camera_field(row, "lens_length")))],
    text(size: font_size)[#camera_missing(camera_field(row, "battery"))],
    text(size: font_size)[#camera_missing(camera_field(row, "storage"))],
    text(size: font_size)[#camera_missing(camera_field(row, "location"))],
    camera_notes_cell(row, font_size),
  )).flatten(),
)