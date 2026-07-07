// checklist_equipment_EN.typ
// Simple Rental / Return Checklist
// designed with Mammouth.AI and Gemini 3.5 Flash
// by Konrad Keck, 2026
#import "checklist_equipment_design.typ": *

#show: doc => setup-page("EQUIPMENT CHECKLIST | RENTAL", doc)
#show: doc => setup-text(doc)

// ---- DOCUMENT CONTENT ----

#align(center)[
  #text(size: 20pt, weight: "bold", fill: brand-dark)[Equipment Checklist] \
  #text(size: 10pt, fill: muted-gray)[Quick Start Guide for Gear Rental & Operations]
]

#v(10pt)

#section-heading("1. Preparation (Before Leaving)")

#check_item("Verify Kit Completeness", "Check whether all items are present as listed. Then inspect the camera body, lenses, batteries, memory cards, and strap for physical damage or dirt.")

#check_item("Check Battery Status", "Ensure all required rechargeable batteries are fully charged. Pack spare batteries and chargers if necessary. Single-use batteries are not provided; please bring your own if needed.")

#check_item("Prepare Memory Cards", "Check SD cards, whether sufficient storage is available and cleanly remove old files. Do not delete files from other users. Pack spare memory cards if necessary.")

#check_item("Select Lenses", "Choose appropriate focal lengths for the planned shoot. Keep protective caps on all unused lenses.")

#check_item("Test Photos", "Take a few test shots to ensure the camera and lenses are functioning correctly and are configured properly. Make adjustments as needed (esp. date and time).")

#check_item("Pack Accessories", "Securely pack tripods, optional microphones, cleaning cloths, and cables into the system bag. Transport bag (please bring your own!) should not be overloaded to avoid damage.")

*Less is more* --
only pack what is portable and needed for the planned shoot. 
This minimizes the risk of damage and makes handling easier during operations.


#section-heading("2. In the Field (During Operation)")

#check_item("Verify Settings", "Check the camera mode (e.g., Program or Manual), ISO settings, and white balance before taking the first shot.")

#check_item("Maintain Lens Cleanliness", "Take off the lens cap and keep it close by. Regularly inspect the front lens element for dust, water droplets, or dirt. If dirty clean gently with a microfiber cloth. After shooting, replace the lens cap to protect the lens.")

#check_item("Changing Batteries", "After changing batteries, check that the camera settings are still in effect (e.g., date and time). Adjust settings again if necessary.")

#check_item("Changing Lenses", "When changing lenses make sure no dust particles get on the sensor. Change lenses carefully and use protective caps.")

*Safety has highest priority!*
Always ensure a safe stance, do not put yourself or your subject in danger, and do not obstruct emergency personnel.
Wearing adequate protective equipment (e.g. PPE) is mandatory on active scenes.


#section-heading("3. Return (After Operation)")

#check_item("Perform Basic Cleaning", "Detach all components. Gently wipe off dust, dirt, or moisture especially from the camera body and lenses. Never pack gear while damp or dirty.")

#check_item("Inventory Check", "Verify that all small parts (lens caps, hot shoe covers, straps, batteries, and cards) are present and accounted for. Report any missing items or damage immediately.")

#check_item("Data Transfer", "Transfer all recorded photo and video files as soon as possible. Please mind backups and data security.")

#check_item("Charge Batteries", "Remove any single-use batteries and dispose of them properly. Recharge all used rechargeable batteries.")

#check_item("Return Equipment", "Return all borrowed equipment and accessories promptly after use.")


#v(3em)

#feedback-link(
  "https://github.com/Troglodyte-me/media_package",
  "Feedback and suggestions for improvement are always welcome.",
  alt-url: "" // already displayed url in footer, so no need to show it again
)