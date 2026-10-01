"""bom/extrusion_cutlist.csv (T-slot rails from the registry) and bom/sheet_cutlist.csv (skin faces).

frame_cutlist.csv is not produced in v0.1: there is no structural frame yet (v0.2).
"""
import csv

from common import GENERATED_HEADER, ROOT, params, skin_faces
from estimates import load, parts, sheet_count

BOM = ROOT / "bom"
SAW_KERF = 0.125


def main():
    BOM.mkdir(exist_ok=True)
    cfg, p = load()
    rails = [x for x in parts() if x["kind"] == "MEMBER"]
    with open(BOM / "extrusion_cutlist.csv", "w", newline="") as f:
        f.write("# " + GENERATED_HEADER.format(script="generate_cutlist.py") + "\n")
        w = csv.writer(f)
        w.writerow(["id", "profile", "cut_length_in", "end_cuts", "qty", "role", "note"])
        for r in rails:
            w.writerow([r["id"], r["profile"], "%.3f" % r["length"], "SQUARE", 1, r["role"], r["note"]])
        total = sum(r["length"] + SAW_KERF for r in rails)
        w.writerow(["TOTAL", "", "%.1f" % total, "", len(rails), "", "incl. %.3f in kerf per cut" % SAW_KERF])
    lo, hi = sheet_count(cfg, p)
    with open(BOM / "sheet_cutlist.csv", "w", newline="") as f:
        f.write("# " + GENERATED_HEADER.format(script="generate_cutlist.py") + "\n")
        f.write("# PRELIMINARY: flat-pattern envelope faces, corner radii and laps ignored. Panel splits are v0.3.\n")
        w = csv.writer(f)
        w.writerow(["id", "description", "width_in", "height_in", "net_area_in2", "group", "fits_4x8", "fits_5x10"])
        faces = skin_faces(p)
        for s in faces:
            a, b = sorted((s["width"], s["height"]))
            w.writerow([s["id"], s["description"], s["width"], s["height"], s["area"], s["group"],
                        "yes" if a <= 48 and b <= 96 else "no (seam)", "yes" if a <= 60 and b <= 120 else "no (seam)"])
        w.writerow(["TOTAL", "", "", "", round(sum(s["area"] for s in faces), 1), "",
                    "%d-%d sheets 4x8 incl. waste" % (lo, hi), ""])
    print("cutlists: extrusion (%d rails), sheet (%d faces)" % (len(rails), len(faces)))


if __name__ == "__main__":
    main()
