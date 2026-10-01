# MINUTEMAN — aluminum slide-in camper shell

A rugged aluminum truck-camper **shell** for a Ford F-350 that provides the protected space and
attachment infrastructure while letting the owner decide what the camper eventually becomes.

**Status: v0.1 — envelope only.** No structural frame yet. Nothing here is engineering-validated;
CAD appearance is not engineering validation.

## Start here

| | |
|---|---|
| Spec (authoritative) | [`PROJECT_HANDOFF.md`](PROJECT_HANDOFF.md) |
| Design decisions | [`decisions/`](decisions/) |
| v0.1 dimensions | [`camper_versions/minuteman_v0.1_envelope/DIMENSIONS.md`](camper_versions/minuteman_v0.1_envelope/DIMENSIONS.md) |
| Truck measurement sheet | [`truck_data/measurement_templates/f350_measurement_sheet.md`](truck_data/measurement_templates/f350_measurement_sheet.md) |
| Assumptions & statuses | [`engineering/assumptions.md`](engineering/assumptions.md) |
| Renderings | [`3D_renderings/`](3D_renderings/) |
| Drawings | [`drawings/`](drawings/) |

## Headline numbers (v0.1, estimates)

- Interior standing height **80"** (6'7"+), ground-to-roof **~10'0"** on an F-350 — tall, not low-profile.
- Dry weight estimate **854–1,071 lb excluding jacks** vs. an 850–950 lb target. Jacks add 100–140 lb.
- Shell material cost estimate **$3,877–7,950 excluding jacks and tooling** vs. a $4–6k target. Jacks add $900–1,600.
- Each +1" of interior height costs ~5–6 lb and ~$9–20.

Full reports: [`bom/weight_report.md`](bom/weight_report.md), [`bom/cost_report.md`](bom/cost_report.md).

## Next physical action

Print [`f350_measurement_sheet.pdf`](truck_data/measurement_templates/f350_measurement_sheet.pdf), measure
the truck, update `cad/config/dimensions.json`, run `make all`.

## Building the outputs

```
make setup   # once
make all     # sync config, render, drawings, reports, validate
```

Requires OpenSCAD (`brew install --cask openscad@snapshot`; the stable `openscad` cask was disabled by
Homebrew on 2026-09-01 for failing Gatekeeper) and Python 3.9+.
`cad/config/dimensions.json` is the single source of truth; everything else is regenerated from it.
