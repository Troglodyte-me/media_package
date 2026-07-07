// checklist_equipment_DE.typ
// Simple Rental / Return Checklist
// designed with Mammouth.AI and Gemini 3.5 Flash
// by Konrad Keck, 2026

#import "checklist_equipment_design.typ": *
#import "@preview/qrcode": qrcode

#show: doc => setup-page("AUSRÜSTUNGS-CHECKLISTE | GERÄTE-LEIHE", doc)
#show: doc => setup-text(doc)

// ---- DOCUMENT CONTENT ----

#align(center)[
  #text(size: 20pt, weight: "bold", fill: brand-dark)[Ausrüstungs-Checkliste] \
  #text(size: 10pt, fill: muted-gray)[Schnellstart-Anleitung für die Geräteausleihe]
]

#v(10pt)

#section-heading("1. Vorbereitung (Vor dem Aufbruch)")

#check_item("Sichtprüfung Set", "Prüfen, ob alles vorhanden ist wie angegeben. Anschließend Kameragehäuse, Objektive, Akkus, Speicherkarten und Tragegurt auf physische Schäden oder Verschmutzungen kontrollieren.")

#check_item("Akkustand kontrollieren", "Sicherstellen, dass alle benötigten Akkus vollständig geladen sind. Ersatzakkus einpacken und ggf. Ladegerät mitnehmen. (Einweg-) Batterien werden nicht mitgeliefert, bitte selbst mitbringen.")

#check_item("Speicherkarten vorbereiten", "SD-Karten überprüfen, ob ausreichend Speicherplatz verfügbar ist. Keine Vorgängerdaten löschen! Gegebenenfalls Ersatz-Speicherkarten einpacken.")

#check_item("Objektivauswahl treffen", "Passende Brennweiten für den geplanten Einsatzzweck auswählen. Schutzdeckel auf ungenutzten Objektiven belassen.")

#check_item("Testphotos machen", "Testaufnahmen durchführen, um Funktionalität und Einstellungen der Kamera zu prüfen. Anpassungen vornehmen, falls erforderlich (insb. Datum und Uhrzeit).")

#check_item("Zubehör verpacken", "Stative, optionale Mikrofone, Reinigungstücher, Verbindungskabel etc. transportsicher in der Tasche verstauen. Transporttasche (bitte selber mitbringen!) nicht überladen, um Schäden zu vermeiden.")

*"Weniger ist mehr"* -- 
nur einpacken, was transportabel ist und für den geplanten Einsatz benötigt wird. 
Das minimiert das Risiko von Schäden und erleichtert die Handhabung im Einsatz.

#section-heading("2. Im Einsatz (Während der Aufnahmen)")

#check_item("Einstellungsprüfung", "Kameramodus (z. B. Programmautomatik oder Manuell), ISO-Wert und Weißabgleich vor den ersten Aufnahmen kontrollieren.")

#check_item("Objektivsauberkeit wahren", "Objektivdeckel abnehmen und griffbereit halten. Frontlinse regelmäßig auf Staub, Wassertropfen oder Schmutz prüfen und bei Bedarf vorsichtig mit dem Reinigungstuch säubern. Nach dem Fotografieren Objektivdeckel wieder aufsetzen, um die Linse zu schützen.")

#check_item("Batteriewechsel", "Nach Batteriewechsel überprüfen, ob die Kameraeinstellungen weiterhin gespeichert sind (z. B. Datum und Uhrzeit). Ggf. Einstellungen erneut anpassen.")

#check_item("Objektivwechsel", "Beim Wechsel von Objektiven darauf achten, dass keine Staubpartikel auf den Sensor gelangen. Objektive vorsichtig wechseln und Schutzkappen verwenden.")

*Sicherheit hat absolute Priorität!* 
Immer auf sicheren Stand achten, nicht in Gefahr begeben und keine Einsatzkräfte behindern.
In Einsatzsituationen ist adequate Schutzausrüstung (z.B. PSA) zu tragen.

#section-heading("3. Rückgabe (Nach dem Einsatz)")

#check_item("Grobe Reinigung durchführen", "Alles wieder in Einzelkomponenten zerlegen. Insbesondere Kameragehäuse und Objektive vorsichtig von Staub, Schmutz oder Feuchtigkeit befreien. Niemals feucht oder dreckig wieder einpacken.")

#check_item("Vollständigkeitskontrolle", "Sämtliche Kleinteile (Objektivdeckel, Blitzschuhabdeckungen, Gurte, Akkus und Speicherkarten) auf Vollständigkeit prüfen. Fehlende Teile und Schäden sofort melden.")

#check_item("Datenübertragung", "Aufgenommenes Bild- und Videomaterial zeitnah auslesen und sichern. Backups und Datensicherheit nicht vergessen.")

#check_item("Akkus laden", "Leere Einwegbatterien entfernen und ordnungsgemäß entsorgen. Wiederaufladbare Akkus aufladen.")

#check_item("Material zurückgeben", "Alle ausgeliehenen Geräte und Zubehörteile zeitnah nach dem Einsatz zurückgeben. ")

#v(3em)

#align(center)[
  #text(size: 9pt, fill: muted-gray)[Feedback und Verbesserungsvorschläge sind stets willkommen.]
  #v(4pt)
  #qrcode("https://github.com/Troglodyte-me/media_package", height: 22mm)
  #v(2pt)
  #text(size: 8pt, fill: muted-gray)[github.com/Troglodyte-me/media_package]
]