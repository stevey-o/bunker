# CLAUDE.md — MINUTEMAN camper shell

DIY aluminum slide-in truck-camper **shell** for a Ford F-350. `PROJECT_HANDOFF.md` is the authoritative
spec; `decisions/` holds the ADRs. Read both before changing design intent.

## Current state

v0.1 = envelope solids only. **Do not start structural frame design (v0.2) without explicit owner
approval.** Do not label anything v1.0 — v1.0 means a built and validated physical shell.

## Resolved decisions — do not revert (see `decisions/`)

- Aluminum welding is GMAW with a spool gun and 100% argon. Self-shielded flux-core aluminum does not exist.
- Any owner-welded member has **min wall 0.125"**. 0.083" wall is bolted/bonded only.
- Welded 6061-T6 joints are sized on **HAZ-reduced allowables** (~40% yield loss).
- `interior_height = 80` (6'7"+ standing). "Low profile" means low drag / clean styling, not low height.
- Solar/battery: structural provisions only (roof bosses, wire chase, reinforced floor zone). No electrical design.
- Report weight and cost honestly; never present an aspiration as achieved.

## Hard rules

- Never silently promote a `CONCEPT` assumption. Statuses: `CONCEPT` · `CALCULATED` ·
  `MANUFACTURER VERIFIED` · `PHYSICALLY TESTED` · `PROFESSIONALLY REVIEWED` · `NEEDS REVIEW`.
  Truck-dependent dimensions are tagged `VERIFY ON TRUCK`. `CALCULATED` requires a file in
  `engineering/calculations/`.
- Safety-critical loads (jacks, tie-downs) terminate in structural members — never skin, trim, thin sheet,
  or a single T-nut.
- Skin is bonded (structural adhesive + selective rivets), never continuously welded.
- No exposed screw penetrations as primary roof attachment. Tailgate is not a structural support.
- No furniture, bed, kitchen, batteries, or water in the model.
- Every exterior joint gets a waterproofing detail; every aluminum/dissimilar-metal interface gets a
  galvanic isolation note.

## Units

Inches, degrees, pounds, USD. No metric except a cited, converted purchased-component datasheet value.

## Part IDs

Grammar `SYSTEM-LOCATION-NUMBER`, defined in `cad/config/part_ids.md`, enforced by
`scripts_code/validate_model.py` (fails on duplicate or malformed IDs). One ID is used everywhere:
CAD, drawings, BOM, cut list, renderings, manual, cost and weight reports. No second naming system.

## Single source of truth — regenerate, don't hand-edit

`cad/config/dimensions.json` is the master. Never hand-edit generated files:
`cad/config/dimensions.scad`, everything in `bom/`, everything in `output/`, the PNGs in
`3D_renderings/`, the PDFs in `drawings/`, `camper_versions/*/DIMENSIONS.md`, and
`truck_data/measurement_templates/f350_measurement_sheet.*`. Edit the source, then run `make all`.

Never scatter literal dimensions through `.scad` files; reference config variables. Keep modules small.

## Commands

```
make setup      # .venv + reportlab
make sync       # dimensions.json -> dimensions.scad
make render     # OpenSCAD renders + parts.json registry
make drawings   # A01/A02/A03 PDFs
make reports    # BOM, cut list, weight, cost
make docs       # DIMENSIONS.md + truck measurement sheet
make validate   # rule checks (min wall, IDs, statuses)
make all
```

OpenSCAD CLI: `/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD` (constant in `scripts_code/common.py`).
Python: `.venv/bin/python` (system 3.9; only dependency is reportlab).

## Loop

MODEL → RENDER → INSPECT → CORRECT → DOCUMENT → COMMIT. Look at the renders before committing.
