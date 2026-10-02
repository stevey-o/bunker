# ADR 0004 — Full 8 ft length; design truck = 2011 F-350; multi-truck fit is checked, not assumed

**Status:** Accepted for the length change. **Multi-truck product direction: OPEN, owner decision needed.**
**Date:** 2026-10-01

## Owner request
1. The camper should fill the whole 8 ft bed with the tailgate shut.
2. On a shorter (~6 ft) bed it should fit with the tailgate down.
3. Use 2011 F-350 dimensions.
4. Fit half-ton trucks and the Toyota Tacoma as well, hanging off the back if safe.

## Decision
- `camper_lower_length = 97.0 in` (FIXED): 98.0 in 2011 Super Duty 8 ft box − 0.5 in front gap − 0.5 in
  to the closed tailgate. Overall length with the 24 in nose: 121 in.
- **Design truck = 2011 F-350 crew cab 4x4 SRW, 8 ft box** (`DESIGN_TRUCK = F350_LONG`). The camper
  geometry is derived from this truck only and never changes shape with the truck shown. Every other
  truck is a *fit check* (`scripts_code/generate_fit_study.py`, `truck_data/fit_study.md`).
- Lower tub width reduced 63 → 59.5 in: the 2011 Super Duty tailgate is ~61 in wide (VERIFY ON TRUCK).
- The tailgate is still never structural. "Tailgate down" means the camper floor cantilevers past the bed end
  and must not bear on the tailgate.

## What the checks found (first-pass estimates, status CONCEPT)
Safety rule used by Ford and camper makers: **camper center of gravity at or ahead of the rear axle**, and
loaded camper within the truck's camper cargo rating (door-jamb sticker).

| Truck | Fits physically | Loaded CG vs rear axle | Loaded camper (~1,800 lb) vs rating | Verdict |
|---|---|---|---|---|
| 2011 F-350, 8 ft, tailgate closed | yes | **7.9 in ahead** | 1,438-3,002 lb by engine | CONDITIONAL (check sticker) |
| 2011 F-350, 6.75 ft, tailgate down | yes, 15.7 in overhang | **8.3 in behind** | 1,650-2,905 lb | **FAIL** |
| F-150 6.5 ft | width yes; body clashes with 21.4 in rails | 4.6 in ahead | 1,300-2,440 lb | CONDITIONAL (most trucks over payload) |
| F-150 5.5 ft | as above | 7.2 in behind | 1,300-2,440 lb | **FAIL** |
| Tacoma 6 ft / 5 ft (2016-23) | **no**: tub base 49.4 in vs 41.5 in between wells | — | 1,050-1,445 lb | **FAIL** |

Why the short F-350 fails: Ford's 2011 crew-cab wheelbases (156.2 / 172.4 in) differ by exactly the bed
difference (16.2 in), so the extra 8 ft bed length is all *ahead of* the axle. On the 6.75 ft box the axle is
only ~35 in behind the bed front wall, and a 97 in camper's CG lands ~8 in behind it.

## Consequences
- The request "fit all three truck types with one camper" cannot be met safely. Tacoma fails on geometry and
  payload; half-tons fail or are marginal on payload; the 6.75 ft F-350 fails on CG.
- **Options for the owner** (not decided here):
  - **A. One camper, 8 ft F-350 only** (current design). Simplest; best CG.
  - **B. One camper for both F-350 boxes:** shorten to roughly 80-84 in so the CG stays ahead of the axle on
    the 6.75 ft box; the 8 ft box then has unused length. Needs re-running the fit study.
  - **C. A family from the same parametric system:** MINUTEMAN-97 (F-350 8 ft), a shorter F-350/half-ton
    version, and a separate narrow, light Tacoma version (tub base <= 40 in, dry weight well under ~700 lb,
    likely a pop-up). Same config architecture, different `dimensions.json` envelopes.
- Weight rises to 985-1,231 lb dry (excl. jacks), above the 850-950 lb target even at the low end. Cost rises to
  $4,402-8,735 (excl. jacks and tooling).
