// Import the cades package for dynamic QR code generation
#import "@preview/cades:0.3.1": qr-code

// ==========================================
// 1. CHOOSE YOUR CARD & PRINT SIZES
// ==========================================
#let card-width = 63.5mm   // Standard Poker width
#let card-height = 88.9mm  // Standard Poker height
#let cols = 3
#let rows = 3
#let cards-per-sheet = cols * rows

// Set A4 print sheet margins (leaves ample room for non-printable printer borders)
#set page(
  paper: "a4",
  margin: (x: 10mm, y: 15mm),
)

// Read CSV rows as dictionaries (safely referencing columns by name)
#let cards = csv("cameras_inventory.csv", row-type: dictionary)

// ==========================================
// 2. DEFINE FRONT AND BACK CARD DESIGNS
// ==========================================

#let draw-front(card) = {
  if card == none { return box(width: card-width, height: card-height) } // Blank padding
  box(
    width: card-width,
    height: card-height,
    stroke: 0.25pt + rgb("#bbbbbb"), // Thin cutline guide
    inset: 5mm,
    align(center + horizon)[
      #image(card.at("image_path"), width: 100%, height: 100%, fit: "contain")
    ]
  )
}

#let draw-back(card) = {
  if card == none { return box(width: card-width, height: card-height) } // Blank padding
  
  box(
    width: card-width,
    height: card-height,
    stroke: 0.25pt + rgb("#bbbbbb"), // Thin cutline guide
    inset: 5mm,
    [
      // Icon in top right
      #place(top + right, dx: 0pt, dy: 0pt)[
        #image(card.at("icon_path"), width: 10mm, height: 10mm, fit: "contain")
      ]
      
      // Center QR & Name
      #align(center + horizon)[
        #stack(
          spacing: 1.2em,
          qr-code(card.at("qr_url"), width: 30mm),
          text(weight: "bold", size: 10pt)[#card.at("name")]
        )
      ]
    ]
  )
}

// ==========================================
// 3. GENERATION LOOP (Chunking and Imposition)
// ==========================================

// Slice the cards array into chunks of 9 (to fit each A4 sheet)
#let total-cards = cards.len()
#let num-sheets = calc.ceil(total-cards / cards-per-sheet)

#for s in range(num-sheets) [
  #let start-idx = s * cards-per-sheet
  #let end-idx = calc.min(start-idx + cards-per-sheet, total-cards)
  #let chunk = cards.slice(start-idx, end-idx)

  // --- A. SHEET FRONTS ---
  #let front-cells = chunk.map(draw-front)
  
  // Pad the rest of the sheet with empty blocks if we don't have a multiple of 9
  #while front-cells.len() < cards-per-sheet {
    front-cells.push(draw-front(none))
  }

  #align(center + horizon)[
    #grid(
      columns: (card-width,) * cols,
      rows: (card-height,) * rows,
      gutter: 0mm, // Zero-gap allows a single slice with a paper cutter
      ..front-cells
    )
  ]

  #pagebreak()

  // --- B. SHEET BACKS (Horizontally Mirrored) ---
  #let back-cells = ()
  
  #for r in range(rows) {
    let row-start = r * cols
    let row-end = row-start + cols
    
    // Extract row or make it empty if we have run out of cards
    let row-chunk = if row-start < chunk.len() {
      chunk.slice(row-start, calc.min(row-end, chunk.len()))
    } else {
      ()
    }
    
    // Pad incomplete row to full column width
    while row-chunk.len() < cols {
      row-chunk.push(none)
    }
    
    // Crucial step: Reverse the row horizontally so double-sided printing aligns!
    let reversed-row = row-chunk.rev()
    
    for card in reversed-row {
      back-cells.push(draw-back(card))
    }
  }

  #align(center + horizon)[
    #grid(
      columns: (card-width,) * cols,
      rows: (card-height,) * rows,
      gutter: 0mm,
      ..back-cells
    )
  ]

  #if s < num-sheets - 1 [
    #pagebreak()
  ]
]
