"""bom/cost_report.md: first-pass shell material cost (excl. jacks, tooling) with height sensitivity."""
import csv

from common import GENERATED_HEADER, ROOT
from estimates import cost, height_sensitivity, load, totals, unit_prices, weight

TARGET = (4000, 6000)


def main():
    cfg, p = load()
    rows = cost(cfg, p, weight(cfg, p))
    lo, hi = totals(rows)
    jack = unit_prices()["jacks"]
    with open(ROOT / "time_cost" / "tooling_costs.csv") as f:
        tool = list(csv.DictReader(f))
    tl, th = sum(float(t["low_usd"]) for t in tool), sum(float(t["high_usd"]) for t in tool)
    s = height_sensitivity(cfg)
    big = max(rows, key=lambda r: r[2])
    L = ["<!-- " + GENERATED_HEADER.format(script="generate_cost_report.py") + " -->",
         "# Cost report - v%s envelope" % cfg["version"], "",
         "**Status: CONCEPT estimate.** Unit prices in `time_cost/material_costs.csv`; none are quotes yet.", "",
         "| Item | Low ($) | High ($) | Basis |", "|---|---:|---:|---|"]
    L += ["| %s | %s | %s | %s |" % (r[0], "{:,.0f}".format(r[1]), "{:,.0f}".format(r[2]), r[3]) for r in rows]
    L += ["| **Shell materials, excl. jacks and tooling** | **{:,.0f}** | **{:,.0f}** | |".format(lo, hi),
          "| Jacks (4), tracked separately | {:,.0f} | {:,.0f} | |".format(float(jack["low_usd"]), float(jack["high_usd"])),
          "| One-time tooling (`tooling_costs.csv`) | {:,.0f} | {:,.0f} | not shell cost |".format(tl, th), "",
          "## Against the target", "",
          "Owner target: ${:,}-${:,} (\"high-end truck topper\"). Estimate: **${:,.0f}-${:,.0f}** excluding jacks and tooling.".format(
              TARGET[0], TARGET[1], lo, hi), "",
          "The low half of the range fits the target; the high half does not. The largest line is **%s** "
          "(up to ${:,.0f}). 6061 tube is priced at a realistic retail $/lb, which is above the handoff's first-pass "
          "$500-900 tube figure; get local quotes before trusting either number.".format(big[2]) % big[0], "",
          "## Sensitivity: interior height", "",
          "Each +1 in of interior_height adds **$%.0f-%.0f** (and %.1f-%.1f lb)." % (s[2], s[3], s[0], s[1]), ""]
    (ROOT / "bom" / "cost_report.md").write_text("\n".join(L))
    print("cost: ${:,.0f}-${:,.0f} excl. jacks/tooling".format(lo, hi))


if __name__ == "__main__":
    main()
