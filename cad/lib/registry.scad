// Parts registry. Every part module calls part_echo(), which prints one line:
//   ECHO: "PART|{json}"
// scripts_code/render_all.py parses these into output/current_design/parts.json, which feeds the
// BOM, cut lists and weight report. Never retype part data into a spreadsheet.

function _js(s) = str("\"", s, "\"");

module part_echo(id, kind, role, profile = "", material = "", length = 0, size = [0, 0, 0],
                 position = [0, 0, 0], rotation = [0, 0, 0], mass = 0, cost_key = "",
                 join = "", status = "CONCEPT", note = "") {
    echo(str("PART|{",
        "\"id\":", _js(id), ",\"kind\":", _js(kind), ",\"role\":", _js(role),
        ",\"profile\":", _js(profile), ",\"material\":", _js(material),
        ",\"length\":", length, ",\"size\":", size,
        ",\"position\":", position, ",\"rotation\":", rotation,
        ",\"mass\":", mass, ",\"cost_key\":", _js(cost_key), ",\"join\":", _js(join),
        ",\"status\":", _js(status), ",\"note\":", _js(note), "}"));
}

// Linear extrusion member along its local +X axis, placed at `position` then rotated.
// join: "WELDED" | "BOLTED" | "BONDED". Welded members must meet MIN_WELDED_WALL (ADR 0001).
module frame_member(id, profile, length, position = [0, 0, 0], rotation = [0, 0, 0],
                    join = "BOLTED", role = "PRIMARY STRUCTURAL FRAME", col = COLOR_FRAME,
                    status = "CONCEPT", note = "") {
    assert(join != "WELDED" || profile_wall(profile) >= MIN_WELDED_WALL,
           str(id, ": welded member wall ", profile_wall(profile), " < ", MIN_WELDED_WALL, " (ADR 0001)"));
    part_echo(id, "MEMBER", role, profile, profile_material(profile), length,
              [length, profile_w(profile), profile_h(profile)], position, rotation,
              profile_lb_per_in(profile) * length, profile, join, status, note);
    translate(position) rotate(rotation)
        color(col) rotate([0, 90, 0]) linear_extrude(length) rotate(90) profile_section(profile);
}
