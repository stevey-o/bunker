"""First-pass weight and cost model. All results are (low, high) ranges with status CONCEPT.

Areas come from the envelope (common.skin_faces); coefficients from dimensions.json estimate_basis;
unit prices from time_cost/material_costs.csv; rail lengths and counts from the parts registry.
"""
import csv
import json
import math

from common import PARTS_JSON, ROOT, load_config, params, skin_faces, surface_areas, utility_rails, variant_names

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
        ("5052 skin sheet (%s sheets 4x8)" % ("%d" % n_lo if n_lo == n_hi else "%d-%d" % (n_lo, n_hi)),) + lh("skin_sheet", n_lo, n_hi) + ("area x waste / 32 ft2",),
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


def height_sensitivity(cfg, variant=None, span=4.0):
    """(lb_low, lb_high, usd_low, usd_high) per +1 in of interior_height, averaged over +/- span inches
    so a single whole-sheet step in skin count does not dominate the per-inch figure."""
    h = cfg["camper"]["interior_height"]["value"]
    out = []
    for dh in (-span, span):
        p = params(cfg, variant, {"interior_height": h + dh})
        w = weight(cfg, p)
        out.append((totals(w), totals(cost(cfg, p, w))))
    (w0, c0), (w1, c1) = out
    d = 2 * span
    return (w1[0] - w0[0]) / d, (w1[1] - w0[1]) / d, (c1[0] - c0[0]) / d, (c1[1] - c0[1]) / d


def load():
    cfg = load_config()
    return cfg, params(cfg)


# ---------------------------------------------------------------- center of gravity
def mass_items(cfg, p, loaded=False):
    """(name, mass_lb, x, z) using the MEAN of each weight range. Distributed items follow face centroids.

    CONCEPT estimate: replaces the v0.1 'floor midpoint' proxy. Replace with frame take-off in v0.2.
    """
    rows = {r[0]: (r[1] + r[2]) / 2 for r in weight(cfg, p)}
    faces = skin_faces(p)
    items = []

    def spread(name, mass, groups):
        sel = [f for f in faces if f["group"] in groups]
        tot = sum(f["area"] for f in sel)
        x = sum(f["area"] * f["cx"] for f in sel) / tot
        z = sum(f["area"] * f["cz"] for f in sel) / tot
        items.append((name, mass, x, z))

    xm = (p["camper_front_x"] + p["camper_rear_x"]) / 2
    for name, m in rows.items():
        if name.startswith("Floor"):
            items.append((name, m, xm, p["floor_sandwich"] / 2))
        elif name == "Wall frames":
            spread(name, m, ("walls",))
        elif name == "Roof frame":
            spread(name, m, ("roof",))
        elif name == "Nose frame":
            spread(name, m, ("nose",))
        elif name.startswith(("Skin", "Insulation", "Interior panel", "Hardware")):
            spread(name, m, ("walls", "roof", "nose"))
        elif name == "Rear door":
            items.append((name, m, p["camper_rear_x"], (p["door_bottom_z"] + p["door_top_z"]) / 2))
        elif name.startswith("Windows"):
            n = 2 + (1 if p["WINDOW_NOSE_ENABLED"] else 0)
            ws = 2 * (p["camper_rear_x"] + p["window_side_center_from_rear"])
            wn = p["nose_front_x"] - p["nose_top_setback"] / 2 if n == 3 else 0
            items.append((name, m, (ws + wn) / n, p["window_side_center_z"]))
        elif name.startswith("T-slot"):
            items.append((name, m, xm, p["interior_floor_z"] + 44))
    if loaded:
        b = cfg["estimate_basis"]
        r = cfg["payload_reservations"]
        items.append(("Jacks (4)", (b["jacks_lb_set"]["low"] + b["jacks_lb_set"]["high"]) / 2, xm, 40))
        pz = p["camper_front_x"] - p["wall_thickness"] - p["power_zone_from_front"] - p["power_zone_length"] / 2
        items.append(("Power zone reservation", r["power_zone_lb"]["value"], pz, p["interior_floor_z"] + 6))
        bx = p["camper_rear_x"] + sum(p["roof_rack_boss_from_rear"]) / len(p["roof_rack_boss_from_rear"])
        items.append(("Roof rack reservation", r["roof_rack_lb"]["value"], bx, p["roof_crown_z"] + 4))
        items.append(("Owner gear allowance", p["owner_gear_allowance_lb"], xm, p["interior_floor_z"] + 12))
    return items


def center_of_gravity(cfg, p, loaded=False):
    items = mass_items(cfg, p, loaded)
    m = sum(i[1] for i in items)
    return m, sum(i[1] * i[2] for i in items) / m, sum(i[1] * i[3] for i in items) / m
