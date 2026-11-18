# Camera Inventory Print: Mission

## Goal

Maintain a clear, accurate, bilingual (English/German) camera and gear
inventory print, generated from the YAML source of truth with Typst. Keep data,
localization, layout, and inventory sections maintainable and reusable.

## Requirements and guardrails

- Keep `cameras_inventory_20261110.yaml` at schema version 1 unless the
  renderers are deliberately updated with it.
- Keep English as the source language; support German output and English
  fallback for missing translations.
- Preserve stable, unique gear IDs, category-matching prefixes, and explicit
  availability. The print omits unavailable gear by default.
- Use natural accessory groupings and represent generic gear as quantities,
  not invented per-unit IDs.
- Keep the lens chart illustrative and based on photographic angle-of-view
  references, with a practical fixed range. Do not describe it as a literal
  model of human vision.
- Preserve the bilingual print, readable table/chart layout, and project QR
  footer. Review rendered output in both locales after layout or copy changes.
- Keep the implementation economical and staged; ask for user input when an
  unresolved choice materially changes behavior or presentation.

## Scope decisions still needing care

- Battery-capacity filtering is deferred; do not introduce a threshold or
  change how generic gear is counted without confirming the desired rule.
- The previous progress report said English was the default print locale, but
  `camera_inventory_common.typ` currently sets `print-locale` to `"de"`.
  Confirm which behavior is intended before changing it.
- Missing availability currently defaults to `true`. A prior report said all
  40 records had explicit values; preserve that invariant or make any new
  fallback/validation behavior explicit.

## Sources

- `README.md` in this directory documents the current data and build workflow.
- `camera_inventory_overview.typ` records implementation progress.
- `camera_inventory_common.typ` contains locale and availability defaults.
- `conversation.md` preserves the relevant user requests and prior feedback.
