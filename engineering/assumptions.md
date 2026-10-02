# Engineering assumptions

> **CAD appearance is not engineering validation.** A shape that looks right in a render has not been
> shown to carry load, stay watertight, or survive road vibration. Nothing in v0.1 has been calculated,
> tested, or reviewed.

Every important structural assumption carries exactly one status:
`CONCEPT` · `CALCULATED` · `MANUFACTURER VERIFIED` · `PHYSICALLY TESTED` · `PROFESSIONALLY REVIEWED` ·
`NEEDS REVIEW`. Truck-dependent values use `VERIFY ON TRUCK`.

Rules (enforced by `scripts_code/validate_model.py`):
- Never promote a status without the evidence. `CALCULATED` requires a file in
  `engineering/calculations/` cited in the Reference column.
- `MANUFACTURER VERIFIED` requires a datasheet in `reference/` cited in the Reference column.

| ID | Assumption | Status | Safety-critical | Reference |
|---|---|---|---|---|
| A-001 | Aluminum is welded GMAW with spool gun, 100% argon, ER5356. Self-shielded flux-core aluminum does not exist. | CONCEPT | yes | decisions/0001-welding-process.md |
| A-002 | Welded 6061-T6 loses ~40% of yield strength in the HAZ (~40 ksi to mid-20s ksi). All welded joints sized on HAZ-reduced allowables. | CONCEPT | yes | ADR 0001; cite Aluminum Design Manual to upgrade to MANUFACTURER VERIFIED |
| A-003 | Owner-welded members have min wall 0.125 in; 0.083 in wall is bolted/bonded only. | CONCEPT | yes | ADR 0001; validate_model.py |
| A-004 | Skin is 5052-H32 bonded with structural adhesive plus selective rivets and acts as a shear diaphragm. Never continuously welded. | CONCEPT | yes | Adhesive datasheet and joint tests required (v0.2) |
| A-005 | Jacks and tie-downs terminate in primary structural members, never in skin, trim, thin sheet, or a single T-nut. | CONCEPT | yes | Hard rule; v0.2 jack/tie-down design |
| A-006 | Tailgate is not a structural support. | CONCEPT | yes | Hard rule |
| A-007 | Camper CG must fall at or forward of the rear axle centerline. Area-centroid estimate, loaded: 7.9 in ahead on the 8 ft F-350; 8.3 in **behind** on the 6.75 ft F-350. | NEEDS REVIEW | yes | scripts_code/estimates.py; truck_data/fit_study.md; axle position is VERIFY ON TRUCK |
| A-008 | Truck payload capacity and rear axle / tire ratings accommodate shell + payload + occupants' gear. | NEEDS REVIEW | yes | Door-jamb payload sticker; weigh truck at a CAT scale |
| A-009 | Shell dry weight 985-1,231 lb excluding jacks (area-based coefficients, 97 in camper). Jacks add 100-140 lb. | CONCEPT | yes | bom/weight_report.md |
| A-010 | Nose (cab-over) is storage/desk volume only and is not engineered to carry two sleeping adults. | CONCEPT | yes | ADR 0002; v0.1 scope |
| A-011 | Nose cantilever (24 in over cab) carries its own weight plus a storage allowance (value TBD in v0.2). | NEEDS REVIEW | yes | v0.2 calculation |
| A-012 | Every aluminum-to-dissimilar-metal interface (stainless fasteners, steel jacks, truck tie-downs) is galvanically isolated (nylon washers, Tef-Gel/Duralac, isolation tape). | CONCEPT | yes | cad/config/hardware.scad notes |
| A-013 | Every exterior joint gets a waterproofing detail; no exposed screw penetrations as primary roof attachment. | CONCEPT | no | Hard rule; drawings E01-E02 in v0.3 |
| A-014 | Owner accessory T-slot rails bolt into frame members, are not primary structure, and carry owner accessories only. Slip/rotation capacity to be tested. | CONCEPT | yes | Test plan: T-slot joint slip and rotation |
| A-015 | 6061-T6 density 0.0975 lb/in3; 5052-H32 0.0968 lb/in3; XPS ~2 pcf. | CONCEPT | no | Standard handbook values; cite datasheet |
| A-016 | 1010-class T-slot extrusion weighs 0.5097 lb/ft. | CONCEPT | no | 80/20 catalog value; add datasheet to reference/ |
| A-017 | Roof crown 0.75 in transverse provides positive drainage at expected parking slopes. | CONCEPT | no | Water test (v0.4) |
| A-018 | Lower tub at 59.5 in width passes the 2011 Super Duty tailgate opening (~61 in) with 0.75 in per side. | VERIFY ON TRUCK | yes | truck_data/measurement_templates/f350_measurement_sheet.md |
| A-019 | Nose underside 4 in above highest cab-roof point (incl. clearance lamps) is enough for cab/bed relative motion. | VERIFY ON TRUCK | yes | Measurement sheet M4; check under articulation |
| A-020 | Power zone reservation: battery or solar generator, 150 lb, 24 x 20 in footprint, forward of rear axle. | CONCEPT | yes | ADR 0003 |
| A-021 | Roof rack + panels: 120 lb distributed over six bosses, each landing on a roof crossmember. | CONCEPT | yes | ADR 0003 |
| A-023 | 2011 F-350 rear axle is ~35.0 in (6.75 ft box) / ~51.2 in (8 ft box) aft of the bed front wall, derived from Ford wheelbases and a quoted cab-to-axle figure. | VERIFY ON TRUCK | yes | truck_data/README.md |
| A-024 | Loaded camper (~1,800 lb: dry + jacks + reservations + 300 lb gear) is within the 2011 F-350 camper cargo rating only for some engine/option combinations (1,438-3,002 lb). | NEEDS REVIEW | yes | Ford 2011 RV & Trailer Towing Guide; door-jamb sticker |
| A-025 | Half-ton and Tacoma fit values (bed floor height, cab height, axle position, tailgate opening) are estimates; fit verdicts for those trucks are indicative only. | CONCEPT | yes | truck_data/README.md |
| A-022 | Road vibration and fatigue at bonded and welded joints are acceptable over the service life. | NEEDS REVIEW | yes | v0.2+ fatigue review; professional review before v1.0 |

## Safety-critical list (from PROJECT_HANDOFF.md §8)

Floor structure, jack mounts, jack stability, tie-downs, nose cantilever, major joints, fastener shear and
tension, T-slot slip, bracket rotation, skin shear transfer, adhesive compatibility, fatigue, road
vibration, truck clearance, center of gravity, payload, rear axle loading, tire loading.
None of these has been addressed beyond the assumptions above. v0.2 starts this work.
