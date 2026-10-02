# Truck data

All truck values live in `cad/config/dimensions.json` (`truck` = 2011 F-350 base, `truck_variants` = per
truck overrides). This page records **where each number came from**. Accessed 2026-10-01.

## 2011 Ford F-350 Super Duty (design truck)

| Value | Used | Source / basis | Confidence |
|---|---|---|---|
| Bed length at floor, 8 ft / 6.75 ft | 98.0 / 81.8 in | Edmunds 2011 F-350 specs; cars.com (98 in) | published |
| Wheelbase, crew cab 6.75 / 8 ft | 156.2 / 172.4 in | Ford 2011 RV & Trailer Towing Guide, slide-in camper chart | official |
| Max camper cargo, 4x4 SRW crew 156.2 in WB | 1,650-2,905 lb by engine | Ford 2011 RV & Trailer Towing Guide p.13 (Camper Pkg 471 required) | official |
| Max camper cargo, 4x4 SRW crew 172.4 in WB | 1,438-3,002 lb by engine | same | official |
| Ground to top of closed tailgate | 59-60 in (F-350 SRW) | same guide, 5th-wheel tailgate clearance table | official |
| Inside box height | 20.0 in | ford-trucks.com 2011 spec summary; cars.com (20 in) | published |
| Between wheelhouses | 50.9 in | ford-trucks.com 2011 spec summary; cars.com (51 in) | published |
| Tailgate width | 61 in | ford-trucks.com spec summary (search excerpt; page blocked) | unconfirmed |
| Ground to bed floor | 39.5 in | 59.5 tailgate height − 20.0 box depth; 4x4 unloaded upper bound | derived |
| Cab roof above bed floor | 41.5 in | 80.8 in overall height (iseecars, crew 4x4) − 39.5 | derived |
| Rear axle aft of bed front wall | 35.0 (6.75) / 51.2 (8) in | Wheelbase difference = bed difference, so axle-to-tailgate is constant; Ford cab-to-axle 40 / 56.2 in (quoted from a Ford manual on a ford-trucks.com forum) less ~5.5 in cab gap + wall | derived, **measure** |
| Inside width at floor/top, rail width, wheel-well height/length | 66 / 6.5 / 10.5 / 34 in | No reliable 2011 figure found (2023+ Super Duty max inside width 66.9 in) | **estimate, measure** |

Ford's guidance (2011 guide p.13): camper CG data for each qualifying truck is printed on the **Consumer
Information Sheet** in the glovebox; trucks that do not qualify are marked "not recommended for camper use."
Ford also recommends a dimensionally stable spacer block between the bed headboard and the camper floor.

## Half-ton (fit study only)

Published bed data (armorthane.com truck bed dimension chart, from maker spec sheets):

| Truck | Box lengths at floor | Between wells | Depth | Notes |
|---|---|---|---|---|
| Ford F-150 (2021+) | 67.1 / 78.9 / 97.6 in | 50.6 | 21.4 | modeled as F150_55 / F150_65 |
| Chevrolet Silverado 1500 (2019+) | 69.9 / 79.4 / 98.2 | 50.6 | 22.4 | deeper box: body underside would clash |
| Ram 1500 (2019+) | 67.4 / 76.3 | 51.0 | 21.4-21.5 | tailgate opening 60.0 |
| Toyota Tundra (2022+) | 65.6 / 77.6 / 96.5 | 48.7 | 20.9 | tub base 49.4 does **not** fit between wells |

Payload: typical crew-cab 4x4 half-tons ~1,300-2,000 lb; the highest 2026 advertised figure is 2,440 lb (F-150).
Options can remove 600-700 lb of capacity on otherwise identical trucks (theweeklydriver.com, tfltruck.com).
Ford's 2011 guide allows F-150 campers only with the Heavy-Duty Payload Package (option 627).
**Estimates in the model:** bed floor height 35 in, cab roof 42 in above bed, tailgate opening 60 in, axle
positions (wheelbase difference = bed difference; absolute value not sourced).

## Toyota Tacoma (fit study only)

| Generation | Box lengths | Between wells | Depth | Payload |
|---|---|---|---|---|
| 2005-2015 (2nd) | ~60.5 / ~73.5 in | 41.5 | ~18 | — |
| 2016-2023 (3rd), modeled | 60.5 / 73.7 | 41.5 | 19.1 | 1,050-1,445 lb (2021) |
| 2024+ (4th) | 60.3 / 73.5 | 44.7 | 20.2 | up to 1,705 lb (5 ft, gas) |

Sources: armorthane.com chart; tustintoyota.com 2026 bed specs; kimboliving.com Tacoma bed dimensions by year;
earnhardttoyota.com 2021 guide. Truck Camper Adventure notes the Tacoma's axle sits far forward relative to the
bed, so a camper's CG generally cannot be brought over or ahead of it.
**Estimates in the model:** bed floor 33 in, cab roof 37.5 in above bed, tailgate opening 53 in, axle position.

## Camper CG and overhang guidance
- Truck Camper Adventure, "Truck Camper Center of Gravity: Getting it Right": CG in front of the rear axle;
  roughly 10-20% of camper weight on the front axle.
- Northern Lite fit guide: measure bed front wall to rear-axle center; the camper CG must be forward of that distance.
- Owner forums (Wander the West, Expedition Portal): campers that overhang the bed generally require the
  tailgate removed; long-bed campers on short beds move the CG behind the axle.
- Tailgates are typically rated ~200-500 lb and cables are rarely rated (SlashGear). Never a camper support.

## Files
- `fit_study.md`, `fit_matrix.csv`: generated verdicts per truck.
- `measurement_templates/f350_measurement_sheet.pdf`: the next physical action.
- `ford_f350/README.md`: notes specific to the owner's truck.
