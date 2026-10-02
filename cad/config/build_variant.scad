// Build variant / view selection. FRAME_SYSTEM and TRUCK defaults are generated into
// dimensions.scad from dimensions.json; override any of these from the CLI, e.g.
//   openscad -D 'TRUCK="LONG"' -D 'VIEW="truck_fit"' main.scad
//   FRAME_SYSTEM: "HYBRID" | "BOLTED_TUBE" | "TSLOT"  (ADR 0001)
//   TRUCK:        "F350_LONG" | "F350_SHORT" | "F150_65" | "F150_55" | "TACOMA_6" | "TACOMA_5"
//   TAILGATE:     "CLOSED" | "DOWN" | "REMOVED"  (default per truck from dimensions.json)
TAILGATE = TAILGATE_DEFAULTS[TRUCK_IDX];
VIEW = "exterior";   // "exterior" | "truck_fit" | "interior" | "registry" | "proj"
PLANE = "side";      // projection plane for VIEW="proj": "side" | "front" | "top" | "xsection" | "ysection"
CUT_X = 0;           // section station for PLANE="xsection"
CUT_Y = 0;           // section station for PLANE="ysection"
PART = "envelope";   // projection subject for VIEW="proj" (see main.scad proj_part)
