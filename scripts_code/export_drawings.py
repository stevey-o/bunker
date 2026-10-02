"""Export the MINUTEMAN drawing set (ANSI C, ASME Y14 conventions; see drawlib.py) as PDFs.

A01 general arrangement · A02 major dimensions · A03 interior sections · A04 truck fit (2011 F-350)
· A05 multi-truck fit study. Geometry comes from OpenSCAD projections; values from common.params();
CG and fit verdicts from estimates.py / generate_fit_study.py. Nothing is typed in twice.
"""
import json

from common import PARTS_JSON, ROOT, load_config, params
from drawlib import (CENTER, GRAY, HIDDEN, IN, LIGHT, PHANTOM, RED, THIN, VISIBLE, Sheet, View, axle_mark,
                     callout, cg_symbol, dim_h, dim_v, fmt, projection, section_arrows, view_title)
from generate_fit_study import evaluate

DWG = ROOT / "drawings"
CAMPER = ["tub_lower", "tub_upper", "body_lower", "body_upper"]
N_SHEETS = 5
REVISIONS = [
    ("A", "V0.1 ENVELOPE - INITIAL RELEASE FOR OWNER REVIEW", "2026-10-01", "-"),
    ("B", "97 IN FULL-LENGTH (ADR 0004), 2011 F-350 DATA, TUB 59.5, ASME Y14 FORMAT, ADD A03-A05", "2026-10-01", "-"),
]
VOT = "<1> VERIFY ON TRUCK: VALUE DEPENDS ON THE PHYSICAL TRUCK. CONFIRM WITH TRUCK_DATA/MEASUREMENT_TEMPLATES/F350_MEASUREMENT_SHEET.PDF."
EST = "<2> ESTIMATE (STATUS CONCEPT): FIRST-PASS WEIGHT / CG MODEL, SCRIPTS_CODE/ESTIMATES.PY. NOT AN ENGINEERING CALCULATION."
DESIGN = "F350_LONG"
VISIBLE_FROM = {"side": ("door", "win_side", "win_nose", "bosses"), "top": ("bosses",),
                "rear": ("door", "bosses"), "front": ("win_nose", "bosses")}


def camper(view, plane, facing=None, line=VISIBLE):
    for part in CAMPER:
        view.polys(projection(part, plane), line)
    for part in VISIBLE_FROM[facing or plane]:
        view.polys(projection(part, plane), THIN)


def truck(view, plane, variant, human=True):
    for part in ("truck_bed", "truck_cab", "truck_wheels", "truck_tailgate"):
        view.polys(projection(part, plane, variant), PHANTOM, GRAY)
    if human:
        view.polys(projection("human_ground", plane, variant), THIN, LIGHT)


def sheet(cfg, path, no, title, scale):
    return Sheet(DWG / path, "MM-A%02d" % no, title, scale, cfg, no, N_SHEETS, REVISIONS)


# ================================================================ A01
def a01(cfg, p):
    s = sheet(cfg, "general_arrangement/A01_general_arrangement.pdf", 1, "GENERAL ARRANGEMENT", "1:16")
    k = 16
    xr, xf, xn = p["camper_rear_x"], p["camper_front_x"], p["nose_front_x"]
    ox = 1.2 * IN + xn * IN / k
    plan = View(s, ox, 12.2 * IN, k, fu=-1, fv=-1)
    camper(plan, "top")
    plan.polys(projection("rails", "top"), HIDDEN)
    plan.line((xn + 3, 0), (xr - 3, 0), CENTER)
    view_title(s, 5.0 * IN, 9.45 * IN, "PLAN (TOP)", "SCALE 1:16   FRONT TO LEFT")
    yb = p["camper_body_width"] / 2 - p["roof_rack_boss_edge_inset"]
    callout(plan, (xr + p["roof_rack_boss_from_rear"][0], -yb), 40, 30, "RACK-ROOF-01..06\nROOF-RACK BOSS (6)")
    callout(plan, (xr + 10, p["body_interior_width"] / 2 - .5), 46, -24, "UTIL-L-01..03 (HIDDEN)")
    callout(plan, (xr + 30, -p["body_interior_width"] / 2 + .5), 46, 52, "UTIL-R-01..03 (HIDDEN)")
    callout(plan, (xf - 2.3, -25), -70, 60, "UTIL-F-01 (HIDDEN)")
    section_arrows(plan, (xn + 4, 3), (xr - 4, 3), "B", (0, -1))
    section_arrows(plan, (xn + 4, -3), (xr - 4, -3), "C", (0, 1))

    z0 = 3.45 * IN
    side = View(s, ox, z0, k, fu=-1)
    camper(side, "side")
    side.polys(projection("rails", "side"), HIDDEN)
    view_title(s, 5.0 * IN, 3.0 * IN, "LEFT ELEVATION", "SCALE 1:16   FRONT TO LEFT")
    callout(side, (xn - 4, 62), 40, 50, "ENV-NOSE-01  NOSE (STORAGE / DESK ONLY)")
    callout(side, (xr + 70, 34), 30, -24, "ENV-BODY-01")
    callout(side, (xr + 60, 6), 50, -26, "ENV-TUB-01")
    callout(side, (xr + 20, p["roof_crown_z"]), 30, 24, "ENV-ROOF-01  .75 CROWN")
    callout(side, (xr + p["window_side_center_from_rear"], p["window_side_center_z"]), 40, 40, "WIN-L-01")
    callout(side, (xr + 40, p["interior_floor_z"] + 44), -60, 50, "UTIL-L-02 (HIDDEN)")

    rear = View(s, 11.6 * IN, z0, k, fu=-1)
    camper(rear, "front", facing="rear")
    view_title(s, 11.6 * IN, 3.0 * IN, "REAR ELEVATION", "SCALE 1:16")
    callout(rear, (0, p["door_bottom_z"] + 40), 60, 10, "DOOR-B-01\nREAR ENTRY DOOR")
    front = View(s, 17.4 * IN, z0, k)
    camper(front, "front", facing="front")
    view_title(s, 17.4 * IN, 3.0 * IN, "FRONT ELEVATION", "SCALE 1:16")
    callout(front, (0, (p["nose_bottom_z"] + p["roof_eave_z"]) / 2), 60, 40, "WIN-N-01 (OPTIONAL)")

    parts = json.loads(PARTS_JSON.read_text())
    s.table(10.4 * IN, 15.1 * IN, ["ITEM", "PART ID", "DESCRIPTION"],
            [[str(i + 1), x["id"], x["role"][:34]] for i, x in enumerate(parts)],
            [0.45 * IN, 1.15 * IN, 2.55 * IN], size=6.5, title="PARTS LIST (FROM CAD REGISTRY)", row_h=10.5)
    s.notes(14.85 * IN, s.rev_bottom - 22, [
        "V0.1 IS AN ENVELOPE ONLY: OUTER SKIN SURFACES. NO STRUCTURAL FRAME IS SHOWN OR IMPLIED.",
        "PART IDS FOLLOW SYSTEM-LOCATION-NUMBER (CAD/CONFIG/PART_IDS.MD) AND MATCH BOM, RENDERS AND MANUAL.",
        "HIDDEN LINES: OWNER ACCESSORY T-SLOT RAILS ON INTERIOR WALL FACES. NOT PRIMARY STRUCTURE.",
        "RACK-ROOF BOSSES ARE STRUCTURAL PROVISIONS; EACH MUST LAND ON A ROOF CROSSMEMBER (V0.2).",
        "DOOR AND WINDOWS ARE ROUGH-OPENING PLACEHOLDERS FOR PURCHASED COMPONENTS. WIN-R-01 MIRRORS WIN-L-01.",
        "NOSE IS STORAGE / DESK VOLUME ONLY; NOT ENGINEERED AS A SLEEPING PLATFORM.",
        "DIMENSIONS: SEE MM-A02. INTERIOR SECTIONS B-B, C-C: MM-A03. TRUCK FIT: MM-A04, MM-A05.",
        VOT,
    ], width=6.6 * IN)
    s.save()


# ================================================================ A02
def a02(cfg, p):
    s = sheet(cfg, "dimensions/A02_major_dimensions.pdf", 2, "MAJOR DIMENSIONS", "1:14")
    k = 14
    z0 = 4.4 * IN
    xr, xf, xn = p["camper_rear_x"], p["camper_front_x"], p["nose_front_x"]
    zc, ze, zn = p["roof_crown_z"], p["roof_eave_z"], p["nose_bottom_z"]
    xt = xn - p["nose_top_setback"]
    side = View(s, 2.6 * IN + xn * IN / k, z0, k, fu=-1)
    camper(side, "side")
    side.polys(projection("human_inside", "side"), THIN, LIGHT)
    view_title(s, 6.9 * IN, 3.55 * IN, "LEFT ELEVATION", "SCALE 1:14   FRONT TO LEFT   6'7\" FIGURE FOR SCALE")
    dim_h(side, (xn, zn), (xr, 0), zc + 16, text="%s OVERALL" % fmt(p["overall_length"]))
    dim_h(side, (xn, zn), (xf, zn), zc + 8)
    dim_h(side, (xf, ze), (xr, ze), zc + 8, text="%s  FILLS 8 FT BED" % fmt(p["camper_lower_length"]))
    dim_h(side, (xn, zn), (xt, ze), zn - 7, text="%s RAKE" % fmt(p["nose_top_setback"]))
    ur = xr - 6
    chain = [0, p["interior_floor_z"], p["tub_step_z"], p["camper_lower_tub_height"]]
    for i, fl in enumerate([None, 1, 1]):
        dim_v(side, (xr, chain[i]), (xr, chain[i + 1]), ur, flag_no=fl)
    dim_v(side, (xr, p["interior_floor_z"]), (xr, p["ceiling_z"]), ur - 13, text="%s INTERIOR" % fmt(p["interior_height"]))
    dim_v(side, (xr, p["ceiling_z"]), (xr, ze), ur - 13)
    dim_v(side, (xr, 0), (xr, zc), ur - 27, text="%s OVERALL" % fmt(zc))
    uf = xn + 6
    dim_v(side, (xf, 0), (xf, zn), uf + 6, flag_no=1)
    dim_v(side, (xn, zn), (xn, ze), uf)
    dim_v(side, (xn, zn), (xn, p["nose_floor_z"]), uf + 16)

    rear = View(s, 17.2 * IN, z0, k, fu=-1)
    camper(rear, "front", facing="rear")
    view_title(s, 17.2 * IN, 3.25 * IN, "REAR ELEVATION", "SCALE 1:14")
    W, tw, tb = p["camper_body_width"], p["camper_lower_tub_width"], p["tub_base_width"]
    dim_h(rear, (W / 2, ze), (-W / 2, ze), zc + 7)
    dim_h(rear, (tw / 2, p["tub_step_z"]), (-tw / 2, p["tub_step_z"]), -4, flag_no=1)
    dim_h(rear, (tb / 2, 0), (-tb / 2, 0), -10, flag_no=1)
    dy, dw = p["door_offset_y"], p["door_width"]
    dim_h(rear, (dy + dw / 2, p["door_top_z"]), (dy - dw / 2, p["door_top_z"]), p["door_top_z"] + 5)
    dim_v(rear, (dy - dw / 2, p["door_bottom_z"]), (dy - dw / 2, p["door_top_z"]), -W / 2 + 7)
    dim_v(rear, (-W / 2, 0), (-W / 2, p["door_bottom_z"]), -W / 2 - 5)
    dim_v(rear, (-W / 2, p["camper_lower_tub_height"]), (-W / 2, ze), -W / 2 - 5)
    dim_v(rear, (-W / 2, 0), (-W / 2, p["camper_lower_tub_height"]), -W / 2 - 12, flag_no=1)

    gc = p["ground_to_crown"]
    rows = [["INTERIOR CLEAR HEIGHT", fmt(p["interior_height"]), "FIXED"],
            ["OVERALL LENGTH / LOWER LENGTH", "%s / %s" % (fmt(p["overall_length"]), fmt(p["camper_lower_length"])), "FIXED"],
            ["BODY WIDTH", fmt(W), "PARAMETRIC"],
            ["TUB WIDTH / TUB BASE WIDTH", "%s / %s" % (fmt(tw), fmt(tb)), "VERIFY ON TRUCK"],
            ["INTERIOR FLOOR WIDTH (TUB BASE)", fmt(p["tub_interior_base_width"]), "VERIFY ON TRUCK"],
            ["INTERIOR WIDTH ABOVE RAILS", fmt(p["body_interior_width"]), "PRELIMINARY"],
            ["NOSE INTERIOR HEIGHT / PROJECTION", "%s / %s" % (fmt(p["nose_interior_height"]), fmt(p["nose_projection"])), "VERIFY ON TRUCK"],
            ["GROUND TO CROWN ON 2011 F-350 4X4", "%s (%d FT %s IN)" % (fmt(gc), gc // 12, fmt(gc % 12)), "VERIFY ON TRUCK"]]
    s.table(1.0 * IN, 15.6 * IN, ["DIMENSION", "VALUE (IN)", "TAG"], rows, [3.1 * IN, 1.6 * IN, 1.4 * IN],
            size=7, title="PRINCIPAL DIMENSIONS")
    s.table(8.0 * IN, 15.6 * IN, ["TAG", "MEANING"],
            [["FIXED", "OWNER REQUIREMENT; CHANGE ONLY BY DECISION RECORD"],
             ["PARAMETRIC", "DESIGN VARIABLE IN DIMENSIONS.JSON"],
             ["PRELIMINARY", "PLACEHOLDER, EXPECTED TO CHANGE (V0.2/V0.3)"],
             ["VERIFY ON TRUCK", "DEPENDS ON THE PHYSICAL TRUCK, FLAG NOTE 1"]],
            [1.3 * IN, 3.9 * IN], size=7, title="DIMENSION TAGS (FULL LIST: DIMENSIONS.MD)")
    s.notes(1.0 * IN, 2.85 * IN, [
        VOT,
        "ORIGIN: BED-FLOOR TOP, TRUCK CENTERLINE, INNER FACE OF BED FRONT WALL. CAMPER FRONT FACE %s AFT; REAR FACE %s AHEAD OF CLOSED TAILGATE (8 FT BED)." % (
            fmt(p["camper_front_gap"]), fmt(p["tailgate_clearance"])),
        "INTERIOR HEIGHT %s IS AN OWNER REQUIREMENT (6'7\" STANDING, ADR 0002). HEADROOM OVER FIGURE %s." % (
            fmt(p["interior_height"]), fmt(p["headroom_6ft7"])),
    ], width=12.2 * IN)
    s.save()


# ================================================================ A03
def a03(cfg, p):
    s = sheet(cfg, "interior/A03_interior_sections.pdf", 3, "INTERIOR SECTIONS AND PROVISIONS", "1:18")
    k = 18
    xr, xf, xn = p["camper_rear_x"], p["camper_front_x"], p["nose_front_x"]
    fz, cz, ze = p["interior_floor_z"], p["ceiling_z"], p["roof_eave_z"]
    wt = p["wall_thickness"]
    xs = round((xr + xf) / 2, 1)  # section station D-D / E-E
    hs = p["utility_rail_side_heights"]
    pz_x1 = xf - wt - p["power_zone_from_front"]

    for title, z0, fu, ox, rails, side_sign, yv in (
            ("SECTION B-B  LEFT WALL, LOOKING LEFT", 9.75 * IN, 1, 2.7 * IN - xr * IN / k, "rails_L", "L", 9.3 * IN),
            ("SECTION C-C  RIGHT WALL, LOOKING RIGHT", 3.45 * IN, -1, 2.7 * IN + xn * IN / k, "rails_R", "R", 3.0 * IN)):
        v = View(s, ox, z0, k, fu=fu)
        v.polys(projection("shell", "ysection"), VISIBLE)
        v.polys(projection(rails, "side"), THIN)
        v.polys(projection("win_side", "side"), THIN)
        v.polys(projection("power_zone", "side"), THIN)
        v.polys(projection("rails_F", "side"), THIN)
        if side_sign == "L":
            v.polys(projection("wire_chase", "side"), HIDDEN)
            v.polys(projection("human_inside", "side"), THIN, LIGHT)
            section_arrows(v, (xs, -6), (xs, ze + 4), "D", (1, 0))
            section_arrows(v, (xs - 20, -6), (xs - 20, ze + 4), "E", (-1, 0))
        view_title(s, 6.1 * IN, yv - 0.1 * IN, title, "SCALE 1:18   FRONT TO %s" % ("RIGHT" if fu > 0 else "LEFT"))
        ur = xr - 6
        chain = [fz] + [fz + h for h in hs] + [cz]
        for a, b in zip(chain, chain[1:]):
            dim_v(v, (xr + wt, a), (xr + wt, b), ur)
        dim_v(v, (xr + wt, fz), (xr + wt, cz), ur - 13, text="%s STANDING" % fmt(p["interior_height"]))
        dim_h(v, (xr + wt, cz), (xf - wt, cz), ze + 7, text="%s INTERIOR" % fmt(p["interior_length"]))
        dim_h(v, (xf - wt, cz), (xn - wt, cz), ze + 7, ref=True)
        dim_v(v, (xn - wt, p["nose_floor_z"]), (xn - wt, cz), xn + 5, flag_no=1)
        dim_v(v, (xf - wt, fz), (xf - wt, p["nose_floor_z"]), xn + 14, flag_no=1)
        sgn = 1 if fu > 0 else -1
        callout(v, (xr + 30, fz + hs[2]), 30 * sgn, 26, "UTIL-%s-03  T-SLOT RAIL\n(OWNER ACCESSORY, TYP 3)" % side_sign)
        callout(v, (xr + p["window_side_center_from_rear"], p["window_side_center_z"]), 70 * sgn, 0,
                "WIN-%s-01  SIDE WINDOW %sx%s" % (side_sign, fmt(p["window_side_width"]), fmt(p["window_side_height"])))
        callout(v, (pz_x1 - p["power_zone_length"] / 2, fz + .2), -40 * sgn, 30,
                "POWER ZONE %sx%s\n150 LB RESERVED, TIE-DOWN FLOOR" % (fmt(p["power_zone_length"]), fmt(p["power_zone_width"])))
        callout(v, (xn - 10, p["nose_floor_z"] + 12), 20 * sgn, 52, "NOSE STORAGE / DESK\n(NOT A SLEEPING PLATFORM)")
        callout(v, (xf - wt - 1.2, fz + p["utility_rail_front_height"]), 16 * sgn, -46, "UTIL-F-01 (BEYOND)")
        callout(v, (xr + 2, fz + 10), 30 * sgn, -26, "REAR WALL / DOOR-B-01 (SEE E-E)")
        if side_sign == "L":
            callout(v, (xf - wt - 1.5, fz + 56), -70, -44, "WIRE CHASE %sx%s\n(RESERVED, NO WIRING)" % (fmt(p["wire_chase_size"]), fmt(p["wire_chase_size"])))
            callout(v, (xr + 0.4 * p["camper_lower_length"] - 4, fz + 74), -40, 24, "6'7\" FIGURE, %s HEADROOM" % fmt(p["headroom_6ft7"]))

    for title, cx, fu, look, st in (("SECTION D-D  LOOKING FORWARD", 13.4 * IN, -1, "fwd", xs),
                                    ("SECTION E-E  LOOKING AFT", 18.5 * IN, 1, "aft", xs - 20)):
        v = View(s, cx, 8.4 * IN, k, fu=fu)
        v.polys(projection("shell", "xsection", cut_x=st), VISIBLE)
        v.polys(projection("rails", "xsection", cut_x=st), VISIBLE)
        if look == "aft":
            v.polys(projection("door", "front"), HIDDEN)
            callout(v, (0, p["door_bottom_z"] + 30), 70, -30, "DOOR-B-01 ROUGH OPENING\n%sx%s (BEYOND, HIDDEN)" % (fmt(p["door_width"]), fmt(p["door_height"])))
        else:
            for it in ("rails_F", "power_zone", "wire_chase"):
                v.polys(projection(it, "front"), THIN)
            callout(v, (0, fz + .2), 60, -26, "POWER ZONE (BEYOND)")
            callout(v, (p["camper_body_width"] / 2 - wt - 1.5, fz + 50), -40, 60, "WIRE CHASE (BEYOND)")
        view_title(s, cx, 7.35 * IN, title, "SCALE 1:18   AT X = %s" % fmt(st))
        W, bi, ti = p["camper_body_width"], p["body_interior_width"], p["tub_interior_base_width"]
        dim_h(v, (bi / 2, cz), (-bi / 2, cz), ze + 6, text="%s INTERIOR" % fmt(bi))
        dim_h(v, (ti / 2, fz), (-ti / 2, fz), -6, flag_no=1, text="%s FLOOR" % fmt(ti))
        dim_v(v, (-bi / 2, fz), (-bi / 2, cz), -W / 2 - 6, text=fmt(p["interior_height"]))
        callout(v, (bi / 2 - .5, fz + hs[1]), -40 * fu, 30, "UTIL-L-02")
    s.notes(11.2 * IN, 6.6 * IN, [
        "SHELL ONLY. NO FURNITURE, BED, KITCHEN, WATER OR ELECTRICAL SYSTEMS ARE PART OF THIS DESIGN; THE INTERIOR IS LEFT OPEN FOR THE OWNER.",
        "SECTIONS SHOW THE INTERIOR SURFACE ENVELOPE AT PRELIMINARY WALL %s, FLOOR %s, ROOF %s THICKNESS." % (
            fmt(wt), fmt(p["floor_sandwich"]), fmt(p["roof_thickness"])),
        "T-SLOT RAIL HEIGHTS ABOVE FLOOR: %s. RAILS BOLT INTO FRAME MEMBERS (V0.2), NEVER SKIN ONLY." % ", ".join(fmt(h) for h in hs),
        "POWER ZONE AND WIRE CHASE ARE RESERVED GEOMETRY (ADR 0003): STRUCTURE ONLY, NO ELECTRICAL DESIGN.",
        VOT,
    ], width=10.0 * IN, size=7)
    s.save()


# ================================================================ A04 / A05 helpers
def truck_elevation(s, cfg, v, front_paper_x, ground_paper_y, k):
    pp = params(cfg, v)
    g = -pp["truck_bed_floor_height"]
    front_x = pp["rear_axle_x"] + pp["truck_wheelbase"] + pp["truck_front_overhang"]
    view = View(s, front_paper_x + front_x * IN / k, ground_paper_y - g * IN / k, k, fu=-1)
    truck(view, "side", v)
    camper(view, "side")
    view.line((front_x + 10, g), (pp["camper_rear_x"] - 45, g), THIN)
    r = evaluate(cfg, v)
    axle_mark(view, pp["rear_axle_x"], pp["roof_crown_z"] + 10, g)
    cg_symbol(view, r["x_load"], r["z_load"], "CG")
    return view, pp, r, g


# ================================================================ A04
def a04(cfg, p):
    s = sheet(cfg, "truck_fit/A04_truck_fit_f350.pdf", 4, "TRUCK FIT - 2011 F-350", "AS NOTED")
    k = 30
    for v, gy, ttl in ((DESIGN, 11.25 * IN, "2011 F-350 CREW CAB 4X4, 8 FT BOX - TAILGATE CLOSED (DESIGN TRUCK)"),
                       ("F350_SHORT", 4.75 * IN, "2011 F-350 CREW CAB 4X4, 6.75 FT BOX - TAILGATE DOWN")):
        view, pp, r, g = truck_elevation(s, cfg, v, 1.0 * IN, gy, k)
        xr = pp["camper_rear_x"]
        view_title(s, 6.0 * IN, gy - 0.95 * IN, ttl, "SCALE 1:30   LEFT ELEVATION")
        dim_v(view, (xr, g), (xr, pp["roof_crown_z"]), xr - 48, flag_no=1, text="%s TRAVEL HT" % fmt(pp["ground_to_crown"]))
        dim_v(view, (xr, g), (xr, 0), xr - 10, flag_no=1)
        dim_h(view, (pp["rear_axle_x"], g), (r["x_load"], g), g - 9, flag_no=2,
              text="CG %s %s AXLE" % (fmt(abs(r["cg_ahead"]), 1), "AHEAD OF" if r["cg_ahead"] >= 0 else "BEHIND"))
        if pp["rear_overhang"] > 0:
            dim_h(view, (pp["tailgate_x"], 0), (xr, 0), g - 18, flag_no=1, text="%s OVERHANG PAST BED" % fmt(pp["rear_overhang"]))
            callout(view, (xr + 4, 2), 40, -64, "TAILGATE DOWN: NOT STRUCTURAL.\nCAMPER MUST NOT BEAR ON IT.")
        else:
            dim_h(view, (pp["tailgate_x"], 0), (xr, 0), g - 18, flag_no=1, text="%s TO CLOSED TAILGATE" % fmt(-pp["rear_overhang"]))
        if r["cg_ahead"] < 0:
            s.text(1.1 * IN, gy + 4.35 * IN, "NOT RECOMMENDED: LOADED CG BEHIND REAR AXLE", 10, True, color=RED)
            s.text(1.1 * IN, gy + 4.17 * IN, "SEE NOTE 3 AND TRUCK_DATA/FIT_STUDY.MD", 8, color=RED)
    pd = params(cfg, DESIGN)
    sec = View(s, 16.4 * IN, 11.6 * IN, 16, fu=-1)
    cx = pd["rear_axle_x"]
    sec.clip((48, -22), (-48, 40))
    sec.polys(projection("truck_bed", "xsection", DESIGN, cx), PHANTOM, GRAY)
    sec.polys(projection("truck_wheels", "xsection", DESIGN, cx), PHANTOM, GRAY)
    sec.polys(projection("envelope", "xsection", DESIGN, cx), VISIBLE)
    s.c.restoreState()
    view_title(s, 16.4 * IN, 10.05 * IN, "SECTION A-A AT REAR AXLE (8 FT BOX)", "SCALE 1:16   LOOKING FORWARD")
    wi, ww = pd["truck_bed_inner_width_top"], pd["truck_wheel_well_width"]
    dim_h(sec, (wi / 2, pd["truck_bed_rail_height"]), (-wi / 2, pd["truck_bed_rail_height"]), 37, flag_no=1)
    dim_h(sec, (pd["camper_lower_tub_width"] / 2, pd["tub_step_z"]), (-pd["camper_lower_tub_width"] / 2, pd["tub_step_z"]), 30, flag_no=1)
    dim_h(sec, (ww / 2, pd["truck_wheel_well_height"]), (-ww / 2, pd["truck_wheel_well_height"]), -7, flag_no=1)
    dim_h(sec, (pd["tub_base_width"] / 2, 0), (-pd["tub_base_width"] / 2, 0), -15, flag_no=1)
    dim_v(sec, (-wi / 2, 0), (-wi / 2, pd["truck_bed_rail_height"]), -wi / 2 - 6, flag_no=1)
    det = View(s, 14.5 * IN, 0.55 * IN, 12, fu=-1)
    x0, y0, w, h = det.clip((34, 33), (-12, 92))
    det.polys(projection("truck_cab", "side", DESIGN), PHANTOM, GRAY)
    det.polys(projection("truck_bed", "side", DESIGN), PHANTOM, GRAY)
    camper(det, "side")
    s.c.restoreState()
    s.c.setLineWidth(0.5); s.c.setStrokeColor(GRAY); s.c.setDash([], 0); s.c.rect(x0, y0, w, h)
    view_title(s, x0 + w / 2, y0 - 16, "DETAIL B - NOSE OVER CAB", "SCALE 1:12")
    dim_v(det, (pd["cab_back_x"] + 6, pd["truck_cab_height_above_bed"]), (pd["cab_back_x"] + 6, pd["nose_bottom_z"]), 28, flag_no=1)
    dim_h(det, (pd["camper_front_x"], 39), (pd["cab_back_x"], 39), 36, flag_no=1)
    dim_h(det, (pd["cab_back_x"], pd["nose_bottom_z"]), (pd["nose_front_x"], pd["nose_bottom_z"]), 64, flag_no=1,
          text="%s OVER CAB" % fmt(pd["nose_over_cab"]))
    rows = []
    for v in (DESIGN, "F350_SHORT"):
        r = evaluate(cfg, v)
        rows.append([v, r["verdict"], "%.0f / %.0f" % (r["m_dry"], r["m_load"]),
                     "%+.1f" % r["cg_ahead"], "%d-%d" % (r["rating"]["low"], r["rating"]["high"])])
    s.table(16.3 * IN, 8.6 * IN, ["TRUCK", "VERDICT", "DRY/LOADED LB", "CG VS AXLE", "CAMPER CARGO RTG"], rows,
            [1.0 * IN, 0.95 * IN, 1.1 * IN, 0.8 * IN, 1.25 * IN], size=7, title="WEIGHT AND CG (FLAG NOTE 2)")
    s.notes(16.3 * IN, 7.45 * IN, [
        VOT, EST,
        "CAMPER CG MUST BE AT OR AHEAD OF THE REAR AXLE (FORD: CG DATA ON THE TRUCK'S CONSUMER INFORMATION SHEET). ON THE 6.75 FT BOX THE 97 IN CAMPER PUTS THE LOADED CG BEHIND THE AXLE: NOT RECOMMENDED.",
        "CAMPER CARGO RATING FROM FORD 2011 RV & TRAILER TOWING GUIDE (CAMPER PKG 471 REQUIRED); RANGE IS BY ENGINE. USE THE DOOR-JAMB STICKER.",
        "TRUCK SHOWN IN PHANTOM IS A SIMPLIFIED REFERENCE. TAILGATE IS NEVER A STRUCTURAL SUPPORT.",
    ], width=5.2 * IN, size=7)
    s.save()


# ================================================================ A05
def a05(cfg, p):
    s = sheet(cfg, "truck_fit/A05_multi_truck_fit.pdf", 5, "MULTI-TRUCK FIT STUDY", "AS NOTED")
    k = 40
    grid = [("F150_65", 1.0, 11.6), ("F150_55", 8.0, 11.6), ("TACOMA_6", 1.0, 6.8), ("TACOMA_5", 8.0, 6.8)]
    for v, fx, gy in grid:
        view, pp, r, g = truck_elevation(s, cfg, v, fx * IN, gy * IN, k)
        lbl = cfg["truck_variants"][v]["label"].replace(" (half-ton representative)", "")
        view_title(s, (fx + 3.2) * IN, (gy - 0.75) * IN, lbl[:52], "SCALE 1:40   VERDICT: %s" % r["verdict"])
        xr = pp["camper_rear_x"]
        dim_h(view, (pp["tailgate_x"], 0), (xr, 0), g - 10, text="%s OVERHANG" % fmt(pp["rear_overhang"]))
        x, y = (fx + 0.1) * IN, view.P(0, pp["roof_crown_z"] + 4)[1]
        s.text(x, y, "%s  CG %+.1f VS AXLE  %.0f LB LOADED" % (r["verdict"], r["cg_ahead"], r["m_load"]), 8, True,
               color=RED if r["verdict"] == "FAIL" else black_())
    pt = params(cfg, "TACOMA_6")
    sec = View(s, 18.4 * IN, 11.9 * IN, 20, fu=-1)
    sec.clip((46, -18), (-46, 40))
    sec.polys(projection("truck_bed", "xsection", "TACOMA_6", pt["rear_axle_x"]), PHANTOM, GRAY)
    sec.polys(projection("envelope", "xsection", "TACOMA_6", pt["rear_axle_x"]), VISIBLE)
    s.c.restoreState()
    view_title(s, 18.4 * IN, 10.85 * IN, "SECTION AT REAR AXLE - TACOMA (2016-23)", "SCALE 1:20   LOOKING FORWARD")
    dim_h(sec, (pt["truck_wheel_well_width"] / 2, pt["truck_wheel_well_height"]),
          (-pt["truck_wheel_well_width"] / 2, pt["truck_wheel_well_height"]), -8, text="%s WELLS" % fmt(pt["truck_wheel_well_width"]))
    dim_h(sec, (pt["tub_base_width"] / 2, 0), (-pt["tub_base_width"] / 2, 0), -15, text="%s TUB BASE" % fmt(pt["tub_base_width"]))
    callout(sec, (-pt["truck_wheel_well_width"] / 2, 5), -30, 40, "INTERFERENCE")
    res = [evaluate(cfg, v) for v in cfg["truck_variants"]]
    short = ["WHEEL WELLS", "WELL TOP", "TAILGATE OPEN.", "BED SIDES", "RAILS", "CAB", "OVERHANG", "CG VS AXLE", "PAYLOAD"]
    rows = [[r["variant"], r["verdict"]] + [x[2] for x in r["rows"]] for r in res]
    s.table(1.0 * IN, 4.95 * IN, ["TRUCK", "VERDICT"] + short, rows,
            [1.05 * IN, 1.05 * IN] + [0.97 * IN] * len(short), size=6.8, title="FIT MATRIX (DETAIL: TRUCK_DATA/FIT_STUDY.MD)")
    s.notes(15.4 * IN, 9.6 * IN, [
        "ONE CAMPER, SIZED TO THE 2011 F-350 8 FT BOX, IS CHECKED AGAINST EACH TRUCK. IT DOES NOT CHANGE SHAPE PER TRUCK.",
        "HALF-TON AND TACOMA VALUES ARE PUBLISHED BED DIMENSIONS PLUS ESTIMATES (AXLE POSITION, BED FLOOR HEIGHT, CAB HEIGHT); SOURCES IN TRUCK_DATA/README.MD.",
        "TACOMA: THE TUB BASE CANNOT SIT BETWEEN THE WHEEL WELLS AND THE LOADED CAMPER EXCEEDS PAYLOAD. NOT SAFE IN ANY CONFIGURATION.",
        "HALF-TON 6.5 FT: CG OK BUT LOADED CAMPER IS AT OR OVER MOST HALF-TON PAYLOADS; BODY UNDERSIDE CLASHES WITH 21.4 IN RAILS. 5.5 FT: CG BEHIND AXLE.",
        "A SAFE MULTI-TRUCK PRODUCT NEEDS DIFFERENT ENVELOPES PER TRUCK CLASS FROM THE SAME PARAMETRIC SYSTEM (SEE ADR 0004).",
        EST,
    ], width=6.0 * IN, size=7)
    s.save()


def black_():
    from reportlab.lib.colors import black
    return black


def main():
    cfg = load_config()
    p = params(cfg, DESIGN)
    for d in ("general_arrangement", "dimensions", "truck_fit", "interior"):
        (DWG / d).mkdir(parents=True, exist_ok=True)
    old = DWG / "truck_fit" / "A03_truck_fit.pdf"
    if old.exists():
        old.unlink()  # superseded by A04/A05 (rev B renumbering)
    a01(cfg, p)
    a02(cfg, p)
    a03(cfg, p)
    a04(cfg, p)
    a05(cfg, p)
    print("drawings: MM-A01..A05 written (ANSI C)")


if __name__ == "__main__":
    main()
