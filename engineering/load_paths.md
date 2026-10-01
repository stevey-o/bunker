# Load paths (concept, v0.1)

Status: **CONCEPT.** These are the intended paths the v0.2 frame must realize. Nothing is sized yet.

| Load case | Path | Safety-critical |
|---|---|---|
| Dead + payload, on truck | Floor sandwich -> floor longitudinals (FLR-L/R) -> bed floor (bearing), restrained by tie-downs | yes |
| Dead + payload, on jacks | Floor/wall -> corner nodes (welded, HAZ-sized) -> JACK-LF/RF/LR/RR brackets -> jacks -> ground | yes |
| Tie-down (braking, cornering, bumps) | Camper mass -> tie-down nodes (TIE-*) in primary frame -> turnbuckles -> truck frame-mounted anchors. **Never** bed rails, tailgate, or skin | yes |
| Nose cantilever | Nose floor + walls -> front wall frame -> floor/side walls; does not bear on the cab | yes |
| Racking (lateral, torsional twist off-road) | Wall frames + **bonded skin acting as shear diaphragm** -> floor | yes |
| Roof rack + panels | Rack -> RACK-ROOF bosses -> roof crossmembers -> wall verticals. Never bare skin | yes |
| Power zone | Equipment -> T-slot tie-downs in reinforced floor zone -> floor crossmembers | yes |
| Owner accessories | Accessory -> UTIL T-slot rail -> bolts into wall verticals (not skin) | moderate |
| Wind / aero | Skin -> frame; raked nose reduces frontal pressure | no |

## Open
Each row becomes a calculation file in `engineering/calculations/` in v0.2 before any status upgrade.
