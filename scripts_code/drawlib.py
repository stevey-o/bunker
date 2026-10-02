"""Engineering-drawing primitives (reportlab) following ASME Y14 conventions as far as practical:

- Y14.1  sheet size (ANSI C, 22 x 17 in), zoned border, title block, tolerance block, projection symbol
- Y14.35 revision block (REV / DESCRIPTION / DATE / APPROVED)
- Y14.2  line conventions: visible (thick), hidden (dashed), center (long-short), phantom (long-short-short)
         for adjacent / reference parts (the truck), thin dimension and extension lines, upper-case lettering
- Y14.3  orthographic views (third-angle), section views with labeled cutting planes, detail views
- Y14.5  unidirectional dimensions (text reads from the bottom), decimal inch without leading zero,
         reference dimensions in parentheses, flag notes (numbered triangles) tying a dimension to a note

Geometry comes from OpenSCAD 2D projections of the same modules used for rendering.
"""
import math
import re
import subprocess

from reportlab.lib.colors import Color, black, white
from reportlab.pdfgen import canvas as rl_canvas

from common import OPENSCAD, OUTPUT, ROOT

PT = 72.0
IN = PT
SHEET_W, SHEET_H = 22 * PT, 17 * PT  # ANSI C landscape
MARGIN = 0.5 * PT
GRAY = Color(0.42, 0.42, 0.42)
LIGHT = Color(0.70, 0.70, 0.70)
RED = Color(0.75, 0.05, 0.05)
MAIN = ROOT / "cad" / "main.scad"
PROJ_DIR = OUTPUT / "proj"

# Y14.2 line types: (width pt, dash pattern)
VISIBLE = (1.0, None)
THIN = (0.45, None)
HIDDEN = (0.5, [5, 2.5])
CENTER = (0.35, [16, 3, 3, 3])
PHANTOM = (0.5, [16, 3, 3, 3, 3, 3])
FONT, FONT_B = "Helvetica", "Helvetica-Bold"


# ---------------------------------------------------------------- projections
def projection(part, plane, truck="F350_LONG", cut_x=0.0, cut_y=0.0, tailgate=None):
    """Closed polylines [(u, v), ...] of PART projected / sectioned onto PLANE (model inches)."""
    PROJ_DIR.mkdir(parents=True, exist_ok=True)
    out = PROJ_DIR / ("%s_%s_%s_%g_%g_%s.svg" % (part, plane, truck, cut_x, cut_y, tailgate or "dflt"))
    extra = ["-D", 'TAILGATE="%s"' % tailgate] if tailgate else []
    r = subprocess.run([OPENSCAD, "-D", 'VIEW="proj"', "-D", 'PLANE="%s"' % plane, "-D", 'PART="%s"' % part,
                        "-D", 'TRUCK="%s"' % truck, "-D", "CUT_X=%g" % cut_x, "-D", "CUT_Y=%g" % cut_y] + extra
                       + ["-o", str(out), str(MAIN)], cwd=MAIN.parent, capture_output=True, text=True)
    bad = [l for l in r.stderr.splitlines() if l.startswith(("WARNING", "ERROR"))]
    if r.returncode or bad:
        raise SystemExit("projection %s/%s failed:\n%s" % (part, plane, "\n".join(bad) or r.stderr))
    polys = []
    for d in re.findall(r'd="([^"]*)"', out.read_text()):
        for sub in re.split(r"[Zz]", d):
            pts = [(float(a), -float(b)) for a, b in re.findall(r"(-?[\d.eE+-]+),(-?[\d.eE+-]+)", sub)]
            if len(pts) > 1:
                polys.append(pts)
    return polys


def fmt(v, places=2):
    """ASME decimal-inch style: no leading zero below 1, trailing zeros trimmed to at least one place."""
    s = ("%.*f" % (places, abs(v))).rstrip("0")
    s = s + "0" if s.endswith(".") else s
    if s.startswith("0."):
        s = s[1:]
    return ("-" if v < 0 else "") + s


# ---------------------------------------------------------------- sheet
class Sheet:
    def __init__(self, path, number, title, scale_note, meta, sheet_no, sheet_count, revisions):
        self.c = rl_canvas.Canvas(str(path), pagesize=(SHEET_W, SHEET_H), invariant=1)
        self.c.setTitle("%s %s" % (number, title))
        self.c.setAuthor("MINUTEMAN project")
        self.number, self.title, self.scale_note, self.meta = number, title, scale_note, meta
        self.sheet_no, self.sheet_count, self.revisions = sheet_no, sheet_count, revisions
        self.frame()

    def text(self, x, y, s, size=8, bold=False, align="left", color=black):
        c = self.c
        c.setFillColor(color)
        c.setFont(FONT_B if bold else FONT, size)
        {"left": c.drawString, "center": c.drawCentredString, "right": c.drawRightString}[align](x, y, s.upper())

    def frame(self):
        c = self.c
        c.setFillColor(white)
        c.rect(0, 0, SHEET_W, SHEET_H, fill=1, stroke=0)
        c.setStrokeColor(black)
        c.setLineWidth(1.4)
        c.rect(MARGIN, MARGIN, SHEET_W - 2 * MARGIN, SHEET_H - 2 * MARGIN)
        # zone markings: 8 columns (numbers, right to left per Y14.1), 4 rows (letters, bottom to top)
        cols, rows = 8, 4
        zw = (SHEET_W - 2 * MARGIN) / cols
        zh = (SHEET_H - 2 * MARGIN) / rows
        c.setLineWidth(0.6)
        for i in range(cols):
            x = MARGIN + i * zw
            if i:
                c.line(x, MARGIN - 8, x, MARGIN)
                c.line(x, SHEET_H - MARGIN, x, SHEET_H - MARGIN + 8)
            for y in (MARGIN - 13, SHEET_H - MARGIN + 4):
                self.text(x + zw / 2, y, str(cols - i), 9, align="center")
        for j in range(rows):
            y = MARGIN + j * zh
            if j:
                c.line(MARGIN - 8, y, MARGIN, y)
                c.line(SHEET_W - MARGIN, y, SHEET_W - MARGIN + 8, y)
            for x in (MARGIN - 9, SHEET_W - MARGIN + 9):
                self.text(x, y + zh / 2, "ABCD"[j], 9, align="center")
        self.title_block()
        self.revision_block()

    def title_block(self):
        c = self.c
        w, h = 7.6 * IN, 2.2 * IN
        x0, y0 = SHEET_W - MARGIN - w, MARGIN
        self.tb_top = y0 + h
        c.setLineWidth(1.1)
        c.setStrokeColor(black)
        c.rect(x0, y0, w, h)
        tw = 2.55 * IN  # tolerance block column
        c.line(x0 + tw, y0, x0 + tw, y0 + h)
        tol = ["UNLESS OTHERWISE SPECIFIED:", "DIMENSIONS ARE IN INCHES", "ENVELOPE = OUTSIDE OF SKIN, NOMINAL",
               "TOLERANCES:", "  X.X  +/- .25     X.XX  +/- .06", "  ANGLES  +/- 1 DEG",
               "INTERPRET PER ASME Y14.5-2018", "DO NOT SCALE DRAWING"]
        for i, t in enumerate(tol):
            self.text(x0 + 6, y0 + h - 12 - 10.5 * i, t, 6.8, bold=(i == 0))
        # third-angle projection symbol (frustum side view + end view circles)
        px, py = x0 + 14, y0 + 12
        c.setLineWidth(0.7)
        p = c.beginPath()
        p.moveTo(px, py + 2); p.lineTo(px + 16, py - 2); p.lineTo(px + 16, py + 14); p.lineTo(px, py + 10); p.close()
        c.drawPath(p, stroke=1, fill=0)
        c.circle(px + 34, py + 6, 8, stroke=1, fill=0)
        c.circle(px + 34, py + 6, 4, stroke=1, fill=0)
        self.text(px + 48, py + 3, "THIRD ANGLE PROJECTION", 6)
        rx, rw = x0 + tw, w - tw
        rows = [0.38, 0.62, 0.40, 0.40, 0.40]
        ys = [y0 + h]
        for r in rows:
            ys.append(ys[-1] - r * IN)
        for y in ys[1:-1]:
            c.line(rx, y, rx + rw, y)

        def cell(y_top, y_bot, xa, label, value, size=9, bold=False):
            if xa > rx + 1:
                c.line(xa, y_bot, xa, y_top)
            self.text(xa + 4, y_top - 8, label, 5.5, color=GRAY)
            self.text(xa + 4, y_bot + 6, value, size, bold=bold)

        cell(ys[0], ys[1], rx, "PROJECT / OWNER", "MINUTEMAN ALUMINUM SLIDE-IN CAMPER SHELL  -  S. ORLIK", 8.5, True)
        self.text(rx + 4, ys[1] - 8, "TITLE", 5.5, color=GRAY)
        self.text(rx + 8, ys[2] + 14, self.title, 13 if len(self.title) < 34 else 11, bold=True)
        cell(ys[2], ys[3], rx, "SIZE", "C", 11, True)
        cell(ys[2], ys[3], rx + 0.7 * IN, "DWG NO.", self.number, 11, True)
        cell(ys[2], ys[3], rx + 3.6 * IN, "REV", self.meta["drawing_revision"], 11, True)
        cell(ys[3], ys[4], rx, "SCALE", self.scale_note, 8.5)
        cell(ys[3], ys[4], rx + 1.9 * IN, "DATE", self.meta["revision_date"], 8.5)
        cell(ys[3], ys[4], rx + 3.6 * IN, "SHEET", "%d OF %d" % (self.sheet_no, self.sheet_count), 8.5)
        cell(ys[4], ys[5], rx, "DRAWN", "CLAUDE (AI) FOR S.O.", 7)
        cell(ys[4], ys[5], rx + 1.7 * IN, "CHECKED", "-", 7)
        cell(ys[4], ys[5], rx + 2.6 * IN, "STATUS", "PRELIMINARY - NOT FOR FABRICATION", 7, True)

    def revision_block(self):
        c = self.c
        w = 7.6 * IN
        x0 = SHEET_W - MARGIN - w
        rh = 13
        top = SHEET_H - MARGIN
        widths = [0.45 * IN, 5.15 * IN, 1.0 * IN, 1.0 * IN]
        rows = [("REV", "DESCRIPTION", "DATE", "APPROVED")] + list(self.revisions)
        c.setLineWidth(0.8)
        c.setStrokeColor(black)
        h = rh * (len(rows) + 1)
        c.setFillColor(white)
        c.rect(x0, top - h, w, h, fill=1, stroke=1)
        self.text(x0 + w / 2, top - 10, "REVISIONS", 7.5, True, "center")
        c.line(x0, top - rh, x0 + w, top - rh)
        for i, row in enumerate(rows):
            y = top - rh * (i + 2)
            c.line(x0, y, x0 + w, y)
            x = x0
            for j, (cw, t) in enumerate(zip(widths, row)):
                if j:
                    c.line(x, y, x, top - rh)
                self.text(x + 4, y + 4, t, 6.5, bold=(i == 0))
                x += cw
        self.rev_bottom = top - h

    def notes(self, x, y, lines, title="NOTES:", width=6.5 * IN, size=7.5):
        """Numbered notes, word-wrapped. A line starting with '<n>' gets flag-note triangle n instead of a number."""
        c = self.c
        self.text(x, y, title, 9, True)
        y -= 14
        for i, ln in enumerate(lines, 1):
            m = re.match(r"^<(\d+)>\s*(.*)", ln)
            if m:
                flag(c, x + 5, y + 3, m.group(1))
                ln = m.group(2)
            else:
                self.text(x, y, "%d." % i, size)
            cur = ""
            for wd in ln.upper().split():
                trial = (cur + " " + wd).strip()
                if c.stringWidth(trial, FONT, size) > width - 18:
                    self.text(x + 16, y, cur, size)
                    y, cur = y - size * 1.3, wd
                else:
                    cur = trial
            self.text(x + 16, y, cur, size)
            y -= size * 1.6
        return y

    def table(self, x, y, headers, rows, widths, size=7, title=None, row_h=11.5):
        c = self.c
        if title:
            self.text(x, y + 5, title, 9, True)
        c.setLineWidth(0.6)
        c.setStrokeColor(black)
        W = sum(widths)
        allrows = [headers] + rows
        H = row_h * len(allrows)
        for i, r in enumerate(allrows):
            yy = y - row_h * (i + 1)
            if i:
                c.line(x, yy + row_h, x + W, yy + row_h)
            xx = x
            for cw, t in zip(widths, r):
                t = str(t)
                col = RED if t.startswith("FAIL") else black
                self.text(xx + 3, yy + 3.5, t, size, bold=(i == 0 or t.split(" ")[0] in ("FAIL", "PASS", "CHECK", "CONDITIONAL")), color=col)
                xx += cw
        c.rect(x, y - H, W, H)
        xx = x
        for cw in widths[:-1]:
            xx += cw
            c.line(xx, y, xx, y - H)
        return y - H

    def save(self):
        self.c.showPage()
        self.c.save()


# ---------------------------------------------------------------- views
class View:
    """Maps model (u, v) inches to paper points. fu/fv flip axes (fu=-1 puts +X on the left)."""

    def __init__(self, sheet, ox, oy, scale, fu=1, fv=1):
        self.s, self.c = sheet, sheet.c
        self.ox, self.oy, self.k, self.fu, self.fv = ox, oy, PT / scale, fu, fv
        self.scale = scale

    def P(self, u, v):
        return self.ox + self.fu * u * self.k, self.oy + self.fv * v * self.k

    def polys(self, polys, line=VISIBLE, color=black, fill=None):
        c = self.c
        c.setLineWidth(line[0])
        c.setStrokeColor(color)
        c.setDash(line[1], 0) if line[1] else c.setDash([], 0)
        c.setLineJoin(1)
        for poly in polys:
            p = c.beginPath()
            p.moveTo(*self.P(*poly[0]))
            for u, v in poly[1:]:
                p.lineTo(*self.P(u, v))
            p.close()
            if fill is not None:
                c.setFillColor(fill)
            c.drawPath(p, stroke=1, fill=1 if fill is not None else 0)
        c.setDash([], 0)

    def line(self, a, b, line=THIN, color=black):
        c = self.c
        c.setLineWidth(line[0])
        c.setStrokeColor(color)
        c.setDash(line[1], 0) if line[1] else c.setDash([], 0)
        c.line(*self.P(*a), *self.P(*b))
        c.setDash([], 0)

    def clip(self, a, b):
        """Begin a rectangular clip in model coords; caller must call c.restoreState()."""
        c = self.c
        c.saveState()
        (x0, y0), (x1, y1) = self.P(*a), self.P(*b)
        p = c.beginPath()
        p.rect(min(x0, x1), min(y0, y1), abs(x1 - x0), abs(y1 - y0))
        c.clipPath(p, stroke=0, fill=0)
        return min(x0, x1), min(y0, y1), abs(x1 - x0), abs(y1 - y0)


def view_title(sheet, x, y, text, scale_text):
    c = sheet.c
    sheet.text(x, y, text, 11, True, "center")
    w = c.stringWidth(text.upper(), FONT_B, 11)
    c.setLineWidth(0.8)
    c.setStrokeColor(black)
    c.line(x - w / 2, y - 3, x + w / 2, y - 3)
    sheet.text(x, y - 14, scale_text, 8, align="center")


# ---------------------------------------------------------------- symbols
def flag(c, x, y, n, size=9):
    """Y14.5 flag note: number in an equilateral triangle centered at (x, y)."""
    h = size * 0.87
    p = c.beginPath()
    p.moveTo(x - size / 2, y - h / 3); p.lineTo(x + size / 2, y - h / 3); p.lineTo(x, y + 2 * h / 3); p.close()
    c.setFillColor(white); c.setStrokeColor(black); c.setLineWidth(0.6)
    c.drawPath(p, stroke=1, fill=1)
    c.setFillColor(black); c.setFont(FONT_B, size * 0.62)
    c.drawCentredString(x, y - h / 3 + 1.4, str(n))


def cg_symbol(view, u, v, label=None, r=6):
    """Center-of-gravity symbol: circle with alternate quadrants filled."""
    c = view.c
    x, y = view.P(u, v)
    c.setStrokeColor(black); c.setLineWidth(0.7)
    c.setFillColor(white); c.circle(x, y, r, stroke=1, fill=1)
    c.setFillColor(black)
    for a in (0, 180):
        p = c.beginPath(); p.moveTo(x, y); p.arcTo(x - r, y - r, x + r, y + r, startAng=a, extent=90); p.close()
        c.drawPath(p, stroke=0, fill=1)
    c.circle(x, y, r, stroke=1, fill=0)
    if label:
        view.s.text(x + r + 3, y - 3, label, 7, True)


def axle_mark(view, u, v_top, v_bot, label="REAR AXLE CL"):
    view.line((u, v_bot), (u, v_top), CENTER)
    x, y = view.P(u, v_top)
    view.s.text(x, y + 3, label, 6.5, align="center")


def section_arrows(view, a, b, letter, look):
    """Cutting-plane line from a to b (model) with view arrows pointing `look` (paper unit vector) and letters."""
    c = view.c
    (x1, y1), (x2, y2) = view.P(*a), view.P(*b)
    c.setLineWidth(1.3); c.setStrokeColor(black); c.setDash([18, 4, 4, 4, 4, 4], 0)
    c.line(x1, y1, x2, y2)
    c.setDash([], 0)
    for (x, y) in ((x1, y1), (x2, y2)):
        tx, ty = x + look[0] * 18, y + look[1] * 18
        c.line(x, y, tx, ty)
        _arrow(c, tx, ty, look[0], look[1], 9, 3.2)
        view.s.text(tx + look[0] * 10, ty + look[1] * 10 - 4, letter, 12, True, "center")


def detail_circle(view, center, radius_in, letter):
    c = view.c
    x, y = view.P(*center)
    r = radius_in * view.k
    c.setLineWidth(0.8); c.setStrokeColor(black); c.setDash([16, 3, 3, 3, 3, 3], 0)
    c.circle(x, y, r, stroke=1, fill=0)
    c.setDash([], 0)
    view.s.text(x + r * 0.72 + 4, y + r * 0.72 + 4, letter, 12, True)


# ---------------------------------------------------------------- dimensions
def _arrow(c, x, y, dx, dy, L=7.0, W=2.2):
    n = math.hypot(dx, dy) or 1
    ux, uy = dx / n, dy / n
    p = c.beginPath()
    p.moveTo(x, y)
    p.lineTo(x - L * ux + W * uy, y - L * uy - W * ux)
    p.lineTo(x - L * ux - W * uy, y - L * uy + W * ux)
    p.close()
    c.setFillColor(black)
    c.drawPath(p, stroke=0, fill=1)


def _dim_text(c, x, y, text, flag_no=None, size=8):
    """Unidirectional dimension text centered at (x, y) in a white break, optional flag note."""
    text = text.upper()
    tw = c.stringWidth(text, FONT, size)
    total = tw + (13 if flag_no else 0)
    c.setFillColor(white)
    c.rect(x - total / 2 - 2, y - size / 2 - 1.5, total + 4, size + 3, fill=1, stroke=0)
    c.setFillColor(black)
    c.setFont(FONT, size)
    c.drawString(x - total / 2, y - size / 2 + 1, text)
    if flag_no:
        flag(c, x - total / 2 + tw + 8, y, flag_no, 8.5)


def dim_h(view, a, b, v_line, flag_no=None, text=None, ref=False):
    """Horizontal dimension between model points a, b; dimension line at model v = v_line."""
    c = view.c
    (x1, y1), (x2, y2) = view.P(*a), view.P(*b)
    _, yd = view.P(a[0], v_line)
    c.setStrokeColor(black)
    c.setLineWidth(0.35)
    for x, y in ((x1, y1), (x2, y2)):
        s = 1 if yd > y else -1
        c.line(x, y + s * 2.5, x, yd + s * 4)
    c.line(x1, yd, x2, yd)
    _arrow(c, x1, yd, x1 - x2, 0)
    _arrow(c, x2, yd, x2 - x1, 0)
    t = text or fmt(abs(b[0] - a[0]))
    _dim_text(c, (x1 + x2) / 2, yd, "(%s)" % t if ref else t, flag_no)


def dim_v(view, a, b, u_line, flag_no=None, text=None, ref=False):
    """Vertical dimension between model points a, b; dimension line at model u = u_line. Text horizontal."""
    c = view.c
    (x1, y1), (x2, y2) = view.P(*a), view.P(*b)
    xd, _ = view.P(u_line, a[1])
    c.setStrokeColor(black)
    c.setLineWidth(0.35)
    for x, y in ((x1, y1), (x2, y2)):
        s = 1 if xd > x else -1
        c.line(x + s * 2.5, y, xd + s * 4, y)
    c.line(xd, y1, xd, y2)
    _arrow(c, xd, y1, 0, y1 - y2)
    _arrow(c, xd, y2, 0, y2 - y1)
    t = text or fmt(abs(b[1] - a[1]))
    _dim_text(c, xd, (y1 + y2) / 2, "(%s)" % t if ref else t, flag_no)


def callout(view, at, dx_pt, dy_pt, text, size=7.5):
    """Leader from a model point (dot on surface) to an upper-case note offset (dx, dy) points, with shoulder."""
    c = view.c
    x, y = view.P(*at)
    tx, ty = x + dx_pt, y + dy_pt
    c.setStrokeColor(black)
    c.setLineWidth(0.45)
    shoulder = 10 if dx_pt >= 0 else -10
    c.line(x, y, tx, ty)
    c.line(tx, ty, tx + shoulder, ty)
    c.setFillColor(black)
    c.circle(x, y, 1.6, fill=1, stroke=0)
    lines = text.upper().split("\n")
    for i, ln in enumerate(lines):
        yy = ty - 3 - i * (size + 1.5) + (len(lines) - 1) * (size + 1.5) / 2
        view.s.text(tx + shoulder + (3 if dx_pt >= 0 else -3), yy, ln, size, align="left" if dx_pt >= 0 else "right")
