# Drafting standards used for the MINUTEMAN drawing set

The drawings follow the **ASME Y14** family as far as a generated PDF practically can. Implementation:
`scripts_code/drawlib.py`.

| Standard | Covers | How the drawings apply it |
|---|---|---|
| ASME Y14.1 | Sheet sizes and format | ANSI C (22 x 17 in) landscape; zoned border (columns 1-8, rows A-D); title block with project, title, size, drawing number (MM-A0n), revision, scale, date, sheet n of 5, drawn/checked, status; tolerance block; third-angle projection symbol |
| ASME Y14.35 | Revisions | Revision block top-right: REV / DESCRIPTION / DATE / APPROVED. Rev A = v0.1 release, Rev B = 97 in length + this format |
| ASME Y14.2 | Line conventions and lettering | Thick visible lines; thin dashed hidden lines (rails behind walls, door beyond a section); long-short center lines (centerline, rear-axle CL); **phantom lines for the truck** (adjacent / reference part); thin dimension and extension lines; upper-case Gothic (Helvetica) lettering |
| ASME Y14.3 | Orthographic and section views | Third-angle views (plan above elevation); cutting-plane lines with view arrows and letters (B-B, C-C on A01; D-D, E-E on A03; A-A on A04); detail view (DETAIL B) with its own scale |
| ASME Y14.5 | Dimensioning | Unidirectional text (reads from the bottom of the sheet); decimal inch with no leading zero (.5); reference dimensions in parentheses; **flag notes** (numbered triangles): flag 1 = VERIFY ON TRUCK, flag 2 = estimate; general tolerance block; "interpret per ASME Y14.5-2018" |

Style borrowed from builder layout sheets (the owner's van reference image): chained interior height
dimensions (floor → rail → rail → rail → ceiling), overall-length chains above the view, and labeled leaders
to the periphery naming each feature (rails, window, power zone, wire chase, nose storage, 6'7" figure).

Deliberate deviations: GD&T feature control frames are not used (an envelope has no fabricated features
yet). Tolerances are envelope-level until v0.3 part drawings exist.

Sources (accessed 2026-10-01): Wikipedia "ASME Y14.5"; GrabCAD tutorial "Overview of ASME Y14 series drawing
standards"; ANSI blog "What are the ASME Y14.5 and ASME Y14.100 standards".
