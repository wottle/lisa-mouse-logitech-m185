# Assembly

Photos below show the full build, in order. Part names refer to the files in
[`models/`](../models/).

## You'll need

- The printed parts ([PRINTING.md](PRINTING.md)): base, top shell, left and right buttons,
  button stop (retainer plate), on/off button, battery covers 1 and 2
- A **Logitech M185** wireless mouse. The photos use a PCB marked *AVALON 22 Single,
  210-002552 REV003*. Other board revisions may have different layouts, so check yours
  against the photos before printing.
- 1 × AA battery
- Optional: self-adhesive PTFE mouse slides for smoother gliding (any you like; the photos use five white oval pads)
- Screwdriver and **M3 screws**:

  | Use | Screw | Qty |
  |-----|-------|:---:|
  | PCB (step 9) | M3×4 flat head | 1 |
  | Button retainer plate (step 12) | M3×6 countersunk | 2 |
  | Joining the shells (step 14) | M3×8 countersunk | 2 |

- Optional: rainbow Apple logo decal (if printing the blank top piece - this logo was taken from a damaged PowerMac 6100 case).

<!-- TODO(author): confirm the case screw count, the source of the logo decal, and battery polarity. -->


## Prepare the donor mouse

### Step 1

Remove the battery door and battery from the M185. The single screw holding the mouse together (circled) sits in the battery area; remove it.

<img src="../images/assembly/1_remove_screw_from_m185.jpg" width="520" alt="Step 1">

### Step 2

Separate the top and bottom halves of the M185 to expose the PCB. The red arrow marks the tab/catch on the left edge to release.

<img src="../images/assembly/2_separate_m185_shell_to_expose_pcb.jpg" width="520" alt="Step 2">

### Step 3

Lift the PCB out of the lower shell, with the battery contact spring and wire still attached. The red arrow marks the scroll wheel, which comes off next.

<img src="../images/assembly/3_pull_pcb_from_m185_shell.jpg" width="520" alt="Step 3">

### Step 4

Pull the scroll wheel out of its holder and set it aside. The printed mouse has no scroll wheel, so the wheel and its click switch are not used.

<img src="../images/assembly/4_remove_scroll_wheel.jpg" width="520" alt="Step 4">

## Install the electronics in the base

### Step 5

Flip the PCB over. Slide the M185's power switch (SW10, circled) to the end of its travel in the direction of the arrow (**ON**).

<img src="../images/assembly/5_slide_power_switch_to_side.jpg" width="520" alt="Step 5">

### Step 6

Take the printed power switch actuator (`on_off_button.stl`, circled) and `base.stl`. Note the Bamboo Lab and Creality print files have two on-off buttons.  One is slightly taller (110%) and in my prints seems to work better. 

<img src="../images/assembly/6_get_3d_printed_power_switch.jpg" width="520" alt="Step 6">

### Step 7

Fit the printed switch into its slot in the base and slide it to the side (arrow), so it lines up with the PCB switch in the ON position.

<img src="../images/assembly/7_install_power_switch_and_slide_to_side.jpg" width="520" alt="Step 7">

### Step 8

Lower the PCB into the base with the optical sensor over the sensor window. Seat the battery contact spring at the far end of the diagonal battery compartment, and lay the long contact wire along the compartment wall into the notches (red arrows).

<img src="../images/assembly/8_install_pcb_in_bottom_shell.jpg" width="520" alt="Step 8">

### Step 9

Screw the PCB down with a single M3×4 flat head screw at the end of the battery compartment.

<img src="../images/assembly/9_screw_down_pcb_in_bottom_shell.jpg" width="520" alt="Step 9">

## Install the buttons in the top shell

### Step 10

Turn the top shell upside down. You need `left_button.stl`, `right_button.stl`, the retainer plate (`button_stop.stl`) and two M3×6 countersunk screws. Not the retainer plate has little nubs on one side.  Those should be installed to face toward the button arms.  

<img src="../images/assembly/10_prepare_to_assemble_top_shell.jpg" width="520" alt="Step 10">

### Step 11

Drop the two buttons into their slots, then lay the retainer plate over them so its fingers interleave with the buttons' tabs.

<img src="../images/assembly/11_install_buttons_and_retainer_plate.jpg" width="520" alt="Step 11">

### Step 12

Screw the plate down with the two M3×6 countersunk screws. The tension matters: it should hold the buttons in place without binding them, and each button should still move freely and spring back. I tightened the retaining clip down until there was a bit of resistance, then I backed it off until the buttons fall with just gravity when pressed up.  

<img src="../images/assembly/12_screw_down_retainer_plate_proper_tension.jpg" width="520" alt="Step 12">

## Close the mouse

### Step 13

You now have the two finished halves: the top shell with buttons, and the base with the PCB. Make sure the buttons are fully seated when combining the shells. 

<img src="../images/assembly/13_combine_two_shells.jpg" width="520" alt="Step 13">

### Step 14

Fit the halves together and screw them together from underneath with the M3×8 countersunk screws. If you're using PTFE slides, stick them on the underside.

<img src="../images/assembly/14_screw_together_shells.jpg" width="520" alt="Step 14">

### Step 15

Install an AA battery in the diagonal compartment.

<img src="../images/assembly/15_install_battery.jpg" width="520" alt="Step 15">

### Step 16

Assemble the battery door from its two printed parts, `battery_cover_1.stl` and `battery_cover_2.stl`.

<img src="../images/assembly/16_combine_battery_door_pieces.jpg" width="520" alt="Step 16">

### Step 17

Fit the battery door into the compartment and latch it.

<img src="../images/assembly/17_install_battery_door.jpg" width="520" alt="Step 17">

## Done

### Step 18

Plug the M185's USB receiver into your computer. The finished mouse: two buttons, a Lisa-style body and (optional) a rainbow Apple logo decal on the embossed logo area.

<img src="../images/assembly/18_assembly_complete.jpg" width="520" alt="Step 18">

