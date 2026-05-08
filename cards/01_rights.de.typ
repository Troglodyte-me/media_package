#import "@preview/cetz:0.2.2": canvas, draw

#set page(
  paper: "a6",
  margin: (top: 0.5cm, bottom: 0.4cm, x: 0.4cm),
)

#set text(
  font: "Arial",
  size: 8.5pt,
  lang: "de"
)

// --- Hilfsfunktionen für das Design ---
#let section(title, clr) = rect(
  width: 100%,
  fill: clr,
  inset: 3pt,
  radius: 1pt,
  stroke: 0.5pt + black,
  align(center, text(size: 9pt, weight: "bold", fill: if clr == black { white } else { black }, title))
)

#let box-style = (inset: 4pt, stroke: 0.5pt + black, radius: 1pt, width: 100%)

// --- SEITE 1: AKTIV (Einsatz & Übung) ---
#section("FOTOGRAFIE: AKTIV (IM DIENST)", black)

#v(2pt)
#grid(
  columns: (1fr, 1fr),
  gutter: 4pt,
  stack(
    spacing: 4pt,
    rect(..box-style, fill: gray.lighten(90%))[
      *✅ ERLAUBT / PFLICHT* \
      #set text(size: 7.5pt)
      - Nur mit Freigabe Einsatzleiter
      - Beweissicherung (Unfälle)
      - Dokumentation (Ausbildung)
      - Nur offizielle Geräte nutzen!
      - Fokus: Technik / Ablauf
    ],
    rect(..box-style)[
      *⚖️ RECHTSGRUNDLAGEN* \
      #set text(size: 7.5pt)
      - § 201a StGB (Bildrechte)
      - §§ 22, 23 KunstUrhG
      - Art. 6 Abs. 1 DSGVO
    ]
  ),
  rect(..box-style, fill: white)[
    *❌ STRENG VERBOTEN* \
    #set text(size: 7.5pt)
    - *Private Handy-Fotos*
    - Abbildung von Opfern/Toten
    - Kennzeichen/Hausnummern
    - Private Räume (Wohnung)
    - Posting in privaten Gruppen
    - Sofort-Upload (Sperrfrist: 48h)
    - Verpixeln ersetzt KEINE Erlaubnis
  ]
)

#v(2pt)
#rect(width: 100%, stroke: 0.5pt + black, inset: 4pt)[
  *Checkliste vor Veröffentlichung (Pressewart/Wehrführung):* \
  #set text(size: 7.5pt)
  1. EL-Freigabe erteilt? | 2. Keine Gesichter/Opfer? | 3. Keine Rückschlüsse auf Privatpersonen? | 4. Ort/Zeit dokumentiert?
]

#v(1fr)
// Minimaler Footer (1.2mm entspricht ca 3.5pt)
#set text(size: 4pt)
© 2026 FF Dohren | Disclaimer: Nutzung auf eigene Gefahr. Rechtsstand: 01/2026. Info/Kontakt: github.com/Troglodyte-me/media_package

#pagebreak()

// --- SEITE 2: PASSIV (Fotografiert werden) ---
#section("FOTOGRAFIE: PASSIV (DURCH DRITTE)", black)

#v(2pt)
#rect(..box-style, fill: gray.lighten(90%))[
  *Einsatzkräfte in Uniform (Öffentlichkeit)* \
  #set text(size: 7.5pt)
  - Abbildung i.d.R. zulässig (Beiwerk/Zeitgeschichte)
  - Presseberichterstattung ist zu dulden
  - *Nicht* die Linse zuhalten / Handgreiflichkeiten
  - *Aber:* Keine Portrait-Nahaufnahmen ohne Grund
]

#v(4pt)
#table(
  columns: (1fr, 2fr),
  inset: 4pt,
  align: horizon,
  stroke: 0.5pt + black,
  [*Situation*], [*Verhalten / Recht*],
  [Einsatz], [Duldungspflicht (sofern keine Behinderung)],
  [Übung], [Einwilligung bei Fokus-Aufnahmen nötig],
  [Privat], [Vollumfängliches Recht am eigenen Bild],
  [Behinderung], [Platzverweis via Polizei erwirken]
)

#v(4pt)
#rect(..box-style, stroke: 1.5pt + black)[
  *⚠️ HÖCHSTE PRIORITÄT: OPFERSCHUTZ* \
  #set text(size: 7.5pt)
  Gaffer/Presse aktiv am Fotografieren von Opfern hindern (Sichtschutz/Decken). § 201a StGB gilt für Dritte massiv – bei Verstößen Polizei hinzuziehen.
]

#v(4pt)
#grid(
  columns: (1fr, 40pt),
  gutter: 10pt,
  [
    #set text(size: 7.5pt)
    *Fragen?* \
    Unklarheiten vor Ort: *Keine* Fotos. \
    Ansprechpartner: Wehrführung / Pressewart.
  ],
  // Platzhalter für QR Code (30x30pt)
  rect(width: 40pt, height: 40pt, stroke: 0.5pt + black)[#align(center + horizon, text(size: 5pt)[QR\ INFO])]
)

#v(1fr)
#set text(size: 4pt)
© 2026 FF Dohren | Disclaimer: Nutzung auf eigene Gefahr. Rechtsstand: 01/2026. Info/Kontakt: github.com/Troglodyte-me/media_package
