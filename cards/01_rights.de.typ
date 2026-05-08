#import "@preview/cetz:0.2.2": canvas, draw

#let ff-dohren-logo = box(width: 200pt, height: 80pt, fill: rgb("#FF0000"), inset: 8pt)[
  #set text(size: 16pt, weight: "bold", fill: rgb("#FFFFFF"))
  FF Dohren
]
#let camera-icon = box(width: 32pt, height: 32pt, fill: rgb("#000000"), radius: 6pt, inset: 2pt)[
  #set text(size: 12pt, fill: rgb("#FFFFFF"))
  CAM
]

#let check-icon = "[CHECK-ICON-PLACEHOLDER]"
#let cross-icon = "[CROSS-ICON-PLACEHOLDER]"

#show: doc => pages[  #set page(
    paper: "a6",
    margin: 8pt,
    header: context {
      if calc.odd(page()) [        #set text(size: 8pt, fill: rgb("#CC0000"))
        #box(width: 100%, height: 12pt, fill: rgb("#FF6666"), inset: 4pt)[          *Freiwillige Feuerwehr Dohren* #h(1fr) *Taschenkarte Fotografie*
        ]
      ] else [        #set text(size: 8pt, fill: rgb("#0066CC"))
        #box(width: 100%, height: 12pt, fill: rgb("#6699FF"), inset: 4pt)[          *Rechte & Pflichten* #h(1fr) *Niedersachsen 2026*
        ]
      ]
    },
    footer: context {
      set text(size: 7pt, fill: rgb("#666666"))
      box(width: 100%, height: 10pt)[        © 2026 FF Dohren | Quellen: Feuerwehrmagazin, LFV Nds, DSGVO | github.com/Troglodyte-me/media_package (CC BY-SA 4.0)
      ]
    }
  )
  
  #doc
]

#set text(
  font: "sans",
  size: 9pt,
  lang: "de"
)

#align(center)[  #set text(size: 14pt, weight: "bold", fill: rgb("#CC0000"))
  *Taschenkarte: Fotografie FF Dohren*
  
  #set text(size: 10pt, weight: "semibold")
  *Aktiv Fotografieren* #h(1fr) *Im Einsatz*
]

#columns(2)[  // Spalte 1: ERLAUBT
  #set text(weight: "bold", fill: rgb("#00AA00"))
  #v(4pt)
  #box(stroke: (paint: rgb("#00AA00"), thickness: 2pt), fill: rgb("#E8F5E8"), radius: 4pt, inset: 8pt)[    *✅ ERLAUBT (mit Freigabe Einsatzleiter):*
    #set text(weight: "regular", size: 8pt)
    - Dokumentation Beweissicherung (Unfälle, Behinderungen)
    - Ausbildung (intern, gesichert)
    - Öffentlicher Raum: Fahrzeuge, Equipment, Ort (ohne Opfer)
    - *Nur offizielle Kamera* (geladen!)
  ]
  
  // Spalte 2: VERBOTEN
  #set text(weight: "bold", fill: rgb("#CC0000"))
  #v(4pt)
  #box(stroke: (paint: rgb("#CC0000"), thickness: 2pt), fill: rgb("#F8E8E8"), radius: 4pt, inset: 8pt)[    *❌ STRENG VERBOTEN:*
    #set text(weight: "regular", size: 8pt)
    - Ohne Erlaubnis Einsatzleiter
    - Private Geräte (Handy!)
    - Verletzte/Opfer/Betroffene
    - Private Räume/Grundstücke
    - Teleobjektiv "über Zaun"
    - Sofort veröffentlichen (48h Wartezeit)
  ]
]

#v(8pt)
#set text(size: 8pt, fill: rgb("#0066CC"))
*Rechtsgrundlage:* § 201a StGB (bis 1 Jahr Haft), KunstUrhG § 23 #line(length: 100%)

#pagebreak()

#align(center)[  #set text(size: 14pt, weight: "bold", fill: rgb("#0066CC"))
  *Taschenkarte: Fotografie FF Dohren*
  
  #set text(size: 10pt, weight: "semibold")
  *Aktiv Fotografieren* #h(1fr) *Außerhalb Einsatz* (Übung, Wettkampf)
]

#columns(2)[  // Spalte 1: ERLAUBT
  #set text(weight: "bold", fill: rgb("#00AA00"))
  #v(4pt)
  #box(stroke: (paint: rgb("#00AA00"), thickness: 2pt), fill: rgb("#E8F5E8"), radius: 4pt, inset: 8pt)[    *✅ ERLAUBT:*
    #set text(weight: "regular", size: 8pt)
    - Mit *schriftlicher Einwilligung*
    - "Beiwerk" (≥5 Personen, Rand)
    - Fahrzeuge, Ausrüstung, Gebäude
    - Mit Bildtext: "Übung FF Dohren, [Datum]"
  ]
  
  // Spalte 2: VERBOTEN
  #set text(weight: "bold", fill: rgb("#CC0000"))
  #v(4pt)
  #box(stroke: (paint: rgb("#CC0000"), thickness: 2pt), fill: rgb("#F8E8E8"), radius: 4pt, inset: 8pt)[    *❌ VERBOTEN:*
    #set text(weight: "regular", size: 8pt)
    - Einzelpersonen im Fokus
    - Minderjährige (ohne Eltern)
    - Private/Gerätehaus-Räume
    - Ohne Wehrführung OK
  ]
]

#v(8pt)
#columns(3, gutter: 10pt)[  #colspan(3)[    #set text(size: 8pt)
    *Privat (zivile Kleidung):* Normale Regeln (KunstUrhG). Fokus = Einwilligung. Kein Dienst-Mix!
  ]
]

#pagebreak()

#align(center)[  #set text(size: 14pt, weight: "bold", fill: rgb("#CC0000"))
  *Passiv: Fotografiert werden*
  
  #set text(size: 10pt, weight: "semibold")
  *Einsatzkräfte in Uniform* #h(1fr) *Öffentlicher Raum*
]

#columns(2)[  // Spalte 1: Recht auf Abbildung
  #set text(weight: "bold", fill: rgb("#0066CC"))
  #v(4pt)
  #box(stroke: (paint: rgb("#0066CC"), thickness: 2pt), fill: rgb("#E6F0FF"), radius: 4pt, inset: 8pt)[    *📷 Recht auf Abbildung:*
    #set text(weight: "regular", size: 8pt)
    - Ohne Einwilligung fotografierbar
    - Veröffentlichung OK (Presse, FF)
    - *Nicht hindern* (Objektiv verdecken)
    - "Person der Zeitgeschichte"
  ]
  
  // Spalte 2: SCHUTZ
  #set text(weight: "bold", fill: rgb("#FF8800"))
  #v(4pt)
  #box(stroke: (paint: rgb("#FF8800"), thickness: 2pt), fill: rgb("#FFF2E6"), radius: 4pt, inset: 8pt)[    *⚠️ SCHUTZ:*
    #set text(weight: "regular", size: 8pt)
    - Opfer/Betroffene: Sichtschutz!
    - Keine Nahaufnahmen Gesichter
    - Privatbereich: Toleranz endet
  ]
]

#v(8pt)
#set text(size: 10pt, weight: "semibold")
*Außerhalb Einsatz:* #box(width: 100%, fill: rgb("#F0F8FF"), inset: 6pt, radius: 3pt)[  *In Uniform:* Wie Einsatz (nicht Fokus).  
  *Zivil:* Voll-Recht am Bild (Einwilligung!).
]

#v(12pt)
#columns(2)[  #colbreak()
  #set text(size: 8pt, weight: "bold")
  *Fragen?* Wehrführung FF Dohren  
  *DSGVO:* Widerruf jederzeit | Löschung nach Zweck
]

#pagebreak()

#align(center)[  #set text(size: 12pt, weight: "bold", fill: rgb("#0066CC"))
  *Zusammenfassung & Allgemeines*
]

#grid(
  columns: (1fr, 1fr),
  gutter: 8pt,
  [    #box(fill: rgb("#E8F5E8"), stroke: rgb("#00AA00"), radius: 4pt, inset: 6pt)[      *✅ DO's immer:*
      - Einwilligungen dokumentieren
      - Offizielle Kamera nutzen
      - Bildtexte setzen
      - Opfer schützen
    ]
  ],
  [    #box(fill: rgb("#F8E8E8"), stroke: rgb("#CC0000"), radius: 4pt, inset: 6pt)[      *❌ DON'Ts immer:*
      - Private Posts (Social Media)
      - Ohne Freigabe veröffentlichen
      - Gesichter pixeln ≠ Einwilligung
      - Privat/Dienst mischen
    ]
  ]
)

#v(8pt)
#set text(size: 7pt, italic: true, fill: rgb("#666666"))
*Basierend auf Feuerwehrmagazin[1], LFV SH[2], DSGVO. Anpassung lokal prüfen. Quelle: github.com/Troglodyte-me/media_package (CC BY-SA 4.0)*
