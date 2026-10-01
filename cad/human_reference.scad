// 6'7" (79 in) human reference figure, feet at local z = 0, facing +X.
module human(h = human_height) {
    u = h / 8;  // head-height unit
    color(COLOR_HUMAN) {
        translate([0, 0, h - u / 2]) scale([0.8, 0.7, 1]) sphere(d = u, $fn = 24);                // head
        translate([0, 0, h - u * 1.15]) cylinder(d = u * 0.45, h = u * 0.3, $fn = 16);           // neck
        hull() {                                                                              // torso
            translate([0, 0, u * 4.1]) scale([0.55, 1, 1]) cylinder(d = u * 1.55, h = 0.1, $fn = 24);
            translate([0, 0, u * 6.8]) scale([0.55, 1, 1]) cylinder(d = u * 1.95, h = 0.1, $fn = 24);
        }
        for (s = [-1, 1]) {
            translate([0, s * u * 0.42, 0]) cylinder(d1 = u * 0.45, d2 = u * 0.7, h = u * 4.2, $fn = 16);   // legs
            translate([0, s * u * 1.05, u * 3.9]) cylinder(d1 = u * 0.35, d2 = u * 0.5, h = u * 2.95, $fn = 16); // arms
        }
    }
}
