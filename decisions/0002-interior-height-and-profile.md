# ADR 0002 — 80" interior height; "sleek" means low drag, not low height

**Status:** Accepted (v0.1) · **Source:** PROJECT_HANDOFF.md §2.2

## Context
The owner needs standing room for a person 6'7" (79") or taller and also asked for a "lowish profile."
In a slide-in camper these cannot both be met. The interior floor sits on the bed floor, which is
already ~34" off the ground on an F-350.

| Element | Value (in) |
|---|---|
| Ground to bed floor | ~34 (VERIFY ON TRUCK) |
| Floor sandwich | ~3 |
| Interior clear height | 80 |
| Roof structure + skin | ~3.5 (+0.75 drainage crown at centerline) |
| **Ground to roof (eave / crown)** | **~120.5 / ~121.25 (≈10'0")** |

## Decision
- `interior_height = 80`, fully parametric.
- "Low profile" is reinterpreted as **low drag and clean styling**: minimum frontal area, flush bonded
  skins with no protruding fasteners, generously radiused vertical corners, a raked nose over the cab,
  no bulges or "ears."
- A pop-up / telescoping high-low variant is a **separate future model**
  (`camper_versions/future_concepts/high_low.md`) and does not influence v0.1.
- `generate_weight_report.py` and `generate_cost_report.py` emit a sensitivity line: lb and $ per inch
  of interior height, so the cost of the 6'7" requirement is visible.

## Consequences
At ~10'0" the camper is in the normal range for hard-side truck campers but is tall. Low bridges,
parking garages, drive-throughs, and some fuel-station canopies become route considerations. The
center of gravity rises, which matters for v0.2 stability work.
