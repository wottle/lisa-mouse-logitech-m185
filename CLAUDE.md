# CLAUDE.md

Notes for working on this repo with Claude. Read this before changing any model.

## What this is

A 3D-printed replica of the Apple Lisa mouse that holds the electronics of a Logitech M185 wireless
mouse and one AA cell. Sister project: the Macintosh M0100 version at
<https://github.com/wottle/mac-mouse-logitech-m185> (local folder `AppleMouseLogitechM185`). Lessons
proven on the Mac mouse are being carried over here.

## Layout

| Path | What |
|------|------|
| `models/` | The STLs people print. Current design. |
| `models/v1/` | The original published parts. **Source geometry for every script; never edit.** |
| `scripts/adjustable_buttons.py` | Builds `left_button`, `right_button`, `button_stop` from `models/v1`. |
| `scripts/front_screws.py` | Builds `base`, `top_shell`, `top_shell_lisa_logo`, `lisa_logo_plate`, `lisa_logo_plate_blank` from `models/v1`. Imports `adjustable_buttons`. Runs the fit checks. |
| `scripts/build_models.py` | Older: converts release OBJ/STL into `models/` and renders previews. Not part of the v2 work. |
| `docs/ASSEMBLY.md`, `docs/PRINTING.md`, `README.md` | User docs. Keep them in step with the models. |
| `print/*.3mf` | Slicer projects. **Still contain v1 parts**; Mike re-saves these himself after test prints. |
| `images/assembly/` | Build photos. Steps 9, 12, 13, 14 show v1 parts; the text says so. |
| repo root `*.stl`, `*.3mf`, `release_files/`, `working files/` | Git-ignored local scratch. Leave alone. |

`models/apple_logo_plate_blank.stl` is a copy of the Mac mouse's `logo_plate_blank.stl`; it is an input
to `front_screws.py` (its outline defines the Apple recess).

## Building

```
pip install numpy trimesh rtree manifold3d
python3 scripts/adjustable_buttons.py     # buttons + retainer, prints fit check
python3 scripts/front_screws.py           # case + logo plates, prints fit check incl. the buttons
```

Both must end with `problems: 0`. Expected non-zero lines:

- `left x shell 0.041 mm3`, `right x shell 0.038 mm3`: hinge-pin slivers, harmless. (The left used to read
  0.507: that was not harmless, see *Free running* below.)
- `left/right x retainer 0.315 mm3 (spring preload)`: the designed interference of the spring pads.
- `top_shell ... watertight False`: a few zero-thickness slivers on the top panel inherited from v1
  (v1 was far worse). Slicers repair it. The logo shell is clean.

`tm(name)` loads from `models/v1` first, then `models/`. So the scripts always start from v1.

## Frames

- **Shell frame S** (all CSG is done here): inside of the shell is +z, the roof is at low z. x is
  left-right, +y is toward the buttons (front). The base seats on a ledge at `SEAT = 33.2`; rim at 35.84.
- **Base frame** (the `base.stl` file): `z_base = Z_BASE − z_S` with `Z_BASE = 40.28`, `x_base = −x_S`,
  y unchanged. `to_S` / `to_B` in `front_screws.py` convert (same transform both ways). Base underside
  is z = 1.4 in its file.
- **Mac mouse frame F** = Lisa base frame + (−1.0, −8.0, −1.4). Use this to carry measurements across.
- `top_shell_lisa_logo.stl` is the same shell translated by `LOGO_SHIFT = (26.81, −11.34, 26.5)`.
- Button files have their own frames; `A_R`, `A_L` map them into S.
- The top panel is the plane `z = −0.06934·y + 7.43803` (holds for y ≥ −26, |x| ≤ 21.7).

Left/right mean the user's left/right. In S the left button is at **+x**.

## Measured facts (do not re-derive)

- M185 switch plungers, base frame: left (−19.92, 34.5), right (+16.73, 34.5): 9 mm and 12 mm in from
  the base edges, about 36.6 mm apart. Plunger free top at z_base ≈ 17.5.
- PCB: 1.6 mm thick, underside on ledges at z_base 8.05. Front edge about y_base 49.3 (carried over from
  a caliper measurement on the Mac print: 6.0 mm from the Mac shell's outside front to the wheel-cutout
  lip, 2 mm bridge in front of the cutout). Front tapers along two angled rails. Not re-measured on the
  Lisa base.
- Hardware: M3 pilot Ø2.7, clearance Ø3.3, countersink recess Ø6.3 with a 90° cone 1.5 deep.
  Screws: M3×4 flat (PCB rear), M3×6 (PCB front), 2 × M3×6 countersunk (retainer), 4 × M3×8 countersunk
  (2 case, 2 strikers).
- v1 shell side walls lean in 0.077 mm/mm (about 1.9 mm per side at the roof). Wall 2.5 mm.
- v1 recesses: Apple 9.0 × 9.4 mm, 0.6 deep, centre (15.85, −20.78); Lisa 21.2 × 9.6, about 1.0 deep
  with a raised wordmark.
- Hinge axis: y_S 17.188; pin seat floor z_S 10.391 (the floor is on the **roof** side, so gravity pulls
  the pin off it onto the retainer).

## The v2 design and why

**Buttons and retainer (`adjustable_buttons.py`)**
- *Strikers:* each button has a Ø6 post with an M3×8 countersunk screw, head toward the switch. Turning
  it sets the click point. Tune with the case screws tight; tightening the case lowers the strikers a
  little. On the Mac the left needed about a quarter turn shorter.
- *Sag:* the switch pushes each button up only at its outer front corner, so weight (and a finger near
  the middle) rolls the button and the inner front corner drops by the pin's play under the retainer.
  Left is worse (switch further outboard). Rigid fingers at 0.08 mm bound when tightened; loosened, they
  sagged. Fix: two spring fingers on the retainer (`SPRING_T` 1.0 mm thick, 6.8 mm free length, about
  6 N/mm) whose pads stand `SPRING_PRELOAD` 0.15 mm into the inner end of each pin. The four rigid
  fingers are a backstop at `FINGER_GAP` 0.25. Each button has bare pin at its inner end for the pad.
  The retainer seats hard on the shell ledge and is screwed down fully.
- *Height:* caps raised `CAP_RAISE` 1.0 mm (2.6 mm proud; v1 1.6).
- Pins fattened to r 1.43 (`PIN_R`).
- *Free running:* the shell has a downward rim round the underside of each window, and the flange has a
  step just outboard of it. v1 left the left step touching the rim (0 mm; the right had 0.15 mm because the
  shell is not quite symmetric). On the print the left button dragged, stuck down, and stopped at 0.5° of
  lift on the rim corner instead of the front edge, so its striker could not be lengthened to full height.
  Fix: ahead of the hinge (`HINGE_KEEP`) each button keeps `SIDE_CLEAR` 0.35 mm from the shell sideways and
  front-to-back, swept through `LIFT_FREE` 1.5° of lift; only the front edge of the flange (`STOP_Y`) is
  left as the up-stop. Both buttons now lift 1.2° (0.35 mm at the striker) and stop on that edge, keep
  ≥ 0.14 mm everywhere else from the stop to 4° pressed, and are held sideways only by the retainer
  fingers (0.2–0.45 mm). Check gaps through the whole swing, not just overlap at rest.
- Button export welds and drops zero-area flakes the clearance cuts leave, and asserts watertight.
- *Left post:* the left switch sits under the window edge, so its striker post is outboard of the cap. It
  must stay below the flange (`FLANGE_TOP`) there. An earlier version let it rise beside the cap into the
  gap to the window edge, where it rubbed. New material may only join the cap wall from inside, so the
  outside of the left button mirrors the right.

**Case (`front_screws.py`)**
- Case screws moved from the rear corners to the front corners (`SCREW`), bosses with 45° ramps so they
  print roof-down. Rear of the base hooks onto two tabs on the shell's rear wall (`TAB`, `TAB_Z`,
  `SLOT_Z`; 0.15 mm on the load side). Hook the rear first, swing the front shut.
- The v1 rear corner blocks **stay** (Mike: solid corners need less support printing on a side). Only
  their pilot holes are filled. Do not remove them again.
- `PARALLEL_SIDES`: side walls warped vertical at the rim width so the shell can print standing on a
  side. Rim unchanged, top about 1.9 mm wider per side, base seat about 0.2 mm looser per side.
- PCB front standoff in the wheel cutout (`ST_B`), as on the Mac: stops the front of the board lifting
  when the rear screw is tightened.
- Relief pocket in the shell's front wall (`RELIEF_*`): v1's leaning wall overlapped the board's front
  edge, which snagged on opening. Now 0.9 mm clear; wall behind is 1.3 mm.
- Logo recesses 1.4 mm deep, cut square to the top panel, for separately printed plates
  (`LOGO_T` 1.4, `LOGO_CLEAR` 0.1, `LOGO_BEVEL` 0.4, same as the Mac). The Apple recess takes the Mac
  mouse's plate. The Lisa plate carries the wordmark traced from the v1 shell, 0.4 mm raised.
- v2 base and shells only fit each other, not v1.

## Status

Branch `adjustable-buttons`. Everything after commit `5fb0fe3` is uncommitted and **not print-tested**:
case redesign, logo plates, spring retainer, taller buttons, PCB standoff and relief. The first v2
buttons (commit `5fb0fe3`) were printed: left button sagged, retainer bound when tight, buttons sat low,
PCB front snagged. Those reports drove the current revision.

Open items:
- Print-test the spring fingers (tune `SPRING_PRELOAD` / `SPRING_T`) and the rear tabs.
- On-side print orientation of the shell has not been checked for supports.
- Re-save `print/*.3mf` with the v2 parts, then drop the "still contain v1" notes in `docs/PRINTING.md`.
- Retake assembly photos for steps 9, 12, 13, 14.
- Lisa wordmark plate: raised relief today; a flush two-colour version is a small change.

## Working conventions

- **Mike runs git himself.** Leave changes uncommitted; give him the commit command. Claude cannot push.
- Never state that something was removed, replaced or delivered without checking the output. Twice in
  this project a render or a file copy was reported as done when it was not:
  - Look at the render of the exact feature before describing it.
  - After writing files to the Mac, compare checksums there against the build. Do not copy and write
    in the same parallel step.
- Print-friendliness rules Mike has asked for: flat bottoms with 45° bevels, 45° ramps under bosses and
  tabs, conical countersinks, parallel sides for on-side printing, keep solid blocks where they save
  supports.
- Prefer one named constant per tunable dimension, with a comment saying what it does, so a fit can be
  adjusted without reading the CSG.
- Checks that have earned their place: overlap between every pair of parts at rest; buttons pressed
  1.5° and 3°; hook-in sweep of the base (with a PCB and screw-head stand-in) from 16° to closed; plates
  seated in their recesses. A clearance scan is needed as well as an overlap test (a 0.15 mm gap once
  passed an overlap-only check on the Mac and collided in print).
- Manifold notes: `trim_by_plane(n, d)` needs `d` divided by |n|; `CrossSection` polygons must be
  counter-clockwise; run `.simplify()` before export so STLs reload cleanly; when measuring a wall by
  ray cast, make sure the ray is not hitting a boss in front of it.
- Mike's caliper readings have been off when not zeroed; confirm a surprising number before building
  on it.
