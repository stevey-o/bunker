// Simplified Ford F-350 reference (transparent gray). Visual and clearance reference only;
// every interface dimension is VERIFY ON TRUCK in dimensions.json.
// Origin: bed-floor top, centerline, inner face of bed front wall. +X forward.

ground_z = -truck_bed_floor_height;
bed_outer_w = truck_bed_inner_width_top + 2 * truck_bed_rail_width;
body_bot_z = -truck_body_bottom_below_bed;
roof_front_x = cab_back_x + truck_cab_roof_length;
hood_x = roof_front_x + truck_windshield_run;
front_axle_x = rear_axle_x + truck_wheelbase;
front_x = front_axle_x + truck_front_overhang;
wheel_r = truck_tire_diameter / 2;

module truck_bed() {
    difference() {
        translate([-truck_bed_length, -bed_outer_w / 2, body_bot_z])
            cube([truck_bed_length + truck_bed_front_wall_thickness, bed_outer_w, truck_bed_rail_height - body_bot_z]);
        // bed cavity
        translate([-truck_bed_length - 1, -truck_bed_inner_width_top / 2, 0])
            cube([truck_bed_length + 1, truck_bed_inner_width_top, truck_bed_rail_height + 1]);
        // wheel arch cut-outs in the bed sides
        for (s = [-1, 1]) translate([rear_axle_x, s * bed_outer_w / 2, ground_z + wheel_r])
            rotate([90, 0, 0]) cylinder(r = wheel_r + 2, h = 30, center = true, $fn = 48);
    }
    truck_wheel_wells();
}

module truck_wheel_wells() {
    for (s = [-1, 1]) intersection() {
        translate([rear_axle_x, s * (truck_bed_inner_width_top / 2 + truck_wheel_well_width / 2) / 2, ground_z + wheel_r])
            rotate([90, 0, 0]) cylinder(r = truck_bed_floor_height + truck_wheel_well_height - wheel_r,
                                        h = (truck_bed_inner_width_top - truck_wheel_well_width) / 2, center = true, $fn = 64);
        translate([rear_axle_x - truck_wheel_well_length / 2, -bed_outer_w / 2, 0])
            cube([truck_wheel_well_length, bed_outer_w, truck_wheel_well_height]);
    }
}

module truck_cab() {
    w = truck_cab_width;
    // lower body: cab + front clip
    translate([cab_back_x, -w / 2, body_bot_z])
        cube([front_x - cab_back_x, w, truck_beltline_above_bed - body_bot_z]);
    // greenhouse with raked windshield
    hull() {
        translate([cab_back_x, -w / 2 + 3, truck_beltline_above_bed]) cube([hood_x - cab_back_x, w - 6, 0.1]);
        translate([cab_back_x, -w / 2 + 5, truck_cab_height_above_bed - 0.1]) cube([truck_cab_roof_length, w - 10, 0.1]);
    }
    // hood
    translate([hood_x, -w / 2, body_bot_z]) cube([front_x - hood_x, w, truck_hood_height_above_bed - body_bot_z]);
}

module truck_wheels() {
    for (x = [rear_axle_x, front_axle_x], s = [-1, 1])
        translate([x, s * truck_track_width / 2, ground_z + wheel_r])
            rotate([90, 0, 0]) cylinder(r = wheel_r, h = 11.5, center = true, $fn = 48);
}

module truck_reference() {
    color(COLOR_TRUCK) { truck_bed(); truck_cab(); }
    color([0.15, 0.15, 0.15, 0.55]) truck_wheels();
}

module ground_plane(x0, x1, w) {
    color([0.92, 0.92, 0.90]) translate([x0, -w / 2, ground_z - 0.5]) cube([x1 - x0, w, 0.5]);
}
