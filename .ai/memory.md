# Memory — settled decisions and context

This file records facts and decisions that are settled and should not be
re-litigated. Update it when new consensus is reached.

---

## Technical facts

- All five tree STL files are **format-agnostic binary STL** — no conversion
  needed. The same files used in the FreeCAD project are used here unchanged.

- All coordinate data (x, y, z, l, w, h, r values) from the FCMacro tool
  blocks is **copied verbatim** to the Blender scripts. Only API call syntax
  changes.

- **Placement convention differs** between FreeCAD and Blender:
  - FreeCAD `Part::Box`: `(x,y,z)` = minimum corner
  - Blender `primitive_cube_add`: `location` = centre of the object
  - Conversion: `blender_x = x + l/2`, `blender_y = y + w/2`, `blender_z = z + h/2`
  - Scale: `(l/2, w/2, h/2)` (default cube is 2×2×2 units)

- **Cylinder placement differs**:
  - FreeCAD: `(x,y,z)` = centre of bottom disk
  - Blender: `location` = centre of cylinder body
  - Conversion: `blender_z = z + h/2`; scale = `(r, r, h/2)`

- **Blender 5.1 STL import**: use `bpy.ops.wm.stl_import(filepath=path)`.
  The legacy `bpy.ops.import_mesh.stl()` operator was removed in Blender 4.0.

- **No OpenCASCADE in Blender**: the three-stage mesh-to-solid pipeline
  (`meshToShape` → `makeSolid` → `fixTolerance`) has no equivalent.
  Replace with a `bmesh` cleanup pass. Results are meshes, not B-Rep solids.

- **T-1 from FreeCAD project**: `high-swell-tree` README Y-axis description
  is inverted (says "Cantle at negative Y" when it should be "Horn at negative Y").
  This is a prose bug only — the STL and coordinates are correct.
  **Fix this in the Blender README when creating that tree's entry.**

---

## Design decisions

- **Standalone scripts, not a full add-on panel (v1.0)**. Scripts run from
  Blender's built-in Text editor, analogous to `.FCMacro`. A UI panel add-on
  is a planned v2.0 enhancement.

- **Boolean modifiers are NOT applied automatically**. This is even more
  non-destructive than FreeCAD's immediate-apply model. Users apply when ready.

- **Shared material palette**. Six named materials (`Cutter_Red`,
  `Cutter_Blue`, `Cutter_Teal`, `Cutter_Purple`, `Cutter_Orange`,
  `Adder_Green`) are created by `create_material_palette()` on first run.
  If materials already exist in the scene (re-run), they are reused.

- **World-origin centring mandatory** — same rule as FreeCAD project.
  Mirror modifier uses X axis (default), which bisects at X=0.

- **Dual licence retained**: MIT for `.py` scripts, CC BY 4.0 for `.stl`
  and `.png` files. Same rationale as FreeCAD project (ADR-001).

---

## Process decisions

- **Conventional Commits** format for commit messages (same as FreeCAD project).
- **Keep a Changelog** format for CHANGELOG.md.
- **Semantic Versioning** for releases. First release: v1.0.0.
- **Git LFS** tracks `*.stl` and `*.png` (same as FreeCAD project).

---

## Things that were tried and rejected

_(Record here if any approaches were explicitly tried and found to not work,
so they are not re-proposed in future sessions.)_

- None yet.
