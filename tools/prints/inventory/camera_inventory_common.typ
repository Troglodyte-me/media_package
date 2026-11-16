// Shared data, localization, styling, and table helpers for the camera inventory print.
#let print-locale = "de"
#let include-unavailable = false
#let project-url = "https://github.com/Troglodyte-me/media_package"

#let inventory = yaml("cameras_inventory_20261110.yaml")
#assert(inventory.at("schema_version", default: none) == 1, message: "Unsupported camera inventory schema version.")
#let translations = inventory.at("translations")
#assert(translations.at(print-locale, default: none) != none, message: "The selected print locale has no translation entry.")
#let gear = inventory.at("gear")

#let color-primary = rgb("1a365d")
#let color-secondary = color-primary
#let color-accent = rgb("e97132")
#let color-background = white
#let color-background-alt = rgb("f2f6f7")
#let color-border = rgb("d9e2e5")
#let color-text = rgb("1c2933")
#let color-text-muted = rgb("637580")
#let font-body = "Libertinus Serif"
#let font-ui = "Arial"

#let locale-copy = translations.at(print-locale, default: (:)).at("global", default: (:))
#let english-copy = translations.at("en", default: (:)).at("global", default: (:))
#let copy(key) = locale-copy.at(key, default: english-copy.at(key, default: key))
#let locale-terms = translations.at(print-locale, default: (:)).at("terms", default: (:))
#let localized-field(item, key) = {
  let id = str(item.at("id", default: ""))
  let selected = translations.at(print-locale, default: (:))
    .at("gear", default: (:))
    .at(id, default: (:))
    .at(key, default: none)
  let english = translations.at("en", default: (:))
    .at("gear", default: (:))
    .at(id, default: (:))
    .at(key, default: none)
  if selected != none { selected }
  else if english != none { english }
  else { item.at(key, default: none) }
}
#let display-field(item, key) = {
  let value = localized-field(item, key)
  let terms = locale-terms.at(key, default: (:))
  if value == none { none } else { terms.at(str(value), default: value) }
}
#let available(item) = item.at("availability", default: true)
#assert(gear.all(item => type(available(item)) == bool), message: "Inventory availability must be a boolean.")
#assert(
  gear.all(item => gear.filter(other => other.at("id", default: none) == item.at("id", default: none)).len() == 1),
  message: "Inventory IDs must be unique.",
)
#let visible-gear = gear.filter(item => available(item) or include-unavailable)

#let copy-footer-title = copy("footer-title") + " · " + datetime.today().display("[year]-[month]-[day]")
#let copy-section-label = copy("section-label")
#let copy-item-label = copy("item-label")
#let copy-empty-value = copy("empty-value")
#let copy-camera-title = copy("camera-title")
#let copy-camera-description = copy("camera-description")
#let copy-assembly-caption = copy("assembly-caption")
#let copy-lens-title = copy("lens-title")
#let copy-lens-description = copy("lens-description")
#let copy-accessories-title = copy("accessories-title")
#let copy-accessories-description = copy("accessories-description")
#let copy-hood-included = copy("hood-included")
#let copy-no-hood = copy("no-hood")
#let symbol-middle-dot = copy("symbol-middle-dot")
#let unit-millimeter = copy("unit-millimeter")
#let symbol-thread-step = copy("symbol-thread-step")

#let clean(value) = if value == none { copy-empty-value } else { str(value) }
#let field(item, key) = item.at(key, default: none)
#let sensor-text(value) = if type(value) == dictionary {
  clean(value.at("type", default: none)) + symbol-middle-dot + clean(value.at("size", default: none))
} else {
  clean(value)
}
#let resolution-text(item) = {
  let pixel = display-field(item, "pixel")
  if pixel != none {
    clean(pixel)
  } else if field(item, "megapixels") != none {
    clean(field(item, "megapixels")) + " MP"
  } else {
    copy-empty-value
  }
}
#let id-suffix(item) = {
  let parts = str(field(item, "id")).split("-")
  if parts.len() > 1 { parts.last() } else { str(field(item, "id")) }
}
#let sort-text(value) = if value == none { "~" } else { str(value) }
#let megapixel-sort(item) = {
  let megapixels = field(item, "megapixels")
  if megapixels != none {
    float(str(megapixels))
  } else {
    let pixel = field(item, "pixel")
    let parts = if pixel == none { () } else { str(pixel).split(" MP") }
    if parts.len() > 1 { float(parts.first()) } else { 1e9 }
  }
}
#let minimum-focal-length(item) = {
  let specs = field(item, "specs")
  let length = if specs == none { none } else { specs.at("length", default: none) }
  let parts = if length == none { () } else { str(length).split("mm") }
  if parts.len() > 1 { float(parts.first().split("-").first()) } else { 1e9 }
}
#let widest-aperture-number(item) = {
  let specs = field(item, "specs")
  let aperture = if specs == none { none } else { specs.at("aperture", default: none) }
  if aperture == none { 1e9 } else { float(str(aperture).replace("f/", "").split("-").first()) }
}
#let numeric-thread(value) = if value == none { 1e9 } else { float(str(value).replace("mm", "")) }
#let prefix-for-category(category) = {
  if category in ("camera", "camera-body", "body") { "cam" }
  else if category == "lens" { "lens" }
  else if category in ("filter", "thread-adapter", "iris", "hood") { "filt" }
  else if category == "mount-adapter" { "mnt" }
  else if category == "microphone" { "mic" }
  else { none }
}
#let categorized-gear = gear.filter(item => prefix-for-category(field(item, "category")) != none)
#assert(categorized-gear.len() == gear.len(), message: "An inventory category is not wired to an overview section.")
#assert(
  categorized-gear.all(item => str(field(item, "id")).split("-").first() == prefix-for-category(field(item, "category"))),
  message: "An inventory ID prefix does not match its category.",
)
#let heading-for(items, fields, fallback: "Other") = {
  let labels = fields
    .filter(((label, key)) => items.any(item => item.at(key, default: none) != none))
    .map(((label, key)) => label)
  if labels.len() == 0 { fallback } else { labels.join(symbol-middle-dot) }
}
#let subline(value) = text(font: font-ui, size: 6.5pt, fill: color-text-muted)[#value]
#let cell(main, detail: none) = if detail == none or detail == "" {
  text(weight: "medium")[#main]
} else {
  [#text(weight: "medium")[#main] #linebreak() #subline(detail)]
}
#let id-cell(item) = cell(field(item, "id"), detail: if available(item) { none } else { copy("unavailable") })
#let heading(label) = text(font: font-ui, size: 7pt, weight: "bold", fill: color-background)[#label]
#let section(title, strap, count) = [
  #text(font: font-ui, size: 7pt, weight: "bold", fill: color-secondary)[#copy-section-label #count #copy-item-label]
  #v(2pt)
  #text(font: font-ui, size: 18pt, weight: "bold", fill: color-primary)[#title]
  #v(1pt)
  #text(font: font-ui, size: 7.5pt, fill: color-text-muted)[#strap]
  #v(8pt)
]
#let draw-table(widths, labels, rows) = table(
  columns: widths,
  inset: (x, y) => if y == 0 { (x: 4pt, y: 4.5pt) } else { (x: 4pt, y: 3.5pt) },
  align: left,
  stroke: (x, y) => if y == 0 { (bottom: 1pt + color-accent) } else { (bottom: 0.35pt + color-border) },
  fill: (x, y) => if y == 0 { color-primary } else if calc.even(y) { color-background-alt } else { color-background },
  table.header(..labels.map(heading)),
  ..rows.flatten(),
)
