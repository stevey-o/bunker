# Cost reduction opportunities

Current estimate: **$3,877-7,950** shell materials, excluding jacks ($900-1,600) and tooling
(`bom/cost_report.md`). Target: $4,000-6,000.

## The real levers
1. **Skin gauge: 0.040 in on walls, 0.050 in reserved for the roof.** Skin is the largest single line
   (9-10 sheets, $1,170-2,300). 0.040 in walls cut skin weight ~20% on those faces and lower sheet cost.
   Trade-off: dent resistance and oil-canning, so test a panel before committing.
2. **Bigger sheets / coil stock.** 5x10 sheets eliminate seams on the roof and reduce offcuts on most
   faces. **Caveat found in v0.1:** at 80 in interior the body sides are 65.1 in tall, taller than a 60 in
   wide sheet, so sides still need a seam unless 72 in wide coil/sheet is sourced (`bom/sheet_cutlist.csv`).
3. **Surplus and remnant sourcing** of 6061 tube and 5052 sheet (metal recyclers, remnant racks, trailer
   manufacturers' drops). Tube is the second-biggest line ($888-1,985) and the most remnant-friendly.
4. **A commercial cargo-trailer door** instead of fabricating one ($400-900 bought vs. many hours and a
   sealing risk).
5. **Fewer windows:** the nose window is optional (`WINDOW_NOSE_ENABLED`), saving $100-200.
6. **Interior panel material choice**, which also moves weight (85-117 lb).
7. **Interior height:** each inch is ~$9-20 and ~5-6 lb (`bom/weight_report.md`). This is a requirement, not
   a lever, but the price is visible.

## Where cost must NOT be cut
- **Jack structures** and their attachment into the frame.
- **Tie-down nodes** and the truck-side anchors.
- **Floor structure.**
- **Adhesive quality** and surface prep: the skin is a structural diaphragm.
- Galvanic isolation hardware and sealants: cheap, and failures are expensive.
