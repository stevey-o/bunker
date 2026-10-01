# Changelog

All notable changes to MINUTEMAN. Versions follow the ladder in `PROJECT_HANDOFF.md` §11:
v0.1 envelope → v0.2 structural frame candidate → v0.3 complete shell CAD → v0.4 prototype →
v0.5 build changes → v1.0 completed and validated physical shell.

## [Unreleased] — v0.1 envelope

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
