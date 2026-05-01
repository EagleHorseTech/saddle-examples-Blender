# saddle-examples-Blender

[![Python checks](https://github.com/EagleHorseTech/saddle-examples-Blender/actions/workflows/syntax-check.yml/badge.svg)](https://github.com/EagleHorseTech/saddle-examples-Blender/actions/workflows/syntax-check.yml)
[![Licence: MIT](https://img.shields.io/badge/scripts-MIT-blue.svg)](LICENSES/MIT.txt)
[![Licence: CC BY 4.0](https://img.shields.io/badge/meshes-CC%20BY%204.0-lightgrey.svg)](LICENSES/CC-BY-4.0.txt)

A collection of five western saddle tree meshes with Blender 5.1 Python
scripts.  Each script imports an STL, cleans up the mesh, and creates a
complete set of named, colour-coded boolean-tool primitives pre-positioned
over anatomically correct saddle regions.

Every tree is scaled to real-world Quarter Horse dimensions and centred at
the world origin.  All scripts target **Blender 5.1**.

---

## Quick start — five steps

> **Git LFS required.**  The `.stl` mesh files and `.png` preview images are stored with
> [Git Large File Storage](https://git-lfs.github.com/).  Before cloning,
> install Git LFS and run `git lfs install` once.  Without it you will
> receive pointer files instead of the actual meshes and images.


> **Unit scale first.** Before running any script, tell Blender you are
> working in millimetres:
> **Scene Properties → Units → Unit System: Metric → Length: Millimeters**
> If you skip this step the mesh will appear roughly 1000 × too large in
> the viewport.

1. Download the `.py` and `.stl` for the tree you want from the
   `trees/<tree-name>/` folder and place both files in the same folder on
   your computer.
2. Open **Blender 5.1** and switch to the **Scripting** workspace
   (tab row at the top of the screen).
3. Click **Open** in the text editor header and select the `.py` file
   from the folder where you saved it.  Both the `.py` and `.stl` must
   be in the same folder.
4. Click **Run Script** (▶ button, or press **Alt + P**).
5. Wait 5–20 seconds.  When the script finishes, the **Outliner** (top-right
   panel) shows two collections: `SaddleSolid` and
   `BooleanTools (cutters & adders)`.

For the complete workflow — resizing tools, applying cuts, mirroring,
exporting — see **[docs/workflow.md](docs/workflow.md)**.

---

## Tree catalogue

| Tree | Discipline | Horn | Cantle | Gullet | Depth |
|------|-----------|------|--------|--------|-------|
| [high-swell-tree](#high-swell-tree) | Ranch / barrel | Yes — tall | Solid | 14.0\" (355.6 mm) | 23.2\" (588.6 mm) |
| [low-cantle-no-horn-saddle-tree](#low-cantle-no-horn-saddle-tree) | Endurance / trail | No | Solid, low | 14.0\" (355.6 mm) | 9.1\" (231.1 mm) |
| [roping-tree](#roping-tree) | Ranch roping | Yes — stout | Solid, moderate | 13.5\" (343.5 mm) | 24.0\" (609.6 mm) |
| [split-cantle-no-horn-saddle-tree](#split-cantle-no-horn-saddle-tree) | Endurance / trail | No | Split wings | 14.0\" (355.6 mm) | 12.7\" (321.6 mm) |
| [split-cantle-horn-tree](#split-cantle-horn-tree) | Ranch / trail hybrid | Yes — moderate | Split wings | 13.3\" (338.9 mm) | 22.0\" (558.8 mm) |

---

## Colour key

Every boolean tool across all five scripts uses one of six colours.
The colour tells you at a glance what the tool does and which operation
to use when you apply it.

| Colour | Viewport tint | Meaning | Modifier operation |
|--------|--------------|---------|-------------------|
| Red | Warm red | CantleSplitCutter — **apply this first** on split-cantle trees | Difference |
| Blue | Sky blue | Standard cutters (cantle, horn, swell, bars) | Difference |
| Teal | Cyan-blue | Gullet-width cutters — **safety-critical**, see below | Difference |
| Purple | Lavender | Rigging mortise cutters | Difference |
| Orange | Amber | Seat scoop cylinder | Difference |
| Green | Lime green | Adders — build material up | Union |

---

## Gullet width safety rule

> ⚠️ **The gullet channel must never touch the horse's spine.**
> Minimum safe width: **70 mm (2.75 ")** at the narrowest point.
> Always verify clearance on the horse before extended riding.
> The teal gullet tools carry "SAFETY-CRITICAL" in their label as a reminder.

---

## Applying a boolean cut — step by step

The tools are set up as **non-destructive Boolean modifiers**.  They
preview the result live in the viewport but do not permanently change the
mesh until you apply them.

1. In the **Outliner**, click a tool object (e.g. `CantleCutter`).
2. Press **N** to open the side panel.  In the **Item** tab, adjust:
   - **Location** — moves the tool.
   - **Scale** — resizes it.  Scale X = half the X dimension in mm.
   - **Rotation** — tilts it (useful for bar-twist adjustment).
3. Click on **SaddleMesh** in the Outliner to select the saddle.
4. Open **Properties → Modifier properties** (the wrench icon, right side).
5. Find the Boolean modifier named after your tool.
6. When you are happy with the preview, click the **▾ dropdown → Apply**.

For the complete workflow including mirroring, chaining operations,
troubleshooting, and STL export, see **[docs/workflow.md](docs/workflow.md)**.

---

## Tree details

### high-swell-tree

Classic western ranch tree.  The tall, wide swell (fork) gives strong
lateral security for ranch work and barrel racing.

![high-swell-tree preview](trees/high-swell-tree/high-swell-tree.png)

| Dimension | mm | inches |
|-----------|-----|--------|
| Bar-to-bar width | 355.6 | 14.0" — standard QH gullet |
| Tree depth front→back | 588.6 | 23.2" |
| Overall height | 347.3 | 13.7" — base to horn tip |

**Boolean tools:** CantleCutter · CantleAdder · SeatScoopCutter ·
BarCurveCutter\_L · BarCurveCutter\_R · SwellCutter · HornCutter · HornAdder

---

### low-cantle-no-horn-saddle-tree

Hornless tree with a low-profile solid cantle.  Designed for endurance
and trail riding where light weight and freedom of movement matter.

![low-cantle-no-horn-saddle-tree preview](trees/low-cantle-no-horn-saddle-tree/low-cantle-no-horn-saddle-tree.png)

| Dimension | mm | inches |
|-----------|-----|--------|
| Bar-to-bar width | 355.6 | 14.0" — standard QH gullet |
| Tree depth front→back | 231.1 | 9.1" |
| Overall height | 137.6 | 5.4" |

**Boolean tools:** CantleCutter · CantleAdder · SeatScoopCutter ·
BarCurveCutter\_L · BarCurveCutter\_R · GulletCutter\_L · GulletCutter\_R ·
PommelCapAdder

---

### roping-tree

Long, strong roping tree.  Stout horn sized for dally wrapping, long bars
for weight distribution, flat seat for quick dismount, double-rigging
mortises for front and rear cinch.

![roping-tree preview](trees/roping-tree/roping-tree.png)

| Dimension | mm | inches |
|-----------|-----|--------|
| Bar-to-bar width | 343.5 | 13.5" — semi-QH gullet |
| Tree depth front→back | 609.6 | 24.0" |
| Overall height | 235.7 | 9.3" |

**Boolean tools:** HornCutter · HornAdder · SwellCutter · SeatScoopCutter ·
BarCurveCutter\_L · BarCurveCutter\_R · CantleCutter · CantleAdder ·
RiggingMortise\_FL · RiggingMortise\_FR · RiggingMortise\_RL · RiggingMortise\_RR

---

### split-cantle-no-horn-saddle-tree

Hornless tree with a vertical slot through the rear cantle face, leaving
two lateral wings.  Reduces weight and allows pelvic tilt for a
lower-back-friendly position on long rides.

![split-cantle-no-horn-saddle-tree preview](trees/split-cantle-no-horn-saddle-tree/split-cantle-no-horn-saddle-tree.png)

| Dimension | mm | inches |
|-----------|-----|--------|
| Bar-to-bar width | 355.6 | 14.0" — standard QH gullet |
| Tree depth front→back | 321.6 | 12.7" |
| Overall height | 190.1 | 7.5" |

**Boolean tools:** CantleSplitCutter **(Red — apply first)** ·
CantleWingCutter\_L · CantleWingCutter\_R · CantleBodyCutter · CantleAdder ·
SeatScoopCutter · BarCurveCutter\_L · BarCurveCutter\_R ·
GulletCutter\_L · GulletCutter\_R · PommelCapAdder

---

### split-cantle-horn-tree

The most fully tooled tree.  Combines a split cantle (long-ride comfort)
with a full western horn (dally wrap, grab point on rough terrain).
Uses all five tool colours.

![split-cantle-horn-tree preview](trees/split-cantle-horn-tree/split-cantle-horn-tree.png)

| Dimension | mm | inches |
|-----------|-----|--------|
| Bar-to-bar width | 338.9 | 13.3" — semi-QH gullet |
| Tree depth front→back | 558.8 | 22.0" |
| Overall height | 208.0 | 8.2" |

**Boolean tools:** CantleSplitCutter **(Red — apply first)** ·
CantleWingCutter\_L · CantleWingCutter\_R · CantleBodyCutter · CantleAdder ·
HornCutter · HornAdder · SwellCutter · SeatScoopCutter ·
BarCurveCutter\_L · BarCurveCutter\_R ·
GulletCutter\_L · GulletCutter\_R ·
RiggingMortise\_FL · RiggingMortise\_FR · RiggingMortise\_RL · RiggingMortise\_RR

---

## Repository structure

```
saddle-examples-Blender/
├── docs/
│   ├── workflow.md              ← detailed step-by-step workflow guide
│   ├── getting-started.md       ← quick-start for first-time users
│   ├── anatomy-reference.md     ← saddle anatomy glossary
│   └── blender-version-notes.md ← API compatibility reference
├── tools/
│   └── validate_stl.py          ← STL validator (run before contributing)
└── trees/
    ├── saddle_addon_utils.py    ← shared Blender utility module
    ├── high-swell-tree/
    │   ├── high-swell-tree.stl
    │   ├── high-swell-tree.py
    │   └── high-swell-tree.png
    └── ...                      ← four more tree folders, same structure
```

---

## How the scripts work

Each `.py` script performs three steps when you run it:

1. **Import** — loads the STL mesh into a new Blender scene using
   `bpy.ops.wm.stl_import()`.
2. **Clean up** — runs a `bmesh` pass to weld near-duplicate vertices and
   fill any small holes in the mesh surface.
3. **Create tools** — adds named cube and cylinder objects (the boolean
   tools), assigns shared colour materials, and attaches a non-destructive
   Boolean modifier to the saddle mesh for each tool.

The Boolean modifiers preview cuts and additions live in the viewport.
Nothing is applied permanently until you click Apply on a modifier.

---

## Coordinate convention

All five trees share the same axis orientation:

| Axis | Direction |
|------|-----------|
| X | Left (negative) → Right (positive), centred at 0 |
| Y | Front / pommel end (negative) → Rear / cantle (positive) |
| Z | Down / bar underside (negative) → Up / horn tip (positive) |

The world origin (0, 0, 0) is at the geometric centre of each tree.

---

## Contributing

Pull requests are welcome.  See [CONTRIBUTING.md](CONTRIBUTING.md) for the
full checklist.  Key requirements for a new tree:

- Binary STL scaled to real-world dimensions, centred at world origin.
- Script uses `saddle_addon_utils` — no inline factory functions.
- All L/R tool pairs verified symmetric (`verify_lr_symmetry()` called).
- Teal gullet cutters present, labelled "SAFETY-CRITICAL".
- PNG preview image included.

---

## Licence

| Content | Licence |
|---------|---------|
| `.py` script files | [MIT](LICENSES/MIT.txt) |
| `.stl` mesh files and `.png` images | [CC BY 4.0](LICENSES/CC-BY-4.0.txt) |
