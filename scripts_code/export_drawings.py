"""Export v0.1 engineering drawings A01-A03 (PDF) from OpenSCAD projections + config dimensions.

Geometry comes from OpenSCAD 2D projections of the same modules used for rendering; dimension
values come from common.params(). Nothing is typed in twice.
"""
import json

from common import PARTS_JSON, ROOT, load_config, params
from drawlib import (GRAY, LIGHT, PT, Sheet, View, callout, dim_h, dim_v, projection, view_title)
from reportlab.lib.colors import black

DWG = ROOT / "drawings"
CAMPER = ["tub_lower", "tub_upper", "body_lower", "body_upper"]
VOT_NOTE = "VOT = VERIFY ON TRUCK: depends on the physical truck; confirm with truck_data/measurement_templates/f350_measurement_sheet.md."
IN = PT  # paper inch in points


# Projections have no hidden-line removal, so each view lists the components visible from it.
VISIBLE = {"side": ("door", "win_side", "win_nose", "bosses"), "top": ("bosses",),
           "rear": ("door", "bosses"), "front": ("win_nose", "bosses")}


def camper(view, plane, width=0.9, facing=None):
    for part in CAMPER:
        view.polys(projection(part, plane), width)
    for part in VISIBLE[facing or plane]:
        view.polys(projection(part, plane), 0.6 if part != "bosses" else 0.5)


def truck(view, plane, variant, human=True):
    for part in ("truck_bed", "truck_cab", "truck_wheels"):
        view.polys(projection(part, plane, variant), 0.5, GRAY)
    if human:
        view.polys(projection("human_ground", plane, variant), 0.4, LIGHT)


# ---------------------------------------------------------------- A01
def a01(cfg, p):
    s = Sheet(DWG / "general_arrangement" / "A01_general_arrangement.pdf", "A01", "GENERAL ARRANGEMENT", "1:24", cfg)
    s.frame()
    k = 24
    xf = p["nose_front_x"]
    plan = View(s, 1.2 * IN + xf * IN / k, 8.3 * IN, k, fu=-1, fv=-1)
    camper(plan, "top")
    plan.polys(projection("rails", "top"), 0.5, GRAY, dash=([3, 2], 0))
    view_title(s, 6.4 * IN, 8.4 * IN, "PLAN (TOP)", "SCALE 1:24  -  FRONT TO LEFT")
    xr = p["camper_rear_x"]
    yb = p["camper_body_width"] / 2 - p["roof_rack_boss_edge_inset"]
    callout(plan, (xr + p["roof_rack_boss_from_rear"][0], yb), 40, -6, "RACK-ROOF-01")
    callout(plan, (xr + 8, p["body_interior_width"] / 2 - 0.5), 34, -22, "UTIL-L-01..03 (hidden)")
    callout(plan, (xr + 8, -p["body_interior_width"] / 2 + 0.5), 34, 22, "UTIL-R-01..03 (hidden)")
    callout(plan, (p["camper_front_x"] - 2.5, -20), 30, 40, "UTIL-F-01 (hidden)")

    z0 = 2.5 * IN
    side = View(s, 1.2 * IN + xf * IN / k, z0, k, fu=-1)
    camper(side, "side")
    side.polys(projection("rails", "side"), 0.5, GRAY, dash=([3, 2], 0))
    view_title(s, 3.3 * IN, 2.2 * IN, "LEFT ELEVATION (DRIVER SIDE)", "SCALE 1:24  -  FRONT TO LEFT")
    callout(side, (p["nose_front_x"] - 6, 70), -26, 30, "ENV-NOSE-01")
    callout(side, (p["camper_rear_x"] + 60, 40), -30, -14, "ENV-BODY-01")
    callout(side, (p["camper_rear_x"] + 50, 6), -20, -16, "ENV-TUB-01")
    callout(side, (p["camper_rear_x"] + 25, p["roof_crown_z"]), -40, 14, "ENV-ROOF-01")
    callout(side, (p["camper_rear_x"] + p["window_side_center_from_rear"], p["window_side_center_z"]), 30, 26, "WIN-L-01")

    rear = View(s, 7.6 * IN, z0, k, fu=-1)
    camper(rear, "front", facing="rear")
    view_title(s, 7.6 * IN, 2.2 * IN, "REAR ELEVATION", "SCALE 1:24")
    callout(rear, (0, p["door_bottom_z"] + 40), 42, 10, "DOOR-B-01")

    front = View(s, 11.4 * IN, z0, k)
    camper(front, "front")
    view_title(s, 11.4 * IN, 2.2 * IN, "FRONT ELEVATION", "SCALE 1:24")
    callout(front, (0, (p["nose_bottom_z"] + p["roof_eave_z"]) / 2), 50, 40, "WIN-N-01 (optional)")

    parts = json.loads(PARTS_JSON.read_text())
    c = s.c
    x, y = 13.3 * IN, 10.35 * IN
    c.setFont("Helvetica-Bold", 8)
    c.drawString(x, y, "PARTS LIST (from CAD registry)")
    c.setFont("Helvetica", 6.5)
    for i, prt in enumerate(parts):
        yy = y - 11 * (i + 1)
        c.drawString(x, yy, prt["id"])
        c.drawString(x + 62, yy, prt["role"][:38])
    s.notes(6.6 * IN, 8.05 * IN, width=6.4 * IN, lines=[
        "1. v0.1 is an ENVELOPE ONLY: outer surfaces of the shell, no structural frame.",
        "2. All IDs follow SYSTEM-LOCATION-NUMBER (cad/config/part_ids.md) and match BOM, renders, manual.",
        "3. Hidden (dashed): owner accessory T-slot rails on interior wall faces. Not primary structure.",
        "4. RACK-ROOF bosses are structural provisions; each must land on a roof crossmember in v0.2.",
        "5. Door and windows are rough-opening placeholders for purchased components. WIN-R-01 mirrors WIN-L-01.",
        "6. Nose is storage/desk volume only; not engineered as a sleeping platform.",
        "7. Roof has %.2f\" transverse drainage crown. Vertical corners R%.1f\"." % (p["roof_crown"], p["body_corner_radius"]),
        "8. Dimensions: see A02. Truck fit: see A03.",
        "9. " + VOT_NOTE,
    ])
    s.save()


# ---------------------------------------------------------------- A02
def a02(cfg, p):
    s = Sheet(DWG / "dimensions" / "A02_major_dimensions.pdf", "A02", "MAJOR DIMENSIONS", "1:16", cfg)
    s.frame()
    k = 16
    z0 = 3.2 * IN
    xf, xr, xb = p["nose_front_x"], p["camper_rear_x"], p["camper_front_x"]
    side = View(s, 1.7 * IN + xf * IN / k, z0, k, fu=-1)
    camper(side, "side")
    side.polys(projection("human_inside", "side"), 0.4, LIGHT)
    view_title(s, 4.9 * IN, 2.75 * IN, "LEFT ELEVATION", "SCALE 1:16  -  FRONT TO LEFT  -  6'7\" FIGURE SHOWN FOR SCALE")
    zc, ze = p["roof_crown_z"], p["roof_eave_z"]
    xt = xf - p["nose_top_setback"]
    # horizontal chains above
    dim_h(side, (xf, p["nose_bottom_z"]), (xr, 0), zc + 14, text='%s OVERALL' % ('%.1f"' % p["overall_length"]))
    dim_h(side, (xf, p["nose_bottom_z"]), (xb, p["nose_bottom_z"]), zc + 7)
    dim_h(side, (xb, ze), (xr, ze), zc + 7)
    dim_h(side, (xf, p["nose_bottom_z"]), (xt, ze), p["nose_bottom_z"] - 6, text='%s RAKE' % ('%.1f"' % p["nose_top_setback"]))
    # rear vertical chain (right side of view)
    ur = xr - 6
    chain = [0, p["interior_floor_z"], p["tub_step_z"], p["camper_lower_tub_height"]]
    vot = [False, True, True]
    for i in range(3):
        dim_v(side, (xr, chain[i]), (xr, chain[i + 1]), ur, verify=vot[i])
    dim_v(side, (xr, p["interior_floor_z"]), (xr, p["ceiling_z"]), ur - 10,
          text='%.0f" INTERIOR' % p["interior_height"])
    dim_v(side, (xr, p["ceiling_z"]), (xr, ze), ur - 10)
    dim_v(side, (xr, 0), (xr, zc), ur - 21, text='%.2f" OVERALL' % zc)
    # front vertical chain (left side of view)
    uf = xf + 6
    dim_v(side, (xb, 0), (xb, p["nose_bottom_z"]), uf, verify=True)
    dim_v(side, (xf, p["nose_bottom_z"]), (xf, ze), uf)
    dim_v(side, (xf, p["nose_bottom_z"]), (xf, p["nose_floor_z"]), uf + 9)

    rear = View(s, 12.0 * IN, z0, k, fu=-1)
    camper(rear, "front", facing="rear")
    view_title(s, 12.0 * IN, 2.3 * IN, "REAR ELEVATION", "SCALE 1:16")
    W, tw, tb = p["camper_body_width"], p["camper_lower_tub_width"], p["tub_base_width"]
    dim_h(rear, (W / 2, ze), (-W / 2, ze), zc + 6)
    dim_h(rear, (tw / 2, p["tub_step_z"]), (-tw / 2, p["tub_step_z"]), -3.5, verify=True)
    dim_h(rear, (tb / 2, 0), (-tb / 2, 0), -9, verify=True)
    dy, dw = p["door_offset_y"], p["door_width"]
    dim_h(rear, (dy + dw / 2, p["door_top_z"]), (dy - dw / 2, p["door_top_z"]), p["door_top_z"] + 5)
    dim_v(rear, (dy - dw / 2, p["door_bottom_z"]), (dy - dw / 2, p["door_top_z"]), -W / 2 + 8)
    dim_v(rear, (-W / 2, 0), (-W / 2, p["door_bottom_z"]), -W / 2 - 6)
    dim_v(rear, (-W / 2, p["camper_lower_tub_height"]), (-W / 2, ze), -W / 2 - 6)
    dim_v(rear, (-W / 2, 0), (-W / 2, p["camper_lower_tub_height"]), -W / 2 - 14, verify=True)

    s.notes(0.7 * IN, 2.3 * IN, width=8.4 * IN, lines=[
        "1. Origin: bed-floor top, truck centerline, inner face of bed front wall. Camper front face %.1f\" aft of it." % p["camper_front_gap"],
        "2. Interior clear height %.0f\" is an owner requirement (6'7\" standing, ADR 0002); headroom over figure %.0f\"." % (p["interior_height"], p["headroom_6ft7"]),
        "3. Lower tub steps: base %.1f\" wide clears wheel wells to %.1f\"; upper %.1f\" wide to %.1f\"; body %.0f\" wide above rails." % (
            tb, p["tub_step_z"], tw, p["camper_lower_tub_height"], W),
        "4. Construction thicknesses (floor %.1f, wall %.2f, roof %.1f, skin %.3f) are PRELIMINARY." % (
            p["floor_sandwich"], p["wall_thickness"], p["roof_thickness"], p["skin_thickness"]),
        "5. Full tagged dimension list: camper_versions/minuteman_v0.1_envelope/DIMENSIONS.md.",
        "6. " + VOT_NOTE,
    ])
    s.save()


# ---------------------------------------------------------------- A03
def a03(cfg, p, pl):
    s = Sheet(DWG / "truck_fit" / "A03_truck_fit.pdf", "A03", "TRUCK FIT - F-350 SHORT AND LONG BED", "AS NOTED", cfg)
    s.frame()
    k = 40
    for variant, pp, ground_y, title in (("SHORT", p, 6.7, "SHORT BED (6.75 FT) - LEFT ELEVATION"),
                                         ("LONG", pl, 2.6, "LONG BED (8 FT) - LEFT ELEVATION")):
        g = -pp["truck_bed_floor_height"]
        v = View(s, 1.0 * IN + 150 * IN / k, ground_y * IN - g * IN / k, k, fu=-1)
        truck(v, "side", variant)
        camper(v, "side", 0.8)
        v.line((170, g), (-125, g), 0.6, black)
        view_title(s, 4.3 * IN, (ground_y + 3.3) * IN, title, "SCALE 1:40")
        xr = pp["camper_rear_x"]
        dim_v(v, (xr, g), (xr, pp["roof_crown_z"]), xr - 8, verify=True, text='%.2f" TRAVEL HT' % pp["ground_to_crown"])
        dim_v(v, (xr, g), (xr, 0), xr - 22, verify=True)
        dim_h(v, (-pp["truck_bed_length"], 0), (xr, 0), g - 9, verify=True,
              text='%.1f" UNUSED BED' % pp["bed_length_unused"])
        ax = pp["rear_axle_x"]
        mid = (pp["camper_front_x"] + xr) / 2
        dim_h(v, (ax, g), (mid, g), g - 18, verify=True, text='%.1f" FLOOR MID FWD OF AXLE' % pp["floor_mid_ahead_of_axle"])
        callout(v, (ax, g + pp["truck_tire_diameter"] / 2), -40, 34, "REAR AXLE")

    # Section A-A through rear axle, short bed
    c = s.c
    ks = 20
    sec = View(s, 10.0 * IN, 7.3 * IN, ks, fu=-1)
    cx = p["rear_axle_x"]
    c.saveState()
    clip = c.beginPath()
    x0, y0 = sec.P(48, -22)
    x1, y1 = sec.P(-48, 40)
    clip.rect(x0, y0, x1 - x0, y1 - y0)
    c.clipPath(clip, stroke=0, fill=0)
    sec.polys(projection("truck_bed", "xsection", "SHORT", cx), 0.6, GRAY)
    sec.polys(projection("truck_wheels", "xsection", "SHORT", cx), 0.4, GRAY)
    sec.polys(projection("envelope", "xsection", "SHORT", cx), 0.9)
    c.restoreState()
    view_title(s, 10.0 * IN, 6.45 * IN, "SECTION A-A AT REAR AXLE (SHORT BED)", "SCALE 1:20  -  LOOKING FORWARD")
    wi, ww = p["truck_bed_inner_width_top"], p["truck_wheel_well_width"]
    dim_h(sec, (wi / 2, p["truck_bed_rail_height"]), (-wi / 2, p["truck_bed_rail_height"]), 36, verify=True)
    dim_h(sec, (p["camper_lower_tub_width"] / 2, p["tub_step_z"]), (-p["camper_lower_tub_width"] / 2, p["tub_step_z"]), 30, verify=True)
    dim_h(sec, (ww / 2, p["truck_wheel_well_height"]), (-ww / 2, p["truck_wheel_well_height"]), -6, verify=True)
    dim_h(sec, (p["tub_base_width"] / 2, 0), (-p["tub_base_width"] / 2, 0), -13, verify=True)
    dim_v(sec, (-wi / 2, 0), (-wi / 2, p["truck_bed_rail_height"]), -wi / 2 - 6, verify=True)
    dim_v(sec, (-ww / 2, 0), (-ww / 2, p["truck_wheel_well_height"]), -wi / 2 - 14, verify=True)

    # Detail B: nose over cab, short bed
    kd = 16
    det = View(s, 14.3 * IN, 4.0 * IN, kd, fu=-1)
    c.saveState()
    clip = c.beginPath()
    x0, y0 = det.P(34, 32)
    x1, y1 = det.P(-12, 92)
    clip.rect(x0, y0, x1 - x0, y1 - y0)
    c.clipPath(clip, stroke=0, fill=0)
    det.polys(projection("truck_cab", "side", "SHORT"), 0.6, GRAY)
    det.polys(projection("truck_bed", "side", "SHORT"), 0.6, GRAY)
    camper(det, "side", 0.9)
    c.restoreState()
    c.setLineWidth(0.5)
    c.setStrokeColor(GRAY)
    c.rect(x0, y0, x1 - x0, y1 - y0)
    view_title(s, (x0 + x1) / 2, y0 - 16, "DETAIL B - NOSE OVER CAB", "SCALE 1:16")
    cab_z = p["truck_cab_height_above_bed"]
    dim_v(det, (p["cab_back_x"] + 4, cab_z), (p["cab_back_x"] + 4, p["nose_bottom_z"]), 28, verify=True)
    dim_h(det, (p["camper_front_x"], 40), (p["cab_back_x"], 40), 36, verify=True)
    dim_h(det, (p["cab_back_x"], p["nose_bottom_z"]), (p["nose_front_x"], p["nose_bottom_z"]), 62, verify=True,
          text='%.1f" OVER CAB' % p["nose_over_cab"])

    s.notes(7.6 * IN, 5.6 * IN, width=8.6 * IN, lines=[
        "1. Truck is a simplified reference; every interface value is VERIFY ON TRUCK (VOT).",
        "2. Same camper fits both beds; on the 8 ft bed the unused length is behind the camper.",
        "3. Lower tub must pass the tailgate opening: tub %.1f\" vs opening %.1f\" (VOT)." % (
            p["camper_lower_tub_width"], p["truck_tailgate_opening_width"]),
        "4. Tailgate is not a structural support. Tie-downs and jacks: v0.2.",
        "5. Camper CG must fall forward of the rear axle: v0.2 calculation required.",
        "6. Travel height excludes roof rack and panels.",
    ])
    s.save()


def main():
    cfg = load_config()
    p = params(cfg, "SHORT")
    pl = params(cfg, "LONG")
    for d in ("general_arrangement", "dimensions", "truck_fit"):
        (DWG / d).mkdir(parents=True, exist_ok=True)
    a01(cfg, p)
    a02(cfg, p)
    a03(cfg, p, pl)
    print("drawings: A01, A02, A03 written")


if __name__ == "__main__":
    main()
