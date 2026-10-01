"""First-pass weight and cost model. All results are (low, high) ranges with status CONCEPT.

Areas come from the envelope (common.skin_faces); coefficients from dimensions.json estimate_basis;
unit prices from time_cost/material_costs.csv; rail lengths and counts from the parts registry.
"""
import csv
import json
import math

from common import PARTS_JSON, ROOT, load_config, params, skin_faces, surface_areas, utility_rails

FT2 = 144.0


def unit_prices():
    with open(ROOT / "time_cost" / "material_costs.csv") as f:
        return {r["cost_key"]: r for r in csv.DictReader(f)}


def parts():
    return json.loads(PARTS_JSON.read_text()) if PARTS_JSON.exists() else []


def weight(cfg, p):
    """Rows of (item, low_lb, high_lb, basis). Shell dry weight excludes jacks."""
    b = cfg["estimate_basis"]
    a = surface_areas(p)
    mats = cfg["materials"]
    win = 2 + (1 if p["WINDOW_NOSE_ENABLED"] else 0)

    def per_ft2(key, area_in2):
        return b[key]["low"] * area_in2 / FT2, b[key]["high"] * area_in2 / FT2

    skin_lb = a["skin_total"] * p["skin_thickness"] * mats["AL5052H32"]["density_lb_in3"]
    ins_lb = a["insulated"] * p["insulation_thickness"] * mats["XPS"]["density_lb_in3"]
    rails = utility_rails(p)
    rail_lb = sum(r["length"] for r in rails) * cfg["profiles"][p["util_profile"]]["lb_per_in"]
    rows = [
        ("Floor structure + tub",) + per_ft2("floor_lb_per_ft2", a["floor_footprint"]) + ("tub floor %.1f ft2" % (a["floor_footprint"] / FT2),),
        ("Wall frames",) + per_ft2("wall_frame_lb_per_ft2", a["walls"]) + ("wall area %.1f ft2" % (a["walls"] / FT2),),
        ("Roof frame",) + per_ft2("roof_frame_lb_per_ft2", a["roof"]) + ("roof area %.1f ft2" % (a["roof"] / FT2),),
        ("Nose frame",) + per_ft2("nose_frame_lb_per_ft2", a["nose"]) + ("nose area %.1f ft2" % (a["nose"] / FT2),),
        ("Skin 5052 %.3f\"" % p["skin_thickness"], skin_lb * b["skin_overlap_factor"]["low"],
         skin_lb * b["skin_overlap_factor"]["high"], "%.1f ft2 x t x density x laps" % (a["skin_total"] / FT2)),
        ("Insulation %.1f\" XPS" % p["insulation_thickness"], ins_lb, ins_lb, "insulated area x t x density"),
        ("Interior panel",) + per_ft2("interior_panel_lb_per_ft2", a["insulated"]) + ("insulated area",),
        ("Rear door", b["door_lb"]["low"], b["door_lb"]["high"], "purchased"),
        ("Windows (%d)" % win, win * b["window_lb_each"]["low"], win * b["window_lb_each"]["high"], "purchased"),
        ("T-slot utility rails (%d)" % len(rails), rail_lb, rail_lb, "registry length x lb/in"),
        ("Hardware + adhesive", b["hardware_adhesive_lb"]["low"], b["hardware_adhesive_lb"]["high"], "allowance"),
    ]
    return rows


def tube_lb(cfg, rows):
    """Purchased 6061 tube mass: wall/roof/nose frames plus a fraction of the floor structure."""
    frac = cfg["estimate_basis"]["floor_tube_fraction"]["value"]
    names = ("Wall frames", "Roof frame", "Nose frame")
    lo = sum(r[1] for r in rows if r[0] in names)
    hi = sum(r[2] for r in rows if r[0] in names)
    fl = [r for r in rows if r[0] == "Floor structure + tub"][0]
    return lo + frac * fl[1], hi + frac * fl[2]


def sheet_count(cfg, p):
    b = cfg["estimate_basis"]
    a = surface_areas(p)["skin_total"]
    s = b["sheet_area_in2"]["value"]
    return (math.ceil(a * b["sheet_waste_factor"]["low"] / s), math.ceil(a * b["sheet_waste_factor"]["high"] / s))


def cost(cfg, p, wrows=None):
    """Rows of (item, low_usd, high_usd, basis). Excludes jacks and tooling."""
    u = unit_prices()
    wrows = wrows or weight(cfg, p)
    a = surface_areas(p)
    n_lo, n_hi = sheet_count(cfg, p)
    f_lo, f_hi = tube_lb(cfg, wrows)
    rails_in = sum(r["length"] for r in utility_rails(p))
    win = 2 + (1 if p["WINDOW_NOSE_ENABLED"] else 0)
    bosses = 2 * len(p["roof_rack_boss_from_rear"])

    def lh(key, qlo, qhi=None):
        qhi = qlo if qhi is None else qhi
        return float(u[key]["low_usd"]) * qlo, float(u[key]["high_usd"]) * qhi

    return [
        ("5052 skin sheet (%d-%d sheets 4x8)" % (n_lo, n_hi),) + lh("skin_sheet", n_lo, n_hi) + ("area x waste / 32 ft2",),
        ("6061 tube",) + lh("tube_6061", f_lo, f_hi) + ("tube mass %.0f-%.0f lb" % (f_lo, f_hi),),
        ("T-slot utility rails",) + lh(p["util_profile"], rails_in) + ("%.0f in total" % rails_in,),
        ("Rear door",) + lh("door", 1) + ("purchased",),
        ("Windows (%d)" % win,) + lh("window", win) + ("purchased",),
        ("Roof-rack bosses (%d)" % bosses,) + lh("rack_boss", bosses) + ("provision",),
        ("Insulation",) + lh("insulation", a["insulated"] / FT2) + ("%.0f ft2" % (a["insulated"] / FT2),),
        ("Interior panel",) + lh("interior_panel", a["insulated"] / FT2) + ("%.0f ft2" % (a["insulated"] / FT2),),
        ("Adhesive + sealant",) + lh("adhesive", 1) + ("lot",),
        ("Fasteners + rivets",) + lh("fasteners", 1) + ("lot",),
        ("Welding consumables + gas",) + lh("welding_consumables", 1) + ("lot",),
    ]


def totals(rows):
    return sum(r[1] for r in rows), sum(r[2] for r in rows)


def height_sensitivity(cfg, variant="SHORT"):
    """(lb_low, lb_high, usd_low, usd_high) per +1 in of interior_height."""
    p0 = params(cfg, variant)
    p1 = params(cfg, variant, {"interior_height": p0["interior_height"] + 1})
    w0, w1 = weight(cfg, p0), weight(cfg, p1)
    c0, c1 = cost(cfg, p0, w0), cost(cfg, p1, w1)
    tw0, tw1, tc0, tc1 = totals(w0), totals(w1), totals(c0), totals(c1)
    return tw1[0] - tw0[0], tw1[1] - tw0[1], tc1[0] - tc0[0], tc1[1] - tc0[1]


def load():
    cfg = load_config()
    return cfg, params(cfg)
