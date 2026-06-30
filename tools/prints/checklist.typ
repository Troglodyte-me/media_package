// Simple Rental / Return Checklist

#set page(margin: 1.5cm)
#set text(size: 11pt, font: "Arial")

#let line = [
	#box(width: 100%, inset: (top: 0.2em, bottom: 0.2em))[______________________________]
]

#let check_item(text) = [
	#v(1em) 
	☐ *#text*
]

= CHECKLIST

== Before Leaving
#check_item("Pick Camera / Lens / Accessory")

Check compatibility of all accessories with the camera / lens being rented.
Avoid picking more than two cameras per person and not more then two lenses per camera body and person. 
Alternatively, consider using a phone camera for some scenarios.
Provide your own bags and cases for the rented items.
Assemble gear, but use lens caps for transportation. 

#check_item("Add Battery / Memory Card")

Ensure batteries are charged. One will charge will last about 2 hours depending on usage. You can take chargers along with you.
Also ensure memory card has sufficient space.
AA and AAA batteries are not provided with the gear. Please bring your own if needed.

#check_item("Configure camera settings")
		- set Date and Time (use test image)
		- set Image Quality (RAW / JPEG) and size 

#check_item("check everything works as expected and isn't damaged")

// #pagebreak()
#v(3em)

== On Return

#check_item("Check everything works as expected and isn't damaged")

Make notes of any damage or issues with the gear. If you notice any damage, please report it immediately.
Keep the gear clean and dry. If the gear is wet, please dry it before returning.

#check_item("Read out data from memory card")

Do not delete any data from previous users. If you have taken photos, please copy them to your own device and delete them from the memory card before returning it.
From here on, post processing and editing of images is your responsibility.

#check_item("Recharge battery and pack in case")

Any AA or AAA batteries used in accessories should be removed and disposed of properly. Rechargeable batteries should be recharged before returning.

#check_item("Disassemble gear and pack in case")

Reattach lens caps and body caps. Ensure all gear is packed securely in its case to prevent damage during transport.