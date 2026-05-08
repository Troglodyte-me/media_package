#import "@preview/cetz:0.2.2": canvas, draw

// --- Placeholder Definition for Images ---
#let img-placeholder(name, clr) = rect(
  width: 100%, 
  height: 20pt, 
  fill: clr.lighten(80%), 
  stroke: 0.5pt + clr,
  radius: 2pt,
  inset: 2pt
)[#align(center + horizon, text(size: 6pt, fill: clr, name))]

#let ff-dohren-logo = img-placeholder("LOGO FF DOHREN", red)
#let camera-icon = "📷"
#let check-icon = "✅"
#let cross-icon = "❌"

// --- Document Setup ---
#set page(
  paper: "a6",
  margin: (top: 25pt, bottom: 25pt, x: 8pt), // Increased margin for header/footer space
  header: context {
    let page-num = counter(page).at(here()).first()
    if calc.odd(page-num) [
      #set text(size: 8pt, fill: rgb("#CC0000"))
      #box(width: 100%, height: 14pt, fill: rgb("#FF6666").lighten(80%), inset: 4pt, radius: 2pt)[
        *Freiwillige Feuerwehr Dohren* #h(1fr) *Taschenkarte Fotografie*
      ]
    ] else [
      #set text(size: 8pt, fill: rgb("#0066CC"))
      #box(width: 100%, height: 14pt, fill: rgb("#6699FF").lighten(80%), inset: 4pt, radius: 2pt)[
        *Rechte & Pflichten* #h(1fr) *Niedersachsen 2026*
      ]
    ]
  },
  footer: context {
    set text(size: 6pt, fill: rgb("#666666"))
    stack(
      spacing: 2pt,
      line(length: 100%, stroke: 0.5pt + gray),
      [© 2026 FF Dohren | Quellen: Feuerwehrmagazin, LFV Nds, DSGVO #h(1fr) github.com/Troglodyte-me/media_package]
    )
  }
)

#set text(
  font: "sans",
  size: 9pt,
  lang: "de"
)

// --- Page 1: Einsatz ---
#align(center)[
  #ff-dohren-logo
  #set text(size: 13pt, weight: "bold", fill: rgb("#CC0000"))
  *Taschenkarte: Fotografie FF Dohren*

  #set text(size: 10pt, weight: "semibold", fill: black)
  *Aktiv Fotografieren* #h(1fr) *Im Einsatz*
]

#grid(
  columns: (1fr, 1fr),
  gutter: 4pt,
  // ERLAUBT
  box(stroke: (paint: rgb("#00AA00"), thickness: 1pt), fill: rgb("#E8F5E8"), radius: 4pt, inset: 6pt)[
    #set text(weight: "bold", fill: rgb("#00AA00"), size: 8pt)
    #check-icon ERLAUBT (mit EL-Freigabe):
    #set text(weight: "regular", size: 7.5pt, fill: black)
    - Beweissicherung (Unfälle)
    - Interne Ausbildung
    - Fahrzeuge / Equipment
    - *Nur offizielle Kamera*
  ],
  // VERBOTEN
  box(stroke: (paint: rgb("#CC0000"), thickness: 1pt), fill: rgb("#F8E8E8"), radius: 4pt, inset: 6pt)[
    #set text(weight: "bold", fill: rgb("#CC0000"), size: 8pt)
    #cross-icon STRENG VERBOTEN:
    #set text(weight: "regular", size: 7.5pt, fill: black)
    - Private Geräte (Handy!)
    - Verletzte / Opfer
    - Private Räume
    - Sofortige Veröffentlichung
  ]
)

#v(4pt)
#set text(size: 7pt, fill: rgb("#0066CC"))
*Rechtsgrundlage:* § 201a StGB (bis 1 Jahr Haft), KunstUrhG § 23 
#line(length: 100%, stroke: 0.5pt + gray)

#pagebreak()

// --- Page 2: Übung ---
#align(center)[
  #set text(size: 13pt, weight: "bold", fill: rgb("#0066CC"))
  *Taschenkarte: Fotografie FF Dohren*

  #set text(size: 10pt, weight: "semibold", fill: black)
  *Aktiv Fotografieren* #h(1fr) *Außerhalb Einsatz*
]

#grid(
  columns: (1fr, 1fr),
  gutter: 4pt,
  box(stroke: (paint: rgb("#00AA00"), thickness: 1pt), fill: rgb("#E8F5E8"), radius: 4pt, inset: 6pt)[
    #set text(weight: "bold", fill: rgb("#00AA00"), size: 8pt)
    #check-icon ERLAUBT:
    #set text(weight: "regular", size: 7.5pt, fill: black)
    - Mit schriftl. Einwilligung
    - "Beiwerk" (>5 Personen)
    - Fahrzeuge & Gebäude
  ],
  box(stroke: (paint: rgb("#CC0000"), thickness: 1pt), fill: rgb("#F8E8E8"), radius: 4pt, inset: 6pt)[
    #set text(weight: "bold", fill: rgb("#CC0000"), size: 8pt)
    #cross-icon VERBOTEN:
    #set text(weight: "regular", size: 7.5pt, fill: black)
    - Einzelpersonen im Fokus
    - Minderjährige o. Eltern
    - Ohne Wehrführung OK
  ]
)

#v(5pt)
#box(fill: gray.lighten(90%), inset: 5pt, radius: 2pt, width: 100%)[
  #set text(size: 7.5pt)
  *Privat (zivil):* Normale Regeln (KunstUrhG). Fokus = Einwilligung nötig. Kein Dienst-Mix! Fotos im Dienst-Zusammenhang sind keine Privatbilder.
]

#pagebreak()

// --- Page 3: Passiv ---
#align(center)[
  #set text(size: 13pt, weight: "bold", fill: rgb("#CC0000"))
  *Passiv: Fotografiert werden*

  #set text(size: 10pt, weight: "semibold", fill: black)
  *Einsatzkräfte in Uniform* #h(1fr) *Öffentlichkeit*
]

#grid(
  columns: (1fr, 1fr),
  gutter: 4pt,
  box(stroke: (paint: rgb("#0066CC"), thickness: 1pt), fill: rgb("#E6F0FF"), radius: 4pt, inset: 6pt)[
    #set text(weight: "bold", fill: rgb("#0066CC"), size: 8pt)
    #camera-icon Recht auf Abbildung:
    #set text(weight: "regular", size: 7.5pt, fill: black)
    - Ohne Einwilligung OK
    - Presseberichte zulässig
    - *Nicht hindern!*
    - "Relativ Zeitgeschichte"
  ],
  box(stroke: (paint: rgb("#FF8800"), thickness: 1pt), fill: rgb("#FFF2E6"), radius: 4pt, inset: 6pt)[
    #set text(weight: "bold", fill: rgb("#FF8800"), size: 8pt)
    ⚠️ SCHUTZ:
    #set text(weight: "regular", size: 7.5pt, fill: black)
    - Opfer: Sichtschutz!
    - Keine Nah-Gesichter
    - Privatbereich beachten
  ]
)

#v(5pt)
#set text(size: 8pt)
*Außerhalb Einsatz:*
#grid(
  columns: (1fr),
  box(width: 100%, fill: rgb("#F0F8FF"), inset: 6pt, radius: 3pt)[
    *In Uniform:* Wie Einsatz (nicht im Fokus). \
    *Zivil:* Volles Recht am eigenen Bild (Einwilligung zwingend!).
  ]
)

#v(10pt)
#set text(size: 8pt)
*Fragen?* Wehrführung FF Dohren \
*DSGVO:* Widerruf jederzeit möglich | Löschung nach Zweckwegfall

#pagebreak()

// --- Page 4: Zusammenfassung ---
#align(center)[
  #set text(size: 12pt, weight: "bold", fill: rgb("#0066CC"))
  *Zusammenfassung & Allgemeines*
]

#grid(
  columns: (1fr, 1fr),
  gutter: 8pt,
  box(fill: rgb("#E8F5E8"), stroke: rgb("#00AA00"), radius: 4pt, inset: 6pt)[
    #set text(size: 8pt)
    *#check-icon DO's immer:*
    #set text(size: 7pt)
    - Einwilligungen dokumentieren
    - Offizielle Kamera nutzen
    - Opfer aktiv schützen
  ],
  box(fill: rgb("#F8E8E8"), stroke: rgb("#CC0000"), radius: 4pt, inset: 6pt)[
    #set text(size: 8pt)
    *#cross-icon DON'Ts immer:*
    #set text(size: 7pt)
    - Private Posts (Social Media)
    - Ohne Freigabe teilen
    - Privat/Dienst mischen
  ]
)

#v(10pt)
#set text(size: 7.5pt, weight: "bold", fill: rgb("#CC0000"))
*Wichtiger Hinweis:* \
Das Verpixeln von Gesichtern ersetzt *nicht* die erforderliche Einwilligung der abgebildeten Personen, wenn diese durch Umstände (Tattoos, Ort, Ausrüstung) identifizierbar bleiben.

#v(1fr)
#set text(size: 7pt, fill: rgb("#666666"))
*Stand 2026. Basierend auf Feuerwehrmagazin & LFV Nds. Anpassung lokal prüfen.*
