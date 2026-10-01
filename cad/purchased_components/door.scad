// Rear entry door placeholder (purchased: commercial cargo-trailer / RV entry door).
// Rough opening only. Final size comes from the selected door's datasheet.
DOOR_PROUD = 0.4;

module rear_door() {
    pos = [camper_rear_x - DOOR_PROUD, door_offset_y, door_bottom_z];
    part_echo("DOOR-B-01", "PURCHASED", "REAR ENTRY DOOR PLACEHOLDER", size = [DOOR_PROUD, door_width, door_height],
              position = pos, mass = 0, cost_key = "door", status = "CONCEPT",
              note = "Rough opening; select commercial door then update dimensions.json");
    color(COLOR_PURCHASED) translate([pos[0], door_offset_y - door_width / 2, door_bottom_z])
        cube([DOOR_PROUD + ENV_EPS * 5, door_width, door_height]);
}
