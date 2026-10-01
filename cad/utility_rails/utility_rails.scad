// OWNER ACCESSORY T-SLOT RAILS (not primary structure). Layout computed once in
// scripts_code/common.py:utility_rails() and synced as UTIL_RAILS.
// v0.1: placeholders on the interior wall faces. Attachment into frame members is a v0.2 task.

module utility_rails() {
    for (r = UTIL_RAILS) {
        id = r[0]; len = r[1]; p = r[2];
        h = profile_h(util_profile) / 2;
        // offset the rail so its back face sits on the interior wall surface
        pos = r[3] == "X" ? [p[0], p[1] - sign(p[1]) * h, p[2]] : [p[0] - h, p[1], p[2]];
        frame_member(id, util_profile, len, pos, r[3] == "X" ? [0, 0, 0] : [0, 0, 90],
                     join = "BOLTED", role = "OWNER ACCESSORY T-SLOT RAIL", col = COLOR_UTIL_RAIL,
                     note = "Must bolt into frame members, never skin-only (v0.2)");
    }
}
