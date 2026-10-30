# Lisa Mouse — Logitech M185 conversion

A 3D-printed shell that turns a **Logitech M185** wireless mouse into a replica of the
**Apple Lisa mouse**. The M185's guts (PCB, sensor, switches, scroll wheel, battery) are
reused; the printed parts replace the stock case. Unlike the original one-button Lisa
mouse, this one has **two buttons**.

> Unofficial fan project. Not affiliated with or endorsed by Apple Inc. or Logitech.
> "Apple" and "Lisa" are trademarks of Apple Inc.; "Logitech" and "M185" are trademarks of Logitech.

![Parts](images/plates/bambu_plate_2.png)

## What you need

| Item | Notes |
|------|-------|
| Logitech M185 wireless mouse | Donor for the electronics. |
| 3D printer + PLA | Parts fit a 0.4 mm nozzle; see [docs/PRINTING.md](docs/PRINTING.md). |
| Small Phillips screwdriver | For the M185's own screws. |
| 1 × AA battery | As used by the M185. |

<!-- TODO(author): add any extra hardware (screws, glue, tape, etc.) and screw sizes. -->

## Printed parts

STL files are in [`models/`](models/). Dimensions are the bounding box in the model's
design orientation (X × Y × Z, mm).

| File | Qty | Size (mm) | Purpose |
|------|:---:|-----------|---------|
| `base.stl` | 1 | 57.7 × 84.8 × 18.1 | Bottom plate; holds the M185 board and battery. |
| `top_shell.stl` **or** `top_shell_lisa_logo.stl` | 1 | 62.2 × 91.7 × 31.1 | The Lisa-style upper shell. The `_lisa_logo` variant has the embossed logo on top; the plain one is smooth. |
| `left_button.stl` | 1 | 20.1 × 27.1 × 23.9 | Left button. |
| `right_button.stl` | 1 | 23.9 × 27.1 × 19.5 | Right button. |
| `button_stop.stl` | 1 | 35.6 × 16.1 × 3.9 | Button bracket / stop. |
| `on_off_button.stl` | 2* | 12.0 × 7.2 × 6.0 | Power switch actuator. |
| `battery_cover_1.stl` | 1 | 14.7 × 53.1 × 8.9 | Battery compartment cover. |
| `battery_cover_2.stl` | 1 | 7.5 × 11.8 × 6.2 | Battery cover latch/clip. |

\* The supplied slicer projects print two; confirm how many you need.
<!-- TODO(author): confirm quantities and the exact roles of button_stop, on_off_button and battery_cover_1/2. -->

Part previews are in [`images/`](images/).

## Build it

1. **Print** the parts — [docs/PRINTING.md](docs/PRINTING.md)
2. **Assemble** — [docs/ASSEMBLY.md](docs/ASSEMBLY.md)

## Repository layout

```
models/     Print-ready STLs (one per part)
print/      Slicer projects with plate layout, orientation and settings
            (Bambu Studio / Bambu Lab A1, Creality Print / K2 Plus)
docs/       Printing and assembly instructions
images/     Part previews and slicer plate previews
scripts/    build_models.py — regenerates models/ and images/ from the source OBJ/STL export
```

## License

[CC BY-NC-SA 4.0](LICENSE) — share and adapt with attribution, non-commercially, under the same license.
