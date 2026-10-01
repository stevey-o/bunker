"""bom/weight_report.md: first-pass dry weight vs target, with interior-height sensitivity."""
from common import GENERATED_HEADER, ROOT
from estimates import height_sensitivity, load, totals, weight

TARGET = (850, 950)


def main():
    cfg, p = load()
    rows = weight(cfg, p)
    lo, hi = totals(rows)
    b = cfg["estimate_basis"]
    jl, jh = b["jacks_lb_set"]["low"], b["jacks_lb_set"]["high"]
    s = height_sensitivity(cfg)
    L = ["<!-- " + GENERATED_HEADER.format(script="generate_weight_report.py") + " -->",
         "# Weight report - v%s envelope" % cfg["version"], "",
         "**Status: CONCEPT estimate.** Area-based coefficients, not a frame take-off. Replace in v0.2.", "",
         "| Item | Low (lb) | High (lb) | Basis |", "|---|---:|---:|---|"]
    L += ["| %s | %.0f | %.0f | %s |" % r for r in rows]
    L += ["| **Shell dry weight, excl. jacks** | **%.0f** | **%.0f** | |" % (lo, hi),
          "| Jacks (4), tracked separately | %d | %d | |" % (jl, jh),
          "| **Shell incl. jacks** | **%.0f** | **%.0f** | |" % (lo + jl, hi + jh), "",
          "## Against the target", "",
          "Target dry weight: %d-%d lb." % TARGET,
          "Estimate excluding jacks: **%.0f-%.0f lb**; including jacks: **%.0f-%.0f lb**." % (lo, hi, lo + jl, hi + jh), "",
          "The %d-%d lb target is reachable only **without jacks** and only at the low end of the range, which "
          "needs disciplined interior paneling. Interior panel and skin thickness are the two biggest levers "
          "(see `time_cost/cost_reduction_opportunities.md`). This is not an achieved weight." % TARGET, "",
          "## Sensitivity: interior height", "",
          "**Each +1 in of interior_height adds %.1f-%.1f lb and $%.0f-%.0f.** "
          "For comparison, 80 in vs. a 76 in interior costs roughly %.0f-%.0f lb and $%.0f-%.0f "
          "versus a 76 in interior. Skin sheet count moves in whole-sheet steps, so the dollar figure is lumpy." % (
              s[0], s[1], s[2], s[3], 4 * s[0], 4 * s[1], 4 * s[2], 4 * s[3]), "",
          "Payload reservations (not in dry weight): power zone %d lb, roof rack + panels %d lb (ADR 0003)." % (
              cfg["payload_reservations"]["power_zone_lb"]["value"], cfg["payload_reservations"]["roof_rack_lb"]["value"]),
          ""]
    (ROOT / "bom" / "weight_report.md").write_text("\n".join(L))
    print("weight: %.0f-%.0f lb excl. jacks; +1in height = %.1f-%.1f lb" % (lo, hi, s[0], s[1]))


if __name__ == "__main__":
    main()
