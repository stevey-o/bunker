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
| Drawings (ANSI C, ASME Y14 style, MM-A01..A05) | [`drawings/`](drawings/) · [standards used](reference/drafting_standards.md) |
| Truck data and sources | [`truck_data/README.md`](truck_data/README.md) |

## Headline numbers (v0.1, estimates)

- **97" long** lower body (fills a 2011 F-350 8 ft bed with the tailgate closed, ADR 0004); 121" overall with the nose.
- Interior standing height **80"** (6'7"+), ground-to-roof **~10'7"** on a 2011 F-350 4x4 — tall, not low-profile.
- Dry weight estimate **985–1,231 lb excluding jacks**, over the 850–950 lb target. Jacks add 100–140 lb.
- Shell material cost estimate **$4,402–8,735 excluding jacks and tooling** vs. a $4–6k target. Jacks add $900–1,600.
- **Truck fit** ([fit study](truck_data/fit_study.md)): 8 ft F-350 OK (check payload sticker); 6.75 ft F-350 with tailgate down, F-150 5.5 ft and every Tacoma **fail** (CG behind axle, geometry, or payload).
- Each +1" of interior height costs ~6–7 lb and ~$26–50.

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
