# Requirements

Status key: **FIXED** (owner requirement) · **TARGET** (goal, may be missed) · **CONSTRAINT** (physics / law / truck).

| ID | Requirement | Type | v0.1 status |
|---|---|---|---|
| R-01 | Fills a 2011 F-350 8 ft bed with the tailgate closed (ADR 0004) | FIXED | Met: 97 in, .5 in to tailgate; VERIFY ON TRUCK |
| R-01a | Fits a 6.75 ft F-350 with the tailgate down, if safe | FIXED (conditional) | **Not met:** loaded CG ~8 in behind rear axle |
| R-01b | Fits half-ton trucks and the Tacoma, overhanging if safe | FIXED (conditional) | **Not met** safely; F-150 6.5 ft marginal on payload; Tacoma fails geometry + payload |
| R-02 | Interior standing height for a 6'7"+ person (80 in clear) | FIXED | Met in envelope |
| R-03 | Low drag, clean styling ("sleek") | TARGET | Raked nose, R3 corners, flush placeholders |
| R-04 | Dry weight 850-950 lb | TARGET | **Not met:** estimate 985-1,231 lb excl. jacks |
| R-05 | Material cost ~$4,000-6,000 ("high-end topper") | TARGET | **Partly:** estimate $4,402-8,735 excl. jacks/tooling |
| R-06 | Buildable by a novice aluminum welder | FIXED | ADR 0001 rules adopted |
| R-07 | One rear entry door, limited windows | FIXED | Placeholders: 1 door, 2 side + optional nose window |
| R-08 | Four camper-jack attachment structures | FIXED | v0.2 |
| R-09 | Truck tie-down structures; tailgate not structural | FIXED | v0.2 |
| R-10 | Interior T-slot utility rails (3 left, 3 right, 1 front) | FIXED | Placeholders placed |
| R-11 | Roof-rack bosses on crossmembers; wire chase; power floor zone | FIXED | Placeholders / reserved geometry |
| R-12 | Insulated walls and roof; interior protective panel | FIXED | Thickness allowances only |
| R-13 | Watertight; every exterior joint detailed | FIXED | v0.3 details |
| R-14 | Legal width (<= 102 in) | CONSTRAINT | 80 in |
| R-15 | Lower tub passes the tailgate opening and clears wheel wells | CONSTRAINT | Checked by validate_model.py; VERIFY ON TRUCK |
| R-16 | CG forward of rear axle; within truck payload / GAWR | CONSTRAINT | Proxy only; v0.2 calculation |
| R-17 | Out of scope: plumbing, electrical systems, HVAC, furniture, bed, kitchen | FIXED | None in model |
