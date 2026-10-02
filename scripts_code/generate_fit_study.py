"""Multi-truck fit study: the FIXED camper (sized to the DESIGN_TRUCK) checked against every truck variant.

Writes truck_data/fit_study.md and truck_data/fit_matrix.csv. Each criterion is PASS / CHECK / FAIL:
  FAIL  = physically does not fit, or violates a safety rule (CG behind rear axle, over payload rating)
  CHECK = depends on the specific truck (door-jamb sticker) or needs a design accommodation
"""
import csv

from common import GENERATED_HEADER, ROOT, load_config, params, variant_names
from estimates import center_of_gravity

OUT = ROOT / "truck_data"
MIN_SIDE = 0.5        # in, minimum lateral clearance per side
MIN_CAB = 3.0         # in, nose over cab roof
MIN_CG_AHEAD = 2.0    # in, loaded CG ahead of rear axle for PASS (CHECK between 0 and this)


def grade(ok, check=False):
    return "PASS" if ok else ("CHECK" if check else "FAIL")


def evaluate(cfg, v):
    p = params(cfg, v)
    meta = cfg["truck_variants"][v]
    m_dry, x_dry, z_dry = center_of_gravity(cfg, p)
    m_load, x_load, z_load = center_of_gravity(cfg, p, loaded=True)
    cg_ahead = x_load - p["rear_axle_x"]
    rating = meta["camper_cargo_rating_lb"]
    rows = [
        ("Tub base between wheel wells", "%.2f in/side" % p["wheel_well_side_clearance"],
         grade(p["wheel_well_side_clearance"] >= MIN_SIDE)),
        ("Tub step above wheel wells", "%.2f in" % p["wheel_well_top_clearance"],
         grade(p["wheel_well_top_clearance"] >= MIN_SIDE)),
        ("Tub through tailgate opening", "%.2f in/side" % p["tailgate_side_clearance"],
         grade(p["tailgate_side_clearance"] >= MIN_SIDE, p["tailgate_side_clearance"] >= 0)),
        ("Tub between bed sides", "%.2f in/side" % p["bed_side_clearance"], grade(p["bed_side_clearance"] >= MIN_SIDE)),
        ("Body underside over bed rails", "%.2f in" % p["rail_clearance"],
         grade(p["rail_clearance"] >= MIN_SIDE, p["rail_clearance"] > -2)),
        ("Nose over cab roof", "%.2f in" % p["cab_clearance"], grade(p["cab_clearance"] >= MIN_CAB)),
        ("Rear overhang past bed end", "%.1f in" % p["rear_overhang"],
         "PASS" if p["rear_overhang"] <= 0 else "CHECK"),
        ("Loaded CG vs rear axle", "%+.1f in (+ = ahead)" % cg_ahead,
         "PASS" if cg_ahead >= MIN_CG_AHEAD else ("CHECK" if cg_ahead >= 0 else "FAIL")),
        ("Loaded camper vs camper cargo rating", "%.0f lb vs %d-%d lb" % (m_load, rating["low"], rating["high"]),
         "PASS" if m_load <= rating["low"] else ("CHECK" if m_load <= rating["high"] else "FAIL")),
    ]
    verdict = "FAIL" if any(r[2] == "FAIL" for r in rows) else ("CONDITIONAL" if any(r[2] == "CHECK" for r in rows) else "PASS")
    return dict(variant=v, label=meta["label"], family=meta["family"], tailgate=p["TAILGATE"], rows=rows, verdict=verdict,
                m_dry=m_dry, m_load=m_load, cg_ahead=cg_ahead, x_load=x_load, z_load=z_load, rating=rating, p=p)


def main():
    cfg = load_config()
    res = [evaluate(cfg, v) for v in variant_names(cfg)]
    crit = [r[0] for r in res[0]["rows"]]
    with open(OUT / "fit_matrix.csv", "w", newline="") as f:
        f.write("# " + GENERATED_HEADER.format(script="generate_fit_study.py") + "\n")
        w = csv.writer(f)
        w.writerow(["variant", "truck", "tailgate", "verdict"] + crit)
        for r in res:
            w.writerow([r["variant"], r["label"], r["tailgate"], r["verdict"]] + ["%s (%s)" % (g, val) for _, val, g in r["rows"]])
    design = cfg["build"]["DESIGN_TRUCK"]["value"]
    L = ["<!-- " + GENERATED_HEADER.format(script="generate_fit_study.py") + " -->",
         "# Multi-truck fit study", "",
         "One camper, sized to the design truck **%s**, checked against each truck. The camper does not change "
         "shape per truck. **Status: CONCEPT.** Truck values other than the 2011 F-350 are published bed "
         "dimensions plus estimates (see `truck_data/README.md`); weights and CG are first-pass estimates." % design, "",
         "Loaded camper = dry estimate (mean) + jacks + power-zone and roof-rack reservations + %d lb owner gear. "
         "CG is computed from envelope face centroids (`scripts_code/estimates.py`), not the floor midpoint." % cfg["camper"]["owner_gear_allowance_lb"]["value"], "",
         "## Summary", "", "| Truck | Tailgate | Verdict | Loaded CG vs axle | Loaded camper | Camper cargo rating |",
         "|---|---|---|---|---|---|"]
    for r in res:
        L.append("| %s | %s | **%s** | %+.1f in | %.0f lb | %d-%d lb |" % (r["label"], r["tailgate"], r["verdict"], r["cg_ahead"],
                                                                     r["m_load"], r["rating"]["low"], r["rating"]["high"]))
    L += ["", "## Criteria by truck", "", "| Criterion | " + " | ".join(r["variant"] for r in res) + " |",
          "|---|" + "---|" * len(res)]
    for i, c in enumerate(crit):
        L.append("| %s | %s |" % (c, " | ".join("%s<br>%s" % (r["rows"][i][2], r["rows"][i][1]) for r in res)))
    L += ["", "## Rules applied", "",
          "- Camper CG must be **at or ahead of the rear axle** (Ford: CG data on the truck's Consumer Information Sheet; "
          "Northern Lite: camper CG must be forward of the bulkhead-to-axle distance). PASS needs >= %.0f in margin." % MIN_CG_AHEAD,
          "- Loaded camper must not exceed the truck's camper cargo rating. A range means it depends on engine/options: "
          "read the door-jamb sticker.",
          "- The tailgate is never structural (hard rule). Overhang means the camper floor cantilevers past the bed end; "
          "the tailgate is lowered or removed and must not carry load.",
          "- Lateral clearance >= %.1f in per side; nose >= %.0f in over the cab roof." % (MIN_SIDE, MIN_CAB), ""]
    (OUT / "fit_study.md").write_text("\n".join(L))
    print("fit study: " + ", ".join("%s %s" % (r["variant"], r["verdict"]) for r in res))
    return res


if __name__ == "__main__":
    main()
