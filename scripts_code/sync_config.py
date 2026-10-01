"""Generate cad/config/dimensions.scad from cad/config/dimensions.json.

Values that differ between truck variants are emitted as `TRUCK == "LONG" ? long : short`, so
OpenSCAD switches trucks with `-D 'TRUCK="LONG"'` and never re-derives anything itself.
"""
import json

from common import GENERATED_HEADER, ROOT, base_params, derive, load_config, utility_rails

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
    variants = list(cfg["truck_variants"])
    per = {}
    for v in variants:
        p = base_params(cfg, v)
        p.update(derive(p))
        per[v] = p
    short, long_ = per["SHORT"], per["LONG"]

    lines = ["// " + GENERATED_HEADER.format(script="sync_config.py"),
             "// Units: inches. Coordinate origin: bed-floor top, centerline, inner face of bed front wall.",
             "// +X forward (toward cab), +Y left (driver), +Z up.", ""]
    lines.append("// Build defaults; override with -D (see build_variant.scad).")
    lines.append("FRAME_SYSTEM = %s;" % lit(cfg["build"]["FRAME_SYSTEM"]["value"]))
    lines.append("TRUCK = %s;" % lit(cfg["build"]["TRUCK"]["value"]))
    lines.append("")
    skip = {"TRUCK", "FRAME_SYSTEM"}
    for k in short:
        if k in skip:
            continue
        a, b = short[k], long_[k]
        if a == b:
            lines.append("%s = %s;" % (k, lit(a)))
        else:
            lines.append('%s = TRUCK == "LONG" ? %s : %s;' % (k, lit(b), lit(a)))

    lines += ["", "// Materials: [name, density_lb_in3]"]
    lines.append("MATERIALS = %s;" % lit([[n, m["density_lb_in3"]] for n, m in cfg["materials"].items()]))
    lines += ["", "// Profiles: [name, kind, w, h, wall, material, lb_per_in]"]
    lines.append("PROFILES = %s;" % lit([[n, x["kind"], x["w"], x["h"], x["wall"], x["material"], x["lb_per_in"]]
                                          for n, x in cfg["profiles"].items()]))
    lines += ["", "// Owner accessory T-slot rails: [id, length, [x,y,z] start, axis]"]
    lines.append("UTIL_RAILS = %s;" % lit([[r["id"], round(r["length"], 3), [round(c, 3) for c in r["start"]], r["axis"]]
                                            for r in utility_rails(short)]))
    OUT.write_text("\n".join(lines) + "\n")
    print("wrote", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
