# MINUTEMAN v0.1: envelope

**Scope:** envelope solids only, with no structural frame. Global config architecture, simplified F-350
reference, lower tub, main body, 24 in nose, crowned roof, door/window/rail/boss placeholders, a 6'7"
reference figure, and truck clearance.

| Deliverable | Location |
|---|---|
| Dimension table | [DIMENSIONS.md](DIMENSIONS.md) |
| Exterior renders (7) | `3D_renderings/exterior/` |
| Truck fit renders (4) | `3D_renderings/truck_fit/` |
| Interior rails render | `3D_renderings/interior_shell/01_utility_rails.png` |
| A01 / A02 / A03 drawings | `drawings/general_arrangement/`, `drawings/dimensions/`, `drawings/truck_fit/` |
| Measurement sheet | `truck_data/measurement_templates/f350_measurement_sheet.pdf` |
| Weight / cost | `bom/weight_report.md`, `bom/cost_report.md` |

## Findings worth a decision before v0.2
1. **Weight:** 854-1,071 lb excluding jacks vs. the 850-950 lb target. Reachable only at the low end and without jacks.
2. **Cost:** $3,877-7,950 excluding jacks/tooling vs. the $4-6k target. Realistic 6061 tube pricing is the
   main reason the range exceeds the handoff's first pass.
3. **Height costs:** each +1 in of interior height adds ~5-6 lb and ~$9-20.
4. **5x10 sheets don't solve the sides:** at 80 in interior the body sides are 65.1 in tall, taller than
   a 60 in sheet, so every side needs a seam (or 72 in coil stock).
5. **Tub width set by the tailgate:** 63 in, not the ~68 in between rails, because the tub must pass a
   ~65 in tailgate opening.
