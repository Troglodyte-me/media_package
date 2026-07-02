// Simple Rental / Return Checklist

#set page(
  paper: "a4",
  margin: (x: 1.8cm, y: 2cm),header: align(right)[
    #text(
      size: 8pt, 
      fill: luma(100), 
      font: "Arial")[
      Media Package | #datetime.today().display("[year]-[month]-[day]") | Equipment Checklist 
    ]
  ],
  footer: align(center)[
    #text(
      size: 8pt,
      fill: luma(120))[Page #context counter(page).display()]
  ]
)
#set text(
  font: "Arial", // Widely available sans-serif
  size: 10pt,
  fill: rgb("#2c3e50") // Dark slate blue/grey instead of harsh pure black
)

// ---- BRAND COLORS & DESIGN ELEMENTS ----
#let brand-red = rgb("#b22222") // Firebrick Red
#let brand-dark = rgb("#1a252f") // Deep Dark Navy
#let brand-bg = rgb("#f8f9fa") // Soft off-white

// Custom Checkbox Function
#let check_item(text, explanation: none) = {
  let indent = 1.1em + 0.8em + 2.3pt // Checkbox width + spacing + stroke width

  block(width: 100%, inset: (y: 2pt))[
    #box(width: 1.1em, height: 1.1em, stroke: 1.2pt + brand-dark, radius: 2pt, baseline: 20%)
    #h(0.8em)
    *#text*

    #if explanation != none [
      // #v(0.35em)
      #pad(left: indent)[#explanation]
    ]
  ]
}

// ---- DOCUMENT CONTENT ----

// Main Title
#align(left)[
  #text(size: 22pt, weight: "bold", fill: brand-red)[
    = EQUIPMENT CHECKLIST
    ] 
]
#v(1em)

#align(left)[
  #text(size: 16pt, weight: "bold", fill: brand-dark)[
    == Vorbereitung
  ]
]
// #todo("Pick Camera / Lens / Accessory")
#check_item("Kamera / Objektiv / Zubehör auswählen", explanation: "Kompatibilität der geliehenen Ausrüstung (Kamera, Objektiv und Filter) überprüfen.
Weniger ist mehr: Wähle nicht mehr als zwei Kameras pro Person und nicht mehr als zwei Objektive pro Kameragehäuse und Person aus.
Alternativ kann in bestimmten Situationen auch die Kamera vom Smartphone genutzt werden.
Ausrüstung am besten gleich zusammenbauen und zum Transport Objektivdeckel verwenden.
Eigene Taschen und Koffer für die geliehenen Gegenstände sind dringend empfohlen.")

#v(1em)
#check_item("Batterie/Speicherkarte einlegen", explanation: "Ladung der Batterien sicherstellen. Eine Ladung reicht je nach Nutzung für etwa 2 Stunden oder 200 Fotos aus. Ladegeräte sind verfügbar und können mitgenommen werden.
Einwegbatterien sind nicht mitgeliefert. Bitte bei Bedarf eigene verwenden.
Stelle außerdem sicher, dass auf der Speicherkarte ausreichend Speicherplatz vorhanden ist.")

#v(1em)
#check_item("Auf Funktionalität und Schäden prüfen", explanation: "Konfigurieren der Kamera prüfen:
  - Eine/Mehrere Testaufnahme machen und 
      - Prüfen, ob Datum und Uhrzeit korrekt sind als auch, ob das Bild fleckig ist
  - Datum und Uhrzeit einstellen
  - Bildqualität (RAW / JPEG) und die Bildgröße einstellen
  - gegebenenfalls Sensor und/oder Objektiv reinigen")

#v(3em)

#align(left)[
  #text(size: 16pt, weight: "bold", fill: brand-dark)[
    == Im Feld 
  ]
]
#check_item("Objektivdeckel abnehmen und griffbereit halten", explanation: "Nicht vergessen, den Objektivdeckel vor dem Fotografieren abzunehmen. Der Deckel sollte griffbereit aufbewahrt werden, um zwischen den Aufnahmen das Eindringen von Staub zu verhindern.
Mit einer Gegenlichtblende lässt sich das Objektiv vor Kratzern schützen und Blendeffekte reduzieren.")

#v(1em)
#check_item("Ausrüstung sauber und trocken halten", explanation: "Das Objektivglas frei von Fingerabdrücken und Staub halten. Zur Reinigung des Objektivs bei Bedarf ein Mikrofasertuch verwenden.
Kameras sind in der Regel wetterfest, sollten jedoch nicht bei starkem Regen oder Schnee eingesetzt werden. Sollte die Ausrüstung nass werden, so schnell wie möglich trocknen.
Die Ausrüstung funktioniert am besten bei Temperaturen zwischen 0 °C und 40 °C. Einsatz der Ausrüstung bei extremen Temperaturen vermeiden -- andernfalls Aufbewahrung in einer Tasche oder einem Koffer ist dringend empfohlen, um sie vor Witterungseinflüssen zu schützen.")

#v(1em)
#check_item("Batteriewechsel", explanation: "Überprüfen, ob die Kameraeinstellungen nach dem Batteriewechsel weiterhin gültig sind (z. B. Datum und Uhrzeit).")

#v(3em)

#align(left)[
  #text(size: 16pt, weight: "bold", fill: brand-dark)[
    == On Return
  ]
]
#check_item("Check everything works as expected and isn't damaged", explanation: "Check that the camera and lens are functioning properly. Make sure all buttons, dials, and switches are working as expected.
Make notes of any damage or issues with the gear. If you notice any damage, please report it immediately.
Keep the gear clean and dry. Clean the gear if necessary before returning it.")

#v(1em)
#check_item("Read out data from memory card", explanation: "Make sure to read out all data from the memory card before returning it.
Do not delete any data from previous users. If you have taken photos, please copy them to your own device and delete them from the memory card before returning it.
From here on, post processing and editing of images is your responsibility.")

#v(1em)
#check_item("Recharge battery and pack in case", explanation:
"Any single-use batteries used in accessories should be removed and disposed of properly. Rechargeable batteries should be recharged before returning.")

#v(1em)
#check_item("Disassemble gear and pack in case", explanation: "Reattach lens caps and body caps. Ensure all gear is packed securely in its case to prevent damage during transport.")