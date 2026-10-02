# Ford F-350 (2011) notes

The model's base truck is a **2011 F-350 Super Duty crew cab 4x4 SRW**. Sourced values and their confidence
are in `../README.md`; every interface value stays **VERIFY ON TRUCK** until measured with
`../measurement_templates/f350_measurement_sheet.pdf`.

Things to confirm on the owner's truck first, because they move the design most:
1. **Which box** (6.75 or 8 ft) and cab style. The design assumes 8 ft.
2. **Rear axle position** (sheet row 6). This decides whether the CG works.
3. **Tailgate opening width** (row 14). It sets the tub width (59.5 in now).
4. **Ground to bed floor** (row 1) and **cab roof height** (row 11). They set travel height (~10'7") and nose clearance.
5. **Camper package (option 471)** and the **door-jamb payload / Consumer Information Sheet** CG data.
