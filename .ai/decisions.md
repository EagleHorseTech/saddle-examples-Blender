# Architecture Decision Records — saddle-examples-Blender

Each ADR documents a significant decision: the context, the options
considered, the decision made, and the consequences.

Format adapted from Michael Nygard's ADR template.

---

## ADR-B001 — Standalone scripts, not a Blender add-on (v1.0)

**Date:** 2026-04-30
**Status:** Accepted

### Context

Blender Python automation can be delivered as:
1. Standalone `.py` scripts run from the built-in Text editor.
2. A proper Blender add-on with `bl_info`, operators, and a UI panel.
3. A hybrid: scripts that can be run both ways.

### Options considered

1. Standalone scripts only (exact analogue of `.FCMacro` pattern).
2. Full add-on with N-panel UI.
3. Hybrid: scripts that register operators if run as an add-on, or execute directly if run as a script.

### Decision

Option 1 (standalone scripts) for v1.0. Option 2 planned for v2.0.

### Rationale

The `.FCMacro` pattern works: users paste the script into the Text editor and
click Run. This is the exact analogue and the simplest entry point. A full
add-on requires install/enable steps and a more complex Python module structure.
The v1.0 goal is functional parity with the FreeCAD package, not UI feature parity.

### Consequences

- Lower barrier to entry — no installation needed, just paste and run.
- No persistent UI elements — users must re-run the script to recreate tools.
- v2.0 add-on work can reuse the same utility module.

---

## ADR-B002 — Use saddle_addon_utils.py shared module from day one

**Date:** 2026-04-30
**Status:** Accepted

### Context

The FreeCAD project had all five macros with duplicated factory functions.
`saddle_macro_utils.py` was added later (ADR-004 in the FreeCAD project).
This created a backlog item (B-4) to refactor the existing macros.

### Decision

All five Blender scripts use `saddle_addon_utils.py` from the start.
No script contains inline factory functions.

### Rationale

The FreeCAD project demonstrated the maintenance cost of duplication.
Starting with the shared module eliminates that technical debt entirely.

### Consequences

- All scripts have a `sys.path.insert` + import block at the top.
- The utility module must be tested before any tree script is created.
- Bug fixes and API updates need to be made in only one place.

---

## ADR-B003 — Boolean modifiers, not applied immediately

**Date:** 2026-04-30
**Status:** Accepted

### Context

In FreeCAD, `Part → Boolean → Cut` applies immediately and creates a new
permanent solid. In Blender, Boolean can be applied immediately (using
`bpy.ops.object.modifier_apply()`) or left as a non-destructive modifier.

### Decision

Scripts add Boolean modifiers but do NOT call `modifier_apply()`.

### Rationale

Non-destructive is strictly better for the iterative saddle-fitting workflow.
The user can resize a tool, see the modifier preview in real time, and only
apply when satisfied. This is an improvement over the FreeCAD workflow.
The workflow documentation must explain this clearly.

### Consequences

- More complex explanation needed in docs/workflow.md.
- Users who want permanent geometry must apply modifiers manually.
- Better user experience for iterative adjustment.

---

## ADR-B004 — Shared material palette, not per-object colours

**Date:** 2026-04-30
**Status:** Accepted

### Context

FreeCAD sets `obj.ViewObject.ShapeColor` directly on each object.
In Blender, colour requires a Material. Materials can be created per-object
or shared across objects.

### Options

1. Create a new material for every tool object.
2. Create a shared palette of six named materials, reused across all objects.

### Decision

Shared palette (option 2). `create_material_palette()` creates the six
standard materials on first call; on subsequent calls it checks if they
already exist and reuses them.

### Rationale

Creating a material per object leads to dozens of nearly identical materials
in the scene. This clutters the Material browser, increases file size, and
makes it hard to change all cutters of one colour simultaneously.
A shared palette is cleaner and more maintainable.

### Consequences

- `create_material_palette()` must be called before any `make_box()` or
  `make_cylinder()` call.
- Re-running a script does not create duplicate materials.
- Changing all blue cutters' transparency requires editing only one material.

---

## ADR-B005 — Placement convention: FreeCAD min-corner → Blender centre

**Date:** 2026-04-30
**Status:** Accepted

### Context

FreeCAD `Part::Box` uses `(x, y, z)` as the minimum corner of the box,
with the box extending in the +X, +Y, +Z directions.
Blender `primitive_cube_add` places the cube with `location` at the centre.

This is a systematic difference that affects every tool in every script.

### Decision

The conversion formula is:
```python
blender_x = x + l / 2
blender_y = y + w / 2
blender_z = z + h / 2
obj.location = (blender_x, blender_y, blender_z)
obj.scale    = (l / 2, w / 2, h / 2)
```
This formula is encapsulated in `saddle_addon_utils.make_box()` so that
all scripts pass FreeCAD min-corner values and the conversion is automatic.

### Rationale

Encapsulating the conversion in the utility module means the coordinate
data in each script can be copied directly from the FCMacro source without
manual recalculation, reducing transcription errors.

### Consequences

- The utility module's `make_box()` signature is identical to the FreeCAD
  `make_box()` signature: `(name, label, x, y, z, l, w, h, color)`.
- The internal implementation differs, but callers see the same interface.
- The L/R symmetry check changes: in Blender, `right_obj.location.x == -left_obj.location.x`
  (checking centres, not min-corners). The utility module should verify this
  and print a warning if drift is detected.

---

## ADR-B006 — Dual licence retained: MIT for code, CC BY 4.0 for assets

**Date:** 2026-04-30
**Status:** Accepted

Same rationale as FreeCAD project ADR-001. Python scripts → MIT.
STL meshes and PNG images → CC BY 4.0. Two licence files in `LICENSES/`.

---

## ADR-B007 — STL files are shared between FreeCAD and Blender packages

**Date:** 2026-04-30
**Status:** Accepted

### Decision

The `.stl` files from the FreeCAD project are used unchanged in the Blender
project. No conversion or modification is performed.

### Rationale

Binary STL is a format-agnostic triangle mesh. Both FreeCAD and Blender
import it identically. The meshes are already centred at world origin and
scaled to real-world Quarter Horse dimensions — these properties are
geometry properties of the STL, not FreeCAD-specific.

### Consequences

- No STL processing step needed in the conversion workflow.
- Changes to STL files must be synchronised between both repos (or one
  repo can reference the other via a git submodule in the future).
- Licence attribution (CC BY 4.0) applies to the STL files in both repos.
