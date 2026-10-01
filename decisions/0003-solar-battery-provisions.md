# ADR 0003 — Solar and battery: structural provisions only

**Status:** Accepted (v0.1) · **Source:** PROJECT_HANDOFF.md §2.3

## Context
The owner wants a roof rack for solar panels and an internal battery or solar generator. The spec
forbids designing electrical systems.

## Decision
Design **only the structure**:
- **Roof-rack mounting bosses** that land on roof crossmembers, never on bare skin. v0.1 shows six boss
  placeholders (`RACK-ROOF-01..06`). In v0.2 each one must sit on a roof crossmember.
- **Wire chase:** a reserved vertical path through the wall/roof cavity (front-left corner in v0.1),
  kept as reserved geometry with no wiring.
- **Reinforced floor zone:** a floor area with T-slot tie-down capability for a battery or solar
  generator, sized by mass and footprint only. Placed forward of the rear axle to help the center of
  gravity.

No panels, wiring, controllers, loads, or capacity math. The reserved masses are payload assumptions in
`engineering/assumptions.md` (A-020, A-021).
