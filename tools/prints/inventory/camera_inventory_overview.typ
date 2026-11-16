// Project: media_package | Source schema: v1 | Updated: 2026-11-17
// Prepared by: Copilot SDK assistant
// Progress:
// [x] English/German copy with English fallback and an explicit print locale.
// [x] Availability filtering, full inventory IDs, and all current gear categories.
// [x] Camera bodies separated from fixed-lens cameras; accessory groups follow use.
// [x] Chart uses photographic angle-of-view references and a practical fixed range.
// [x] Checklist-style footer, project QR link, and section source files.
// [x] Both print locales keep the full lens table together; chart labels do not overlap.
// [x] Inventory print documentation updated and both locales compiled.
// [~] Battery capacity filtering is deferred; generic gear is counted in the PDF.

#import "@preview/tiaoma:0.3.0": qrcode
#import "camera_inventory_common.typ": *
#import "sections/cameras.typ": render-cameras
#import "sections/lenses.typ": render-lenses
#import "sections/accessories.typ": render-accessories

#set page(paper: "a4", flipped: false, margin: (x: 10mm, y: 18mm), footer: context [
  #line(length: 100%, stroke: 0.45pt + color-border)
  #v(3pt)
  #grid(
    columns: (11mm, 1fr, auto),
    gutter: 5pt,
    align: (left, left, right),
    qrcode(project-url, width: 10mm),
    text(font: font-ui, size: 6.2pt, fill: color-text-muted)[#copy-footer-title],
    text(font: font-ui, size: 6.2pt, fill: color-text-muted)[#counter(page).display("1")],
  )
])
#set text(font: font-body, size: 7.2pt, fill: color-text)
#set par(leading: 0.9em, spacing: 0pt)
#show table.cell: set text(font: font-body, size: 7.1pt, fill: color-text)

#render-cameras()
#pagebreak()
#render-lenses()
#pagebreak()
#render-accessories()
