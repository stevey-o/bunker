// Material lookup and the rendering color convention (PROJECT_HANDOFF.md §9).
// Densities live in dimensions.json -> MATERIALS; colors live here.

function material_density(name) = MATERIALS[search([name], MATERIALS)[0]][1];

COLOR_EXISTING   = [0.82, 0.82, 0.82];        // existing assembly
COLOR_FRAME      = [0.15, 0.40, 0.85];        // new frame pieces
COLOR_BRACKET    = [1.00, 0.55, 0.10];        // brackets
COLOR_FASTENER   = [0.85, 0.10, 0.10];        // fasteners
COLOR_SKIN       = [0.80, 0.82, 0.85];        // skin (silver)
COLOR_INSULATION = [0.95, 0.85, 0.20];        // insulation
COLOR_ADHESIVE   = [0.20, 0.70, 0.30];        // adhesive / sealant
COLOR_UTIL_RAIL  = [0.05, 0.12, 0.45];        // owner accessory T-slot rails (dark blue)
COLOR_TRUCK      = [0.45, 0.45, 0.45, 0.30];  // truck reference (transparent gray)
// Additions for v0.1 placeholders (documented in DIMENSIONS.md legend):
COLOR_PURCHASED  = [0.25, 0.25, 0.28];        // purchased component placeholder (door)
COLOR_GLASS      = [0.35, 0.55, 0.70];        // window placeholder
COLOR_PROVISION  = [0.60, 0.25, 0.70, 0.45];  // reserved provision zone (power zone, wire chase)
COLOR_HUMAN      = [0.85, 0.65, 0.45];        // 6'7" human reference
