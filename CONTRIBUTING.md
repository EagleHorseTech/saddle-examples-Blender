# Contributing to saddle-examples-Blender

Thank you for your interest in contributing.  This document covers the
requirements for adding a new tree, fixing a bug, or updating documentation.

---

## Prerequisites

- **Blender 5.1** for testing scripts.
- **Python 3.11+** (system install) for running `tools/validate_stl.py`.
- **Git LFS** installed (`git lfs install`) — required for `.stl` and `.png` files.

---

## Adding a new tree

Use the prompt in `.ai/prompts/add-new-tree.md` to get AI assistance.

Manual checklist:

### 1. STL file requirements

- [ ] Binary STL format (not ASCII).
- [ ] Scaled to real-world Quarter Horse dimensions (or explicitly documented otherwise).
- [ ] Centred at the world origin (0, 0, 0) — bounding-box midpoint ≈ (0, 0, 0).
- [ ] Passes `tools/validate_stl.py` with no errors.
- [ ] Tracked by Git LFS: `git lfs track "*.stl"` (already configured in `.gitattributes`).

### 2. Script requirements

- [ ] Named identically to the STL (stem only), e.g. `wade-tree.py`.
- [ ] Uses `from saddle_addon_utils import ...` — no inline factory functions.
- [ ] Passes syntax check: `python -m py_compile trees/wade-tree/wade-tree.py`.
- [ ] Passes pyflakes: `python -m pyflakes trees/wade-tree/wade-tree.py`.
- [ ] All L/R tool pairs verified symmetric: `verify_lr_symmetry()` called for each pair.
- [ ] Teal gullet cutters present with "SAFETY-CRITICAL" in their label.
- [ ] Coordinate comment at the top documenting the bounding box.

### 3. Documentation requirements

- [ ] Entry added to README catalogue table.
- [ ] Entry added to README tree details section.
- [ ] CHANGELOG.md updated under `[Unreleased]`.
- [ ] PNG preview image included in the tree folder (tracked by Git LFS).

---

## Commit message format

This project uses [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(trees): add wade-tree script and STL
fix(utils): correct cylinder placement formula
docs(readme): update catalogue table for wade-tree
test(ci): add syntax check for new tree scripts
```

---

## Code style

- Python: follow PEP 8.  4-space indentation.  Maximum line length 99 characters.
- Use the `.editorconfig` settings (UTF-8, LF line endings, trailing newline).

---

## Pull request process

1. Fork the repository and create a feature branch: `git checkout -b feat/wade-tree`.
2. Make your changes following the checklist above.
3. Run `tools/validate_stl.py` on any new STL files.
4. Run `python -m py_compile` on any new `.py` files.
5. Open a pull request against `main`.
6. Complete the pull request template.

---

## Licence

By contributing, you agree that:
- Your `.py` script contributions are submitted under the **MIT licence**.
- Your `.stl` mesh and `.png` image contributions are submitted under the **CC BY 4.0 licence**.
