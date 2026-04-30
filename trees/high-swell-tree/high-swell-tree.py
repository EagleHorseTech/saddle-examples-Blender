# =============================================================================
#  high-swell-tree.py
#  Blender 5.1 compatible  (converted from high-swell-tree.FCMacro v1.2)
#
#  WHAT THIS SCRIPT DOES
#  ---------------------
#  1. Imports high-swell-tree.stl.  Pre-scaled to 14" gullet / 23.2" depth
#     ranch Quarter Horse.  Centred at world origin (0, 0, 0).
#  2. Runs mesh cleanup (merge doubles + fill holes).
#  3. Creates named, colour-coded boolean-tool primitives.
#     Tools are non-destructive Boolean modifier previews — NOT applied.
#
#  HOW TO RUN
#  ----------
#  1. Blender 5.1 → Scripting workspace.
#  2. Place this script AND high-swell-tree.stl in the same folder,
#     OR edit STL_PATH in section 0.
#  3. Click Open → select this file → Run Script (▶ / Alt+P).
#
#  REAL-WORLD DIMENSIONS
#  ----------------------
#  Bar-to-bar width (X) : 355.6 mm  (14.0")  — standard QH gullet
#  Tree depth F→B   (Y) : 588.6 mm  (23.2")
#  Overall height   (Z) : 347.3 mm  (13.7")  — base to horn tip
#
#  COORDINATE SYSTEM  (centred at world origin 0, 0, 0)
#  ----------------------------------------------------
#  X: -177.8 → +177.8   Y: -294.3 → +294.3   Z: -173.6 → +173.6
#
#  NOTE — Y-AXIS ORIENTATION
#  --------------------------
#  Horn at NEGATIVE Y; cantle at POSITIVE Y.
#  Consistent with all other trees in this collection.
#
#  SADDLE REGION MAP  (mm, horn at negative Y)
#  --------------------------------------------
#  Cantle          : Y -294.0 → -147.0  max Z ~ +173.6 mm
#  Seat / gullet   : Y -147.0 →    0.0  min Z ~ -173.6 mm
#  Swell / fork    : Y    0.0 → +147.0  max Z ~  +60.0 mm
#  Horn            : Y +147.0 → +294.0  max Z ~ +173.6 mm
#
#  BOOLEAN TOOL COLOUR KEY
#  -----------------------
#  Blue   (0.2, 0.6, 1.0) — standard cutters  → DIFFERENCE
#  Orange (1.0, 0.5, 0.1) — seat scoop cutter → DIFFERENCE
#  Green  (0.2, 1.0, 0.4) — adders            → UNION
#
#  CHANGELOG
#  ---------
#  v1.0  Converted from high-swell-tree.FCMacro v1.2.
#        Coordinates identical to FCMacro source.
#        T-1 Y-axis orientation corrected in documentation.
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
STL_PATH = os.path.join(_THIS_DIR, "high-swell-tree.stl")

# ---------------------------------------------------------------------------
# 1–3.  Setup
# ---------------------------------------------------------------------------
palette    = create_material_palette()
mesh_obj, cleanup_ok = import_and_cleanup_stl(STL_PATH)
coll_tools = make_collections(mesh_obj)

# ---------------------------------------------------------------------------
# 4.  Boolean tool placeholders
#     Bounding box: X ±177.8  Y ±294.3  Z ±173.6  (all mm)
#     All L/R pairs verified symmetric (right_x == -left_x - left_L).
# ---------------------------------------------------------------------------

# ── CANTLE CUTTER ───────────────────────────────────────────────────────────
# Full-width box covering the rear cantle zone (negative Y end).
# Increase h to trim cantle height.  Move y toward 0 to shift taper start.
make_box(
    coll_tools, mesh_obj, palette,
    "CantleCutter",
    "CANTLE -- cutter: increase H to trim cantle height; move Y to shift taper start",
    x=-177.8, y=-311.5, z=-116.7,
    l=355.6,  w=106.7,  h=199.1,
    color=(0.2, 0.6, 1.0),
)

# ── CANTLE ADDER ────────────────────────────────────────────────────────────
# Narrower box above the cantle crown.  Union to raise or widen cantle top.
make_box(
    coll_tools, mesh_obj, palette,
    "CantleAdder",
    "CANTLE -- adder: union to raise or widen cantle crown",
    x=-71.1, y=-268.8, z=25.5,
    l=142.2, w=71.1,   h=56.9,
    color=(0.2, 1.0, 0.4),
)

# ── SEAT SCOOP CUTTER ───────────────────────────────────────────────────────
# Cylinder in the seat/gullet zone.  Increase Radius → flatter seat.
make_cylinder(
    coll_tools, mesh_obj, palette,
    "SeatScoopCutter",
    "SEAT -- scoop cutter: increase Radius for flatter seat, decrease for deeper dish",
    x=0.0, y=-112.3, z=-145.2,
    r=78.2, h=142.2,
    color=(1.0, 0.5, 0.1),
)

# ── BAR CURVE CUTTERS — symmetric L/R ───────────────────────────────────────
# Symmetry: right_x (126.6) = -(-183.5) - 56.9 = 126.6. ✓
bar_l = make_box(
    coll_tools, mesh_obj, palette,
    "BarCurveCutter_L",
    "BARS -- left bar cutter: move Z for rock; rotate for twist",
    x=-183.5, y=-147.9, z=-173.6,
    l=56.9,   w=284.5,  h=113.8,
    color=(0.2, 0.6, 1.0),
)
bar_r = make_box(
    coll_tools, mesh_obj, palette,
    "BarCurveCutter_R",
    "BARS -- right bar cutter: true mirror of left",
    x=126.6,  y=-147.9, z=-173.6,
    l=56.9,   w=284.5,  h=113.8,
    color=(0.2, 0.6, 1.0),
)
verify_lr_symmetry(bar_l, bar_r)

# ── SWELL / FORK CUTTER ─────────────────────────────────────────────────────
# Full-width across the swell zone.  High swell is the defining feature.
# Increase h to reduce swell height.  Increase w to narrow the fork.
make_box(
    coll_tools, mesh_obj, palette,
    "SwellCutter",
    "SWELL/FORK -- cutter: increase H to lower swell; increase W to narrow undercut",
    x=-177.8, y=-5.7,  z=-138.0,
    l=355.6,  w=156.5, h=142.2,
    color=(0.2, 0.6, 1.0),
)

# ── HORN CUTTER ─────────────────────────────────────────────────────────────
# Box around the upper horn.  Reduce h to shorten; reduce l/w to slim neck.
make_box(
    coll_tools, mesh_obj, palette,
    "HornCutter",
    "HORN -- cutter: reduce H to shorten; reduce L/W to slim neck diameter",
    x=-71.1, y=214.8, z=96.7,
    l=142.2, w=92.5,  h=92.5,
    color=(0.2, 0.6, 1.0),
)

# ── HORN ADDER ──────────────────────────────────────────────────────────────
# Small cylinder above the horn tip.  Union to raise height or widen cap.
make_cylinder(
    coll_tools, mesh_obj, palette,
    "HornAdder",
    "HORN -- adder: union to raise horn height or widen cap for dally wrap",
    x=0.0, y=257.5, z=139.3,
    r=28.4, h=56.9,
    color=(0.2, 1.0, 0.4),
)

# ---------------------------------------------------------------------------
# 5.  Finalise
# ---------------------------------------------------------------------------
finalise(mesh_obj, cleanup_ok)

print()
print("=" * 62)
print("  high-swell-tree — Quarter Horse scale — complete")
print("=" * 62)
print()
print("  Bar-to-bar width : 355.6 mm  (14.0\")  — standard QH gullet")
print("  Tree depth F->B  : 588.6 mm  (23.2\")")
print("  Overall height   : 347.3 mm  (13.7\")")
print()
print("  Horn at NEGATIVE Y  |  Cantle at POSITIVE Y")
print()
print("  Tools: CantleCutter/Adder · SeatScoopCutter")
print("         BarCurveCutter_L/R · SwellCutter · HornCutter/Adder")
print()
print("  GULLET SAFETY: minimum 70 mm (2.75\") clearance. Verify on horse.")
