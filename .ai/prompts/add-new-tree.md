# Prompt: Add a new saddle tree (Blender package)

Use this prompt when adding a new tree to the Blender package.

---

## Prompt to paste

> I need to add a new tree to the `saddle-examples-Blender` repository.
>
> Please read `.ai/claude.md` for full project context before starting.
>
> **New tree details:**
> - Tree name (folder name, snake-case):  [e.g. wade-tree]
> - Discipline:  [e.g. Ranch / cutting]
> - Horn:  [yes / no, describe]
> - Cantle:  [solid / split, describe height]
> - Gullet (bar-to-bar width):  [mm and inches]
> - Tree depth (front → back):  [mm and inches]
> - Overall height (base → horn tip):  [mm and inches]
> - STL file provided:  [yes / no]
>
> **Boolean tools needed:**  [list by name, e.g. HornCutter, HornAdder, etc.]
>
> **Bounding box of the new STL:**
> - X: [min] → [max]  (width: [mm])
> - Y: [min] → [max]  (depth: [mm])
> - Z: [min] → [max]  (height: [mm])
>
> Please:
> 1. Create `trees/[tree-name]/[tree-name].py` using `saddle_addon_utils`.
> 2. Add the entry to the README catalogue table.
> 3. Add the entry to CHANGELOG.md.
> 4. Verify L/R symmetry for all paired tools.
> 5. Verify gullet-width label on teal tools.
> 6. Check the new STL with `tools/validate_stl.py`.

---

## Checklist for reviewer

Before merging a new tree PR:

- [ ] `[tree-name].py` uses `saddle_addon_utils` — no inline factory functions.
- [ ] STL is binary format, centred at world origin (0,0,0) on all axes.
- [ ] `validate_stl.py` passes with no errors.
- [ ] All L/R tool pairs satisfy `right_blender_x == -left_blender_x`.
- [ ] Gullet-width teal tools are present and labelled as safety-critical.
- [ ] README catalogue table updated.
- [ ] CHANGELOG.md updated.
- [ ] PNG preview image included.
- [ ] Git LFS is tracking the new `.stl` and `.png` (confirm with `git lfs ls-files`).
