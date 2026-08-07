// Media Equipment & Camera Inventory
// Repository: https://github.com/Troglodyte-me/media_package/
// thanks at Google Gemini.Canvas for the inspiration and guidance on this project. The inventory overview is designed to provide a comprehensive snapshot of all cameras, lenses, filters, and accessories included in the media package. It includes detailed specifications, usage notes, and visual aids to help users understand the equipment's capabilities and applications.

#set page(
  paper: "a4",
  margin: (x: 1.8cm, top: 2cm, bottom: 2.5cm),
  header: align(right)[
    #text(size: 8pt, fill: luma(120))[
      Media Equipment Package | Inventory Overview
    ]
  ],
  footer: [
    #align(center)[
      #text(size: 8pt, fill: luma(120))[
        Page #context counter(page).display() | github.com/Troglodyte-me/media_package
      ]
    ]
  ]
)
#set text(
  font: "Arial",
  size: 9.5pt,
  lang: "de"
)
#let primary-color = rgb("#1a365d")
#let secondary-color = rgb("#2b6cb0")
#let light-bg = rgb("#f7fafc")// Document Title Header
#align(center)[
  #block(
    fill: primary-color,
    inset: 14pt,
    radius: 4pt,
    width: 100%,
    [
      #text(
        fill: white,
        size: 18pt,
        weight: "bold"
      )[Kamera & Medienausstattung]
      #v(2pt)
      #text(fill: white.darken(10%), size: 11pt)[Camera & Media Equipment Inventory]
    ]
  )
]
#v(10pt)
#block(
  fill: light-bg,
  inset: 10pt,
  stroke: 0.5pt + rgb("#e2e8f0"),
  radius: 4pt,
  [
    #text(
      weight: "bold",
      size: 10pt,
      fill: primary-color
    )[Hinweis für Einsteiger / Guide for Beginners]
#v(3pt)
Diese Übersicht dokumentiert alle Kameras, Objektive, Filter und Zubehörteile im Medienpaket.
Kurzer Begriffserklärungs-Guide:
- Sensor / Crop-Faktor: Gibt die Größe des Lichtsensors an. Vollformat (35mm) dient als Referenz; kleinere Sensoren (z. B. MFT, 1/2.3") verengen den Bildwinkel (Crop).
- Brennweite (Focal Length): Gemessen in mm. Weitwinkel (< 35mm) erfasst viel Raum; Tele (> 70mm) holt entfernte Motive nah heran; ~50mm entspricht etwa der menschlichen Wahrnehmung.
- Blende (Aperture / f-stop): Kleine Zahlen (z. B. f/1.7) bedeuten eine große Öffnung (viel Licht, unscharfer Hintergrund); große Zahlen (z. B. f/8) bedeuten viel Durchgehende Schärfe.
- Filtergewinde (Filter Thread ø): Durchmesser in Millimetern (z. B. 52mm) zum Aufschrauben von Filtern oder Gegenlichtblenden.
  ]
)
#v(12pt)// Section 1: Cameras
== 1. Kameras / Cameras
#let camera-data = csv("cameras_inventory.csv")
#table(
  columns: (auto, 2.2fr, 2fr, 1.8fr, 1.2fr, 1fr, 1fr, 1.2fr, 2fr),
  fill: (x, y) => if y == 0 { secondary-color } else if calc.even(y) { rgb("#f1f5f9") } else { white },
  stroke: (x, y) => if y == 0 { none } else { 0.4pt + rgb("#cbd5e1") },
  align: (col, row) => if row == 0 { center + horizon } else { left + horizon },// Table Headers with white text
..camera-data.at(0).map(header => text(fill: white, weight: "bold", size: 8.5pt)[#header]),// Table Rows
..camera-data.slice(1).flatten().map(cell => text(size: 8.5pt)[#cell])
)
#v(16pt)// Section 2: Focal Length & Sensor Field of View Visualizer
== 2. Sensorgrößen & Brennweiten / Sensor Sizes & Perception
#block(
  width: 100%,
  stroke: 0.5pt + rgb("#cbd5e1"),
  inset: 10pt,
  radius: 4pt,
  [
    #align(center)[
      // External Image Reference
      // #image("sensor_focal_length_diagram.png", width: 85%)
      #image("../../../docs/SensorLensSizes.svg", width: 85%)
      
    ]
    #v(4pt)
    #text(
      size: 8pt,
      style: "italic",
      fill: luma(100))[
    Abbildung 1: Zusammenhang zwischen Sensorformat (Full-frame, APS-C, M4/3, 1/2.3"), Brennweite (25mm - 100mm) und Bildwinkel (Weitwinkel vs. Tele vs. Menschliche Wahrnehmung).
      ]
  ]
)
#v(16pt)// Section 3: Lenses
== 3. Objektive / Lenses
#let lens-data = csv("lenses_inventory.csv")
#table(
  columns: (auto, 1.8fr, 1.2fr, 1.2fr, 0.8fr, 1fr, 1fr, 1fr, 0.7fr, 1.2fr, 1.2fr, 1.8fr),
  fill: (x, y) => if y == 0 { secondary-color } else if calc.even(y) { rgb("#f1f5f9") } else { white },
  stroke: (x, y) => if y == 0 { none } else { 0.4pt + rgb("#cbd5e1") },
  align: (col, row) => if row == 0 { center + horizon } else { left + horizon },..lens-data.at(0).map(header => text(fill: white, weight: "bold", size: 8pt)[#header]),
..lens-data.slice(1).flatten().map(cell => text(size: 8pt)[#cell])
)
#v(16pt)// Section 4: Filters & Adapters
== 4. Filter & Adapter / Filters & Adapters
#let filter-data = csv("filters_inventory.csv")
#table(
  columns: (auto, 1.8fr, 3fr, 1.2fr, 1.5fr, 3fr),
  fill: (x, y) => if y == 0 { secondary-color } else if calc.even(y) { rgb("#f1f5f9") } else { white },
  stroke: (x, y) => if y == 0 { none } else { 0.4pt + rgb("#cbd5e1") },
  align: (col, row) => if row == 0 { center + horizon } else { left + horizon },..filter-data.at(0).map(header => text(fill: white, weight: "bold", size: 8.5pt)[#header]),
  ..filter-data.slice(1).flatten().map(cell => text(size: 8.5pt)[#cell])
)
== 5. Sonstiges & Zubehör / Miscellaneous & Accessories
#grid(
  columns: (1fr, 1fr),
  gutter: 12pt,
  block(
    fill: light-bg,
    inset: 10pt,
    width: 100%,
    stroke: 0.4pt + rgb("#cbd5e1"),
    radius: 4pt,
    [
  #text(
    weight: "bold",
    fill: primary-color
  )[
    Adapter & Stromversorgung / Adapters & Power
  ]
- 2x Objektiv-Adapter: P/K Mount $-->$ M4/3 System (1x Koffer, 1x auf Anfrage)
- 2x Makro-Zwischenringe: M4/3 Extension Tubes (10mm FT1 & 16mm FT1)
- Akkus & Ladegeräte:
- Newmowa Dual-USB-Ladegerät für BLN-1 (Koffer)
- Newmowa Dual-USB-Ladegerät für BLS-1 / BLS-5 (Koffer)
- Smart Dual-USB Charger & LED-Intelligent Charger (auf Anfrage)
    ]
  ),
  block(
    fill: light-bg,
    inset: 10pt,
    width: 100%,
    stroke: 0.4pt + rgb("#cbd5e1"),
    radius: 4pt,
    [
      #text(
        weight: "bold",
        fill: primary-color
      )[Licht & Stative / Lighting & Tripods]
- Blitzgeräte:
- 2x Clip-on Ansteckblitz für Olympus/OM-System (Koffer / auf Anfrage)
- 1x Ringblitz-Set für Makroaufnahmen (Box / Koffer)
- Stative / Tripods:
- Rollei Compact Light Travel Tripod mit Smartphone-Halterung
- Cullmann Alpha 2500 Universal-Stativ mit 3-Wege-Kopf ($165"cm"$, max. $2.5"kg"$)
- Selfie Ring Light Stativ
    ]
  )
)