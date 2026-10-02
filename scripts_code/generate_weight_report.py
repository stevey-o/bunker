"""bom/weight_report.md: first-pass dry weight vs target, with interior-height sensitivity."""
from common import GENERATED_HEADER, ROOT
from estimates import height_sensitivity, load, totals, weight

TARGET = (850, 950)


def verdict(lo, hi, jl, jh):
    """Plain-language comparison with the target, computed rather than hard-coded."""
    t_lo, t_hi = TARGET
    if hi <= t_hi:
        return "The estimate is within the %d-%d lb target even at the high end (excluding jacks)." % TARGET
    if lo <= t_hi:
        return ("The %d-%d lb target is reachable only **without jacks** and only at the low end of the range, "
                "which needs disciplined interior paneling. Interior panel and skin thickness are the two biggest "
                "levers (see `time_cost/cost_reduction_opportunities.md`). This is not an achieved weight." % TARGET)
    return ("**The %d-%d lb target is not reachable with this envelope.** Even the low estimate (%.0f lb, excluding "
            "jacks) is %.0f lb over the top of the target. The full-length 97 in camper (ADR 0004) is the main reason. "
            "Levers: 0.040 in wall skin, lighter interior panel, or a shorter camper. "
            "This is an estimate, not a weighed result." % (t_lo, t_hi, lo, lo - t_hi))


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
          verdict(lo, hi, jl, jh), "",
          "## Sensitivity: interior height", "",
          "**Each +1 in of interior_height adds %.1f-%.1f lb and $%.0f-%.0f** (averaged over +/-4 in). "
          "For comparison, 80 in vs. a 76 in interior costs roughly %.0f-%.0f lb and $%.0f-%.0f. "
          "Skin sheet count moves in whole-sheet steps, so actual dollar changes are lumpy." % (
              s[0], s[1], s[2], s[3], 4 * s[0], 4 * s[1], 4 * s[2], 4 * s[3]), "",
          "Payload reservations (not in dry weight): power zone %d lb, roof rack + panels %d lb (ADR 0003)." % (
              cfg["payload_reservations"]["power_zone_lb"]["value"], cfg["payload_reservations"]["roof_rack_lb"]["value"]),
          ""]
    (ROOT / "bom" / "weight_report.md").write_text("\n".join(L))
    print("weight: %.0f-%.0f lb excl. jacks; +1in height = %.1f-%.1f lb" % (lo, hi, s[0], s[1]))


if __name__ == "__main__":
    main()
