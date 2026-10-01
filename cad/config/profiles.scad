// Profile catalog lookup. Data lives in dimensions.json -> PROFILES:
// [name, kind, w, h, wall, material, lb_per_in]

function profile(name) = let(i = search([name], PROFILES)[0])
    assert(i != [], str("Unknown profile ", name)) PROFILES[i];
function profile_w(name)        = profile(name)[2];
function profile_h(name)        = profile(name)[3];
function profile_wall(name)     = profile(name)[4];
function profile_material(name) = profile(name)[5];
function profile_lb_per_in(name)= profile(name)[6];

MIN_WELDED_WALL = 0.125;  // ADR 0001: owner-welded members

// 2D section centered on origin. Tubes are hollow; T-slot is drawn as a solid square with slots.
module profile_section(name) {
    p = profile(name);
    w = p[2]; h = p[3]; t = p[4];
    if (p[1] == "TSLOT") {
        slot = w * 0.26;
        difference() {
            square([w, h], center = true);
            for (a = [0, 90, 180, 270]) rotate(a)
                translate([w / 2 - slot / 2, 0]) square([slot, slot], center = true);
        }
    } else {
        difference() {
            square([w, h], center = true);
            square([w - 2 * t, h - 2 * t], center = true);
        }
    }
}
