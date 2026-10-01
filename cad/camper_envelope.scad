// v0.1 camper envelope: stepped lower tub, main body, raked nose, crowned roof.
// Envelope solids only - no frame. All dimensions from config/dimensions.scad.
//
// The same builders produce the outer envelope (inset 0) and the interior volume (inset by wall /
// roof / floor thickness), so the hollow shell used for interior views stays consistent.

ENV_EPS = 0.01;
ROOF_R = (pow(camper_body_width, 2) / 4 + pow(roof_crown, 2)) / (2 * roof_crown);  // crown arc radius
CROWN_STEPS = 6;

// Plan-view rounded rectangle slab between x0..x1, width w, thickness h, base at z.
module rrect_slab(x0, x1, w, r, z, h = ENV_EPS) {
    rr = max(min(r, w / 2 - ENV_EPS, (x1 - x0) / 2 - ENV_EPS), ENV_EPS);
    translate([0, 0, z]) hull() for (x = [x0 + rr, x1 - rr], y = [-w / 2 + rr, w / 2 - rr])
        translate([x, y, 0]) cylinder(r = rr, h = h, $fn = 32);
}

// Crown height above eave at lateral offset y (circular arc).
function crown_dz(y) = sqrt(pow(ROOF_R, 2) - y * y) - (ROOF_R - roof_crown);

module tub_lower(t = 0, tf = 0) {
    translate([camper_rear_x + t, -(tub_base_width / 2 - t), tf])
        cube([camper_lower_length - 2 * t, tub_base_width - 2 * t, tub_step_z + t - tf]);
}

module tub_upper(t = 0) {
    translate([camper_rear_x + t, -(camper_lower_tub_width / 2 - t), tub_step_z + t])
        cube([camper_lower_length - 2 * t, camper_lower_tub_width - 2 * t,
              camper_lower_tub_height - tub_step_z + ENV_EPS]);
}

// Main body below the nose underside: plan rounded rectangle, full width.
module body_lower(t = 0) {
    w = camper_body_width - 2 * t;
    hull() {
        rrect_slab(camper_rear_x + t, camper_front_x - t, w, body_corner_radius - t, camper_lower_tub_height + t);
        rrect_slab(camper_rear_x + t, camper_front_x - t, w, body_corner_radius - t,
                   nose_bottom_z + (t > 0 ? nose_floor_thickness + ENV_EPS : 0));
    }
}

// Body above the nose underside, including the nose and the crowned roof (convex hull).
module body_upper(t = 0, tr = 0) {
    w = camper_body_width - 2 * t;
    r = body_corner_radius - t;
    e = roof_edge_radius;
    x0 = camper_rear_x + t;
    xb = nose_front_x - t;                       // lower nose edge
    xt = nose_front_x - nose_top_setback - t;    // top of raked nose face
    z0 = nose_bottom_z + (t > 0 ? nose_floor_thickness : 0);
    ze = roof_eave_z - tr;
    hull() {
        rrect_slab(x0, xb - e, w, r, z0);
        rrect_slab(x0, xb, w, r, z0 + e);
        rrect_slab(x0, xt, w, r, ze - e);
        // crowned roof: stacked slabs following the arc, inset at the eave for an edge radius
        for (i = [0 : CROWN_STEPS - 1]) let(y = (w / 2 - e) * (1 - i / CROWN_STEPS))
            rrect_slab(x0 + e, xt - e, 2 * y, r, ze + crown_dz(y) * (tr > 0 ? 0 : 1));
        rrect_slab(x0 + e, xt - e, 2, 0, ze + (tr > 0 ? 0 : roof_crown));
    }
}

module envelope_outer() {
    color(COLOR_SKIN) union() { tub_lower(); tub_upper(); body_lower(); body_upper(); }
}

module envelope_inner() {
    t = wall_thickness;
    union() {
        tub_lower(t, interior_floor_z);
        tub_upper(t);
        body_lower(t);
        body_upper(t, roof_thickness);
    }
}

// Hollow shell. cut_roof / cut_rear remove the roof and rear wall for interior views.
module envelope_shell(cut_roof = false, cut_rear = false, cut_left = false) {
    big = 400;
    color(COLOR_SKIN) difference() {
        union() { tub_lower(); tub_upper(); body_lower(); body_upper(); }
        envelope_inner();
        if (cut_roof) translate([-big / 2, -big / 2, ceiling_z - ENV_EPS]) cube(big);
        if (cut_rear) translate([camper_rear_x - big + wall_thickness + ENV_EPS, -big / 2, -1]) cube(big);
        if (cut_left) translate([-big / 2, 0, -1]) cube(big);
    }
}

module envelope_registry() {
    part_echo("ENV-TUB-01", "ENVELOPE", "LOWER TUB ENVELOPE", size = [camper_lower_length, camper_lower_tub_width, camper_lower_tub_height],
              position = [camper_rear_x, 0, 0], status = "CONCEPT", note = "Stepped: base width tub_base_width to tub_step_z");
    part_echo("ENV-BODY-01", "ENVELOPE", "MAIN BODY ENVELOPE", size = [camper_lower_length, camper_body_width, roof_eave_z - camper_lower_tub_height],
              position = [camper_rear_x, 0, camper_lower_tub_height], status = "CONCEPT");
    part_echo("ENV-NOSE-01", "ENVELOPE", "NOSE ENVELOPE", size = [nose_projection, camper_body_width, roof_eave_z - nose_bottom_z],
              position = [camper_front_x, 0, nose_bottom_z], status = "CONCEPT", note = "Storage/desk volume; not a sleeping platform");
    part_echo("ENV-ROOF-01", "ENVELOPE", "ROOF ENVELOPE", size = [overall_length - nose_top_setback, camper_body_width, roof_thickness + roof_crown],
              position = [camper_rear_x, 0, ceiling_z], status = "CONCEPT", note = str("Transverse crown ", roof_crown, " in"));
}
