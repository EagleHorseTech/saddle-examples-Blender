## Description

What does this PR do?  Reference any related issues with `Fixes #NNN`.

## Type of change

- [ ] Bug fix
- [ ] New tree (adds a new saddle tree script and STL)
- [ ] Documentation update
- [ ] CI / tooling change
- [ ] Other (describe):

## Checklist

### For all PRs
- [ ] Python files pass syntax check: `python -m py_compile <file.py>`
- [ ] Python files pass pyflakes: `python -m pyflakes <file.py>`
- [ ] CHANGELOG.md updated under `[Unreleased]`

### For new tree scripts
- [ ] STL is binary format, centred at world origin (±0.5 mm on all axes)
- [ ] STL passes `tools/validate_stl.py` with no FAIL results
- [ ] Script uses `from saddle_addon_utils import …` — no inline factory functions
- [ ] `__file__` guard uses the `try/except NameError` pattern from other scripts
- [ ] All L/R tool pairs call `verify_lr_symmetry()` and report zero drift
- [ ] Teal gullet cutters present and labelled with "SAFETY-CRITICAL"
- [ ] Bounding-box comment at the top of the tool-placeholders section
- [ ] PNG preview image included in the tree folder
- [ ] STL and PNG tracked by Git LFS (`git lfs ls-files` confirms)
- [ ] README catalogue table updated
- [ ] README tree details section updated

## Testing

Describe how you tested this change (Blender version, OS, steps taken).

## Screenshots

If this is a visual change (new tree, viewport fix), add before/after screenshots.
