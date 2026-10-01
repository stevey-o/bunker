# ADR 0001 — Aluminum welding: GMAW spool gun, novice-driven design rules

**Status:** Accepted (v0.1) · **Source:** PROJECT_HANDOFF.md §2.1

## Context
The original spec asked for "self-shielded flux-core MIG" on aluminum. There is no self-shielded
flux-cored aluminum wire on the market. Aluminum needs inert-gas shielding, and flux-cored processes
rely on slag chemistry that does nothing against aluminum's tenacious oxide layer. The owner's clarified
requirement was "whatever I need for strong, cheap, beginner-friendly aluminum welding."

## Decision
- **Process:** GMAW (MIG) with a **spool gun**, 100% argon at 25–35 CFH.
- **Machine class:** 200–230 A (e.g. Hobart Handler 210MVP + SpoolRunner 100, Eastwood MIG 180,
  Primeweld MIG 230). One-time tooling budget $800–1,400, tracked in `time_cost/tooling_costs.csv`,
  never in shell material cost.
- **Wire:** ER5356, 0.035". Push angle, fast travel, no preheat below 1/4" thickness.
- **Architecture is HYBRID:** weld only small safety-critical nodes (jack boxes, tie-down nodes, floor
  corner nodes) that a local shop could also weld. Bolt, rivet, and bond everything else.
  `FRAME_SYSTEM` stays switchable between `HYBRID`, `BOLTED_TUBE`, and `TSLOT`.

## Consequences (must propagate into CAD and engineering)
1. **Owner-welded members: minimum wall 0.125".** A novice will burn through the original spec's
   1×1×0.083" tube. 0.083" wall is restricted to bolted/bonded secondary framing.
   Enforced by `scripts_code/validate_model.py` (any part with `join = "WELDED"` and wall < 0.125 fails).
2. **Heat-affected-zone strength loss.** Welded 6061-T6 loses roughly 40% of its yield strength in the
   HAZ (≈40 ksi down to the mid-20s ksi, effectively annealed). Every welded joint is sized on
   HAZ-reduced allowables. Recorded as assumption A-002 in `engineering/assumptions.md`, status
   `CONCEPT` until a datasheet / Aluminum Design Manual reference is cited.
3. Aluminum skin is never welded to the frame (thin sheet distortion and burn-through); it is bonded.

## Do not revert
Do not reintroduce flux-core, and do not specify 0.083" wall for any welded joint.
