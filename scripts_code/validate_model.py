"""Rule checks for MINUTEMAN. Exits non-zero on any FAIL.

Checks: part-ID grammar and uniqueness, welded min-wall (ADR 0001), tag/status vocabularies,
CALCULATED requires a calculation file, generated-file headers, and truck-fit geometry for every
truck variant.
"""
import json
import re
import sys

from common import (GENERATED_HEADER, PARTS_JSON, ROOT, STATUSES, TAGS, load_config, params, variant_names)

ID_RE = re.compile(r"^([A-Z]{2,5})-([A-Z]{1,4})-[A-Z]?[0-9]{2,3}$")
MIN_WELDED_WALL = 0.125
LEGAL_WIDTH = 102.0
results = []


def check(ok, msg):
    results.append((bool(ok), msg))


def codes(section):
    text = (ROOT / "cad" / "config" / "part_ids.md").read_text()
    block = text.split("## " + section)[1].split("\n## ")[0]
    return set(re.findall(r"`([A-Z]{1,5})`", block))


def check_parts(cfg):
    if not PARTS_JSON.exists():
        check(False, "parts.json exists (run render_all.py)")
        return
    parts = json.loads(PARTS_JSON.read_text())
    systems, locations = codes("SYSTEM codes"), codes("LOCATION codes")
    ids = [p["id"] for p in parts]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    check(not dupes, "part IDs unique%s" % (": duplicates " + ", ".join(dupes) if dupes else ""))
    bad = []
    for i in ids:
        m = ID_RE.match(i)
        if not m or m.group(1) not in systems or m.group(2) not in locations:
            bad.append(i)
    check(not bad, "part IDs match SYSTEM-LOCATION-NUMBER grammar%s" % (": " + ", ".join(bad) if bad else ""))
    weak = [p["id"] for p in parts if p["join"] == "WELDED"
            and cfg["profiles"].get(p["profile"], {}).get("wall", 0) < MIN_WELDED_WALL]
    check(not weak, "welded members have wall >= %.3f in (ADR 0001)%s" % (MIN_WELDED_WALL, ": " + ", ".join(weak) if weak else ""))
    bad_status = [p["id"] for p in parts if p["status"] not in STATUSES]
    check(not bad_status, "part statuses valid%s" % (": " + ", ".join(bad_status) if bad_status else ""))
    util_as_struct = [p["id"] for p in parts if p["id"].startswith("UTIL") and p["role"] != "OWNER ACCESSORY T-SLOT RAIL" and not p["note"]]
    check(not util_as_struct, "UTIL rails not silently used as primary structure")


def check_config(cfg):
    bad = []
    for section in ("camper", "truck"):
        bad += [k for k, v in cfg[section].items() if v.get("tag") not in TAGS]
    for vname, v in cfg["truck_variants"].items():
        bad += ["%s.%s" % (vname, k) for k, x in v.items() if isinstance(x, dict) and "value" in x and x.get("tag") not in TAGS]
    check(not bad, "every dimension carries one tag of %s%s" % ("/".join(TAGS), ": " + ", ".join(bad) if bad else ""))
    missing = [k for k, v in cfg["truck"].items() if v["tag"] == "VERIFY ON TRUCK" and not v.get("measure")]
    check(not missing, "every truck VERIFY ON TRUCK value has measuring instructions%s" % (": " + ", ".join(missing) if missing else ""))
    sts = [m.get("status") for m in cfg["materials"].values()] + [m["status"] for m in cfg["payload_reservations"].values()]
    check(all(s in STATUSES for s in sts), "material / payload statuses valid")
    for name, prof in cfg["profiles"].items():
        if prof["kind"] != "TSLOT" and prof["wall"] < MIN_WELDED_WALL:
            check("bolted" in prof.get("note", "").lower(), "%s (wall %.3f) is flagged bolted/bonded only" % (name, prof["wall"]))


def check_assumptions():
    path = ROOT / "engineering" / "assumptions.md"
    if not path.exists():
        check(False, "engineering/assumptions.md exists")
        return
    rows = [l for l in path.read_text().splitlines() if re.match(r"^\| A-\d{3} ", l)]
    check(rows, "assumptions.md has A-### rows")
    allowed = set(STATUSES) | {"VERIFY ON TRUCK"}
    calc_dir = ROOT / "engineering" / "calculations"
    for l in rows:
        cells = [c.strip() for c in l.strip("|").split("|")]
        aid, status, ref = cells[0], cells[2].strip("`* "), cells[-1]
        check(status in allowed, "%s status '%s' is a valid status" % (aid, status))
        if status == "CALCULATED":
            files = re.findall(r"engineering/calculations/[\w./-]+", ref)
            check(files and all((ROOT / f).exists() for f in files),
                  "%s is CALCULATED and cites an existing engineering/calculations/ file" % aid)


def check_generated():
    files = [ROOT / "cad" / "config" / "dimensions.scad"] + sorted((ROOT / "bom").glob("*.csv")) + sorted((ROOT / "bom").glob("*.md"))
    marker = GENERATED_HEADER.split(" by ")[0]
    bad = [str(f.relative_to(ROOT)) for f in files if f.exists() and marker not in f.read_text()[:300]]
    check(not bad, "generated files carry the GENERATED header%s" % (": " + ", ".join(bad) if bad else ""))


def check_geometry(cfg):
    """Hard checks on the DESIGN_TRUCK. Other trucks are reported by generate_fit_study.py, not enforced here."""
    from estimates import center_of_gravity
    v = cfg["build"]["DESIGN_TRUCK"]["value"]
    p = params(cfg, v)
    t = "[%s] " % v
    c2 = 2 * p["tub_side_clearance"]
    check(p["camper_lower_tub_width"] <= p["truck_tailgate_opening_width"] - c2,
          t + "tub %.1f passes tailgate opening %.1f with %.2f clearance" % (p["camper_lower_tub_width"], p["truck_tailgate_opening_width"], c2))
    check(p["camper_lower_tub_width"] <= min(p["truck_bed_inner_width_top"], p["truck_bed_floor_width"]) - c2,
          t + "tub fits between bed sides")
    check(p["tub_base_width"] <= p["truck_wheel_well_width"] - c2 + 1e-6, t + "tub base clears wheel wells laterally")
    check(p["tub_step_z"] >= p["truck_wheel_well_height"] + p["wheel_well_clearance"] - 1e-6, t + "tub step clears wheel-well height")
    check(p["camper_lower_tub_height"] > p["truck_bed_rail_height"], t + "body underside above bed rails")
    check(p["nose_bottom_z"] >= p["truck_cab_height_above_bed"] + p["camper_to_cab_clearance"] - 1e-6, t + "nose clears cab roof")
    check(p["nose_bottom_z"] > p["camper_lower_tub_height"], t + "nose underside above body underside")
    check(p["rear_overhang"] <= -p["tailgate_clearance"] + 1e-6,
          t + "camper fits the bed with the tailgate CLOSED (rear clearance %.2f in, ADR 0004)" % -p["rear_overhang"])
    m, x, _z = center_of_gravity(cfg, p, loaded=True)
    check(x - p["rear_axle_x"] >= 0, t + "loaded CG %.1f in ahead of rear axle (estimate)" % (x - p["rear_axle_x"]))
    check(p["interior_height"] >= p["human_height"] + 1, "interior height gives >= 1 in headroom over 6'7\"")
    check(p["camper_body_width"] <= LEGAL_WIDTH, "body width within %.0f in legal limit" % LEGAL_WIDTH)
    check(p["door_top_z"] <= p["ceiling_z"], "door head below ceiling")
    check(p["door_width"] + 2 * abs(p["door_offset_y"]) <= p["tub_interior_base_width"], "door fits within tub base interior width")
    zmin = p["camper_lower_tub_height"] + p["wall_thickness"]
    hs = [p["interior_floor_z"] + h for h in p["utility_rail_side_heights"][:max(p["utility_rail_left_count"], p["utility_rail_right_count"])]]
    check(all(zmin < z < p["ceiling_z"] for z in hs), "side utility rails sit on the full-width body wall")
    check(max(p["roof_rack_boss_from_rear"]) <= p["overall_length"] - p["nose_top_setback"], "roof-rack bosses on the roof")
    for name in variant_names(cfg):
        params(cfg, name)  # every variant must at least derive cleanly
    check(True, "all %d truck variants derive (fit verdicts: truck_data/fit_study.md)" % len(variant_names(cfg)))


def main():
    cfg = load_config()
    check_parts(cfg)
    check_config(cfg)
    check_assumptions()
    check_generated()
    check_geometry(cfg)
    fails = [m for ok, m in results if not ok]
    for ok, m in results:
        print("%s  %s" % ("PASS" if ok else "FAIL", m))
    print("\n%d checks, %d failed" % (len(results), len(fails)))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
