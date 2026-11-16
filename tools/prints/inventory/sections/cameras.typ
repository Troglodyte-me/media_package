#import "../camera_inventory_common.typ": *

#let render-cameras() = {
  let cameras = {
    visible-gear
      .filter(item => field(item, "category") in ("camera", "camera-body", "body"))
      .sorted(key: item => (
        sort-text(field(item, "mount")),
        sort-text(field(item, "location")),
        megapixel-sort(item),
        sort-text(field(item, "brand")),
        sort-text(field(item, "model")),
        id-suffix(item),
      ))
  }
  let fixed-lens-cameras = cameras.filter(item => field(item, "category") == "camera")
  let camera-bodies = cameras.filter(item => field(item, "category") in ("camera-body", "body"))
  let camera-rows(items) = items.map(item => {
    let serial = clean(field(item, "serial_id"))
    let lens = field(item, "lens_specs")
    let actual = if lens == none { none } else { lens.at("focal_length_actual", default: lens.at("length", default: none)) }
    let equivalent = if lens == none { none } else { lens.at("focal_length_equiv_35mm", default: lens.at("focal_length_equivalent_35mm", default: none)) }
    let aperture = if lens == none { none } else { lens.at("aperture_range", default: lens.at("aperture", default: none)) }
    let zoom = if lens == none { none } else { lens.at("zoom_optical", default: none) }
    let focal-labels = (
      if actual == none { none } else { clean(actual) + " " + copy("actual") },
      if equivalent == none { none } else { clean(equivalent) + " " + copy("equivalent") },
    ).filter(value => value != none)
    let optics = if field(item, "mount") != none {
      clean(field(item, "mount"))
    } else if focal-labels.len() > 0 {
      focal-labels.join(symbol-middle-dot)
    } else {
      copy-empty-value
    }
    let optics-detail = (
      if aperture == none { none } else { clean(aperture) },
      if zoom == none { none } else { clean(zoom) + " " + copy("optical-zoom") },
      if display-field(item, "camera_type") == none { none } else { display-field(item, "camera_type") },
    ).filter(value => value != none).join(symbol-middle-dot)
    (
      id-cell(item),
      cell(clean(field(item, "brand")) + symbol-middle-dot + clean(field(item, "model")), detail: serial),
      cell(sensor-text(field(item, "sensor")), detail: resolution-text(item)),
      cell(optics, detail: optics-detail),
      cell(clean(display-field(item, "battery")), detail: clean(display-field(item, "storage"))),
      cell(clean(display-field(item, "location")), detail: clean(display-field(item, "notes"))),
    )
  })
  let camera-columns(items) = (
    copy("id"),
    heading-for(items, ((copy("brand"), "brand"), (copy("model"), "model"), (copy("serial-no"), "serial_id"))),
    heading-for(items, ((copy("sensor"), "sensor"), (copy("resolution"), "pixel"), (copy("megapixels"), "megapixels"))),
    heading-for(items, ((copy("mount"), "mount"), (copy("built-in-lens"), "lens_specs"), (copy("camera-type-label"), "camera_type"))),
    heading-for(items, ((copy("battery"), "battery"), (copy("storage"), "storage"))),
    heading-for(items, ((copy("location-label"), "location"), (copy("notes-label"), "notes"))),
  )
  let draw-camera-group(title, items) = if items.len() == 0 { none } else {[
    #text(font: font-ui, size: 10pt, weight: "bold", fill: color-primary)[#title]
    #v(3pt)
    #draw-table(
      (0.62fr, 1.65fr, 1.22fr, 1.4fr, 1.18fr, 1.8fr),
      camera-columns(items),
      camera-rows(items),
    )
    #v(7pt)
  ]}
  [
    #section(copy-camera-title, copy-camera-description, cameras.len())
    #align(center)[
      #block(stroke: 0.4pt + color-border, radius: 2pt, inset: 5pt)[
        #image("../camera_gear_assembly.svg", width: 68%)
        #v(2pt)
        #align(center)[#text(font: font-ui, size: 7pt, weight: "medium", fill: color-primary)[#copy-assembly-caption]]
      ]
    ]
    #v(6pt)
    #draw-camera-group(copy("fixed-camera-title"), fixed-lens-cameras)
    #draw-camera-group(copy("camera-body-title"), camera-bodies)
  ]
}
