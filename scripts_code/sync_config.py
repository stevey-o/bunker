"""Generate cad/config/dimensions.scad from cad/config/dimensions.json.

Values that differ between truck variants are emitted as `[v1, v2, ...][TRUCK_IDX]`, so OpenSCAD
switches trucks with `-D 'TRUCK="F350_SHORT"'` and never re-derives anything itself. Camper geometry is
identical for every variant (it comes from the DESIGN_TRUCK), so it is emitted as plain scalars.
"""
import json

from common import GENERATED_HEADER, ROOT, load_config, params, utility_rails, variant_names

OUT = ROOT / "cad" / "config" / "dimensions.scad"


def lit(v):
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, str):
        return json.dumps(v)
    if isinstance(v, (list, tuple)):
        return "[" + ", ".join(lit(x) for x in v) + "]"
    return repr(round(v, 4)) if isinstance(v, float) else str(v)


def main():
    cfg = load_config()
    variants = variant_names(cfg)
    per = {v: params(cfg, v) for v in variants}
    first = per[variants[0]]

    lines = ["// " + GENERATED_HEADER.format(script="sync_config.py"),
             "// Units: inches. Coordinate origin: bed-floor top, centerline, inner face of bed front wall.",
             "// +X forward (toward cab), +Y left (driver), +Z up.", "",
             "// Build defaults; override with -D (see build_variant.scad).",
             "FRAME_SYSTEM = %s;" % lit(cfg["build"]["FRAME_SYSTEM"]["value"]),
             "TRUCK = %s;" % lit(cfg["build"]["TRUCK"]["value"]),
             "TRUCK_NAMES = %s;" % lit(variants),
             "TRUCK_IDX = search([TRUCK], TRUCK_NAMES)[0];",
             'TAILGATE_DEFAULTS = %s;' % lit([per[v]["TAILGATE"] for v in variants]), ""]
    skip = {"TRUCK", "FRAME_SYSTEM", "TAILGATE", "DESIGN_TRUCK", "tailgate"}
    for k in first:
        if k in skip:
            continue
        vals = [per[v][k] for v in variants]
        if all(x == vals[0] for x in vals):
            lines.append("%s = %s;" % (k, lit(vals[0])))
        else:
            lines.append("%s = %s[TRUCK_IDX];" % (k, lit(vals)))

    lines += ["", "// Materials: [name, density_lb_in3]"]
    lines.append("MATERIALS = %s;" % lit([[n, m["density_lb_in3"]] for n, m in cfg["materials"].items()]))
    lines += ["", "// Profiles: [name, kind, w, h, wall, material, lb_per_in]"]
    lines.append("PROFILES = %s;" % lit([[n, x["kind"], x["w"], x["h"], x["wall"], x["material"], x["lb_per_in"]]
                                          for n, x in cfg["profiles"].items()]))
    lines += ["", "// Owner accessory T-slot rails: [id, length, [x,y,z] start, axis]"]
    lines.append("UTIL_RAILS = %s;" % lit([[r["id"], round(r["length"], 3), [round(c, 3) for c in r["start"]], r["axis"]]
                                            for r in utility_rails(first)]))
    OUT.write_text("\n".join(lines) + "\n")
    print("wrote", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
