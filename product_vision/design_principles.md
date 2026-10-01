# Design principles

## Priorities, in order
1. Safety
2. Structural integrity
3. Water resistance
4. Low weight
5. Simplicity
6. Low cost
7. Repairability
8. Configurability
9. Ease of fabrication
10. Appearance

When two solutions perform similarly, prefer the one that is easier to understand, cut, assemble,
repair, replace, document, and modify later, and that depends on fewer specialized tools.

## Rules that follow from them
- **Weld little, weld thick.** Owner welds only small safety-critical nodes, never thinner than 0.125 in
  wall, sized on heat-affected-zone allowables (ADR 0001). Everything else is bolted, riveted, bonded.
- **Loads go into structure.** Jacks, tie-downs, roof rack, and power zone attach to primary members, never skin.
- **Skin is structure, not decoration.** It is bonded as a shear diaphragm, never continuously welded.
- **Water first.** Every exterior joint gets a waterproofing detail; no screw penetrations as primary
  roof attachment; positive roof drainage.
- **"Sleek" means low drag**, not low height (ADR 0002): flush skins, radiused corners, raked nose, no bulges.
- **One source of truth.** A dimension lives in `dimensions.json` once; drawings, BOM, and manual are generated.
- **Honest numbers.** Estimates are labeled estimates; an aspiration is never reported as achieved.
