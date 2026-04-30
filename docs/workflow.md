# Workflow guide — saddle-examples-Blender

Complete step-by-step instructions for using the saddle tree scripts in
Blender 5.1.  Covers first-time setup, running a script, resizing tools,
applying boolean operations, mirroring, bar fitting, troubleshooting, and
exporting your finished mesh.

---

## Contents

1. [First-time Blender setup](#1-first-time-blender-setup)
2. [Running a tree script](#2-running-a-tree-script)
3. [Understanding what the script created](#3-understanding-what-the-script-created)
4. [Resizing a boolean tool](#4-resizing-a-boolean-tool)
5. [Applying a Difference (cut)](#5-applying-a-difference-cut)
6. [Applying a Union (add material)](#6-applying-a-union-add-material)
7. [Applying multiple operations in order](#7-applying-multiple-operations-in-order)
8. [Working with split-cantle trees](#8-working-with-split-cantle-trees)
9. [Mirroring for left/right symmetry](#9-mirroring-for-leftright-symmetry)
10. [Adjusting bar rock and twist](#10-adjusting-bar-rock-and-twist)
11. [Adjusting gullet width](#11-adjusting-gullet-width)
12. [Troubleshooting](#12-troubleshooting)
13. [Exporting the finished mesh to STL](#13-exporting-to-stl)
14. [Gullet width safety checklist](#14-gullet-width-safety-checklist)

---

## 1. First-time Blender setup

Do this once before running any script.  It tells Blender you are working
in millimetres, which matches the real-world dimensions in the STL files.

1. Open Blender 5.1.
2. In the **Properties editor** on the right side, click the **Scene
   Properties** tab (the funnel/cone icon).
3. Expand the **Units** panel.
4. Set **Unit System** to **Metric**.
5. Set **Length** to **Millimeters**.

> If you skip this step the saddle mesh will appear roughly 1000 × too
> large in the viewport (several hundred metres wide instead of several
> hundred millimetres).  The geometry is still correct — just change the
> unit setting and the display corrects itself immediately.

---

## 2. Running a tree script

1. Download the `.py` file and the matching `.stl` from the same
   `trees/<tree-name>/` folder.  Place both files in **the same folder**
   on your computer.
2. In Blender, switch to the **Scripting** workspace using the tabs at the
   top of the screen.
3. In the text editor area, click **Open** and navigate to the `.py` file
   you downloaded.  Select it and click **Open Text**.
4. Click **Run Script** (the ▶ button in the text editor header, or press
   **Alt + P** on your keyboard).
5. Progress messages appear in the **System Console**:
   - **Windows:** Window menu → Toggle System Console.
   - **macOS / Linux:** launch Blender from a terminal; messages appear there.
6. The script takes 5–20 seconds.  When it finishes you will see the message
   `[5/5] Setup complete` in the console.

> **STL path error?**  If the console shows `STL not found`, open the script
> in the text editor, find the line `STL_PATH = os.path.join(...)` near the
> top, and edit it to the full path of your STL file.  Then run again.

---

## 3. Understanding what the script created

After the script completes, look at the **Outliner** (the panel in the
top-right corner of the screen).  You will see two collections:

```
SaddleSolid
  └── SaddleMesh          ← your working mesh object

BooleanTools (cutters & adders)
  ├── CantleSplitCutter   ← red  (split-cantle trees only)
  ├── CantleWingCutter_L
  ├── CantleWingCutter_R
  ├── CantleBodyCutter
  ├── SeatScoopCutter
  ├── BarCurveCutter_L
  ├── BarCurveCutter_R
  └── ...
```

Each tool in **BooleanTools** is already attached to **SaddleMesh** as a
**Boolean modifier**.  You can see the modifier stack by clicking on
SaddleMesh and opening **Properties → Modifier properties** (wrench icon).

The tools are displayed as transparent wire objects in the viewport so you
can see the saddle mesh beneath them.  The modifiers preview the result of
each cut or union in real time — nothing is permanent yet.

**Colour reference:**

| Colour | Meaning | Operation when applied |
|--------|---------|----------------------|
| Red | CantleSplitCutter — the signature slot cut | Difference |
| Blue | Standard cutters (cantle, horn, swell, bars) | Difference |
| Teal | Gullet-width cutters | Difference |
| Purple | Rigging mortise cutters | Difference |
| Orange | Seat scoop cylinder | Difference |
| Green | Adders — add material | Union |

---

## 4. Resizing a boolean tool

1. Click on the tool object in the **Outliner** (e.g. `CantleCutter`).
2. Press **N** to open the **Side Panel** (or click the small ▸ arrow at
   the right edge of the viewport).
3. Select the **Item** tab.
4. You will see three sections: **Location**, **Rotation**, and **Scale**.

**Location** moves the centre of the tool box.  All coordinates are in
millimetres.

**Scale** changes the tool size.  Because the underlying primitive is a
2×2×2 unit cube or a radius-1 height-2 cylinder, the relationship is:
- Scale X = half the X dimension in mm  (so Scale X 50 = 100 mm wide)
- Scale Y = half the Y dimension in mm
- Scale Z = half the Z dimension in mm

**Rotation** tilts the tool.  This is used mainly for bar-twist adjustment
(see [section 10](#10-adjusting-bar-rock-and-twist)).

The viewport updates in real time as you change these values because the
Boolean modifier is non-destructive.

---

## 5. Applying a Difference (cut)

A Difference modifier removes the tool's volume from the saddle mesh.  All
blue, teal, purple, orange, and red tools are set to Difference.

1. Click on **SaddleMesh** in the Outliner to select it.
2. Open **Properties → Modifier properties** (wrench icon on the right).
3. Scroll down to find the Boolean modifier named after the tool you want
   to apply (e.g. `CantleCutter`).
4. Click the **▾ dropdown arrow** on the right side of that modifier.
5. Click **Apply**.

The cut is now permanent on the mesh.  The tool object remains in
`BooleanTools` — you can delete it or keep it for reference.

> **Tip:** You can click the eye icon on a modifier to temporarily hide its
> effect and see the mesh before that cut.  This is useful for checking the
> result of earlier operations without undoing them.

---

## 6. Applying a Union (add material)

A Union modifier adds the tool's volume to the saddle mesh.  All green
adder tools (CantleAdder, HornAdder, PommelCapAdder) are set to Union.

The steps are identical to applying a Difference — select SaddleMesh, open
the modifier stack, find the Union modifier, click ▾ → Apply.

---

## 7. Applying multiple operations in order

You can have the entire modifier stack active at once and preview the fully
modified saddle before applying any modifier permanently.  This is the
main advantage of the non-destructive workflow.

When you are ready to commit, apply modifiers **one at a time from top to
bottom** in the modifier stack.  The stack order for most trees is:

1. CantleSplitCutter (if present — red, apply first)
2. CantleWingCutter\_L then CantleWingCutter\_R
3. CantleBodyCutter
4. CantleAdder (if desired)
5. HornCutter / HornAdder (if present)
6. SwellCutter
7. SeatScoopCutter
8. BarCurveCutter\_L (then add Mirror modifier for right bar — see section 9)
9. RiggingMortise cutters (FL, FR, RL, RR)
10. Remaining green adders

You do not need to apply them all.  Apply only the ones that represent
changes you want to keep.

---

## 8. Working with split-cantle trees

The `split-cantle-no-horn-saddle-tree` and `split-cantle-horn-tree` both
use a **CantleSplitCutter** (shown in red).  This tool creates the central
vertical slot that defines the split cantle.

**Always apply CantleSplitCutter before the wing cutters.**  The wings
are the cantle material that remains on either side of the slot.  If you
apply a wing cutter before the slot exists, you will remove material from
a solid cantle and the geometry will be wrong.

Workflow for split-cantle trees:

1. Resize `CantleSplitCutter` to the slot width and depth you want
   (Location Y adjusts the slot depth; Scale X adjusts the width).
2. Apply `CantleSplitCutter` (Difference).
3. Resize `CantleWingCutter_L` — reduce Scale Z to lower the wing height,
   or shift Location X outward to slim the wing.
4. Apply `CantleWingCutter_L` (Difference).
5. Repeat for `CantleWingCutter_R`.
6. Apply `CantleBodyCutter` to set the overall cantle wall height below
   the wings.
7. Continue with the remaining tools.

---

## 9. Mirroring for left/right symmetry

All trees are centred at the world origin (0, 0, 0).  This means a Mirror
modifier on the X axis produces a geometrically perfect bilateral mirror.

**Workflow for bar cutters:**

1. Make all your bar adjustments on `BarCurveCutter_L` (move Z for rock,
   rotate Y for twist) and apply that modifier.
2. Select the SaddleMesh.
3. In the Modifier properties, click **Add Modifier → Generate → Mirror**.
4. In the Mirror modifier, ensure **X** is the active axis.
5. Leave **Mirror Object** empty (defaults to world origin, which is correct).
6. Apply the Mirror modifier.

**To use the pre-placed right bar tool instead:**

Each tree also includes `BarCurveCutter_R` as a separate tool.  You can
resize it independently if the horse has an asymmetric back, then apply
both cutters separately.

---

## 10. Adjusting bar rock and twist

**Rock** is the front-to-back arch of the bar that matches the curve of
the horse's back.

**Twist** is the tilt angle of the bar relative to horizontal, which
affects shoulder clearance.

### Adjusting rock

1. Select `BarCurveCutter_L` in the Outliner.
2. In the N-panel → Item → Location, adjust **Location Z**:
   - Move Z **down** (more negative) → more rock (more arch, for a horse
     with a rounder back profile).
   - Move Z **up** (less negative) → flatter bars (for a straight-backed horse).

### Adjusting twist

1. Select `BarCurveCutter_L`.
2. In the N-panel → Item → Rotation, adjust **Rotation Y**:
   - Positive Y degrees → front of bar tilts downward (more shoulder angle).
   - Negative Y degrees → front of bar tilts upward.
   - Typical range: 2–8 degrees.

After setting rock and twist on the left bar, use a Mirror modifier
(see section 9) to replicate the same geometry to the right side.

---

## 11. Adjusting gullet width

> ⚠️ **Gullet width is a horse-fit safety dimension.**
> Minimum safe width is **70 mm (2.75 ")** at the narrowest point.
> Narrowing the gullet below this risks compressing the horse's spine.

The teal `GulletCutter_L` and `GulletCutter_R` tools control the width of
the gullet channel.

**To widen the gullet:**

1. Select `GulletCutter_L`.
2. In the N-panel → Location, shift **Location X** toward 0 (less negative).
3. Select `GulletCutter_R` and shift **Location X** toward 0 by the same
   amount (less positive) to keep the channel symmetric.
4. Apply both modifiers.

**To measure the resulting gullet width:**

1. Select SaddleMesh and enter **Edit Mode** (Tab).
2. Select two vertices on opposite sides of the gullet at the narrowest point.
3. Press **N** and look at **Item → Edge Info** or use
   **Mesh → Vertices → Measure**.

---

## 12. Troubleshooting

### Boolean modifier shows no visible effect

- Ensure the modifier's **solver** is set to **Exact** (not Fast).
  Click the modifier to expand it and check the Solver dropdown.
- Confirm the tool object **intersects** the saddle mesh.  Select the
  tool, check its Location in the N-panel, and compare with the saddle
  bounding box.
- If the mesh has open holes or non-manifold edges, fill them first:
  Edit Mode → Select All (A) → Mesh → Clean Up → Fill Holes.

### Performance is slow / Blender is unresponsive

The STL meshes contain roughly 500,000 triangles.  Boolean operations on
dense meshes can take several seconds each.  To speed up interactive work:

1. Select SaddleMesh and press **Shift + D** to duplicate it.
2. On the duplicate, add a **Decimate modifier** and set Ratio to 0.1.
3. Do all your boolean fitting work on the decimated copy.
4. Once satisfied, apply the same Location/Scale/Rotation values to the
   tools on the full-resolution original.

### The mesh looks 1000× too large

Blender is displaying in metres but the STL is in millimetres.  Fix:
**Scene Properties → Units → Unit System: Metric → Length: Millimeters**.
The mesh size is correct; only the display scale changes.

### The script reports "STL not found"

Both the `.py` script and the `.stl` file must be in the same folder.  If
they are in different locations, edit the `STL_PATH = ...` line near the
top of the script to the full absolute path of the STL file, then run again.

### Holes in the mesh after import

The cleanup pass fills most holes automatically.  If any remain:

1. Select SaddleMesh.
2. Enter **Edit Mode** (Tab).
3. Select All (A).
4. **Mesh → Clean Up → Merge by Distance** — set threshold to 0.01 mm.
5. **Mesh → Clean Up → Fill Holes**.
6. Return to Object Mode (Tab).

---

## 13. Exporting to STL

After all modifiers are applied and you are satisfied with the result:

1. Select **SaddleMesh** in the Outliner.
2. Go to **File → Export → STL (.stl)**.
3. In the export panel on the right side of the file browser:
   - Enable **Selection Only** to export only the selected mesh.
   - Set **Scale** to **1.0** (coordinates are already in mm).
   - Choose **Binary** format (smaller file, same data as ASCII).
4. Choose a filename and location.
5. Click **Export STL**.

> If your exported STL opens in another program at the wrong scale, check
> that the scene Unit Scale is 0.001 (Blender's convention for mm → m
> conversion) rather than 1.0.  The setting is in
> **Scene Properties → Units → Unit Scale**.

---

## 14. Gullet width safety checklist

Work through this checklist before placing any modified tree on a horse.

- [ ] Measure the gullet width at the narrowest point (typically at the
      pommel, just behind the front arch).
      **Minimum: 70 mm (2.75").**
- [ ] Place the saddle on the horse's back without a pad.  Run two fingers
      along the gullet channel from front to back.  Both fingers should
      move freely at all points without touching the spine.
- [ ] With the saddle on the horse, ask someone to observe from behind
      while the horse lowers and raises its head.  The gullet must not
      contact the spine in any head position.
- [ ] Have a qualified saddle fitter or equine veterinarian confirm the fit
      before the saddle is used for extended riding.

Gullet width in the Blender model can be measured by selecting two vertices
on opposite sides of the channel in Edit Mode and reading the distance in
the N-panel.
