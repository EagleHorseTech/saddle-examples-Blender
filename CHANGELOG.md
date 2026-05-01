# Changelog

All notable changes to saddle-examples-Blender are documented here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

---

## [Unreleased] — RC-002-A

### Added
- `README.md`: PNG preview image added to each of the five tree-details
  sections (`high-swell-tree`, `low-cantle-no-horn-saddle-tree`,
  `roping-tree`, `split-cantle-no-horn-saddle-tree`, `split-cantle-horn-tree`).
- `README.md`: Quick-start Git LFS note updated to mention `.png` files
  are also LFS-tracked.

---


All notable changes to saddle-examples-Blender are documented here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
Versioning: [Semantic Versioning](https://semver.org/spec/v2.0.0.html)

---

## [Unreleased] — rev-003

### Changed
- All user-facing documentation rewritten for a Blender-only audience.
  No external tool references remain in any documentation file.
- `docs/getting-started.md` added (replaces the old migration guide); `docs/getting-started.md` —
  a complete first-use guide for Blender users new to this package.
- `docs/workflow.md` fully rewritten as a 14-section step-by-step guide
  covering unit setup, running scripts, resizing tools, applying boolean
  operations, split-cantle workflow, mirroring, bar rock/twist, gullet
  adjustment, troubleshooting, export, and the gullet safety checklist.
- `README.md` rewritten: leads with a five-step quick start, removes all
  references to other tools, adds colour-key table and gullet safety
  warning at the top level.
- `docs/blender-version-notes.md` updated: safe collection-unlink pattern
  documented, `blend_method` deprecation note updated.

### Fixed — `.github/workflows/syntax-check.yml`
- **Bash globstar bug:** the workflow used `trees/**/*.py` which silently
  matches nothing on GitHub Actions because `globstar` is not enabled by
  default in bash.  Replaced with `find trees tools -name "*.py" -print0`
  piped through a `while read` loop.
- **AST check logic bug:** the bpy-at-module-level check used
  `ast.walk(tree)` which visits all nodes including those inside function
  bodies, making the `not isinstance(n, ast.FunctionDef)` filter
  meaningless.  Replaced with `ast.iter_child_nodes(module)` which visits
  only top-level statements.
- **Added pyflakes step:** installs and runs `python -m pyflakes` against
  all Python files in the workflow, replacing the manual `py_compile`-only
  check.

---

## [Unreleased] — rev-002

### Changed
- Repo name finalised as `saddle-examples-Blender` throughout all files.
  (The name passed through `saddle-examples-Blender` → `examples-saddles-Blender`
  → `saddle-examples-Blender` across development revisions before the
  GitHub repository was created.)

### Fixed — `trees/saddle_addon_utils.py` v1.0 → v1.1
- Removed unused `from mathutils import Vector` import inside `make_box()`.
- Removed deprecated `mat.blend_method` assignment (dropped in Blender 4.2).
- Added `_safe_unlink_from_all_collections()` — replaces all fragile
  `scene.collection.objects.unlink()` calls.
- Added default scene clear (removes Cube / Camera / Light) at the start
  of `import_and_cleanup_stl()`.

### Verified
- All 6 Python files pass syntax check.
- All 11 L/R boolean-tool pairs have zero centre-X drift.
- All teal gullet tools carry "SAFETY-CRITICAL" in their label.

---

## [Unreleased] — rev-001

### Added
- `trees/saddle_addon_utils.py` — shared Blender 5.1 utility module.
- Five tree scripts: roping-tree, high-swell-tree,
  low-cantle-no-horn-saddle-tree, split-cantle-no-horn-saddle-tree,
  split-cantle-horn-tree.
- `docs/workflow.md` — Blender boolean modifier workflow guide.
- `docs/anatomy-reference.md` — saddle anatomy glossary.
- Repository scaffolding: README, LICENSE, LICENSES/, CHANGELOG,
  CONTRIBUTING, CITATION.cff, CODE\_OF\_CONDUCT, .editorconfig,
  .gitattributes, .gitignore, GitHub Actions workflow.
