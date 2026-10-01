"""Engineering-drawing primitives on reportlab: sheet frame, title block, views built from OpenSCAD
2D projections, dimensions, callouts. White background, black/gray linework, inch units.
"""
import re
import subprocess

from reportlab.lib.colors import Color, black, white
from reportlab.pdfgen import canvas as rl_canvas

from common import OPENSCAD, OUTPUT, ROOT

PT = 72.0
SHEET_W, SHEET_H = 17 * PT, 11 * PT  # ANSI B landscape
MARGIN = 0.4 * PT
GRAY = Color(0.45, 0.45, 0.45)
LIGHT = Color(0.72, 0.72, 0.72)
MAIN = ROOT / "cad" / "main.scad"
PROJ_DIR = OUTPUT / "proj"


# ---------------------------------------------------------------- projections
def projection(part, plane, truck="SHORT", cut_x=0.0):
    """Closed polylines [(u, v), ...] of PART projected onto PLANE (model inches)."""
    PROJ_DIR.mkdir(parents=True, exist_ok=True)
    out = PROJ_DIR / ("%s_%s_%s_%g.svg" % (part, plane, truck, cut_x))
    r = subprocess.run([OPENSCAD, "-D", 'VIEW="proj"', "-D", 'PLANE="%s"' % plane, "-D", 'PART="%s"' % part,
                        "-D", 'TRUCK="%s"' % truck, "-D", "CUT_X=%g" % cut_x, "-o", str(out), str(MAIN)],
                       cwd=MAIN.parent, capture_output=True, text=True)
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


# ---------------------------------------------------------------- sheet
class Sheet:
    def __init__(self, path, number, title, scale_note, meta):
        self.c = rl_canvas.Canvas(str(path), pagesize=(SHEET_W, SHEET_H), invariant=1)
        self.c.setTitle("%s %s" % (number, title))
        self.c.setAuthor("MINUTEMAN project")
        self.number, self.title, self.scale_note, self.meta = number, title, scale_note, meta

    def frame(self):
        c = self.c
        c.setFillColor(white)
        c.rect(0, 0, SHEET_W, SHEET_H, fill=1, stroke=0)
        c.setStrokeColor(black)
        c.setLineWidth(1.2)
        c.rect(MARGIN, MARGIN, SHEET_W - 2 * MARGIN, SHEET_H - 2 * MARGIN)
        # title block
        w, h = 6.2 * PT, 1.55 * PT
        x, y = SHEET_W - MARGIN - w, MARGIN
        c.setLineWidth(0.9)
        c.rect(x, y, w, h)
        rows = [("PROJECT", "MINUTEMAN aluminum slide-in camper shell  -  v%s envelope" % self.meta["version"]),
                ("TITLE", self.title),
                ("DWG NO.", "%s      REV %s      DATE %s" % (self.number, self.meta["drawing_revision"], self.meta["revision_date"])),
                ("SCALE", "%s      UNITS: INCHES      SHEET: ANSI B" % self.scale_note),
                ("STATUS", "PRELIMINARY - CONCEPT ENVELOPE - NOT FOR FABRICATION")]
        rh = h / len(rows)
        for i, (k, v) in enumerate(rows):
            ry = y + h - (i + 1) * rh
            if i:
                c.line(x, ry + rh, x + w, ry + rh)
            c.setFont("Helvetica", 6.5)
            c.setFillColor(GRAY)
            c.drawString(x + 4, ry + rh - 8, k)
            c.setFillColor(black)
            c.setFont("Helvetica-Bold" if k in ("TITLE", "DWG NO.") else "Helvetica", 9 if k == "TITLE" else 8)
            c.drawString(x + 52, ry + rh / 2 - 3, v)
        c.line(x + 48, y, x + 48, y + h)

    def notes(self, x, y, lines, title="NOTES", width=6.5 * PT):
        """Numbered notes, word-wrapped to `width` points. Returns the y below the last line."""
        c = self.c
        c.setFillColor(black)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(x, y, title)
        c.setFont("Helvetica", 7)
        y -= 11
        for ln in lines:
            words, cur, indent = ln.split(), "", 0
            for w in words:
                trial = (cur + " " + w).strip()
                if c.stringWidth(trial, "Helvetica", 7) > width - indent:
                    c.drawString(x + indent, y, cur)
                    y, cur, indent = y - 9.5, w, 9
                else:
                    cur = trial
            c.drawString(x + indent, y, cur)
            y -= 11
        return y

    def save(self):
        self.c.showPage()
        self.c.save()


# ---------------------------------------------------------------- views
class View:
    """Maps model (u, v) inches to paper points. fu/fv flip axes (e.g. fu=-1 puts +X on the left)."""

    def __init__(self, sheet, ox, oy, scale, fu=1, fv=1):
        self.s, self.c = sheet, sheet.c
        self.ox, self.oy, self.k, self.fu, self.fv = ox, oy, PT / scale, fu, fv
        self.scale = scale

    def P(self, u, v):
        return self.ox + self.fu * u * self.k, self.oy + self.fv * v * self.k

    def polys(self, polys, width=0.8, color=black, dash=None, fill=None):
        c = self.c
        c.setLineWidth(width)
        c.setStrokeColor(color)
        c.setDash(*(dash or ([], 0)))
        for poly in polys:
            p = c.beginPath()
            x, y = self.P(*poly[0])
            p.moveTo(x, y)
            for u, v in poly[1:]:
                p.lineTo(*self.P(u, v))
            p.close()
            if fill is not None:
                c.setFillColor(fill)
            c.drawPath(p, stroke=1, fill=1 if fill is not None else 0)
        c.setDash([], 0)

    def line(self, a, b, width=0.5, color=black, dash=None):
        c = self.c
        c.setLineWidth(width)
        c.setStrokeColor(color)
        c.setDash(*(dash or ([], 0)))
        c.line(*self.P(*a), *self.P(*b))
        c.setDash([], 0)



def view_title(sheet, x, y, text, scale_text):
    c = sheet.c
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(x, y, text)
    w = c.stringWidth(text, "Helvetica-Bold", 9)
    c.setLineWidth(0.6)
    c.line(x - w / 2, y - 2, x + w / 2, y - 2)
    c.setFont("Helvetica", 7)
    c.drawCentredString(x, y - 11, scale_text)


# ---------------------------------------------------------------- dimensions
def _arrow(c, x, y, ang_dx, ang_dy):
    import math
    L, W = 6.0, 2.0
    n = math.hypot(ang_dx, ang_dy) or 1
    ux, uy = ang_dx / n, ang_dy / n
    p = c.beginPath()
    p.moveTo(x, y)
    p.lineTo(x - L * ux + W * uy, y - L * uy - W * ux)
    p.lineTo(x - L * ux - W * uy, y - L * uy + W * ux)
    p.close()
    c.setFillColor(black)
    c.drawPath(p, stroke=0, fill=1)


def _tagged_text(c, x, y, text, verify, rotate=False):
    c.saveState()
    c.translate(x, y)
    if rotate:
        c.rotate(90)
    c.setFillColor(black)
    c.setFont("Helvetica", 7.5)
    tw = c.stringWidth(text, "Helvetica", 7.5)
    total = tw + (22 if verify else 0)
    c.setFillColor(white)
    c.rect(-total / 2 - 1.5, -1, total + 3, 9, fill=1, stroke=0)
    c.setFillColor(black)
    c.drawString(-total / 2, 1, text)
    if verify:
        bx = -total / 2 + tw + 3
        c.setLineWidth(0.6)
        c.setStrokeColor(black)
        c.rect(bx, -0.5, 18, 8.5, fill=0, stroke=1)
        c.setFont("Helvetica-Bold", 5.5)
        c.drawString(bx + 2, 1.5, "VOT")
    c.restoreState()


def fmt(v):
    s = ("%.2f" % v).rstrip("0").rstrip(".")
    return s + '"'


def dim_h(view, a, b, v_line, verify=False, text=None):
    """Horizontal dimension between model points a, b; dimension line at model v = v_line."""
    c = view.c
    (x1, y1), (x2, y2) = view.P(*a), view.P(*b)
    _, yd = view.P(a[0], v_line)
    c.setStrokeColor(GRAY)
    c.setLineWidth(0.35)
    for x, y in ((x1, y1), (x2, y2)):
        s = 1 if yd > y else -1
        c.line(x, y + s * 2, x, yd + s * 3)
    c.setStrokeColor(black)
    c.line(x1, yd, x2, yd)
    _arrow(c, x1, yd, x1 - x2, 0)
    _arrow(c, x2, yd, x2 - x1, 0)
    _tagged_text(c, (x1 + x2) / 2, yd + 1.5, text or fmt(abs(b[0] - a[0])), verify)


def dim_v(view, a, b, u_line, verify=False, text=None):
    """Vertical dimension between model points a, b; dimension line at model u = u_line."""
    c = view.c
    (x1, y1), (x2, y2) = view.P(*a), view.P(*b)
    xd, _ = view.P(u_line, a[1])
    c.setStrokeColor(GRAY)
    c.setLineWidth(0.35)
    for x, y in ((x1, y1), (x2, y2)):
        s = 1 if xd > x else -1
        c.line(x + s * 2, y, xd + s * 3, y)
    c.setStrokeColor(black)
    c.line(xd, y1, xd, y2)
    _arrow(c, xd, y1, 0, y1 - y2)
    _arrow(c, xd, y2, 0, y2 - y1)
    _tagged_text(c, xd - 2.5, (y1 + y2) / 2, text or fmt(abs(b[1] - a[1])), verify, rotate=True)


def callout(view, at, dx_pt, dy_pt, text):
    """Leader from model point `at` to a boxed part-ID label offset by (dx, dy) points."""
    c = view.c
    x, y = view.P(*at)
    tx, ty = x + dx_pt, y + dy_pt
    c.setStrokeColor(black)
    c.setLineWidth(0.45)
    c.line(x, y, tx, ty)
    c.setFillColor(black)
    c.circle(x, y, 1.3, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 6.5)
    w = c.stringWidth(text, "Helvetica-Bold", 6.5)
    bx = tx if dx_pt >= 0 else tx - w - 4
    c.setFillColor(white)
    c.rect(bx, ty - 4, w + 4, 9, fill=1, stroke=1)
    c.setFillColor(black)
    c.drawString(bx + 2, ty - 1.5, text)
