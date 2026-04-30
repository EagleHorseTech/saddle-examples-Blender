# Prompt: Update scripts for a new Blender version

Use this prompt when Blender releases a new version that may require
API changes to the scripts.

---

## Prompt to paste

> I need to update `saddle-examples-Blender` for **Blender [version]**.
>
> Please read `.ai/claude.md` for full project context.
>
> The following API changes are known or suspected for this version:
> [list any known breaking changes here, or "unknown — please investigate"]
>
> Please:
> 1. Check `bpy.ops.wm.stl_import()` — still available? Parameters changed?
> 2. Check `bmesh.ops.remove_doubles()` and `holes_fill()` — still available?
> 3. Check `bpy.data.collections.new()` and `scene.collection.children.link()`.
> 4. Check `bpy.ops.mesh.primitive_cube_add()` and `primitive_cylinder_add()`.
> 5. Check Boolean modifier syntax: `obj.modifiers.new(type='BOOLEAN')`.
> 6. Update `docs/blender-version-notes.md` with findings.
> 7. Update `saddle_addon_utils.py` if any API changes are required.
> 8. If a tree script needs updating, update all five consistently.
> 9. Update the version target in `.ai/claude.md`.
> 10. Add a CHANGELOG entry.

---

## API stability history (update as versions are tested)

| Blender version | STL import | bmesh | Boolean modifier | Tested? |
|----------------|-----------|-------|-----------------|---------|
| 4.0 | `wm.stl_import` (legacy `import_mesh.stl` removed) | OK | OK | — |
| 4.x | `wm.stl_import` | OK | OK | — |
| 5.1 | `wm.stl_import` | OK | OK | Target |
