#import "../inventory_common.typ": *

#let render-lenses() = {
  let lenses = {
    visible-gear
      .filter(item => item.at("category", default: none) == "lens")
      .sorted(key: item => (
        sort-text(field(item, "mount")),
        numeric-thread(if field(item, "specs") == none { none } else { field(item, "specs").at("filter_thread", default: none) }),
        sort-text(field(item, "location")),
        minimum-focal-length(item),
        widest-aperture-number(item),
        sort-text(field(item, "brand")),
        sort-text(field(item, "model")),
        id-suffix(item),
      ))
  }
  let lens-rows = lenses.map(item => {
    let specs = field(item, "specs")
    let filter-thread = if specs == none { none } else { specs.at("filter_thread", default: none) }
    let filter = if filter-thread == none { copy-empty-value } else { clean(filter-thread) + unit-millimeter }
    let hood = if field(item, "hood_included") == "yes" { copy-hood-included } else { copy-no-hood }
    let connector = clean(display-field(item, "mount_connector"))
    let focus = if specs == none { copy-empty-value } else { clean(locale-terms.at("focus", default: (:)).at(str(specs.at("focus", default: none)), default: specs.at("focus", default: none))) }
    let lens-type = display-field(item, "lens_type")
    (
      id-cell(item),
      cell(clean(field(item, "brand")) + symbol-middle-dot + clean(field(item, "model")), detail: clean(field(item, "serial_id"))),
      cell(if specs == none { copy-empty-value } else { clean(specs.at("length", default: none)) + symbol-middle-dot + clean(specs.at("aperture", default: none)) }, detail: clean(lens-type)),
      cell(focus + symbol-middle-dot + clean(field(item, "mount")), detail: connector),
      cell(filter, detail: hood),
      cell(clean(display-field(item, "location")), detail: clean(display-field(item, "notes"))),
    )
  })
  let lens-has-spec = key => lenses.any(item => {
    let specs = field(item, "specs")
    specs != none and specs.at(key, default: none) != none
  })
  let optics-heading = (
    if lens-has-spec("length") { copy("focal-length") } else { none },
    if lens-has-spec("aperture") { copy("aperture") } else { none },
    if lenses.any(item => field(item, "lens_type") != none) { copy("lens-type") } else { none },
  ).filter(label => label != none).join(symbol-middle-dot)
  let connection-heading = (
    if lens-has-spec("focus") { copy("focus") } else { none },
    if lenses.any(item => field(item, "mount") != none) { copy("mount") } else { none },
    if lenses.any(item => field(item, "mount_connector") != none) { copy("system") } else { none },
  ).filter(label => label != none).join(symbol-middle-dot)
  let lens-columns = (
    copy("id"),
    heading-for(lenses, ((copy("brand"), "brand"), (copy("model"), "model"), (copy("serial-no"), "serial_id"))),
    if optics-heading == "" { copy("focal-length") + " / " + copy("lens-type") } else { optics-heading },
    if connection-heading == "" { copy("focus") + " / " + copy("mount") + " / " + copy("system") } else { connection-heading },
    heading-for(lenses, ((copy("filter-diameter"), "specs"), (copy("hood"), "hood_included"))),
    heading-for(lenses, ((copy("location-label"), "location"), (copy("notes-label"), "notes"))),
  )
  [
    #section(copy-lens-title, copy-lens-description, lenses.len())
    #align(center)[#image("../perception_length.svg", width: 100%)]
    #align(center)[#text(font: font-ui, size: 7pt, fill: color-text-muted)[#copy("lens-chart-caption")]]
    #linebreak()
    #align(right)[#text(font: font-ui, size: 6.5pt, fill: color-text-muted)[#copy("lens-chart-formula")]]
    #v(6pt)
    #draw-table(
      (0.62fr, 1.42fr, 1.42fr, 1.35fr, 1.03fr, 1.9fr),
      lens-columns,
      lens-rows,
    )
  ]
}
