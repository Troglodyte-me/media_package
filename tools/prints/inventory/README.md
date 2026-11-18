# Camera Inventory Print

The bilingual camera inventory PDF is generated from `camera_inventory_overview.typ`.
Shared data, localization, and table helpers live in `camera_inventory_common.typ`;
the camera, lens, and accessory sections are in `sections/`.

## Data and localization

- `cameras_inventory_20261110.yaml` is the source of truth. Keep its top-level
  `schema_version` at `1` unless the Typst renderers are updated for a new schema.
- Each gear record has a stable, unique ID, a category, and an `availability`
  boolean. Missing availability is treated as available. By default, unavailable
  items are omitted; change `include-unavailable` in
  `camera_inventory_common.typ` to include them.
- UI strings and item prose are translated under `translations.en` and
  `translations.de`. Set `print-locale` in `camera_inventory_common.typ` to `en`
  or `de`; missing localized item fields fall back to English, then source data.
- IDs must use the prefix associated with their category. The renderer checks
  schema version, category coverage, ID uniqueness/prefixes, and availability
  types during compilation.

## Build and review

From this directory, compile with Typst:

```powershell
typst compile camera_inventory_overview.typ camera_inventory_overview.pdf
```

Review the resulting PDF in both locales after changing translations or layout.
The overview uses the `tiaoma` Typst package for its footer QR code. Its
perception chart is conceptual, spans actual focal lengths from 0 to 200 mm,
and deliberately omits longer lenses.

## Handoff notes

For contributors or assistants picking up this work, see
[`handoff/mission.md`](handoff/mission.md),
[`handoff/conversation.md`](handoff/conversation.md), and
[`handoff/progress.md`](handoff/progress.md).
