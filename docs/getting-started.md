# Getting started

New to this package?  This page walks you through everything from
downloading Blender to running your first saddle tree script.

---

## What this package is

**saddle-examples-Blender** is a set of five western saddle tree STL
meshes paired with Blender Python scripts.  Each script:

1. Imports the STL mesh into a clean Blender scene.
2. Cleans up the mesh (welds near-duplicate vertices, fills small holes).
3. Creates a set of named, colour-coded boolean-tool objects positioned over
   the anatomically correct regions of the saddle tree.

The tools appear as transparent wire objects in the viewport.  They are
attached to the saddle mesh as **non-destructive Boolean modifiers** — you
can resize them and see the result live without permanently changing the
mesh.  When you are happy with a position, you apply the modifier to make
it permanent.

---

## What you need

- **Git LFS** — install from [git-lfs.github.com](https://git-lfs.github.com/) and run `git lfs install` once before cloning.  The `.stl` files are stored with LFS.
- **Blender 5.1** — [blender.org/download](https://www.blender.org/download/)
- The `.py` and `.stl` files for the tree you want, from this repository.
- No Blender experience is required to follow this guide.

---

## Step 1 — Download the files

From the `trees/` folder in this repository, download **two files** for the
tree you want to work with.  For example, for the roping tree:

```
trees/roping-tree/roping-tree.py
trees/roping-tree/roping-tree.stl
```

Place both files in the **same folder** on your computer.

---

## Step 2 — Open Blender and set the unit scale

1. Launch Blender 5.1.  Close the splash screen if it appears.
2. Look at the **Properties editor** on the right side of the screen
   (the vertical strip of icons).  Click the **Scene Properties** tab —
   it looks like a small funnel/inverted triangle.
3. Scroll down to the **Units** section and expand it.
4. Set **Unit System** to **Metric**.
5. Set **Length** to **Millimeters**.

You only need to do this once per new Blender file.  The saddle trees are
modelled in real-world millimetres, and this setting tells Blender to
display them at the correct scale.

---

## Step 3 — Switch to the Scripting workspace

At the top of the Blender window you will see a row of workspace tabs:
**Layout**, **Modelling**, **Sculpting**, and others.  Click **Scripting**.

This opens a text editor on the left and the 3D viewport on the right, plus
a Python console at the bottom.

---

## Step 4 — Load the script

In the text editor area:

1. Click **Open** (the folder icon in the text editor header).
2. Navigate to the folder where you saved both the `.py` and the `.stl` file.
3. Select the `.py` file and click **Open Text**.

> **Important:** Always use **Open** to load the script from disk — do not
> copy and paste the script text.  The script locates the `.stl` file
> relative to its own saved location on disk; pasting it gives it no
> disk location to work from.

You should now see the Python script in the text editor.  Take a moment to
read the comment block at the top — it describes the tree dimensions and
lists the boolean tools the script will create.

---

## Step 5 — Run the script

Click the **▶ Run Script** button in the text editor header, or press
**Alt + P** with the cursor inside the text editor.

The script will:

1. Clear the default Blender scene (removes the default Cube, Camera, and
   Light).
2. Import the `.stl` file from the same folder as the script.
3. Run a mesh cleanup pass.
4. Create all the boolean tool objects and attach them to the saddle mesh
   as modifiers.

**This takes 5–20 seconds.**  Progress messages appear in the System Console
(Window menu → Toggle System Console on Windows; terminal on macOS/Linux).
The final message is `[5/5] Setup complete`.

---

## Step 6 — Explore what was created

After the script finishes, look at the **Outliner** in the top-right corner.
You will see two collections:

**SaddleSolid**
- Contains `SaddleMesh` — the imported and cleaned mesh.  This is the
  object you will modify.

**BooleanTools (cutters & adders)**
- Contains all the boolean tool objects.  They appear as transparent
  wire shapes overlaid on the saddle in the viewport.

In the **3D viewport**, hold the middle mouse button and drag to orbit
around the scene, or press numpad 5 for an orthographic view.

---

## Step 7 — Understand the tool colours

| Colour | Meaning |
|--------|---------|
| Red | CantleSplitCutter — the central cantle slot (split-cantle trees only) |
| Blue | Standard cutters — remove material |
| Teal | Gullet-width cutters — safety-critical spine-clearance dimension |
| Purple | Rigging mortise cutters — hardware plate recesses |
| Orange | Seat scoop cylinder — sets the seat dish depth |
| Green | Adders — add material via union |

---

## Step 8 — Make your first adjustment

Let's resize the CantleCutter as a first exercise.

1. In the Outliner, click **CantleCutter** to select it.
2. Press **N** to open the side panel in the viewport.
3. Click the **Item** tab.
4. Look at the **Scale** values.  Scale X = 177.8 means the tool is
   177.8 mm wide on each side of centre, for a total of 355.6 mm — the
   full bar-to-bar width.
5. Change **Location Z** slightly — move it up or down.  Watch the saddle
   mesh in the viewport update as you type.  This is the Boolean modifier
   preview.

Nothing has been permanently changed yet.  To make the cut permanent, see
**[docs/workflow.md — section 5](workflow.md#5-applying-a-difference-cut)**.

---

## Step 9 — Read the full workflow guide

The complete workflow — applying cuts, applying unions, mirroring for
bilateral symmetry, adjusting bar rock and twist, adjusting gullet width,
troubleshooting, and exporting — is documented in
**[docs/workflow.md](workflow.md)**.

---

## Frequently asked questions

### The viewport looks enormous — the saddle is huge

You skipped the unit-scale step.  Go to **Scene Properties → Units →
Length: Millimeters** and the display will correct itself immediately.
The geometry is fine; only the displayed scale changes.

### The script says "STL not found"

The `.py` and `.stl` files must be in the same folder.  If they are in
different places, open the script, find the line `STL_PATH = os.path.join(...)`,
and change it to the full absolute path of the STL file.  Then run again.

### I applied a modifier and now the mesh looks wrong

Press **Ctrl + Z** to undo.  Blender's undo history works on applied
modifiers.  Undo until the mesh looks correct, then resize the tool and
try applying again.

### Can I use these scripts with a different horse's dimensions?

Yes.  The tools are starting-point placeholders sized for an average
Quarter Horse.  You resize them (Scale and Location in the N-panel) to
match measurements taken from your specific horse before applying.

### What is the minimum safe gullet width?

**70 mm (2.75")** at the narrowest point, with the saddle placed on the
horse's bare back.  Always verify clearance on the horse.  See
**[docs/workflow.md — section 14](workflow.md#14-gullet-width-safety-checklist)**
for the full safety checklist.
