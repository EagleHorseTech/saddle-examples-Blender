# Prompt: Review a pull request

Use this prompt when reviewing a PR to the Blender package.

---

## Prompt to paste

> Please review this pull request to `saddle-examples-Blender`.
>
> Read `.ai/claude.md` for project context before reviewing.
>
> PR contents:
> [paste the diff or describe the changes]
>
> Please check:
> 1. Does the script use `saddle_addon_utils`? No inline factory functions?
> 2. Are all tool coordinates correct (min-corner convention passed in)?
> 3. Are L/R pairs symmetric? (`right_blender_x == -left_blender_x` for centres)
> 4. Are teal gullet tools present and labelled safety-critical?
> 5. Is the Blender 5.1 STL import API used (`bpy.ops.wm.stl_import`)?
> 6. Is the material palette used (not raw colour tuples)?
> 7. Is there a facet-count guard (>= 1000 triangles)?
> 8. Does the script handle the case where STL path is not found?
> 9. Is CHANGELOG.md updated?
> 10. Is README.md updated if a new tree was added?
> 11. Are the STL and PNG tracked by Git LFS?
>
> Provide a structured review with: Summary / Issues (blocking) / Suggestions (non-blocking).
