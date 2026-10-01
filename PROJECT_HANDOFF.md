# MINUTEMAN CAMPER — HANDOFF FOR CLAUDE CODE

**Repo:** `bunker` (https://github.com/stevey-o/bunker) · **Local:** `/Users/cree/Documents/bunker-camper`
**Owner/builder:** Steven Orlik · **Product codename:** MINUTEMAN · **Current target:** v0.1 ENVELOPE ONLY
**Status of this document:** authoritative. It supersedes any earlier verbal spec where the two conflict.

---

## 0. READ THIS FIRST

You are picking up a project that has had one planning pass. Three decisions were already made after the
original spec was written, because the original spec contained requirements that were **physically
impossible or mutually contradictory**. They are recorded in §2. Do not re-litigate them and do not
silently revert to the original spec's numbers.

Your job right now is narrow:

1. Scaffold the repository (§5).
2. Build the parametric config architecture (§6).
3. Build the **v0.1 envelope** model and its deliverables (§10).
4. **STOP at the approval gate (§11).** Do not begin detailed structural frame design.

The single most common way to fail this task is to start designing the frame. v0.1 is envelope solids
only. Another way to fail is to create hundreds of empty placeholder files; every document you create
should contain real content or an explicit, honest list of open questions.

---

## 1. WHAT MINUTEMAN IS

A DIY aluminum slide-in truck camper **shell** for a Ford F-350. Shell only.

> A rugged aluminum truck-camper shell that provides the protected space and attachment
> infrastructure while allowing the owner to decide what the camper eventually becomes.

The shell must be useful on the day it is finished even if nothing is installed inside it.

**Explicitly out of scope:** shower, toilet, permanent bed, kitchen, sink, plumbing, water tanks,
propane, refrigerator, permanent cabinetry, electrical system, wiring, charge controllers, batteries,
solar panels, HVAC, entertainment, luxury finishes, and any assumption about interior layout.

**In scope:** structural floor, aluminum frame, bonded aluminum skin, insulated walls and roof, interior
protective panel, one rear entry door, limited windows, four camper jack attachment structures, truck
tie-down structures, interior T-slot utility rails, and *structural provisions* for a roof rack and a
battery/generator bay (see §2.3).

### Design priorities, in order

Safety → structural integrity → water resistance → low weight → simplicity → low cost →
repairability → configurability → ease of fabrication → appearance.

When two solutions perform similarly, prefer the one that is easier to understand, cut, assemble,
repair, replace, document, and modify later, and that depends on fewer specialized tools.

---

## 2. RESOLVED DECISIONS (do not revert)

### 2.1 Welding: aluminum GMAW with a spool gun — and the design bends to suit a novice

The owner asked for "self-shielded flux-core MIG" on aluminum. **That does not exist.** There is no
self-shielded flux-cored aluminum wire on the market; aluminum requires inert gas coverage, and
flux-cored processes depend on slag chemistry that does not work against aluminum's oxide layer. The
owner's clarified requirement was "whatever I need for strong, cheap, beginner-friendly aluminum
welding," which resolves to:

- **Process:** GMAW (MIG) with a **spool gun**, 100% argon at 25–35 CFH.
- **Machine class:** 200–230 A (e.g. Hobart Handler 210MVP + SpoolRunner 100, Eastwood MIG 180,
  Primeweld MIG 230). Budget **$800–1,400** one-time tooling, tracked in `time_cost/tooling_costs.csv`,
  never in the shell material cost.
- **Wire:** ER5356, 0.035". Push angle, fast travel, no preheat under 1/4".

Two consequences that **must** propagate into the CAD and the engineering docs:

- **Minimum wall thickness for any owner-welded member is 0.125".** The original spec's
  1×1×0.083" tube will burn through for a novice. 0.083" wall is therefore restricted to
  **bolted/bonded** secondary framing only. Encode this as a hard rule in `validate_model.py`.
- **Welded 6061-T6 loses roughly 40% of its yield strength in the heat-affected zone** (about 40 ksi
  down into the mid-20s ksi, effectively annealed). Every welded joint must be sized on HAZ-reduced
  allowables. Record this in `engineering/assumptions.md` with status `MANUFACTURER VERIFIED` once a
  datasheet is cited, `CONCEPT` until then.

This is the reason the architecture is **HYBRID**: weld only the small safety-critical nodes (jack
boxes, tie-down nodes, floor corner nodes) where a local shop could also do the work, and bolt, rivet,
and bond everything else. Keep `FRAME_SYSTEM` switchable between `"HYBRID"`, `"BOLTED_TUBE"`, and
`"TSLOT"` so all three remain evaluable from one envelope.

### 2.2 Height: 80" interior standing height; "sleek" means aerodynamic, not short

The owner needs standing room for a **6'7" person or taller**, so `interior_height = 80`. The owner also
asked for a "lowish profile." **These cannot both be satisfied in a slide-in camper.** Stack-up on an
F-350:

| Element | Value (in) |
|---|---|
| Ground to bed floor | ~34 (VERIFY ON TRUCK) |
| Floor sandwich | ~3 |
| Interior clear height | 80 |
| Roof structure + skin | ~3.5 |
| **Ground to roof** | **~120.5 (10'0.5")** |

That is a tall camper, in the normal range for hard-side truck campers but nowhere near low-profile.
Therefore **low profile is reinterpreted as low drag and clean styling**, not reduced height: minimum
frontal area, flush bonded skins with no protruding fasteners, generously radiused vertical corners, a
raked/tapered nose over the cab, and no bulges or "ears."

The pop-up/telescoping "high-low" variant the owner wants is **a separate future model**. Put a concept
note in `camper_versions/future_concepts/high_low.md` and do not let it influence v0.1.

Make `interior_height` fully parametric and have `generate_weight_report.py` emit a **sensitivity line**
showing lb and $ per inch of height, so the owner can see exactly what the 6'7" requirement costs.

### 2.3 Solar and battery: structural provisions only, zero system design

The owner wants a roof rack for solar and an internal battery/solar generator; the spec forbids
designing electrical systems. Both are satisfied by designing **only the structure**:

- Roof-rack mounting bosses that land on roof crossmembers, never on bare skin.
- A wire chase path through the wall/roof cavity, reserved as geometry.
- A reinforced floor zone with T-slot tie-down capability for a battery or solar generator, sized by
  mass and footprint only.

No panels, no wiring, no controllers, no loads, no capacity math. Record the reserved masses as
payload assumptions in `engineering/assumptions.md`.

### 2.4 Cost: the skin dominates, and the target is tight

Owner's target is "ballpark of a high-end truck topper," i.e. **$4,000–6,000**, consistent with the
spec's $5,000–7,000. First-pass reality, **excluding jacks and tooling**:

- 5052 sheet, ~10 sheets of 4×8 at 0.050": **$1,300–2,300** ← largest single line item
- 6061 tube: $500–900 · T-slot: $250–500 · door: $400–900 · windows: $300–600
- Insulation: $150–250 · adhesive/sealant: $150–300 · fasteners/rivets: $200–350
- Interior panel: $200–400 · welding consumables and gas: $150–300
- **Subtotal ≈ $3,600–6,800.** Jacks add $900–1,600 and are tracked separately.

`time_cost/cost_reduction_opportunities.md` must open with the real levers: 0.040" skin on walls with
0.050" reserved for the roof, 5×10 sheets to eliminate seams and offcuts, surplus and remnant sourcing,
and a commercial cargo-trailer door instead of custom fabrication. It must also state where cost must
**not** be cut: jack structures, tie-down nodes, floor structure, adhesive quality.

### 2.5 Weight: state the honest number, not the aspirational one

Spec target is 850–950 lb dry. First-pass build-up, excluding jacks:

floor 180–230 · wall frames 120–160 · roof frame 50–70 · nose frame 35–50 · skin 190–210 ·
insulation ~60 · interior panel 85–110 · door 45–70 · windows ~30 · T-slot rails ~18 ·
hardware and adhesive 40–60 → **≈ 860–1,060 lb**, plus 100–140 lb for four jacks.

Conclusion to write down plainly: the 850–950 lb target is reachable only without jacks and only with
disciplined interior paneling. Interior panel and skin thickness are the two biggest levers. Do not
report a weight as achieved when it is an aspiration.

---

## 3. ENVIRONMENT (already verified on this machine)

- macOS (darwin 25.3.0), zsh, Homebrew 6.0.21 at `/opt/homebrew`.
- **OpenSCAD is NOT installed** → `brew install --cask openscad`. Verify the CLI binary at
  `/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD` and wrap its path in a Python constant.
- Python is **system 3.9.6 only**, with no third-party modules → create `.venv`. The **only** dependency
  is `reportlab` (pure Python, draws PDF directly, no system libs). Do not add cairo/svglib/matplotlib.
- **`gh` is NOT installed anywhere** — not in Homebrew, not in `/opt/pmk/env/global/bin`, not in any
  project's `node_modules/.bin`, and there is no `~/.config/gh`. It is **not needed** for pushing.
- **Git auth already works over HTTPS.** `credential.helper = osxkeychain` is set in the *system*
  gitconfig (not global, which is why it is easy to miss), and a github.com credential for account
  `202304373` resolves via `git credential fill`. The owner's other repos (`stevey-o/social-circles`,
  `stevey-o/web-scraper`) use the same mechanism.
- Git identity is already set globally: `Steven Orlik <steven.orlik5@gmail.com>`.
- Remote to add: `git remote add origin https://github.com/stevey-o/bunker.git`, branch `main`. The
  repo exists and is empty. **Make a scaffold commit and push early** to prove the token's scopes before
  a large amount of work is sitting unpushed. If the push fails on scope or expiry, fall back to
  `brew install gh && gh auth login`.

**Units are inches throughout.** Degrees for angles, pounds for mass, USD for cost. No metric anywhere
in the model or reports except where a purchased component's datasheet is metric, in which case convert
and cite.

---

## 4. HARD RULES

- Never silently promote a `CONCEPT` assumption to a verified fact. Use the §8 status system.
- Never attach a safety-critical load to exterior skin, decorative panel, thin sheet, a single T-nut, or
  lightweight trim. Jacks and tie-downs terminate in structural members, full stop.
- Never continuously weld thin exterior skin to the frame. Skin is **bonded** with structural
  adhesive plus selective rivets, acting as a shear diaphragm.
- Never rely on exposed screw penetrations as the primary roof attachment system.
- Do not assume the tailgate is a structural camper support.
- Do not place furniture, a bed, a kitchen, batteries, or water in the model.
- Do not create a second naming system for any document. One part ID appears everywhere (§7).
- Do not hand-edit generated files (`cad/config/dimensions.scad`, everything in `bom/` and `output/`).
  Edit the source and regenerate.
- Every exterior joint gets a waterproofing detail. Every aluminum-to-dissimilar-metal interface gets a
  galvanic isolation note.
- Write a `CLAUDE.md` at the repo root during scaffolding that restates these hard rules, the units
  convention, the part ID grammar, and the "regenerate, don't hand-edit" rule, so future sessions
  inherit them automatically.

---

## 5. REPOSITORY LAYOUT

Initialize git at the workspace root and lay the tree out **directly at the root** (not nested inside a
`Minuteman-Camper/` subdirectory). There is exactly one product today; if the high-low model ever
becomes real, move things into `models/` with a `git mv` then.

```
bunker-camper/
├── README.md                  PROJECT_HANDOFF.md (this file)   CLAUDE.md
├── CHANGELOG.md               Makefile                         .gitignore
├── decisions/                 numbered ADRs; 0001-welding, 0002-height, 0003-solar-provisions
├── product_vision/            vision, design_principles, requirements, shell_scope,
│                              owner_configurability, future_roadmap
├── camper_versions/           minuteman_v0.1_envelope … v0.4_prototype, future_concepts/
├── cad/
│   ├── main.scad  truck_reference.scad  camper_envelope.scad
│   ├── config/    dimensions.json (MASTER)  dimensions.scad (GENERATED)
│   │              materials.scad  profiles.scad  hardware.scad  build_variant.scad  part_ids.md
│   ├── frame/     floor, left/right/front/rear_wall, roof, nose, jack_structure, tiedowns
│   ├── profiles/  square_tube, rectangular_tube, tslot_20/30/40
│   ├── joints/    angle_bracket, gusset, joining_plate, tnut, through_bolt
│   ├── skin/      left, right, front, rear, roof
│   ├── utility_rails/   left_wall_rails, right_wall_rails, front_wall_rail
│   └── purchased_components/  door, windows, jacks
├── drawings/        general_arrangement, dimensions, frame, floor, walls, roof, nose,
│                    utility_rails, jack_mounts, tiedowns, joints, sheet_metal,
│                    waterproofing, truck_fit
├── 3D_renderings/   exterior, interior_shell, frame, exploded, truck_fit, utility_rails,
│                    joints, assembly_steps
├── scripts_code/    sync_config.py  render_all.py  render_steps.py  generate_bom.py
│                    generate_cutlist.py  generate_weight_report.py  generate_cost_report.py
│                    generate_manual.py  validate_model.py  export_drawings.py
├── bom/             master_bom.csv  frame_cutlist.csv  extrusion_cutlist.csv  sheet_cutlist.csv
│                    fasteners.csv  purchased_components.csv  suppliers.csv
├── manual/          build_manual.md  steps/  diagrams/  inspections/  testing/
├── engineering/     assumptions.md  load_paths.md  structural_questions.md  calculations/
│                    manufacturer_data/  joint_testing/  water_testing/  engineering_review/
├── truck_data/      ford_f350/  generic_short_bed/  generic_long_bed/  measurement_templates/
├── time_cost/       project_budget.md  material_costs.csv  tooling_costs.csv  labor_estimate.csv
│                    build_timeline.md  sourcing.md  cost_reduction_opportunities.md
├── competitors/     kimbo, aluminum_campers, composite_campers, diy_builds, modular_shells,
│                    comparison_matrix.csv
├── business_outlook/  positioning, target_customer, market_questions, manufacturing_options,
│                    pricing_model, scalability, risks, future_products
├── reference/       inspiration/  manufacturer_catalogs/  material_datasheets/
│                    fastener_datasheets/  adhesives/  source_links.md
└── output/          current_design/  drawings/  renderings/  manual/  bom/  release_packages/
```

`.gitignore` covers `.venv/`, `output/`, `__pycache__/`, `.DS_Store`. Generated renderings and drawings
**are** committed (they are review artifacts the owner looks at on GitHub); `output/` staging is not.

---

## 6. SINGLE SOURCE OF TRUTH

`cad/config/dimensions.json` is the **master**. `scripts_code/sync_config.py` generates
`cad/config/dimensions.scad` from it. The Python reporting scripts read the same JSON. A dimension can
therefore never disagree between model, drawings, BOM, weight report, and manual.

```
dimensions.json ──sync_config.py──> dimensions.scad ──> main.scad + modules
       │                                                      │
       │                                         ┌────────────┴────────────┐
       │                                   render_all.py            echo() metadata
       │                                   (OpenSCAD CLI)                  │
       │                                         │                  output/current_design/parts.json
       │                                   3D_renderings/**                │
       │                                                      ┌────────────┼────────────┐
       └──> export_drawings.py ──> drawings/**.pdf      generate_bom  cutlist  weight_report
                                                              └────────────┼────────────┘
                                                                     bom/*.csv ──> cost_report
                                                                           └──> generate_manual.py
```

**The parts registry is the key mechanism.** Every `frame_member()` and `utility_rail()` call `echo()`s
its own metadata — part ID, profile, material, length, position, rotation, computed mass, cost key.
`render_all.py` captures OpenSCAD's stdout and parses it into `output/current_design/parts.json`, which
feeds the BOM, cut list, and weight report. This is what makes CAD changes propagate automatically
instead of requiring a human to retype numbers into spreadsheets.

Module signature concept:

```scad
frame_member(
    id       = "WALL-L-V03",
    profile  = "TUBE_1X1_125",
    material = "AL6061T6",
    length   = 42,
    position = [x, y, z],
    rotation = [0, 0, 0],
    join     = "WELDED"        // or "BOLTED" / "BONDED" — drives the 0.125" min-wall check
);
```

Do not scatter literal dimensions through the `.scad` files. Everything references config variables.
Do not write one enormous `.scad` file; use small reusable modules.

Starting parameter values, all parametric:

```
camper_lower_length   = 78     camper_body_width = 80     interior_height = 80
nose_projection       = 24     skin_thickness    = 0.050  floor_sandwich  = 3.0
utility_rail_left_count = 3    utility_rail_right_count = 3   utility_rail_front_count = 1
FRAME_SYSTEM = "HYBRID"
```

Truck interface parameters, **all flagged VERIFY ON TRUCK**: `truck_bed_length`,
`truck_bed_floor_width`, `truck_bed_rail_width`, `truck_bed_rail_height`,
`truck_tailgate_opening_width`, `truck_wheel_well_width`, `truck_wheel_well_height`,
`truck_cab_height_above_bed`, `truck_cab_to_bed_clearance`, `camper_to_cab_clearance`,
`camper_lower_tub_width`, `camper_lower_tub_height`.

Preliminary F-350 reference values to seed the model (**every one VERIFY ON TRUCK**): bed floor ~34"
above ground, bed depth / rail height ~20.4", inside bed width ~69.3" at the top, ~50.6" between wheel
wells, 6.75 ft bed length ~81.9", 8 ft bed length ~98.0", cab roof ~46" above bed floor.

Key geometric relationship to honor: the **lower tub** must fit *between* the bed rails (≈68" max
width), while the **body** widens to 80" and sits above bed-rail height. The same camper must fit both
a ~6.5 ft and an 8 ft bed; unused bed length on the 8 ft truck is acceptable.

---

## 7. PART IDENTIFICATION

Grammar: `SYSTEM-LOCATION-NUMBER`. Define it once in `cad/config/part_ids.md` and enforce it in
`validate_model.py`, which must fail the build on a duplicate or malformed ID.

```
FLR-L-001  FLR-R-001  FLR-X-001        floor longitudinal / rail / crossmember
WALL-L-V01  WALL-L-H01                 wall vertical / horizontal
ROOF-X-01   NOSE-L-01
UTIL-L-01  UTIL-R-02                   owner accessory T-slot rails
JACK-LF-01  JACK-RF-01  JACK-LR-01  JACK-RR-01
SKIN-L-01  SKIN-R-01  SKIN-ROOF-01
```

The same ID must appear in CAD, drawings, BOM, cut list, renderings, manual, cost report, and weight
report. Keep **PRIMARY STRUCTURAL FRAME** and **OWNER ACCESSORY T-SLOT RAIL** clearly distinguished;
a member may serve both roles only deliberately and only with a note.

---

## 8. ENGINEERING STATUS SYSTEM

Every important structural assumption carries exactly one status:

`CONCEPT` · `CALCULATED` · `MANUFACTURER VERIFIED` · `PHYSICALLY TESTED` ·
`PROFESSIONALLY REVIEWED` · `NEEDS REVIEW`

At v0.1 nearly everything is `CONCEPT` or `VERIFY ON TRUCK`. `validate_model.py` must refuse to accept a
`CALCULATED` status unless a corresponding file exists in `engineering/calculations/`.

**Safety-critical list** requiring particular attention as the project progresses: floor structure, jack
mounts, jack stability, tie-downs, nose cantilever, major joints, fastener shear and tension, T-slot
slip, bracket rotation, skin shear transfer, adhesive compatibility, fatigue, road vibration, truck
clearance, center of gravity, payload, rear axle loading, tire loading. **CAD appearance is not
engineering validation.** Say so in `engineering/assumptions.md`.

---

## 9. OUTPUT CONVENTIONS

**Renderings** — repeatable named cameras, consistent colors:

| Element | Color |
|---|---|
| Existing assembly | light gray |
| New frame pieces | blue |
| Brackets | orange |
| Fasteners | red |
| Skin | silver |
| Insulation | yellow |
| Adhesive / sealant | green |
| Utility T-slot rails | dark blue |
| Truck reference | transparent gray |

Standard views: rear iso, front iso, left, right, front, rear, top, bottom, interior forward, interior
rearward, frame-only, skin-only, exploded, truck installation.

**Drawings** — true engineering drawings, not pretty renders: white background, black/gray linework,
dimension arrows, inch dimensions, section and detail callouts, part IDs, title block, revision number,
scale, notes, legend. Dimensions that depend on the physical truck must be visibly tagged
**VERIFY ON TRUCK**. Eventual full set: A01, A02, F01–F02, W01–W04, R01, N01, U01–U02, J01–J02, T01,
S01–S05, E01–E02.

**Manual** — LEGO Technic / IKEA style, not a textbook. Each step gets a number, parts required,
hardware required, tools required, one large isometric image, new components highlighted, part IDs,
orientation arrows, important dimensions, a detail view if needed, and an inspection check before
continuing. Never hide five fabrication operations inside one instruction.

**Development loop:** MODEL → RENDER → INSPECT → CORRECT → DOCUMENT → COMMIT. Commit meaningful
milestones. Never overwrite known-good geometry without revision history.

---

## 10. v0.1 SCOPE AND DELIVERABLES

**Envelope solids only. No detailed structural frame.** v0.1 contains: global config architecture,
material definitions, simplified F-350 bed and cab reference in transparent gray, camper lower-tub
envelope, main body envelope, ~24" nose envelope, roof envelope with positive drainage crown, rear door
placeholder, window placeholders (2 side + optional nose), interior T-slot utility rail placeholders,
roof-rack boss placeholders, a **6'7" human reference figure**, major dimensions, and truck/camper
clearance visualization.

The nose is additional enclosed volume and future storage/desk space. **Do not engineer it to support
two sleeping adults.** A larger cab-over is a separate future structural revision.

Required files:

```
3D_renderings/exterior/01_rear_iso.png       05_front.png
3D_renderings/exterior/02_front_iso.png      06_rear.png
3D_renderings/exterior/03_left.png           07_top.png
3D_renderings/exterior/04_right.png
3D_renderings/truck_fit/01_short_bed.png     03_side_clearance.png
3D_renderings/truck_fit/02_long_bed.png      04_cab_clearance.png
3D_renderings/interior_shell/01_utility_rails.png
drawings/general_arrangement/A01_general_arrangement.pdf
drawings/dimensions/A02_major_dimensions.pdf
drawings/truck_fit/A03_truck_fit.pdf
camper_versions/minuteman_v0.1_envelope/DIMENSIONS.md
```

`DIMENSIONS.md` must list **every** major design dimension, each tagged exactly one of:
**FIXED** · **PARAMETRIC** · **PRELIMINARY** · **VERIFY ON TRUCK**.

Also produce in this pass: `truck_data/measurement_templates/f350_measurement_sheet.md` — a printable
sheet the owner takes to the truck with a tape measure, listing every VERIFY ON TRUCK dimension with
space to write the real number and a diagram reference. This is the owner's next physical action, so
make it genuinely usable.

### Suggested execution order

1. Scaffold tree, `.gitignore`, `Makefile`, `README.md`, `CLAUDE.md`, `CHANGELOG.md`; add remote; commit
   and **push** to verify auth.
2. Install OpenSCAD; create `.venv` with `reportlab`; verify CLI PNG export and 2D projection work.
3. Write `decisions/0001`–`0003` from §2.
4. Build `dimensions.json`, `materials.scad`, `profiles.scad`, `hardware.scad`, `build_variant.scad`,
   `sync_config.py`.
5. Write `truck_reference.scad`, `camper_envelope.scad`, placeholders, human reference, `main.scad`
   view switching.
6. Implement the `echo()`-based parts registry and `parts.json` capture.
7. `render_all.py` + the 12 renderings.
8. `export_drawings.py` + A01/A02/A03.
9. `generate_weight_report.py`, `generate_cost_report.py`, `generate_bom.py`,
   `generate_cutlist.py`, `validate_model.py`; seed `bom/` and `time_cost/` CSVs with the §2.4/§2.5
   first-pass numbers.
10. Write the prose docs: `product_vision/`, `engineering/`, `competitors/` (Kimbo, Four Wheel Camper,
    Alaskan, Total Composites, Scout, plus DIY builds — with source URLs and access dates),
    `truck_data/`, `time_cost/`, `business_outlook/`, `manual/` skeleton.
11. `DIMENSIONS.md` and the measurement sheet.
12. Commit, push, present, **stop**.

---

## 11. APPROVAL GATE — STOP HERE

After v0.1 is committed and pushed, present to the owner:

1. The repository tree.
2. The dimension table.
3. Exterior renderings (embedded inline).
4. The interior-shell rendering showing utility rails.
5. Short-bed truck fit.
6. Long-bed truck fit.
7. The dimensioned general arrangement drawing.
8. The list of unresolved dimensions.
9. The list of assumptions requiring physical truck measurements.

Then **wait**. Do not begin v0.2 structural frame development without explicit approval. Do not label
anything v1.0 merely because the CAD looks complete — v1.0 means a completed and validated physical
shell.

Version ladder: v0.1 envelope → v0.2 structural frame candidate → v0.3 complete shell CAD →
v0.4 prototype/fabrication candidate → v0.5 changes discovered during physical construction →
v1.0 completed and validated first shell.

---

## 12. WHAT THE FINISHED v0.1-THROUGH-v0.4 PROJECT OWES THE OWNER

Not required for the v0.1 gate, but this is the destination, so do not architect anything that makes it
harder to reach: verified envelope, truck-fit model, complete frame/floor/wall/roof/nose CAD, rear door,
window openings, bonded aluminum skin, interior T-slot rails, jack structures, tie-down structures,
waterproofing details, thermal/insulation concept with thermal bridging documented, dimensioned
drawings, exploded drawings, part IDs, three cut lists, fastener BOM, purchased-component BOM, weight
report, cost report, fabrication-time estimate, truck-fit checklist, structural-review checklist,
water-test procedure, assembly renderings, and the LEGO-style construction manual.

Plus test plans, because small tests are cheaper than a wrong camper: T-slot joint slip, T-slot joint
rotation, frame racking, frame-plus-skin racking, adhesive bonding, riveted skin, representative corner
waterproofing, roof/wall joint waterproofing, and jack attachment structure.

**The CAD model, BOM, drawings, cut list, and manual must all describe the same camper.**

---

## 13. CORE PRINCIPLE

Minuteman is not initially a finished RV. It is a durable, weatherproof, lightweight, configurable
aluminum platform. Build the shell correctly first. Leave the interior open. Provide strategically
placed T-slot infrastructure. Let the owner evolve the camper over years rather than forcing every
decision on day one.
