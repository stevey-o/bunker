// MINUTEMAN camper shell - top-level assembly and view switch.
//   openscad -D 'VIEW="truck_fit"' -D 'TRUCK="LONG"' -o out.png main.scad
// VIEW: "exterior" | "truck_fit" | "interior" | "registry" | "proj"
// Units: inches. Do not put literal dimensions here; use config variables.

include <config/dimensions.scad>
include <config/build_variant.scad>
include <config/materials.scad>
include <config/profiles.scad>
include <config/hardware.scad>
include <lib/registry.scad>
include <camper_envelope.scad>
include <truck_reference.scad>
include <purchased_components/door.scad>
include <purchased_components/windows.scad>
include <utility_rails/utility_rails.scad>
include <provisions.scad>
include <human_reference.scad>

assert(FRAME_SYSTEM == "HYBRID" || FRAME_SYSTEM == "BOLTED_TUBE" || FRAME_SYSTEM == "TSLOT", "bad FRAME_SYSTEM");

module camper_exterior() {
    envelope_outer();
    rear_door();
    side_windows();
    nose_window();
    roof_rack_bosses();
}

module camper_interior() {
    envelope_shell(cut_roof = true, cut_rear = true);
    utility_rails();
    power_zone();
    wire_chase();
    translate([camper_rear_x + camper_lower_length * 0.4, 20, interior_floor_z]) rotate([0, 0, 180]) human();
}

// 2D projections for scripts_code/export_drawings.py. PLANE maps 3D -> 2D:
//   side: (x, z)   front: (y, z) viewed from the front   top: (x, y)
module plane_map() {
    if (PLANE == "side") multmatrix([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]) children();
    else if (PLANE == "front") multmatrix([[0, 1, 0, 0], [0, 0, 1, 0], [1, 0, 0, 0], [0, 0, 0, 1]]) children();
    else children();
}

module proj_part() {
    if (PART == "tub_lower") tub_lower();
    else if (PART == "tub_upper") tub_upper();
    else if (PART == "body_lower") body_lower();
    else if (PART == "body_upper") body_upper();
    else if (PART == "envelope") { tub_lower(); tub_upper(); body_lower(); body_upper(); }
    else if (PART == "door") rear_door();
    else if (PART == "windows") { side_windows(); nose_window(); }
    else if (PART == "bosses") roof_rack_bosses();
    else if (PART == "rails") utility_rails();
    else if (PART == "truck_bed") truck_bed();
    else if (PART == "truck_cab") truck_cab();
    else if (PART == "truck_wheels") truck_wheels();
    else if (PART == "human_inside") translate([camper_rear_x + camper_lower_length * 0.45, -4, interior_floor_z]) human();
    else if (PART == "human_ground") translate([camper_rear_x - 30, camper_body_width / 2 + 18, -truck_bed_floor_height]) human();
}

if (VIEW == "exterior") camper_exterior();
else if (VIEW == "truck_fit") {
    camper_exterior();
    truck_reference();
    translate([camper_rear_x - 30, camper_body_width / 2 + 18, -truck_bed_floor_height]) human();
}
else if (VIEW == "interior") camper_interior();
else if (VIEW == "registry") {
    envelope_registry(); rear_door(); side_windows(); nose_window(); roof_rack_bosses(); utility_rails();
}
else if (VIEW == "proj") projection() plane_map() proj_part();
