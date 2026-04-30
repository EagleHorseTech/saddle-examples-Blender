# =============================================================================
#  split-cantle-no-horn-saddle-tree.py
#  Blender 5.1 compatible  (converted from split-cantle-no-horn-saddle-tree.FCMacro v1.1)
#
#  WHAT THIS SCRIPT DOES
#  ---------------------
#  1. Imports split-cantle-no-horn-saddle-tree.stl.  14" gullet, 12.7" depth,
#     hornless split-cantle endurance/trail tree.  Centred at world origin.
#  2. Mesh cleanup.
#  3. Named, colour-coded boolean-tool primitives as modifier previews.
#
#  HOW TO RUN — Blender 5.1 Scripting workspace → Run Script (▶)
#
#  REAL-WORLD DIMENSIONS
#  ----------------------
#  Bar-to-bar width (X) : 355.6 mm  (14.0")  — standard QH gullet
#  Tree depth F→B   (Y) : 321.6 mm  (12.7")  — mid-length, no horn
#  Overall height   (Z) : 190.1 mm  ( 7.5")  — split cantle rise
#
#  COORDINATE SYSTEM  (centred at world origin 0, 0, 0)
#  ----------------------------------------------------
#  X: -177.8 → +177.8   Y: -160.8 → +160.8   Z: -95.0 → +95.0
#  Pommel at negative Y; cantle wings at positive Y.
#
#  SPLIT-CANTLE DESIGN NOTE
#  ------------------------
#  A central vertical slot through the rear cantle face leaves two lateral
#  wings.  Benefits: reduced weight, pelvic tilt freedom on long rides.
#  CantleSplitCutter (RED) is the signature tool — apply it FIRST.
#
#  BOOLEAN TOOL COLOUR KEY
#  -----------------------
#  Red    (0.9, 0.2, 0.2) — CantleSplitCutter (apply FIRST)  → DIFFERENCE
#  Blue   (0.2, 0.6, 1.0) — standard cutters                 → DIFFERENCE
#  Teal   (0.4, 0.8, 1.0) — gullet-width cutters             → DIFFERENCE
#  Orange (1.0, 0.5, 0.1) — seat scoop cutter                → DIFFERENCE
#  Green  (0.2, 1.0, 0.4) — adders                           → UNION
#
#  RECOMMENDED WORKFLOW (apply modifiers in this order)
#  ----------------------------------------------------
#  1. CantleSplitCutter (RED) — creates the central cantle slot.
#  2. CantleWingCutter_L / _R — shape each wing independently.
#  3. CantleBodyCutter — set overall cantle rise below the wings.
#  4. SeatScoopCutter — seat dish depth.
#  5. BarCurveCutter_L → apply → Mirror modifier (X) for right bar.
#  6. Green adders — union as needed.
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
STL_PATH = os.path.join(_THIS_DIR, "split-cantle-no-horn-saddle-tree.stl")

# ---------------------------------------------------------------------------
# 1–3.  Setup
# ---------------------------------------------------------------------------
palette    = create_material_palette()
mesh_obj, cleanup_ok = import_and_cleanup_stl(STL_PATH)
coll_tools = make_collections(mesh_obj)

# ---------------------------------------------------------------------------
# 4.  Boolean tool placeholders
#     Bounding box: X ±177.8  Y ±160.8  Z ±95.0  (all mm)
#     All L/R pairs verified symmetric.
# ---------------------------------------------------------------------------

# ── CANTLE SPLIT CUTTER — RED — APPLY FIRST ─────────────────────────────────
# THE signature tool.  Tall narrow box centred on X=0, at rear cantle face.
# Widen l for wider slot; deepen w for deeper slot; increase h to extend
# the slot downward.  MUST be applied before wing cutters.
make_box(
    coll_tools, mesh_obj, palette,
    "CantleSplitCutter",
    "CANTLE SPLIT — RED — Apply FIRST: widen L for wider slot; deepen W; increase H to extend downward",
    x=-20.0,  y=112.0, z=-20.0,
    l=40.0,   w=48.8,  h=115.0,
    color=(0.9, 0.2, 0.2),
)

# ── CANTLE WING CUTTERS — symmetric L/R ─────────────────────────────────────
# Applied after split cutter.  Reduce h to shorten wing height.
# Shift x outward to slim wings.
# Symmetry: right_x (40.0) = -(-177.8) - 137.8 = 40.0. ✓
wing_l = make_box(
    coll_tools, mesh_obj, palette,
    "CantleWingCutter_L",
    "CANTLE WING — left: reduce H to shorten wing; shift X outward to slim",
    x=-177.8, y=112.0, z=50.0,
    l=137.8,  w=48.8,  h=55.0,
    color=(0.2, 0.6, 1.0),
)
wing_r = make_box(
    coll_tools, mesh_obj, palette,
    "CantleWingCutter_R",
    "CANTLE WING — right: mirror of left wing cutter",
    x=40.0,   y=112.0, z=50.0,
    l=137.8,  w=48.8,  h=55.0,
    color=(0.2, 0.6, 1.0),
)
verify_lr_symmetry(wing_l, wing_r)

# ── CANTLE BODY CUTTER ──────────────────────────────────────────────────────
# Full-width box for the lower cantle zone below the wing split.
# Increase h to reduce main cantle rise.
make_box(
    coll_tools, mesh_obj, palette,
    "CantleBodyCutter",
    "CANTLE BODY — cutter: increase H to lower cantle rise below wing split",
    x=-177.8, y=48.2,  z=30.0,
    l=355.6,  w=63.8,  h=65.0,
    color=(0.2, 0.6, 1.0),
)

# ── CANTLE ADDER ────────────────────────────────────────────────────────────
make_box(
    coll_tools, mesh_obj, palette,
    "CantleAdder",
    "CANTLE — adder: union to raise cantle body or add rear-face dish",
    x=-91.4,  y=96.0,  z=95.0,
    l=182.9,  w=50.0,  h=25.0,
    color=(0.2, 1.0, 0.4),
)

# ── SEAT SCOOP CUTTER ───────────────────────────────────────────────────────
# Semi-flat seat for endurance/trail (posting trot and two-point friendly).
make_cylinder(
    coll_tools, mesh_obj, palette,
    "SeatScoopCutter",
    "SEAT — scoop cutter: increase Radius for flatter endurance seat",
    x=0.0,  y=-26.3, z=-40.0,
    r=75.0, h=60.0,
    color=(1.0, 0.5, 0.1),
)

# ── BAR CURVE CUTTERS — symmetric L/R ───────────────────────────────────────
# Symmetry: right_x (122.8) = -(-177.8) - 55.0 = 122.8. ✓
bar_l = make_box(
    coll_tools, mesh_obj, palette,
    "BarCurveCutter_L",
    "BARS — left bar cutter: move Z for rock; rotate for twist",
    x=-177.8, y=-100.0, z=-95.0,
    l=55.0,   w=260.0,  h=75.0,
    color=(0.2, 0.6, 1.0),
)
bar_r = make_box(
    coll_tools, mesh_obj, palette,
    "BarCurveCutter_R",
    "BARS — right bar cutter: mirror of left",
    x=122.8,  y=-100.0, z=-95.0,
    l=55.0,   w=260.0,  h=75.0,
    color=(0.2, 0.6, 1.0),
)
verify_lr_symmetry(bar_l, bar_r)

# ── GULLET WIDTH CUTTERS — symmetric L/R ────────────────────────────────────
# SAFETY-CRITICAL.  Minimum 70 mm (2.75") at narrowest point.
# Symmetry: right_x (35.0) = -(-60.0) - 25.0 = 35.0. ✓
gul_l = make_box(
    coll_tools, mesh_obj, palette,
    "GulletCutter_L",
    "GULLET — left cutter: SAFETY-CRITICAL — shift X toward 0 to widen gullet",
    x=-60.0,  y=-160.8, z=-95.0,
    l=25.0,   w=75.0,   h=190.1,
    color=(0.4, 0.8, 1.0),
)
gul_r = make_box(
    coll_tools, mesh_obj, palette,
    "GulletCutter_R",
    "GULLET — right cutter: SAFETY-CRITICAL — shift X toward 0 to widen gullet",
    x=35.0,   y=-160.8, z=-95.0,
    l=25.0,   w=75.0,   h=190.1,
    color=(0.4, 0.8, 1.0),
)
verify_lr_symmetry(gul_l, gul_r)

# ── POMMEL CAP ADDER ────────────────────────────────────────────────────────
make_box(
    coll_tools, mesh_obj, palette,
    "PommelCapAdder",
    "POMMEL — adder: union to build up or round the hornless pommel cap",
    x=-40.0,  y=-160.8, z=55.0,
    l=80.0,   w=45.0,   h=40.0,
    color=(0.2, 1.0, 0.4),
)

# ---------------------------------------------------------------------------
# 5.  Finalise
# ---------------------------------------------------------------------------
finalise(mesh_obj, cleanup_ok)

print()
print("=" * 62)
print("  split-cantle-no-horn-saddle-tree — Quarter Horse scale — complete")
print("=" * 62)
print()
print("  Bar-to-bar width : 355.6 mm  (14.0\")  — standard QH gullet")
print("  Tree depth F->B  : 321.6 mm  (12.7\")  — mid-length, no horn")
print("  Overall height   : 190.1 mm  ( 7.5\")  — split cantle profile")
print()
print("  Tools: CantleSplitCutter (RED — apply first)")
print("         CantleWingCutter_L/R · CantleBodyCutter/Adder")
print("         SeatScoopCutter · BarCurveCutter_L/R")
print("         GulletCutter_L/R · PommelCapAdder")
print()
print("  GULLET SAFETY: minimum 70 mm (2.75\") clearance. Verify on horse.")
