# Owner configurability

What the owner can change without re-engineering the shell, and what needs care.

## Free to change (accessory level)
- Anything bolted to UTIL T-slot rails within the rail's rated load. **Rating TBD:** T-slot slip and
  rotation tests are in the v0.2 test plan, so do not hang heavy loads until then.
- Equipment strapped into the power zone, up to the 150 lb reservation.
- Roof rack and panels on the six bosses, up to the 120 lb reservation.

## Change in `dimensions.json` and regenerate (design level)
- Rail counts and heights, door offset, window sizes/positions, nose window on/off, nose projection,
  interior height (see the sensitivity line in `bom/weight_report.md`).

## Do not change without engineering review
- Anything touching jack structures, tie-down nodes, the floor structure, or the nose cantilever.
- Cutting new openings in skin panels (the skin is a structural shear diaphragm).
- Converting the nose into a sleeping platform (it is not engineered for that, A-010).
