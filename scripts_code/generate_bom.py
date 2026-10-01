"""bom/master_bom.csv and bom/purchased_components.csv from the CAD parts registry."""
import csv

from common import GENERATED_HEADER, ROOT
from estimates import parts, unit_prices

BOM = ROOT / "bom"


def main():
    BOM.mkdir(exist_ok=True)
    reg = parts()
    if not reg:
        raise SystemExit("parts.json missing: run render_all.py first")
    with open(BOM / "master_bom.csv", "w", newline="") as f:
        f.write("# " + GENERATED_HEADER.format(script="generate_bom.py") + "\n")
        w = csv.writer(f)
        w.writerow(["id", "kind", "role", "qty", "profile", "material", "length_in", "size_in", "mass_lb",
                    "join", "cost_key", "status", "note"])
        for p in reg:
            w.writerow([p["id"], p["kind"], p["role"], 1, p["profile"], p["material"], p["length"] or "",
                        "x".join("%g" % s for s in p["size"]), round(p["mass"], 2) or "", p["join"],
                        p["cost_key"], p["status"], p["note"]])
    u = unit_prices()
    with open(BOM / "purchased_components.csv", "w", newline="") as f:
        f.write("# " + GENERATED_HEADER.format(script="generate_bom.py") + "\n")
        w = csv.writer(f)
        w.writerow(["id", "description", "qty", "unit_low_usd", "unit_high_usd", "status", "note"])
        for p in reg:
            if p["kind"] == "PURCHASED":
                r = u[p["cost_key"]]
                w.writerow([p["id"], r["description"], 1, r["low_usd"], r["high_usd"], p["status"], p["note"]])
        r = u["jacks"]
        w.writerow(["JACK-SET", r["description"], 1, r["low_usd"], r["high_usd"], r["status"],
                    "Tracked separately from shell cost; jack structures JACK-LF/RF/LR/RR-01 are v0.2"])
    print("bom: master_bom.csv (%d parts), purchased_components.csv" % len(reg))


if __name__ == "__main__":
    main()
