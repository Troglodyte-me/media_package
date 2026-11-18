#import "../inventory_common.typ": *

#let render-accessories() = {
  let accessory-categories = ("filter", "thread-adapter", "iris", "hood")
  let accessories = {
    visible-gear
      .filter(item => item.at("category", default: none) in accessory-categories)
      .sorted(key: item => (
        numeric-thread(field(item, "filter_thread")),
        numeric-thread(field(item, "outer_thread")),
        sort-text(field(item, "location")),
        sort-text(field(item, "filter_type")),
        sort-text(field(item, "brand")),
        sort-text(field(item, "model")),
        id-suffix(item),
      ))
  }
  let filters = accessories.filter(item => field(item, "category") == "filter")
  let thread-accessories = accessories.filter(item => field(item, "category") in ("thread-adapter", "iris", "hood"))
  let accessory-rows(items) = items.map(item => {
    let thread = field(item, "filter_thread")
    let outer = field(item, "outer_thread")
    let thread-label = if thread == none {
      copy-empty-value
    } else if outer == none {
      clean(thread) + unit-millimeter
    } else {
      clean(thread) + symbol-thread-step + clean(outer) + unit-millimeter
    }
    let title = clean(field(item, "model"))
    let description = clean(display-field(item, "description"))
    let filter-type = clean(display-field(item, "filter_type"))
    let serial-id = clean(field(item, "serial_id"))
    let brand-detail = if filter-type == copy-empty-value {
      serial-id
    } else if serial-id == copy-empty-value {
      filter-type
    } else {
      filter-type + symbol-middle-dot + serial-id
    }
    (
      id-cell(item),
      cell(clean(field(item, "brand")), detail: brand-detail),
      cell(title, detail: if description == copy-empty-value { none } else { description }),
      cell(thread-label),
      cell(clean(display-field(item, "location"))),
      cell(clean(display-field(item, "notes"))),
    )
  })
  let accessory-columns(items) = (
    copy("id"),
    heading-for(items, ((copy("brand"), "brand"), (copy("camera-type-label"), "filter_type"), (copy("serial-no"), "serial_id"))),
    heading-for(items, ((copy("model"), "model"), (copy("description"), "description"))),
    heading-for(items, ((copy("threads-diameter"), "filter_thread"), (copy("outer-thread"), "outer_thread"))),
    copy("location-label"),
    copy("notes-label"),
  )
  let draw-accessory-group(title, items) = if items.len() == 0 { none } else {[
    #text(font: font-ui, size: 10pt, weight: "bold", fill: color-primary)[#title]
    #v(3pt)
    #draw-table(
      (0.62fr, 1.0fr, 2.22fr, 1.0fr, 0.82fr, 1.85fr),
      accessory-columns(items),
      accessory-rows(items),
    )
    #v(7pt)
  ]}
  let mount-adapters = visible-gear.filter(item => field(item, "category") == "mount-adapter")
  let mount-adapter-rows = mount-adapters.map(item => (
    id-cell(item),
    cell(clean(field(item, "brand")) + symbol-middle-dot + clean(field(item, "model")), detail: clean(display-field(item, "description"))),
    cell(clean(display-field(item, "location"))),
    cell(clean(display-field(item, "notes"))),
  ))
  let microphones = visible-gear.filter(item => field(item, "category") == "microphone")
  let microphone-rows = microphones.map(item => {
    let specs = field(item, "specs")
    let connector = if specs == none { none } else { specs.at("output_connector", default: specs.at("rx_output", default: none)) }
    let identification = (field(item, "brand"), field(item, "model"))
      .filter(value => value != none and value != "")
      .join(" ")
    (
      id-cell(item),
      cell(clean(display-field(item, "description")), detail: if identification == "" { none } else { identification }),
      cell(clean(connector)),
      cell(clean(display-field(item, "location")), detail: clean(display-field(item, "notes"))),
    )
  })
  [
    #section(
      copy-accessories-title,
      copy-accessories-description,
      accessories.len() + mount-adapters.len() + microphones.len(),
    )
    #draw-accessory-group(copy("filter-group-title"), filters)
    #draw-accessory-group(copy("thread-group-title"), thread-accessories)
    #if mount-adapters.len() > 0 [
      #text(font: font-ui, size: 10pt, weight: "bold", fill: color-primary)[#copy("mount-adapter-title")]
      #v(3pt)
      #draw-table(
        (0.62fr, 2.2fr, 0.9fr, 2fr),
        (copy("id"), copy("item"), copy("location-label"), copy("notes-label")),
        mount-adapter-rows,
      )
      #v(7pt)
    ]
    #if microphones.len() > 0 [
      #text(font: font-ui, size: 10pt, weight: "bold", fill: color-primary)[#copy("microphone-title")]
      #v(3pt)
      #draw-table(
        (0.62fr, 2.4fr, 1.65fr, 2fr),
        (copy("id"), copy("item"), copy("connector"), copy("location-label") + " / " + copy("notes-label")),
        microphone-rows,
      )
    ]
  ]
}
