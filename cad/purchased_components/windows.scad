// Window placeholders: one per side wall, optional raked nose window.
WIN_PROUD = 0.3;

module side_windows() {
    x = camper_rear_x + window_side_center_from_rear;
    for (s = [["L", 1], ["R", -1]]) {
        y = s[1] * (camper_body_width / 2);
        part_echo(str("WIN-", s[0], "-01"), "PURCHASED", "SIDE WINDOW PLACEHOLDER",
                  size = [window_side_width, WIN_PROUD, window_side_height], position = [x, y, window_side_center_z],
                  cost_key = "window", status = "CONCEPT");
        color(COLOR_GLASS) translate([x - window_side_width / 2, y - (s[1] < 0 ? WIN_PROUD : 0), window_side_center_z - window_side_height / 2])
            cube([window_side_width, WIN_PROUD, window_side_height]);
    }
}

module nose_window() {
    if (WINDOW_NOSE_ENABLED) {
        h = roof_eave_z - nose_bottom_z;
        rake = atan(nose_top_setback / h);            // face angle from vertical
        c = [nose_front_x - nose_top_setback / 2, 0, nose_bottom_z + h / 2];
        part_echo("WIN-N-01", "PURCHASED", "NOSE WINDOW PLACEHOLDER (OPTIONAL)",
                  size = [WIN_PROUD, window_nose_width, window_nose_height], position = c, rotation = [0, -rake, 0],
                  cost_key = "window", status = "CONCEPT");
        color(COLOR_GLASS) translate(c) rotate([0, -rake, 0])
            translate([-WIN_PROUD / 2, -window_nose_width / 2, -window_nose_height / 2])
                cube([WIN_PROUD, window_nose_width, window_nose_height]);
    }
}
