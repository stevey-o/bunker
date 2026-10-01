# Ford F-350 reference data

The model is seeded with **preliminary** values (PROJECT_HANDOFF.md §6). Every interface value is
**VERIFY ON TRUCK** until measured with `../measurement_templates/f350_measurement_sheet.pdf`.

| Item | Seed value (in) | Notes |
|---|---|---|
| Ground to bed floor | ~34 | varies with 2WD/4WD, tires, load |
| Bed depth (floor to rail top) | ~20.4 | |
| Inside width at top | ~69.3 | |
| Between wheel wells | ~50.6 | |
| Bed length, 6.75 ft | ~81.9 | |
| Bed length, 8 ft | ~98.0 | |
| Cab roof above bed floor | ~46 | include roof marker lamps |
| Rear axle aft of bed front wall | 48 (6.75) / 52 (8) | rough estimate; **no reliable source yet** |
| Tailgate opening | ~65 | rough estimate; **no reliable source yet** |
| Wheel-well height | ~10.5 | rough estimate; **no reliable source yet** |

The last three rows are placeholders chosen so the model is plausible, not published Ford figures. They
are the most likely values to move after measurement.

`generic_short_bed/` and `generic_long_bed/` are reserved for future fitments; the config's
`truck_variants` section already supports adding them.
