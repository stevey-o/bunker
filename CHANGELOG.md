# Changelog

All notable changes to MINUTEMAN. Versions follow the ladder in `PROJECT_HANDOFF.md` §11:
v0.1 envelope → v0.2 structural frame candidate → v0.3 complete shell CAD → v0.4 prototype →
v0.5 build changes → v1.0 completed and validated physical shell.

## [Unreleased] — v0.1 envelope, rev B (2026-10-01)

### Changed (ADR 0004)
- Lower length 78 → **97 in**: fills the 2011 F-350 8 ft bed with the tailgate closed. Overall 121 in.
- Truck data re-based on the **2011 F-350** (Ford 2011 RV & Trailer Towing Guide + spec summaries): bed floor
  39.5 in, box depth 20.0, wells 50.9, tailgate ~61, wheelbases 156.2/172.4, camper cargo ratings.
- Lower tub width 63 → **59.5 in** (61 in tailgate). Camper geometry now derives only from the DESIGN_TRUCK.
- Weight 985-1,231 lb, cost $4,402-8,735 (both excl. jacks); reports now state the target miss computed, not hard-coded.

### Added
- Truck variants: F-350 8 ft / 6.75 ft (tailgate down), F-150 6.5 / 5.5 ft, Tacoma 6 / 5 ft; tailgate model.
- Center-of-gravity estimate from envelope face centroids; multi-truck fit study (`truck_data/fit_study.md`).
- Drawing set re-done to ASME Y14 conventions on ANSI C: MM-A01..A05 (new: A03 interior sections,
  A04 F-350 fit with CG, A05 multi-truck fit). Old A03 truck-fit sheet superseded by A04/A05.
- `reference/drafting_standards.md`, `truck_data/README.md` (sources), measurement sheet rows 15-16 (tailgate).

## v0.1 envelope, rev A

### Added
- Repository scaffold, `CLAUDE.md`, `Makefile`, `.gitignore`.
- ADRs 0001 (welding), 0002 (80 in interior / low-drag), 0003 (solar/battery provisions).
- `cad/config/dimensions.json` master config -> generated `dimensions.scad`; build variants SHORT/LONG.
- Envelope model: stepped lower tub (49.1/63 in), 80 in body, raked 24 in nose, 0.75 in roof crown;
  F-350 reference; door, window, T-slot rail, roof-boss placeholders; reserved power zone and wire chase;
  6'7" figure.
- `echo()` parts registry -> `parts.json` -> BOM, cut lists, weight and cost reports with height sensitivity.
- 12 renderings; drawings A01 general arrangement, A02 major dimensions, A03 truck fit.
- `validate_model.py` (57 checks: IDs, welded min wall, statuses, truck-fit geometry).
- DIMENSIONS.md and printable F-350 measurement sheet (generated).
- Product vision, engineering assumptions/load paths/questions, competitors (sourced), time/cost,
  business outlook, manual skeleton.

### Changed vs. handoff first pass
- Lower tub width 63 in (not ~68 in): it must pass a ~65 in tailgate opening.
- 6061 tube priced at realistic retail $/lb; shell cost range rises to $3,877-7,950.
