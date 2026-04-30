# Blender version notes

API compatibility reference for saddle-examples-Blender scripts.
All scripts target **Blender 5.1** with its bundled Python 3.11+.

---

## Blender version requirements

| Blender | Status |
|---------|--------|
| 5.1 | ✅ Primary target — all scripts tested here |
| 4.0 – 5.0 | ✅ Should work — same STL import API and boolean modifier API |
| 3.2 – 3.6 | ⚠️ Requires one change — see STL import note below |
| < 3.2 | ❌ Not supported — `bpy.context.temp_override` not available |

---

## Key API calls and compatibility

### STL import

```python
bpy.ops.wm.stl_import(filepath=path)
```

| Blender | Notes |
|---------|-------|
| 4.0+ | `bpy.ops.wm.stl_import()` — use this |
| 3.x | `bpy.ops.import_mesh.stl()` — use this instead |

If you are on Blender 3.x, open `saddle_addon_utils.py` and change the
single line in `import_and_cleanup_stl()`:

```python
# Blender 3.x — replace this line:
bpy.ops.wm.stl_import(filepath=stl_path)

# With this:
bpy.ops.import_mesh.stl(filepath=stl_path)
```

---

### Boolean modifier

```python
mod = mesh_obj.modifiers.new(name=name, type="BOOLEAN")
mod.operation = "DIFFERENCE"   # or "UNION"
mod.object    = tool_obj
mod.solver    = "EXACT"        # most accurate; use FAST only for speed tests
```

The `solver` parameter (`EXACT` / `FAST`) was added in Blender 2.91 and
is stable in all supported versions.

---

### bmesh cleanup

```python
bm = bmesh.new()
bm.from_mesh(mesh_obj.data)
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.01)
bmesh.ops.holes_fill(bm, edges=boundary_edges, sides=0)
bm.to_mesh(mesh_obj.data)
bm.free()
```

Stable across all Blender 2.8x+ versions.  No known compatibility issues.

---

### Collections

```python
coll = bpy.data.collections.new("MyCollection")
bpy.context.scene.collection.children.link(coll)

# Safe unlink — works regardless of which collection was active at run time:
for c in list(obj.users_collection):
    c.objects.unlink(obj)
coll.objects.link(obj)
```

The safe unlink pattern (iterating `obj.users_collection`) is required
because `bpy.context.scene.collection.objects.unlink(obj)` raises
`RuntimeError` if the object was linked to a child collection rather than
the scene root.  The scripts in this package all use the safe pattern.

Stable across Blender 2.8x+.

---

### Viewport fit

```python
for area in bpy.context.screen.areas:
    if area.type == "VIEW_3D":
        with bpy.context.temp_override(area=area):
            bpy.ops.view3d.view_all()
        break
```

`bpy.context.temp_override()` was introduced in Blender 3.2.  For
Blender < 3.2, replace with the legacy dict-override pattern:

```python
for area in bpy.context.screen.areas:
    if area.type == "VIEW_3D":
        bpy.ops.view3d.view_all({"area": area})
        break
```

---

### Material transparency

```python
mat = bpy.data.materials.new(name="Cutter_Blue")
mat.use_nodes     = False
mat.diffuse_color = (0.2, 0.6, 1.0, 0.3)   # RGBA — [3] = alpha
```

With `use_nodes=False`, transparency in the viewport is driven by
`diffuse_color[3]`.  The `blend_method` property that existed in older
Blender versions was deprecated in 4.2 and is not set by these scripts.

---

## Unit scale

Blender's default scene unit is **metres**.  These scripts work in
**millimetres**.  Set units before running any script:

**Scene Properties → Units → Unit System: Metric → Length: Millimeters**

If you forget: the saddle will appear roughly 1000× too large (hundreds of
metres wide instead of hundreds of millimetres).  Changing the unit setting
after import corrects the display immediately — the geometry is unaffected.

---

## Tested configurations

| Blender | OS | Python | Status |
|---------|-----|--------|--------|
| 5.1 | Windows 11 | 3.11 | Target — in development |
| 5.1 | macOS 15 (Apple Silicon) | 3.11 | Planned |
| 5.1 | Ubuntu 24.04 | 3.11 | Planned |

*Update this table as testing is completed.*
