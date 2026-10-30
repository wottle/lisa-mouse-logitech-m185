# Assembly

> **Draft.** The steps below are outlined from the part geometry; items marked
> **TODO(author)** need to be filled in or corrected from the physical build.

## Before you start

- Printed parts ready (see [PRINTING.md](PRINTING.md)); remove supports and brim, and
  test-fit the buttons in the shell.
- A Logitech M185 to cannibalise. Take the USB receiver out of the mouse first and keep it.

## 1. Strip the M185

1. Remove the battery cover and the AA battery, and take out the USB nano receiver.
2. Remove the M185's screw(s) and separate the top shell from the base.
3. Lift out the PCB with the scroll wheel, the two microswitches, the optical sensor and
   the power slide switch.

<!-- TODO(author): add photos, and note which M185 parts are discarded (shell, scroll wheel
     housing?) vs. reused, plus the M185 hardware revision you used. -->

## 2. Fit the electronics to the printed base

1. Seat the PCB into `base.stl`.
2. Fit the battery in the battery compartment of the base.

<!-- TODO(author): PCB orientation, screws used, how the sensor lines up with the base opening. -->

## 3. Install the buttons

1. Place `left_button.stl` and `right_button.stl` in the top shell so each sits over its
   microswitch.
2. Fit `button_stop.stl` to retain the buttons.

<!-- TODO(author): confirm how the button bracket secures them, direction of travel, and
     whether anything (e.g. the scroll wheel slot in the shell) needs separate handling. -->

## 4. Power switch

Fit `on_off_button.stl` so that it drives the M185's slide switch.

<!-- TODO(author): describe how the actuator fits; why two are printed. -->

## 5. Close up

1. Join the top shell to the base.
2. Fit `battery_cover_1.stl` and `battery_cover_2.stl` over the battery compartment.
3. Insert the battery, and plug the USB receiver into the computer.

<!-- TODO(author): fasteners vs. snap fit; how the shell and base are held together. -->

## 6. Test

Pair with the receiver (it is already paired in the donor mouse), check both buttons,
the scroll wheel and the power switch.

## Troubleshooting

<!-- TODO(author): common problems (sticky buttons, no click, cursor jitter from sensor height, etc.). -->
