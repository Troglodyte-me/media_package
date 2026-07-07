// checklist_equipment_template.typ
// Template for equipment checklist printouts
// designed with Mammouth.AI and Gemini 3.5 Flash
// by Konrad Keck, 2026
// 
// Use to create new language versions of the equipment checklist printout or make your own custom version.

#import "checklist_equipment/checklist_equipment_design.typ": *

#show: doc => setup-page("EQUIPMENT CHECKLIST | RENTAL", doc)
#show: doc => setup-text(doc)

// ---- DOCUMENT CONTENT ----

#align(center)[
  #text(size: 20pt, weight: "bold", fill: brand-dark)[Equipment Checklist Template] \
  #text(size: 10pt, fill: muted-gray)[Barebone template for creating your own checklist printout]
]

#v(10pt)

#section-heading("1. Before")

#check_item("First Item", "Include some explanatory text here for the first checklist item. This is a template, so you can customize it as needed.")

#check_item("Second Item", "Include some explanatory text here for the second checklist item. This is a template, so you can customize it as needed.")

#check_item("Third Item", "Include some explanatory text here for the third checklist item. This is a template, so you can customize it as needed.")

*Hint* --
This is just regularly text for additional information. 
You can add as many of these as you like, and they will be displayed in the checklist printout.


#section-heading("2. While")

#check_item("Another Item", "Include some explanatory text here for another checklist item. This is a template, so you can customize it as needed.")


#section-heading("3. After")

#check_item("Last Item", "Include some explanatory text here for the last checklist item. This is a template, so you can customize it as needed.")

Feedback and suggestions for improvement are always welcome!