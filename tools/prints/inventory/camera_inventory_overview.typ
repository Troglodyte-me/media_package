// Portrait equipment register; all inventory rows are read from the adjacent YAML file.

// This file defines the layout and content for the camera equipment inventory overview, including sections for cameras, lenses, and accessories.


// Load the inventory data from the YAML file and extract the gear section.
#let inventory = yaml("cameras_inventory_20261110.yaml")
#let gear = inventory.at("gear")

// Define color scheme and visual constants for the inventory overview.
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

// Define copy text for various sections and labels in the inventory overview.
#let copy-footer-title = "Camera equipment inventory · " + datetime.today().display("[day] [month repr:short] [year]")
#let copy-section-label = "Equipment register /"
#let copy-item-label = "items"
#let copy-empty-value = "—"
#let copy-camera-title = "Cameras & bodies"
#let copy-camera-description = "Mount or built-in optics, sensor, power, storage and location are grouped for quick checks."
#let copy-assembly-caption = "Body → mount → lens → optional front-thread accessory"
#let copy-lens-title = "Lenses"
#let copy-lens-description = "Check mount and filter-thread compatibility, then compare focal range and aperture."
#let copy-accessories-title = "Filters & accessories"
#let copy-accessories-description = "Filters, step-up rings, soft-focus disc, iris and hood; thread sizes are shown in millimeters."
#let copy-hood-included = "hood included"
#let copy-no-hood = "no hood"
#let symbol-middle-dot = " · "
#let unit-millimeter = "mm"
#let symbol-thread-step = " → "

// Define page layout, footer, and text styles for the inventory overview.
// Changes:
// - enhance readability and enforce structure: 
//   --> consider using a font with sarifs within text body for better legibility
//   --> change font to sans-serif when it's not part of the text 
//   --> depending on the OS, use fonts that are available and render well for both serif and sans-serif text
// - sort lines in the tables by given criteria for better organization and readability (see below), but use the IDs as the primary reference for uniqueness and consistency from the YAML file
//    --> only take the numbers from the IDs (e.g. "cam_01" --> "01" etc)
//   --> sort cameras by megapixels in ascending order, then by Brand and then Model. If there is still doubt, use the ID as the final tiebreaker.
//   --> sort lenses by focal length in ascending order, then by aperture, inner and outer threading, and finally by ID as the tiebreaker.
//   --> sort filters & (filter) accessories by inner thread, then outer thread (if available) size then by type, brand and model, and finally by ID as the tiebreaker.
// - for the tables, filter the gear based on ID pre-fixes: 
//   --> "cam_" for cameras, "lens_" for lenses, "flt_" for filters and (filter related) accessories, 
//   --> other gear and accessories are not yet systematized. Ignore for now
// - The margins are not satisfactory given the page size and content density; consider adjusting their values for better layout and readability in a consistent manner. 
//   --> subjective observation: width appears reasonable for cameras and lenses, but appears loose for filters and other accessories
//   --> the headers are consistently tightly spaced, which may affect readability. consider increasing the spacing between headers and content for better readability
//   --> the footers are currently good enough (to be maintained as is)
// - consider applying a color scheme more friendly to a generic fire fighter branding in blues (i.e. #1a365d) and reds (or orange for special highlights i.e. #e97132). 
// - I like the subtitle for the camera .SVG picture. However, it's visually a bit detached from its subject. Consider a style that doesn't describe but complement the visual content instead. Perhaps use a more integrated placement or subtle visual cues to connect it with the image.
// - Currently YAML and TYP files mixing English and German terminology, which may lead to inconsistencies and confusion. 
//   --> Consider coding in a setup for a multilingual approach
//   --> operational language is English, raising maintainability and consistency across the project and different cultures or teams involved in its development
//   --> English is also useful when looking up gear specifications, manuals, and online resources, therefore maintaining English as the operational language ensures easier access to relevant information.
//   --> the final print version should display content in the operational language, as a fallback where translations are missing or incomplete
//   --> to ensure non-english speakers can still operate the files, provide clear documentation and translation support within the file structure and put all variables needing translation or case individual configuration in a dedicated section at the beginning of the file well separated and easily identifiable
// - I've filled the YAML with actual data and I'm still in the process of refining its configuration. 
//   --> for the purpose of this project, ensure that the YAML structure and TYP configuration are aligned and consistently applied throughout the files. For this you can access and restructure both files as needed to maintain consistency and correctness.
//   --> propose templates for consistent structure and formatting across in the YAML for seamless integration with the TYP configuration
//   --> consider that not all available data may be useful in the YAML, but may still be necessary for completeness or future use
//   --> Users of this list will probably not have access to the full YAML configuration or deeper knowledge of photography. All data in the final output should be understandable and usable without requiring direct access to the YAML or further marking of the gear - and the table needs to hold all necessary information for practical use.
//   --> also brush over the YAML and see if redundant or complicated data can be simplified or removed for clarity (e.g. the notes should be short and concise, not run over several lines just repeating the same information or bloating with information hardly used)
//   --> ensure that the final output is user-friendly and does not require specialized knowledge to interpret correctly
// [x] Applied serif body/sans-serif interface typography, stable ID suffixes, section-specific category filters, sort keys, and clearer table hierarchy.
// [x] Category controls inclusion; a build-time check verifies known category-to-ID prefixes without rewriting inventory IDs.
// [x] Numeric sorting parses comparable MP/mm values only; magnification-only values such as "8x" remain unchanged and are excluded from numeric focal-length sorting. Fixed-lens cameras show actual and 35 mm-equivalent ranges when available.
// [x] Updated the navy/orange palette, modest header spacing, integrated camera diagram caption, and narrower accessory table; the existing footer and A4 margins remain.
// [x] English labels/copy are centralized above; original YAML values remain unchanged as agreed. A separate translation layer and YAML cleanup/template migration are deferred to avoid altering evolving source data.
// [x] Kept the YAML as the source of truth and render only the fields needed for practical identification, compatibility, location, and comparison.
#set page(paper: "a4", flipped: false, margin: (x: 10mm, y: 9mm), footer: context [
  #line(length: 100%, stroke: 0.45pt + color-border)
  #v(3pt)
  #text(font: font-ui, size: 6.2pt, fill: color-text-muted)[#copy-footer-title]
  #h(1fr)
  #text(font: font-ui, size: 6.2pt, fill: color-text-muted)[#counter(page).display("1")]
])
#set text(font: font-body, size: 7.2pt, fill: color-text)
#set par(leading: 0.9em, spacing: 0pt)
#show table.cell: set text(font: font-body, size: 7.1pt, fill: color-text)

#let clean(value) = if value == none { copy-empty-value } else { str(value) }
#let field(item, key) = item.at(key, default: none)
#let sensor-text(value) = if type(value) == dictionary {
  clean(value.at("type", default: none)) + symbol-middle-dot + clean(value.at("size", default: none))
} else {
  clean(value)
}
#let resolution-text(item) = if field(item, "pixel") != none {
  clean(field(item, "pixel"))
} else if field(item, "megapixels") != none {
  clean(field(item, "megapixels")) + " MP"
} else {
  copy-empty-value
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
#let heading(label) = text(font: font-ui, size: 7pt, weight: "bold", fill: color-background)[#label]
#let section(title, strap, count) = [
  #text(font: font-ui, size: 7pt, weight: "bold", fill: color-secondary)[#copy-section-label #count #copy-item-label]
  #v(2pt)
  #text(font: font-ui, size: 18pt, weight: "bold", fill: color-primary)[#title]
  #v(1pt)
  #text(font: font-ui, size: 7.5pt, fill: color-text-muted)[#strap]
  #v(5pt)
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

// Extract and prepare camera-related data from the inventory for display in the overview.
#let cameras = {
  gear
    .filter(item => item.at("category", default: none) in ("camera", "camera-body", "body"))
    .sorted(key: item => (
      sort-text(field(item, "mount")),
      sort-text(field(item, "location")),
      megapixel-sort(item),
      sort-text(field(item, "brand")),
      sort-text(field(item, "model")),
      id-suffix(item),
    ))
}
#let camera-rows = cameras.map(item => {
  let id = clean(field(item, "serial_id"))
  let lens = field(item, "lens_specs")
  let actual = if lens == none { none } else { lens.at("focal_length_actual", default: lens.at("length", default: none)) }
  let equivalent = if lens == none { none } else { lens.at("focal_length_equiv_35mm", default: lens.at("focal_length_equivalent_35mm", default: none)) }
  let aperture = if lens == none { none } else { lens.at("aperture_range", default: lens.at("aperture", default: none)) }
  let zoom = if lens == none { none } else { lens.at("zoom_optical", default: none) }
  let focal-labels = (
    if actual == none { none } else { clean(actual) + " actual" },
    if equivalent == none { none } else { clean(equivalent) + " eq" },
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
    if zoom == none { none } else { clean(zoom) + " optical zoom" },
    if field(item, "camera_type") == none { none } else { clean(field(item, "camera_type")) },
  ).filter(value => value != none).join(symbol-middle-dot)
  (
    cell(id-suffix(item)),
    cell(clean(field(item, "brand")) + symbol-middle-dot + clean(field(item, "model")), detail: id),
    cell(sensor-text(field(item, "sensor")), detail: resolution-text(item)),
    cell(optics, detail: optics-detail),
    cell(clean(field(item, "battery")), detail: clean(field(item, "storage"))),
    cell(clean(field(item, "location")), detail: clean(field(item, "notes"))),
  )
})


// Camera section
#section(copy-camera-title, copy-camera-description, cameras.len())
#align(center)[
  #block(fill: color-background-alt, stroke: 0.4pt + color-border, radius: 2pt, inset: 5pt)[
    #image("camera_gear_assembly.svg", width: 68%)
    #v(2pt)
    #align(center)[#text(font: font-ui, size: 7pt, weight: "medium", fill: color-primary)[#copy-assembly-caption]]
  ]
]
#v(4pt)
#let camera-columns = (
  "ID",
  heading-for(cameras, (("Brand", "brand"), ("model", "model"), ("Serial no.", "serial_id"))),
  heading-for(cameras, (("Sensor", "sensor"), ("resolution", "pixel"), ("megapixels", "megapixels"))),
  heading-for(cameras, (("Mount", "mount"), ("built-in lens", "lens_specs"), ("type", "camera_type"))),
  heading-for(cameras, (("Battery", "battery"), ("storage", "storage"))),
  heading-for(cameras, (("Location", "location"), ("notes", "notes"))),
)
#draw-table(
  (0.34fr, 1.55fr, 1.23fr, 1.35fr, 1.18fr, 1.75fr),
  camera-columns,
  camera-rows,
)

#pagebreak()
// Lens section
// Changes:
// - add image here: perception_length.svg
//   --> file needs assambling first...
// - to illustrate the perception of focal length as it relates to lens characteristics and sensor size, a visual representation will be included using the perception_length.svg image.
//   --> this will help users better understand how different lenses affect the field of view and image composition, when they select it in conjunction with their camera's sensor size (see camera table).
//   --> the image will be placed above the lens table for visual reference.
// - build the code for the SVG like this: 
//   --> the SVG will be a grid x:y
//   --> x represents the focal length and starts at coordinate 0
//   --> y represents the size of the sensor, with the biggest sensor at the top and the smallest at the bottom, ergo:
//     >> sensor size "0" is at the bottom, where y = 0
//     >> the biggest sensor size "n" is at the top, where y = n
//   --> in the negative space of focal length (x<0) will be the names of sensor sizes, providing a reference for the corresponding y-coordinate.
//     >> a considerate spacing for the sensor names to avoid overlap and ensure readability is required
//     >> selection of sensor types/sizes meaningful for the intended visualization is important. As a baseline full-frame (35mm) can be used as a reference point. "Medium format" can be used for larger sensors, and "APS-C" or "Micro Four Thirds" for smaller sensors. Also consider including other sensor sizes relevant to the intended audience and use case (see the YAML for reference, but also include sensor sizes for typical smart phones e.g. my phones are iPhone SE and Google Pixel 9 Pro).
// --> add a reference line for normal human vision, indicating the typical field of view perceived by the human eye.
//     >> it should intersect y-axis (Sensor=Full-frame) and x-axis (focal length) = 50mm
//     >> then it should run accordingly in a single uninterrupted and streight line through MFT (~25mm), APS-C (~35mm), and other sensor sizes as appropriate. In order to make this work, the sensor sizes need to be accurately represented along the y-axis.
//     >> to further enhance the visualization, consider adding labels or markers along the human perception reference line to indicate areas of interest:
//       >>> left and right of the reference line add confidence intervals as a range of human perception (e.g., ±33%). Keep this less prominent than the main reference line to avoid visual clutter and also to provide context for the variability in human vision.
//       >>> spell out, which area of the grid corresponds to the typical human field of view, providing a clear visual cue for users to understand the relationship between sensor size, focal length, and perceived field of view, like wide angle, normal vision, and telephoto.
//       >>> utilize the YAML file, to see how big the grid must be to accommodate all relevant sensor sizes and focal lengths.
//       >>> ensure that the grid is scaled appropriately so that the visual representation remains accurate and informative for users.
//   --> consider adding grid lines and shading to improve readability and visual separation of different sensor sizes and focal lengths.
//     >> do vertical grid lines for focal lengths at regular intervals, 25mm, 50mm, 75mm, 100mm, and so on
//     >> consider adding vertical shading on the grid to differentiate between focal length ranges and improve visual clarity e.g. at every 5mm interval
//     >> highlight the Full-frame sensor line to make it easily distinguishable from other sensor sizes
//   --> consider adding annotations or labels for reference lines, sensor sizes, and focal lengths to improve clarity and user understanding of the visualization. 
//     >> add device references to the sensor label in fine print so readers can associate a specific sensor size with the corresponding class of devices (e.g. full-frame as industry standard for analog photography, versus 1/4" CMOS for typical smartphones, and so on).
//     >> consider adding the calculation factor (full-frame = "1:1") for other sensor sizes as well, indicating their relative size compared to full-frame.
// the x and y coordinates run on the 0,0 coordinates of the  point will represent the origin for the visual representation of focal length perception.
// [x] Created the SVG with actual focal length on x and normalized sensor diagonal on y; included labeled representative formats, a 25 mm grid, and the 35/50/70 mm full-frame-equivalent references.
// [~] Reframed the suggested "human vision" line and ±33% intervals as photographic wide/normal/telephoto conventions. The 50 mm line is not presented as a claim about human vision.
// [x] Added approximate generic phone sensor examples and source notes; no exact iPhone SE or Pixel model claim is made because sensor configurations vary by model/camera.
// [x] Placed the chart above the lens table at less than half-page height; retained readable table sizing and repeatable table headers.
#let lenses = {
  gear
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
#let lens-rows = lenses.map(item => {
  let specs = field(item, "specs")
  let filter-thread = if specs == none { none } else { specs.at("filter_thread", default: none) }
  let filt = if filter-thread == none { copy-empty-value } else { clean(filter-thread) + unit-millimeter }
  let hood = if field(item, "hood_included") == "yes" { copy-hood-included } else { copy-no-hood }
  let connector = clean(field(item, "mount_connector"))
  let focus = if specs == none { copy-empty-value } else { clean(specs.at("focus", default: none)) }
  (
    cell(id-suffix(item)),
    cell(clean(field(item, "brand")) + symbol-middle-dot + clean(field(item, "model")), detail: clean(field(item, "serial_id"))),
    cell(if specs == none { copy-empty-value } else { clean(specs.at("length", default: none)) + symbol-middle-dot + clean(specs.at("aperture", default: none)) }, detail: clean(field(item, "lens_type"))),
    cell(focus + symbol-middle-dot + clean(field(item, "mount")), detail: connector),
    cell(filt, detail: hood),
    cell(clean(field(item, "location")), detail: clean(field(item, "notes"))),
  )
})
#let lens-has-spec = key => lenses.any(item => {
  let specs = field(item, "specs")
  specs != none and specs.at(key, default: none) != none
})
#let lens-optics-heading = (
  if lens-has-spec("length") { "Focal length" } else { none },
  if lens-has-spec("aperture") { "aperture" } else { none },
  if lenses.any(item => field(item, "lens_type") != none) { "type" } else { none },
).filter(label => label != none).join(symbol-middle-dot)
#let lens-connection-heading = (
  if lens-has-spec("focus") { "Focus" } else { none },
  if lenses.any(item => field(item, "mount") != none) { "Mount" } else { none },
  if lenses.any(item => field(item, "mount_connector") != none) { "system" } else { none },
).filter(label => label != none).join(symbol-middle-dot)
#let lens-columns = (
  "ID",
  heading-for(lenses, (("Brand", "brand"), ("model", "model"), ("Serial no.", "serial_id"))),
  if lens-optics-heading == "" { "Optics / type" } else { lens-optics-heading },
  if lens-connection-heading == "" { "Focus / mount / system" } else { lens-connection-heading },
  heading-for(lenses, (("Filter (Ø)", "specs"), ("hood", "hood_included"))),
  heading-for(lenses, (("Location", "location"), ("notes", "notes"))),
)
#section(copy-lens-title, copy-lens-description, lenses.len())
#align(center)[#image("perception_length.svg", width: 100%)]
#v(4pt)
#draw-table(
  (0.34fr, 1.42fr, 1.42fr, 1.35fr, 1.03fr, 1.9fr),
  lens-columns,
  lens-rows,
)


#pagebreak()
// Filter & accessories section
#let accessory-categories = ("filter", "thread-adapter", "iris", "hood")
#let accessories = {
  gear
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
#let accessory-rows = accessories.map(item => {
  let thread = field(item, "filter_thread")
  let outer = field(item, "outer_thread")
  let thread-label = if thread == none { copy-empty-value } else if outer == none { clean(thread) + unit-millimeter } else { clean(thread) + symbol-thread-step + clean(outer) + unit-millimeter }
  let title = clean(field(item, "model"))
  let description = clean(field(item, "description"))
  let filter-type = clean(field(item, "filter_type"))
  let serial-id = clean(field(item, "serial_id"))
  let brand-detail = if filter-type == copy-empty-value { serial-id } else if serial-id == copy-empty-value { filter-type } else { filter-type + symbol-middle-dot + serial-id }
  (
    cell(id-suffix(item)),
    cell(clean(field(item, "brand")), detail: brand-detail),
    cell(title, detail: if description == copy-empty-value { none } else { description }),
    cell(thread-label),
    cell(clean(field(item, "location"))),
    cell(clean(field(item, "notes"))),
  )
})
#let accessory-columns = (
  "ID",
  heading-for(accessories, (("Brand", "brand"), ("type", "filter_type"), ("Serial no.", "serial_id"))),
  heading-for(accessories, (("Model", "model"), ("description", "description"))),
  heading-for(accessories, (("Threads (Ø)", "filter_thread"), ("outer thread", "outer_thread"))),
  heading-for(accessories, (("Location", "location"),)),
  heading-for(accessories, (("Notes", "notes"),)),
)
#section(copy-accessories-title, copy-accessories-description, accessories.len())
#align(center)[
  #box(width: 94%)[
    #draw-table(
      (0.34fr, 1.0fr, 2.22fr, 1.0fr, 0.82fr, 1.85fr),
      accessory-columns,
      accessory-rows,
    )
  ]
]
