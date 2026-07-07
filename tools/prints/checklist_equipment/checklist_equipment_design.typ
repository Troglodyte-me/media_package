// checklist_equipment_design.typ
// Centralized design system for the Gear Rental Checklist
// designed with Mammouth.AI and Gemini 3.5 Flash
// by Konrad Keck, 2026

#let brand-red = rgb("#b22222")     // Primary accent (Fire Service Red)
#let brand-dark = rgb("#1a252f")    // Text and headers
#let brand-bg = rgb("#fcfcfc")      // Soft page background
#let muted-gray = rgb("#7f8c8d")    // Details and borders

#let setup-page(title, body) = {
  set page(
    paper: "a4",
    margin: (x: 2cm, y: 2.2cm),
    fill: brand-bg,
    header: align(right)[
      #text(8pt, fill: muted-gray, weight: "bold")[#title]
    ],
    footer: [
      #line(length: 100%, stroke: 0.5pt + muted-gray)
      #grid(
        columns: (1fr, 1fr),
        text(8pt, fill: muted-gray)[github.com/Troglodyte-me/media_package],
        context align(right, text(8pt, fill: muted-gray)[#counter(page).display("1 / 1", both: true)])
      )
    ]
  )
  body
}

#let setup-text(body) = {
  // Gracefully falls back to sans-serif if Arial is missing on the compiling system
  set text(font: ("Arial", "Liberation Sans", "sans-serif"), size: 10pt, fill: brand-dark)
  body
}

// Reusable checklist item component
#let check_item(title, detail) = {
  block(width: 100%, below: 12pt)[
    #grid(
      columns: (22pt, 1fr),
      align: (center + top, left),
      // Clean square checkbox
      rect(width: 11pt, height: 11pt, radius: 2.5pt, stroke: 1.2pt + brand-dark),
      [
        #text(weight: "bold", size: 10.5pt)[#title] \
        #text(size: 9pt, fill: brand-dark.lighten(20%))[#detail]
      ]
    )
  ]
}

// Reusable styled header
#let section-heading(title) = {
  // Keep heading with following content so late-page headings move to next page.
  block(width: 100%, below: 14pt, above: 18pt, sticky: true)[
    #text(weight: "bold", size: 13pt, fill: brand-red)[#title]
    #v(-4pt)
    #line(length: 100%, stroke: 1.5pt + brand-red)
  ]
}
