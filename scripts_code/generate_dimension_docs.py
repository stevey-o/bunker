"""Generate camper_versions/minuteman_v0.1_envelope/DIMENSIONS.md and the F-350 measurement sheet
(Markdown + printable PDF with diagrams) from dimensions.json, so the documents can never disagree
with the model.
"""
from common import DERIVED, GENERATED_HEADER, ROOT, fmt_in, load_config, params
from reportlab.lib.colors import Color, black, white
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas as rl_canvas

DIMS_MD = ROOT / "camper_versions" / "minuteman_v0.1_envelope" / "DIMENSIONS.md"
SHEET_DIR = ROOT / "truck_data" / "measurement_templates"
GRAY = Color(0.5, 0.5, 0.5)


def val(v):
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, list):
        return ", ".join("%g" % x for x in v)
    if isinstance(v, float):
        return "%g" % v
    return str(v)


def dimensions_md(cfg):
    ps, pl = params(cfg, "F350_LONG"), params(cfg, "F350_SHORT")
    L = ["<!-- " + GENERATED_HEADER.format(script="generate_dimension_docs.py") + " -->",
         "# MINUTEMAN v%s envelope - dimensions" % cfg["version"], "",
         "Every major design dimension, each tagged exactly one of:", "",
         "- **FIXED**: owner requirement or hard constraint; change only by decision record.",
         "- **PARAMETRIC**: free design variable; change in `dimensions.json` and regenerate.",
         "- **PRELIMINARY**: engineering placeholder; expected to change in v0.2/v0.3.",
         "- **VERIFY ON TRUCK**: depends on the physical truck; confirm with the measurement sheet.", "",
         "Units: inches. Origin: bed-floor top, truck centerline, inner face of bed front wall; "
         "+X forward, +Y left (driver), +Z up.", "",
         "## Headline", "",
         "| | Value | Tag |", "|---|---|---|",
         "| Interior clear standing height | %s | FIXED |" % fmt_in(ps["interior_height"]),
         "| Overall length (rear face to nose tip) | %s | PARAMETRIC |" % fmt_in(ps["overall_length"]),
         "| Body width | %s | PARAMETRIC |" % fmt_in(ps["camper_body_width"]),
         "| Ground to roof eave / crown on 2011 F-350 4x4 | %s / %s | VERIFY ON TRUCK |" % (fmt_in(ps["ground_to_eave"]), fmt_in(ps["ground_to_crown"])),
         "| Lower length (fills 8 ft bed, tailgate closed) | %s | FIXED |" % fmt_in(ps["camper_lower_length"]),
         "| Nose underside above cab roof | %s | VERIFY ON TRUCK |" % fmt_in(ps["camper_to_cab_clearance"]), ""]
    groups = {}
    for k, v in cfg["camper"].items():
        groups.setdefault(v.get("group", "Other"), []).append((k, v))
    L += ["## Design parameters", ""]
    for g, items in groups.items():
        L += ["### %s" % g, "", "| Parameter | Description | Value | Tag | Note |", "|---|---|---|---|---|"]
        L += ["| `%s` | %s | %s | %s | %s |" % (k, v.get("label", ""), val(v["value"]), v["tag"], v.get("note", ""))
              for k, v in items]
        L.append("")
    L += ["## Derived dimensions (computed in `scripts_code/common.py`)", "",
          "| Name | Description | 8 ft bed (design) | 6.75 ft bed | Tag |", "|---|---|---|---|---|"]
    for name, label, tag, _scope, _fn in DERIVED:
        L.append("| `%s` | %s | %g | %g | %s |" % (name, label, ps[name], pl[name], tag))
    L += ["", "## Truck interface (2011 F-350 base values)", "",
          "| Parameter | Description | Value | Tag | Sheet fig. |", "|---|---|---|---|---|"]
    for k, v in cfg["truck"].items():
        L.append("| `%s` | %s | %s | %s | %s |" % (k, v["label"], val(v["value"]), v["tag"], v.get("fig", "")))
    names = list(cfg["truck_variants"])
    L += ["", "### All truck variants (fit study only; the camper is sized to %s)" % cfg["build"]["DESIGN_TRUCK"]["value"], "",
          "| Value | " + " | ".join(names) + " |", "|---|" + "---|" * len(names)]
    keys = ["truck_bed_length", "truck_rear_axle_from_bulkhead", "truck_wheelbase", "truck_bed_floor_height",
            "truck_bed_rail_height", "truck_wheel_well_width", "truck_bed_floor_width", "truck_tailgate_opening_width",
            "truck_cab_height_above_bed"]
    pv = {n: params(cfg, n) for n in names}
    for k in keys:
        L.append("| `%s` | %s |" % (k, " | ".join(val(pv[n][k]) for n in names)))
    L.append("| camper cargo rating (lb) | %s |" % " | ".join(
        "%d-%d" % (cfg["truck_variants"][n]["camper_cargo_rating_lb"]["low"], cfg["truck_variants"][n]["camper_cargo_rating_lb"]["high"]) for n in names))
    L += ["", "Sources and estimate flags for every value: `truck_data/README.md`. Fit verdicts: `truck_data/fit_study.md`."]
    L += ["", "## Unresolved dimensions", "",
          "These cannot be closed until the truck is measured or v0.2 structure exists:", ""]
    unresolved = [(k, v) for sec in ("camper", "truck") for k, v in cfg[sec].items() if v["tag"] == "VERIFY ON TRUCK"]
    L += ["- `%s`: %s (now %s)" % (k, v["label"], val(v["value"])) for k, v in unresolved]
    L += ["- `truck_bed_length`, `truck_rear_axle_from_bulkhead`: which bed does the owner's truck have?",
          "- Construction thicknesses (`floor_sandwich`, `wall_thickness`, `roof_thickness`, `nose_floor_thickness`) "
          "are PRELIMINARY until the v0.2 frame sections exist.",
          "- Door and window sizes are PRELIMINARY until specific purchased products are selected.", "",
          "## Rendering color legend", "",
          "| Element | Color |", "|---|---|",
          "| Skin / envelope | silver |", "| New frame pieces, roof-rack bosses | blue |",
          "| Utility T-slot rails | dark blue |", "| Truck reference | transparent gray |",
          "| Purchased placeholder (door) | charcoal |", "| Window placeholder | steel blue |",
          "| Reserved provision zone (power zone, wire chase) | translucent purple |",
          "| 6'7\" human reference | tan |", ""]
    DIMS_MD.parent.mkdir(parents=True, exist_ok=True)
    DIMS_MD.write_text("\n".join(L))


# ---------------------------------------------------------------- measurement sheet
EXTRA = [
    ("Which bed is on the truck?", "6.75 ft or 8 ft; cab style (crew / super cab / regular); SRW or DRW."),
    ("Model year and trim", "Door-jamb sticker."),
    ("Payload capacity (lb)", "Door-jamb tire & loading sticker: \"combined weight of occupants and cargo should never exceed\"."),
    ("GVWR / rear GAWR (lb)", "Door-jamb certification label."),
    ("Tire load index / size", "Tire sidewall."),
    ("Cab-roof items", "Clearance/marker lamps, antenna, roof rack? Note heights (affects M4)."),
    ("Bed liner / rail caps / tonneau rails", "Type and thickness: they change bed widths and rail height."),
    ("Gooseneck / 5th-wheel puck or hitch in bed floor", "Location from front wall; anything that protrudes above the floor."),
    ("Stake pockets and factory tie-down points", "Positions along the bed (for v0.2 tie-downs)."),
    ("Bed-mounted brake light / camera", "Location; the camper will block it."),
]


def sheet_rows(cfg):
    rows = []
    for k, v in cfg["truck"].items():
        if v["tag"] == "VERIFY ON TRUCK":
            rows.append((v.get("fig", ""), v["label"], v["measure"], val(v["value"]), k))
    for k, v in cfg["truck_variants"]["F350_LONG"].items():
        if isinstance(v, dict) and v.get("tag") == "VERIFY ON TRUCK":
            rows.append((v["fig"], v["label"], v["measure"],
                         "%s (8 ft) / %s (6.75)" % (val(v["value"]), val(cfg["truck_variants"]["F350_SHORT"][k]["value"])), k))
    rows.sort(key=lambda r: r[0])
    return rows


def sheet_md(cfg, rows):
    L = ["<!-- " + GENERATED_HEADER.format(script="generate_dimension_docs.py") + " -->",
         "# F-350 measurement sheet", "",
         "**This is the next physical action.** Nothing past the envelope can be trusted until these numbers come "
         "from the actual truck. Print `f350_measurement_sheet.pdf` (diagrams M1-M5 on page 1), take it to the "
         "truck, fill it in, then update `cad/config/dimensions.json` and run `make all`.", "",
         "**Setup:** level ground; truck loaded as it normally travels (fuel full, usual tools); tires at normal "
         "pressure; tailgate open or removed. **Tools:** 25 ft tape, 4-6 ft straightedge or level, plumb bob or "
         "string with a nut, masking tape and marker, a helper. Measure twice; where left and right can differ, "
         "record both.", "",
         "| # | Fig | Measurement | How | Model now | Left / A | Right / B |", "|---|---|---|---|---|---|---|"]
    for i, (fig, label, how, model, _k) in enumerate(rows, 1):
        L.append("| %d | %s | %s | %s | %s | ______ | ______ |" % (i, fig, label, how, model))
    L += ["", "## Also record", "", "| Item | Where to find it | Value |", "|---|---|---|"]
    L += ["| %s | %s | ______ |" % e for e in EXTRA]
    L += ["", "Date measured: ________  Measured by: ________", ""]
    (SHEET_DIR / "f350_measurement_sheet.md").write_text("\n".join(L))


def _arrow_dim(c, x1, y1, x2, y2, label, side=1):
    c.setStrokeColor(black)
    c.setLineWidth(0.7)
    c.line(x1, y1, x2, y2)
    for (xa, ya, xb, yb) in ((x1, y1, x2, y2), (x2, y2, x1, y1)):
        import math
        a = math.atan2(yb - ya, xb - xa)
        p = c.beginPath()
        p.moveTo(xa, ya)
        p.lineTo(xa + 6 * math.cos(a + 0.35), ya + 6 * math.sin(a + 0.35))
        p.lineTo(xa + 6 * math.cos(a - 0.35), ya + 6 * math.sin(a - 0.35))
        p.close()
        c.setFillColor(black)
        c.drawPath(p, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", 7)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    if abs(x2 - x1) > abs(y2 - y1):
        c.drawCentredString(mx, my + (4 if side > 0 else -10), label)
    else:
        c.drawString(mx + (4 if side > 0 else -4 - c.stringWidth(label, "Helvetica-Bold", 7)), my - 3, label)


def _panel(c, x, y, w, h, title):
    c.setStrokeColor(GRAY)
    c.setLineWidth(0.6)
    c.rect(x, y, w, h)
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(x + 6, y + h - 13, title)


def sheet_pdf(cfg, rows):
    c = rl_canvas.Canvas(str(SHEET_DIR / "f350_measurement_sheet.pdf"), pagesize=letter, invariant=1)
    c.setTitle("F-350 measurement sheet")
    W, H = letter
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, H - 45, "MINUTEMAN - F-350 measurement sheet: diagrams")
    c.setFont("Helvetica", 8)
    c.drawString(40, H - 58, "Schematic, not to scale. Level ground, normal travel load, tailgate open. Numbers in brackets = row # on page 2.")
    num = {r[4]: i for i, r in enumerate(rows, 1)}
    n = lambda k: "[%d]" % num[k] if k in num else ""
    pw, ph = 255, 205
    # M1 ground to bed floor
    x, y = 40, H - 80 - ph
    _panel(c, x, y, pw, ph, "M1  Ground to bed floor")
    c.setStrokeColor(black)
    c.line(x + 10, y + 30, x + pw - 10, y + 30)
    c.rect(x + 50, y + 95, 170, 45)
    c.circle(x + 110, y + 62, 32)
    c.setFont("Helvetica", 7)
    c.drawString(x + 60, y + 128, "bed floor (top surface)")
    c.drawString(x + 12, y + 20, "level ground")
    _arrow_dim(c, x + 230, y + 30, x + 230, y + 140, "floor height " + n("truck_bed_floor_height"), -1)
    # M2 bed side section
    x = 40 + pw + 20
    _panel(c, x, y, pw, ph, "M2  Bed, side section (looking at left wall)")
    bx0, bx1, by0 = x + 20, x + pw - 20, y + 50
    c.line(bx0, by0, bx1, by0)
    c.line(bx0, by0, bx0, by0 + 85)
    c.line(bx1, by0, bx1, by0 + 70)
    c.setDash(3, 2)
    c.line(bx0, by0 + 85, bx1, by0 + 85)
    c.setDash()
    c.rect(bx0 + 110, by0, 60, 32)
    c.setFont("Helvetica", 7)
    c.drawString(bx0 + 2, by0 + 88, "front wall")
    c.drawString(bx1 - 40, by0 + 73, "tailgate")
    c.drawString(bx0 + 115, by0 + 22, "wheel well")
    c.circle(bx0 + 140, by0 - 22, 2, fill=1)
    c.drawString(bx0 + 145, by0 - 25, "rear axle")
    _arrow_dim(c, bx0, by0 - 12, bx1, by0 - 12, "bed length " + n("truck_bed_length"), -1)
    _arrow_dim(c, bx0, by0 - 32, bx0 + 140, by0 - 32, "axle from front wall " + n("truck_rear_axle_from_bulkhead"), -1)
    _arrow_dim(c, bx0 + 110, by0 + 40, bx0 + 170, by0 + 40, "well length " + n("truck_wheel_well_length"))
    _arrow_dim(c, bx0 + 178, by0, bx0 + 178, by0 + 32, "well ht " + n("truck_wheel_well_height"))
    _arrow_dim(c, bx0 + 12, by0, bx0 + 12, by0 + 85, "rail ht " + n("truck_bed_rail_height"))
    # M3 end view
    y2 = y - 20 - ph
    x = 40
    _panel(c, x, y2, pw, ph, "M3  Bed, end view looking forward")
    cx, fy = x + pw / 2, y2 + 55
    c.line(cx - 100, fy, cx + 100, fy)
    for s in (-1, 1):
        c.line(cx + s * 100, fy, cx + s * 100, fy + 110)
        c.line(cx + s * 100, fy + 110, cx + s * 118, fy + 110)
        c.rect(cx + s * 100 - (28 if s > 0 else 0), fy, 28, 34)
    _arrow_dim(c, cx - 100, fy + 95, cx + 100, fy + 95, "width at rail top " + n("truck_bed_inner_width_top"))
    _arrow_dim(c, cx - 100, fy + 60, cx + 100, fy + 60, "width at floor " + n("truck_bed_floor_width"))
    _arrow_dim(c, cx - 72, fy + 20, cx + 72, fy + 20, "between wells " + n("truck_wheel_well_width"))
    _arrow_dim(c, cx + 100, fy + 122, cx + 118, fy + 122, "rail " + n("truck_bed_rail_width"))
    # M4 cab
    x = 40 + pw + 20
    _panel(c, x, y2, pw, ph, "M4  Cab and bed front wall (side)")
    gx, gy = x + 20, y2 + 35
    c.line(gx, gy, gx + 215, gy)
    c.rect(gx + 100, gy, 8, 70)                 # bed front wall
    c.rect(gx + 124, gy, 85, 140)               # cab
    c.rect(gx + 150, gy + 140, 14, 5, fill=1)   # roof lamps
    c.setFont("Helvetica", 7)
    c.drawString(gx + 150, gy + 60, "cab")
    c.drawString(gx + 168, gy + 141, "lamps")
    c.drawString(gx + 30, gy + 4, "bed floor")
    _arrow_dim(c, gx + 5, gy, gx + 5, gy + 145, "to top of cab roof,")
    c.setFont("Helvetica-Bold", 7)
    c.drawString(gx + 9, gy + 62, "incl. lamps " + n("truck_cab_height_above_bed"))
    _arrow_dim(c, gx + 108, gy + 100, gx + 124, gy + 100, "gap " + n("truck_cab_to_bed_clearance"))
    _arrow_dim(c, gx + 100, gy + 80, gx + 108, gy + 80, "")
    c.setLineWidth(0.4)
    c.line(gx + 100, gy + 80, gx + 80, gy + 40)
    c.drawString(gx + 40, gy + 32, "wall thk " + n("truck_bed_front_wall_thickness"))
    # M5 tailgate
    y3 = y2 - 20 - 150
    x = 40
    _panel(c, x, y3, pw * 2 + 20, 150, "M5  Tailgate opening (rear view, tailgate open or removed)")
    cx, fy = x + pw + 75, y3 + 30
    c.line(cx - 125, fy, cx + 125, fy)
    for s in (-1, 1):
        c.rect(cx + s * 110 - (10 if s < 0 else 0), fy, 10, 85)
    c.setFont("Helvetica", 7)
    c.drawString(cx + 92, fy + 92, "post / latch striker")
    _arrow_dim(c, cx - 100, fy + 50, cx + 100, fy + 50, "narrowest clear width " + n("truck_tailgate_opening_width"))
    # side inset: lowered tailgate (only matters for short-bed / tailgate-down use)
    sx, sy = x + 30, fy + 10
    c.setFont("Helvetica", 7)
    c.drawString(sx, sy + 78, "side view, tailgate down:")
    c.line(sx, sy + 40, sx + 60, sy + 40)
    c.drawString(sx, sy + 30, "bed floor")
    c.rect(sx + 60, sy + 42, 70, 4)
    _arrow_dim(c, sx + 60, sy + 58, sx + 130, sy + 58, "length " + n("truck_tailgate_length"))
    c.setFont("Helvetica-Bold", 7)
    c.drawString(sx + 62, sy + 25, "step vs floor " + n("truck_tailgate_down_offset"))
    c.showPage()

    # page 2: the table
    c.setFont("Helvetica-Bold", 13)
    c.drawString(40, H - 45, "F-350 measurements  -  record left/right (or front/rear) where they can differ")
    cols = [40, 62, 92, 300, 470, 530]
    yy = H - 70
    c.setFont("Helvetica-Bold", 7.5)
    for x0, t in zip(cols, ("#", "Fig", "Measurement", "Model value now", "A / Left", "B / Right")):
        c.drawString(x0, yy, t)
    yy -= 6
    c.line(40, yy, W - 40, yy)
    c.setFont("Helvetica", 7.5)
    for i, (fig, label, _how, model, _k) in enumerate(rows, 1):
        yy -= 24
        c.drawString(cols[0], yy + 6, str(i))
        c.drawString(cols[1], yy + 6, fig)
        c.drawString(cols[2], yy + 6, label[:58])
        c.drawString(cols[3], yy + 6, model)
        c.line(cols[4], yy + 2, cols[4] + 50, yy + 2)
        c.line(cols[5], yy + 2, cols[5] + 40, yy + 2)
        c.setStrokeColor(Color(0.85, 0.85, 0.85))
        c.line(40, yy - 4, W - 40, yy - 4)
        c.setStrokeColor(black)
    yy -= 30
    c.setFont("Helvetica-Bold", 9)
    c.drawString(40, yy, "Also record")
    c.setFont("Helvetica", 7.5)
    for item, where in EXTRA:
        yy -= 20
        c.drawString(40, yy, item)
        c.setFillColor(GRAY)
        c.drawString(40, yy - 9, where[:110])
        c.setFillColor(black)
        c.line(420, yy, W - 40, yy)
    yy -= 30
    c.drawString(40, yy, "Date measured: ________________      Measured by: ________________")
    c.setFont("Helvetica", 6.5)
    c.drawString(40, 30, "How to measure each row: see f350_measurement_sheet.md. After measuring: update cad/config/dimensions.json, run `make all`.")
    c.showPage()
    c.save()


def main():
    cfg = load_config()
    dimensions_md(cfg)
    SHEET_DIR.mkdir(parents=True, exist_ok=True)
    rows = sheet_rows(cfg)
    sheet_md(cfg, rows)
    sheet_pdf(cfg, rows)
    print("docs: DIMENSIONS.md, f350_measurement_sheet.md/.pdf (%d measurements)" % len(rows))


if __name__ == "__main__":
    main()
