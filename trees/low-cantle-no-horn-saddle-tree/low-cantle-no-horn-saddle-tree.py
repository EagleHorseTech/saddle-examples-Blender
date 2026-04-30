# =============================================================================
#  low-cantle-no-horn-saddle-tree.py
#  Blender 5.1 compatible  (converted from low-cantle-no-horn-saddle-tree.FCMacro v1.1)
#
#  WHAT THIS SCRIPT DOES
#  ---------------------
#  1. Imports low-cantle-no-horn-saddle-tree.stl.  Pre-scaled to 14" gullet,
#     9.1" depth — hornless endurance/trail tree.  Centred at world origin.
#  2. Mesh cleanup (merge doubles + fill holes).
#  3. Named, colour-coded boolean-tool primitives as non-destructive
#     Boolean modifier previews — NOT applied automatically.
#
#  HOW TO RUN — Blender 5.1 Scripting workspace → Run Script (▶)
#
#  REAL-WORLD DIMENSIONS
#  ----------------------
#  Bar-to-bar width (X) : 355.6 mm  (14.0")  — standard QH gullet
#  Tree depth F→B   (Y) : 231.1 mm  ( 9.1")  — hornless / endurance
#  Overall height   (Z) : 137.6 mm  ( 5.4")  — low cantle profile
#
#  COORDINATE SYSTEM  (centred at world origin 0, 0, 0)
#  ----------------------------------------------------
#  X: -177.8 → +177.8   Y: -115.6 → +115.6   Z: -68.8 → +68.8
#  Pommel end at negative Y; cantle at positive Y.
#
#  BOOLEAN TOOL COLOUR KEY
#  -----------------------
#  Blue   (0.2, 0.6, 1.0) — standard cutters  → DIFFERENCE
#  Teal   (0.4, 0.8, 1.0) — gullet-width cutters (safety-critical) → DIFFERENCE
#  Orange (1.0, 0.5, 0.1) — seat scoop cutter → DIFFERENCE
#  Green  (0.2, 1.0, 0.4) — adders            → UNION
#
#  CHANGELOG
#  ---------
#  v1.0  Initial version.
# =============================================================================

import os
import sys

try:
    _THIS_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # Script was pasted into the Text Editor (not opened from disk).
    # Try to get the path from the active text block; fall back to cwd.
    import bpy as _bpy
    _text = getattr(_bpy.context.space_data, "text", None)
    _fp   = getattr(_text, "filepath", "") if _text else ""
    _THIS_DIR = os.path.dirname(os.path.abspath(_fp)) if _fp else os.getcwd()
    if not _fp:
        print("WARNING: Script was pasted without a saved filepath.")
        print("         Edit STL_PATH below to the full path of your STL file.")
_TREES_ROOT = os.path.dirname(_THIS_DIR)
if _TREES_ROOT not in sys.path:
    sys.path.insert(0, _TREES_ROOT)

from saddle_addon_utils import (
    create_material_palette,
    import_and_cleanup_stl,
    make_collections,
    make_box,
    make_cylinder,
    finalise,
    verify_lr_symmetry,
)

# ---------------------------------------------------------------------------
# 0.  USER SETTINGS
# ---------------------------------------------------------------------------
STL_PATH = os.path.join(_THIS_DIR, "low-cantle-no-horn-saddle-tree.stl")

# ---------------------------------------------------------------------------
# 1–3.  Setup
# ---------------------------------------------------------------------------
palette    = create_material_palette()
mesh_obj, cleanup_ok = import_and_cleanup_stl(STL_PATH)
coll_tools = make_collections(mesh_obj)

# ---------------------------------------------------------------------------
# 4.  Boolean tool placeholders
#     Bounding box: X ±177.8  Y ±115.6  Z ±68.8  (all mm)
#     All L/R pairs verified symmetric (right_x == -left_x - left_L).
# ---------------------------------------------------------------------------

# ── CANTLE CUTTER ───────────────────────────────────────────────────────────
# Full-width box over the rear cantle zone.  Low profile — limited material.
# Increase h to trim cantle height.  Move y toward 0 to shift taper start.
make_box(
    coll_tools, mesh_obj, palette,
    "CantleCutter",
    "CANTLE — cutter: increase H to trim cantle height; move Y to shift taper start",
    x=-177.8, y=40.0,  z=20.0,
    l=355.6,  w=75.6,  h=55.0,
    color=(0.2, 0.6, 1.0),
)

# ── CANTLE ADDER ────────────────────────────────────────────────────────────
# Narrow box above the cantle crown.  Union to add a small rear rise.
make_box(
    coll_tools, mesh_obj, palette,
    "CantleAdder",
    "CANTLE — adder: union to add modest rise across cantle top",
    x=-100.0, y=55.0,  z=68.8,
    l=200.0,  w=50.0,  h=20.0,
    color=(0.2, 1.0, 0.4),
)

# ── SEAT SCOOP CUTTER ───────────────────────────────────────────────────────
# Cylinder in the seat zone.  Increase Radius → flatter seat (posting trot).
make_cylinder(
    coll_tools, mesh_obj, palette,
    "SeatScoopCutter",
    "SEAT — scoop cutter: increase Radius for flatter seat, decrease for deeper dish",
    x=0.0, y=-15.0, z=-10.0,
    r=60.0, h=50.0,
    color=(1.0, 0.5, 0.1),
)

# ── BAR CURVE CUTTERS — symmetric L/R ───────────────────────────────────────
# Symmetry: right_x (117.8) = -(-177.8) - 60.0 = 117.8. ✓
bar_l = make_box(
    coll_tools, mesh_obj, palette,
    "BarCurveCutter_L",
    "BARS — left bar cutter: move Z to change rock; rotate for twist",
    x=-177.8, y=-100.0, z=-68.8,
    l=60.0,   w=200.0,  h=80.0,
    color=(0.2, 0.6, 1.0),
)
bar_r = make_box(
    coll_tools, mesh_obj, palette,
    "BarCurveCutter_R",
    "BARS — right bar cutter: mirror of left after Cut",
    x=117.8,  y=-100.0, z=-68.8,
    l=60.0,   w=200.0,  h=80.0,
    color=(0.2, 0.6, 1.0),
)
verify_lr_symmetry(bar_l, bar_r)

# ── GULLET WIDTH CUTTERS — symmetric L/R ────────────────────────────────────
# SAFETY-CRITICAL: gullet must clear the horse's spine.
# Minimum safe gullet width: 70 mm (2.75") at narrowest point.
# Shift left cutter x toward 0 (less negative) to widen gullet.
# Symmetry: right_x (30.0) = -(-50.0) - 20.0 = 30.0. ✓
gul_l = make_box(
    coll_tools, mesh_obj, palette,
    "GulletCutter_L",
    "GULLET — left cutter: SAFETY-CRITICAL — shift X toward 0 to widen gullet channel",
    x=-50.0,  y=-115.6, z=-68.8,
    l=20.0,   w=80.0,   h=137.6,
    color=(0.4, 0.8, 1.0),
)
gul_r = make_box(
    coll_tools, mesh_obj, palette,
    "GulletCutter_R",
    "GULLET — right cutter: SAFETY-CRITICAL — shift X toward 0 to widen gullet channel",
    x=30.0,   y=-115.6, z=-68.8,
    l=20.0,   w=80.0,   h=137.6,
    color=(0.4, 0.8, 1.0),
)
verify_lr_symmetry(gul_l, gul_r)

# ── POMMEL CAP ADDER ────────────────────────────────────────────────────────
# Small box at the top-front of the fork.  Hornless trees use a flat pommel.
# Union to build up height or add forward tilt to the cap.
make_box(
    coll_tools, mesh_obj, palette,
    "PommelCapAdder",
    "POMMEL — adder: union to build up or round the hornless pommel cap",
    x=-35.6,  y=-115.6, z=40.0,
    l=71.1,   w=40.0,   h=28.8,
    color=(0.2, 1.0, 0.4),
)

# ---------------------------------------------------------------------------
# 5.  Finalise
# ---------------------------------------------------------------------------
finalise(mesh_obj, cleanup_ok)

print()
print("=" * 62)
print("  low-cantle-no-horn-saddle-tree — Quarter Horse scale — complete")
print("=" * 62)
print()
print("  Bar-to-bar width : 355.6 mm  (14.0\")  — standard QH gullet")
print("  Tree depth F->B  : 231.1 mm  ( 9.1\")  — hornless / endurance")
print("  Overall height   : 137.6 mm  ( 5.4\")  — low cantle profile")
print()
print("  Tools: CantleCutter/Adder · SeatScoopCutter")
print("         BarCurveCutter_L/R · GulletCutter_L/R · PommelCapAdder")
print()
print("  GULLET SAFETY: minimum 70 mm (2.75\") clearance. Verify on horse.")
