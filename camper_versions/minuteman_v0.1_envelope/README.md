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
| MM-A01..A05 drawings (ANSI C) | `drawings/general_arrangement/`, `dimensions/`, `interior/`, `truck_fit/` |
| Fit study renders | `3D_renderings/fit_study/` |
| Measurement sheet | `truck_data/measurement_templates/f350_measurement_sheet.pdf` |
| Weight / cost | `bom/weight_report.md`, `bom/cost_report.md` |

## Findings worth a decision before v0.2
0. **Rev B (ADR 0004):** lower length 97 in to fill the 2011 F-350 8 ft bed with the tailgate closed. The fit study
   shows the 6.75 ft bed (tailgate down), F-150 5.5 ft and all Tacomas are **unsafe or don't fit**; see
   `truck_data/fit_study.md`. Product direction (8 ft only / shorter / family) is an open owner decision.
1. **Weight:** 985-1,231 lb excluding jacks; over the 850-950 lb target even at the low end.
2. **Cost:** $4,402-8,735 excluding jacks/tooling vs. the $4-6k target. Realistic 6061 tube pricing is the
   main reason the range exceeds the handoff's first pass.
3. **Height costs:** each +1 in of interior height adds ~6-7 lb and ~$26-50.
4. **5x10 sheets don't solve the sides:** at 80 in interior the body sides are 65.5 in tall, taller than
   a 60 in sheet, so every side needs a seam (or 72 in coil stock).
5. **Tub width set by the tailgate:** 59.5 in (2011 Super Duty ~61 in opening): the tub must pass the tailgate opening, not just fit between the rails.
