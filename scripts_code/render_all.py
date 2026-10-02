"""Render the parts registry and all standard v0.1 views.

1. Runs OpenSCAD with VIEW="registry", parses the `PART|{json}` echo lines into
   output/current_design/parts.json (the input to BOM, cut list and weight report).
2. Renders the named-camera PNGs into 3D_renderings/.

Fails on any OpenSCAD WARNING or ERROR so a silently-broken include cannot ship.
Markers in a camera list: FIXED = explicit framing (no --viewall), FULL = full geometry render.
Camera convention (OpenSCAD gimbal rot z): 0 = from right (-Y), 90 = from front (+X),
180 = from left (+Y), 270 = from rear (-X).
"""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

from common import OPENSCAD, OUTPUT, PARTS_JSON, ROOT

MAIN = ROOT / "cad" / "main.scad"
REN = ROOT / "3D_renderings"
SIZE = "1600,1100"

ISO = "--projection=perspective"
ORTHO = "--projection=ortho"


def gimbal(rx, rz):
    return "--camera=0,0,0,%d,0,%d,0" % (rx, rz)


# (output path, VIEW, TRUCK, camera args)
RENDERS = [
    ("exterior/01_rear_iso.png", "exterior", "F350_LONG", [gimbal(62, 225), ISO]),
    ("exterior/02_front_iso.png", "exterior", "F350_LONG", [gimbal(62, 45), ISO]),
    ("exterior/03_left.png", "exterior", "F350_LONG", [gimbal(90, 180), ORTHO]),
    ("exterior/04_right.png", "exterior", "F350_LONG", [gimbal(90, 0), ORTHO]),
    ("exterior/05_front.png", "exterior", "F350_LONG", [gimbal(90, 90), ORTHO]),
    ("exterior/06_rear.png", "exterior", "F350_LONG", [gimbal(90, 270), ORTHO]),
    ("exterior/07_top.png", "exterior", "F350_LONG", [gimbal(0, 0), ORTHO]),
    ("truck_fit/01_short_bed.png", "truck_fit", "F350_SHORT", [gimbal(65, 230), ISO]),
    ("truck_fit/02_long_bed.png", "truck_fit", "F350_LONG", [gimbal(65, 230), ISO]),
    ("truck_fit/03_side_clearance.png", "truck_fit", "F350_LONG", [gimbal(90, 180), ORTHO]),
    ("truck_fit/04_cab_clearance.png", "truck_fit", "F350_LONG",
     ["--camera=10,300,46,10,0,46", ORTHO, "FIXED"]),
    ("truck_fit/05_short_bed_side.png", "truck_fit", "F350_SHORT", [gimbal(90, 180), ORTHO]),
    ("interior_shell/01_utility_rails.png", "interior", "F350_LONG", [gimbal(58, 270), ISO, "FULL"]),
    ("fit_study/01_f150_6p5ft.png", "truck_fit", "F150_65", [gimbal(90, 180), ORTHO]),
    ("fit_study/02_f150_5p5ft.png", "truck_fit", "F150_55", [gimbal(90, 180), ORTHO]),
    ("fit_study/03_tacoma_6ft.png", "truck_fit", "TACOMA_6", [gimbal(90, 180), ORTHO]),
    ("fit_study/04_tacoma_5ft.png", "truck_fit", "TACOMA_5", [gimbal(90, 180), ORTHO]),
    ("fit_study/05_tacoma_rear_iso.png", "truck_fit", "TACOMA_6", [gimbal(60, 250), ISO]),
]


def openscad(args):
    r = subprocess.run([OPENSCAD] + args + [str(MAIN)], cwd=MAIN.parent, capture_output=True, text=True)
    bad = [l for l in (r.stdout + r.stderr).splitlines() if l.startswith(("WARNING", "ERROR"))]
    if r.returncode != 0 or bad:
        raise SystemExit("OpenSCAD failed (%s):\n%s" % (" ".join(args), "\n".join(bad) or r.stderr))
    return r


def registry():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    echo = OUTPUT / "registry.echo"
    openscad(["-D", 'VIEW="registry"', "-o", str(echo)])
    parts = []
    for line in echo.read_text().splitlines():
        if line.startswith("WARNING") or line.startswith("ERROR"):
            raise SystemExit("registry: " + line)
        if line.startswith('ECHO: "PART|'):
            parts.append(json.loads(line[len('ECHO: "PART|'):-1]))
    PARTS_JSON.write_text(json.dumps(parts, indent=1) + "\n")
    print("registry: %d parts -> %s" % (len(parts), PARTS_JSON.relative_to(ROOT)))
    return parts


def render(job):
    rel, view, truck, cam = job
    out = REN / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    fixed = "FIXED" in cam  # explicit framing: skip auto-fit
    full = ["--render", "--backend=manifold"] if "FULL" in cam else []  # preview cannot show nested cuts
    cam = [c for c in cam if c not in ("FIXED", "FULL")]
    fit = [] if fixed else ["--viewall", "--autocenter"]
    openscad(["-D", 'VIEW="%s"' % view, "-D", 'TRUCK="%s"' % truck, "-o", str(out),
              "--imgsize=" + SIZE, "--colorscheme=Tomorrow"] + full + fit + cam)
    return rel


def main():
    registry()
    only = sys.argv[1:]
    jobs = [j for j in RENDERS if not only or any(o in j[0] for o in only)]
    with ThreadPoolExecutor(max_workers=4) as ex:
        for rel in ex.map(render, jobs):
            print("rendered", rel)


if __name__ == "__main__":
    main()
