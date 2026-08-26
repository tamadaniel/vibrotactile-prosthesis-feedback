# Enclosure (3D-printable)

![Enclosure views](enclosure_views.png)

Two-part 3D-printable housing that holds the battery and the circuit board and clamps onto the distal prosthetic tube. Three features make the assembly tool-free:

- **C-shaped clamp** — snaps onto the tube by interference fit; no screws, no structural modification of the prosthesis.
- **Motor recess** — the coin motor seats in a recess facing the tube, so closing the clamp automatically presses the motor against the prosthesis. There is no separate motor mounting step, and the vibration is injected directly into the prosthesis structure.
- **Three ⌀3.75 mm holes (4 mm pitch)** on the outer face, so discrete through-hole indicator LEDs can be soldered to sit flush with the surface: charging, power-on, and motor activity stay visible with the device closed.

## Files

| File | Description |
|---|---|
| `enclosure_housing.stl` / `.SLDPRT` | main body: clamp, motor recess, LED holes, battery/circuit compartment |
| `enclosure_lid.stl` / `.SLDPRT` | closing lid |
| `gcode/housing+lid_K1Max_0.4_PLA.gcode` | both parts, PLA profile (as used in the study) |
| `gcode/housing+lid_K1Max_0.4_PETG.gcode` | both parts, PETG profile |
| `gcode/lid_only_K1Max_0.4_PETG.gcode` | lid only |

## Measured dimensions (from the meshes)

| Feature | Value |
|---|---|
| Housing envelope | 66.3 × 23.0 × 34.3 mm |
| Lid | 31.8 × 26.6 × 1.9 mm |
| C-clamp bore | ⌀ ≈ 33.6 mm |
| LED holes | 3 × ⌀3.75 mm, 4 mm pitch |
| Outer face thickness at the LED holes | ≈ 2 mm |
| Complete device mass (enclosure + battery + circuit + motor + sensor) | 22 g |

## Print settings

Both profiles were generated with Creality Print 4.3.7 for a **Creality K1 Max**, 0.4 mm nozzle. The prototype used in the study was printed in **PLA**; a PETG profile is also provided, since PETG is the tougher choice for the clamp arms, which flex on every installation.

| Parameter | PLA (as used) | PETG (alternative) |
|---|---|---|
| Filament | Generic PLA, 1.75 mm | Creality CR-PETG, 1.75 mm |
| Nozzle / bed temperature | 230 °C / 45 °C | 250 °C / 80 °C |
| Layer height (first layer) | 0.25 mm (0.20 mm) | 0.20 mm (0.20 mm) |
| Wall line count | 2 (≈0.87 mm) | 2 (≈0.87 mm) |
| Top / bottom layers | 4 / 4 | 4 / 4 |
| Infill | grid, 50 % | grid, 15 % |
| Supports | enabled | enabled |
| Bed adhesion | brim | auto brim |
| Print speed | 250 mm/s (outer wall 175, top/bottom 175) | 300 mm/s (outer wall 200, top/bottom 200) |
| Flow ratio | 95 % | 100 % |
| Both parts | 30 min, 6.35 m (≈19 g) | 33 min, 4.79 m (≈14 g) |

Filament figures include brim and supports, so the finished parts weigh less. Z-seam is set to *sharpest corner / hide seam*, and *only one wall for roofing* is enabled in both profiles.

## Printing notes

The clamp relies on the elasticity of the print for its interference fit, so orient the part such that layer lines do not run perpendicular to the clamp arms — otherwise the arms tend to delaminate when snapped onto the tube. Verify the bore against the tube you are targeting before printing a batch (the modular standard is 30 mm; the bore in this model is larger and was matched to the tube used in our prototype), and adjust the diameter in the SolidWorks part if needed.
