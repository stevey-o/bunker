// Structural provisions only (ADR 0003): roof-rack bosses, reserved power floor zone, wire chase.
// No electrical design. Zones are reserved geometry, not components.

module roof_rack_bosses() {
    n = len(roof_rack_boss_from_rear);
    for (i = [0 : n - 1], s = [0, 1]) {
        y = (s == 0 ? 1 : -1) * (camper_body_width / 2 - roof_rack_boss_edge_inset);
        x = camper_rear_x + roof_rack_boss_from_rear[i];
        z = roof_eave_z + crown_dz(y);
        id = str("RACK-ROOF-", i * 2 + s + 1 < 10 ? "0" : "", i * 2 + s + 1);
        part_echo(id, "PROVISION", "ROOF-RACK MOUNTING BOSS", size = [roof_rack_boss_diameter, roof_rack_boss_diameter, roof_rack_boss_height],
                  position = [x, y, z], cost_key = "rack_boss", status = "CONCEPT",
                  note = "Must land on a roof crossmember in v0.2");
        color(COLOR_FRAME) translate([x, y, z - 0.25]) cylinder(d = roof_rack_boss_diameter, h = roof_rack_boss_height + 0.25, $fn = 24);
    }
}

module power_zone() {
    x1 = camper_front_x - wall_thickness - power_zone_from_front;
    color(COLOR_PROVISION) translate([x1 - power_zone_length, -power_zone_width / 2, interior_floor_z])
        cube([power_zone_length, power_zone_width, 0.25]);
}

module wire_chase() {
    color(COLOR_PROVISION)
        translate([camper_front_x - wall_thickness - wire_chase_size,
                   camper_body_width / 2 - wall_thickness - wire_chase_size, camper_lower_tub_height + wall_thickness])
            cube([wire_chase_size, wire_chase_size, ceiling_z - camper_lower_tub_height - wall_thickness]);
}
