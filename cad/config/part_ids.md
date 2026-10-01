# Part identification

One ID per part, used everywhere: CAD registry, drawings, BOM, cut lists, renderings, manual, cost and
weight reports. `scripts_code/validate_model.py` reads the SYSTEM and LOCATION tables below and fails the
build on a malformed or duplicate ID.

## Grammar

```
SYSTEM-LOCATION-NUMBER
NUMBER = optional role letter + 2 or 3 digits     e.g. 01, 001, V03 (vertical), H01 (horizontal)
regex:  ^[A-Z]{2,5}-[A-Z]{1,4}-[A-Z]?[0-9]{2,3}$
```

## SYSTEM codes

| Code | Meaning | Role |
|---|---|---|
| `FLR` | Floor structure | PRIMARY STRUCTURAL FRAME |
| `WALL` | Wall frame | PRIMARY STRUCTURAL FRAME |
| `ROOF` | Roof frame | PRIMARY STRUCTURAL FRAME |
| `NOSE` | Nose (cab-over) frame | PRIMARY STRUCTURAL FRAME |
| `JACK` | Jack attachment structure | PRIMARY STRUCTURAL FRAME (safety-critical) |
| `TIE` | Truck tie-down structure | PRIMARY STRUCTURAL FRAME (safety-critical) |
| `UTIL` | Owner accessory T-slot rail | OWNER ACCESSORY T-SLOT RAIL (not primary structure) |
| `SKIN` | Exterior skin panel | Bonded shear diaphragm |
| `ENV` | Envelope solid (v0.1 only) | Reference geometry |
| `DOOR` | Door (purchased) | Purchased component |
| `WIN` | Window (purchased) | Purchased component |
| `RACK` | Roof-rack mounting boss | Structural provision (ADR 0003) |
| `BRKT` | Bracket / gusset / joining plate | Joint hardware |

## LOCATION codes

| Code | Meaning |
|---|---|
| `L` / `R` | Left (driver, +Y) / right (passenger, -Y) |
| `F` / `B` | Front (toward cab) / back (rear) |
| `X` | Transverse crossmember |
| `LF` `RF` `LR` `RR` | Corners: left-front, right-front, left-rear, right-rear |
| `N` | Nose |
| `C` | Centerline |
| `ROOF` | Roof surface |
| `TUB` `BODY` `NOSE` | Envelope regions (ENV only) |

`B` is used for "rear" so that `R` always means right.

## Examples

```
FLR-L-001  FLR-R-001  FLR-X-001        floor longitudinal / rail / crossmember
WALL-L-V01  WALL-L-H01                 wall vertical / horizontal
ROOF-X-01   NOSE-L-01
UTIL-L-01  UTIL-R-02  UTIL-F-01        owner accessory T-slot rails
JACK-LF-01  JACK-RF-01  JACK-LR-01  JACK-RR-01
SKIN-L-01  SKIN-R-01  SKIN-ROOF-01  SKIN-NOSE-02  SKIN-B-01
ENV-TUB-01  DOOR-B-01  WIN-N-01  RACK-ROOF-03
```

A member may serve as both PRIMARY STRUCTURAL FRAME and OWNER ACCESSORY T-SLOT RAIL only deliberately,
with a `note` in its `frame_member()` call explaining why.
