# Project context — saddle-examples-Blender

Load this file at the start of every AI-assisted session on this repo.
It gives Claude (or any AI assistant) the full technical context needed
to work effectively without a lengthy briefing.

---

## What this repo is

A collection of five western saddle-tree STL meshes paired with Blender 5.1
Python scripts. Each script:
1. Imports the STL as a Blender mesh object.
2. Runs a mesh cleanup pass (remove doubles, fill holes) using bmesh.
3. Creates named, colour-coded boolean-tool primitives (cubes and cylinders)
   pre-positioned over anatomically correct saddle regions.
4. Organises everything into named Collections in the Blender Outliner.

Tools are NOT applied automatically — they are placeholders the user resizes
in the Properties panel and applies via the Boolean modifier.

**Source repo (FreeCAD original):**
https://github.com/EagleHorseTech/saddle-examples-FreeCAD

**This repo (Blender conversion):**
https://github.com/EagleHorseTech/saddle-examples-Blender  (planned)

---

## Blender version target

**Blender 5.1** — primary development and test target.
Python 3.11+ (Blender's bundled Python).
STL import uses `bpy.ops.wm.stl_import()` (legacy `import_mesh.stl` removed in 4.0).

---

## Coordinate convention

All five trees follow this convention (identical to FreeCAD source project):

| Axis | Direction |
|------|-----------|
| X | Left (negative) → Right (positive), centred at 0 |
| Y | Front / horn end (negative) → Rear / cantle (positive) |
| Z | Down / bar underside (negative) → Up / horn tip (positive) |

All trees are centred at the world origin (0, 0, 0).
Mirror axis is always X (Blender Mirror modifier default).

---

## Colour key (consistent across all five scripts)

| Colour | RGB tuple | Blender material name | Meaning | Operation |
|--------|-----------|----------------------|---------|-----------|
| Red | (0.9, 0.2, 0.2) | `Cutter_Red` | CantleSplitCutter | Difference |
| Blue | (0.2, 0.6, 1.0) | `Cutter_Blue` | Standard cutters | Difference |
| Teal | (0.4, 0.8, 1.0) | `Cutter_Teal` | Gullet-width cutters | Difference |
| Purple | (0.6, 0.4, 1.0) | `Cutter_Purple` | Rigging mortise cutters | Difference |
| Orange | (1.0, 0.5, 0.1) | `Cutter_Orange` | Seat scoop cutter | Difference |
| Green | (0.2, 1.0, 0.4) | `Adder_Green` | Adders | Union |

All tool objects: alpha 0.3 (70% transparent) in Blender viewport.
Materials are created once by `create_material_palette()` and reused by name.

---

## Tree catalogue

| Folder | Discipline | Horn | Cantle | Gullet | Depth |
|--------|-----------|------|--------|--------|-------|
| `high-swell-tree` | Ranch / barrel | Yes — tall | Solid | 14.0" (355.6 mm) | 23.2" (588.6 mm) |
| `low-cantle-no-horn-saddle-tree` | Endurance / trail | No | Solid, low | 14.0" (355.6 mm) | 9.1" (231.1 mm) |
| `roping-tree` | Ranch roping | Yes — stout | Solid, moderate | 13.5" (343.5 mm) | 24.0" (609.6 mm) |
| `split-cantle-no-horn-saddle-tree` | Endurance / trail | No | Split wings | 14.0" (355.6 mm) | 12.7" (321.6 mm) |
| `split-cantle-horn-tree` | Ranch / trail hybrid | Yes — moderate | Split wings | 13.3" (338.9 mm) | 22.0" (558.8 mm) |

---

## Repository structure

```
saddle-examples-Blender/
├── .ai/                        ← AI-assisted development context
│   ├── claude.md               ← (this file) project context
│   ├── memory.md               ← settled decisions and why
│   ├── restart.md              ← compact session pickup prompt
│   ├── backlog.md              ← prioritised work items
│   ├── decisions.md            ← Architecture Decision Records
│   └── prompts/                ← reusable prompt templates
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── new_tree_request.md
│   ├── pull_request_template.md
│   └── workflows/
│       └── syntax-check.yml    ← CI: Python syntax check (py -m py_compile)
├── docs/
│   ├── anatomy-reference.md    ← saddle anatomy glossary (copied from FreeCAD)
│   ├── blender-version-notes.md
│   ├── freecad-migration.md    ← how to migrate from FreeCAD package
│   └── workflow.md             ← detailed Blender boolean workflow guide
├── LICENSES/
│   ├── MIT.txt                 ← applies to .py script files
│   └── CC-BY-4.0.txt           ← applies to .stl and .png files
├── tools/
│   └── validate_stl.py         ← pre-submission STL validator (same as FreeCAD)
├── trees/
│   ├── saddle_addon_utils.py   ← shared Blender utility module
│   ├── high-swell-tree/
│   │   ├── high-swell-tree.stl  (same STL as FreeCAD project)
│   │   ├── high-swell-tree.py   (converted from .FCMacro)
│   │   └── high-swell-tree.png
│   └── ...                     ← four more tree folders, same structure
├── .editorconfig
├── .gitattributes              ← LFS tracking for .stl and .png
├── .gitignore
├── CHANGELOG.md
├── CITATION.cff
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
└── SECURITY.md
```

---

## Shared utility module

`trees/saddle_addon_utils.py` exports:

- `create_material_palette()` → dict of {name: material}
- `import_and_cleanup_stl(stl_path)` → `(mesh_obj, cleanup_ok)`
- `make_collections(mesh_obj)` → `coll_tools`
- `make_box(coll_tools, name, label, x, y, z, l, w, h, color_name)` → `obj`
- `make_cylinder(coll_tools, name, label, x, y, z, r, h, color_name)` → `obj`
- `finalise(mesh_obj, cleanup_ok)`

Import pattern in a tree script:
```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from saddle_addon_utils import (
    create_material_palette, import_and_cleanup_stl,
    make_collections, make_box, make_cylinder, finalise
)
```

---

## Key API translations (FreeCAD → Blender 5.1)

| Operation | FreeCAD | Blender 5.1 |
|-----------|---------|-------------|
| Import STL | `Mesh.insert(path, doc.Name)` | `bpy.ops.wm.stl_import(filepath=path)` |
| Mesh cleanup | `MeshPart.meshToShape()` → `Part.makeSolid()` | `bmesh.ops.remove_doubles()` + `holes_fill()` |
| Create box | `doc.addObject("Part::Box", name)` | `bpy.ops.mesh.primitive_cube_add()` + scale |
| Create cylinder | `doc.addObject("Part::Cylinder", name)` | `bpy.ops.mesh.primitive_cylinder_add()` |
| Set colour | `obj.ViewObject.ShapeColor = (r,g,b)` | Assign named material from palette |
| Transparency | `obj.ViewObject.Transparency = 70` | `mat.diffuse_color = (r,g,b,0.3)` |
| Group | `doc.addObject("App::DocumentObjectGroup")` | `bpy.data.collections.new(label)` |
| Recompute | `doc.recompute()` | `bpy.context.view_layer.update()` |
| View fit | `Gui.SendMsgToActiveView("ViewFit")` | `bpy.ops.view3d.view_all()` |
| Boolean cut | `Part → Boolean → Cut` | Add Boolean modifier, DIFFERENCE |
| Boolean union | `Part → Boolean → Union` | Add Boolean modifier, UNION |
| Mirror | `Part → Mirror, YZ plane` | Mirror modifier, X axis |

---

## Symmetry rule (same as FreeCAD project)

For every left/right boolean tool pair:
```
right_x == −left_x − left_l
```
where `left_l` is the X dimension of the left tool.

In Blender terms: `right_obj.location.x == -left_obj.location.x` when using
the cube-centred placement convention (location = centre, not min-corner).
Scripts must convert min-corner (FreeCAD convention) to centre (Blender
convention): `blender_location_x = x + l/2`.

---

## Placement convention difference (critical!)

FreeCAD `Part::Box` placement: `(x, y, z)` is the **minimum corner**.
Blender `primitive_cube_add` placement: `location` is the **centre**.

Conversion formula:
```python
# Given FreeCAD min-corner (x, y, z) and dimensions (l, w, h):
blender_x = x + l / 2
blender_y = y + w / 2
blender_z = z + h / 2
obj.location = (blender_x, blender_y, blender_z)
obj.scale    = (l / 2, w / 2, h / 2)  # primitive_cube_add creates a 2×2×2 cube
```

For `Part::Cylinder`: FreeCAD `(x, y, z)` is the **centre of the bottom disk**.
Blender `primitive_cylinder_add`: location is the **centre of the cylinder body**.
```python
blender_x = x
blender_y = y
blender_z = z + h / 2
obj.location = (blender_x, blender_y, blender_z)
obj.scale    = (r, r, h / 2)  # default cylinder: radius 1, height 2
```

---

## Gullet safety rule (non-negotiable)

Gullet width ≥ 70 mm (2.75") at the narrowest point. This must be
verified in every tree script and documented in the teal tool labels.

---

## Known issues carried from FreeCAD project

- **T-1**: `high-swell-tree` README Y-axis description is inverted.
  When creating the Blender version, fix this in the README entry.
  The STL itself and the tool coordinates are correct — only the prose description is wrong.

---

## Dual licence

- `.py` script files: MIT (see `LICENSES/MIT.txt`)
- `.stl` and `.png` files: CC BY 4.0 (see `LICENSES/CC-BY-4.0.txt`)
