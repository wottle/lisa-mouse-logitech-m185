# Printing

## Settings used

These come from the slicer projects in [`print/`](../print/) and were used for the
prototype build.

| Setting | Value |
|---------|-------|
| Printers | Bambu Lab A1 (Bambu Studio), Creality K2 Plus (Creality Print) |
| Nozzle | 0.4 mm |
| Layer height | 0.20 mm (first layer 0.20 mm) |
| Walls | 2 |
| Top / bottom layers | 5 / 3 |
| Infill | 15 %, grid |
| Supports | Yes — tree (auto), 30° threshold |
| Brim | Auto |
| Seam | Aligned |
| Material | PLA (PolyTerra PLA used for the prototype) |
| Nozzle / bed temp | 220 °C / 65 °C |
| Bed | Textured PEI |

Any FDM printer with roughly a 100 × 100 mm bed can print every part.

## Slicer projects

Open one of these rather than the bare STLs: they carry the **print orientation**,
supports and plate arrangement. The STLs in `models/` are in design orientation and need
to be laid out by you if you slice them directly.

| Project | Slicer |
|---------|--------|
| [`print/LisaMouse_BambuStudio_A1.3mf`](../print/LisaMouse_BambuStudio_A1.3mf) | Bambu Studio |
| [`print/LisaMouse_CrealityPrint_K2Plus.3mf`](../print/LisaMouse_CrealityPrint_K2Plus.3mf) | Creality Print |

> **Note:** these projects were saved before the final `top_shell_v4` model and still
> reference the v3 top shell. Replace the shell object with `models/top_shell.stl` (or
> `top_shell_lisa_logo.stl`) and re-orient it as in the project (top surface up).
<!-- TODO(author): re-save the 3MFs with the v4 shell and remove this note. -->

### Plate layout

| Plate | Bambu A1 | Creality K2 Plus |
|-------|----------|------------------|
| 1 | ![](../images/plates/bambu_plate_1.png) | ![](../images/plates/creality_plate_1.png) |
| 2 | ![](../images/plates/bambu_plate_2.png) | ![](../images/plates/creality_plate_2.png) |
| 3 | ![](../images/plates/bambu_plate_3.png) | ![](../images/plates/creality_plate_3.png) |

Bambu project: plate 1 = base, button stop, on/off buttons, battery cover 2;
plate 2 = top shell (logo) and buttons; plate 3 = battery cover 1.
Creality project: plate 1 = base, on/off buttons, battery covers, left button;
plate 2 = button variants and button stop; plate 3 = top shell (logo).

## Tips

- Print the **top shell** with its top surface facing up so the visible surface has no
  support scarring.
- Parts that mate (buttons in the shell, covers on the base) are tight-tolerance. If your
  printer runs a little over-sized, test-fit the buttons first and enlarge clearances or
  sand lightly.
<!-- TODO(author): add tolerance/fit findings (the 3MFs contain button clearance experiments of -0.4 / -0.3 / +0.2 mm), colour recommendations, and any parts that need extra care. -->
