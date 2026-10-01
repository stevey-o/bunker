// Build variant / view selection. FRAME_SYSTEM and TRUCK defaults are generated into
// dimensions.scad from dimensions.json; override any of these from the CLI, e.g.
//   openscad -D 'TRUCK="LONG"' -D 'VIEW="truck_fit"' main.scad
//   FRAME_SYSTEM: "HYBRID" | "BOLTED_TUBE" | "TSLOT"  (ADR 0001)
//   TRUCK:        "SHORT" | "LONG"
VIEW = "exterior";   // "exterior" | "truck_fit" | "interior" | "registry" | "proj"
PLANE = "side";      // projection plane for VIEW="proj": "side" | "front" | "top" | "xsection"
CUT_X = 0;           // section station for PLANE="xsection"
PART = "envelope";   // projection subject for VIEW="proj" (see main.scad proj_part)
