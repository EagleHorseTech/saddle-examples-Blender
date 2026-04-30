# =============================================================================
#  roping-tree.py
#  Blender 5.1 compatible  (converted from roping-tree.FCMacro)
#
#  WHAT THIS SCRIPT DOES
#  ---------------------
#  1. Imports roping-tree.stl as a Blender mesh object.
#     The STL is pre-scaled to a ranch Quarter Horse in a roping
#     configuration: 24" tree length, 13.5" semi-QH gullet.
#  2. Runs a mesh cleanup pass (merge doubles + fill holes).
#  3. Creates named, colour-coded boolean-tool primitives (cubes and
#     cylinders) pre-positioned over anatomically correct saddle regions.
#     These are NOT applied — they are non-destructive Boolean modifier
#     previews.  Resize tools in the Properties panel (N-panel → Item),
#     then apply each modifier when satisfied.
#
#  HOW TO RUN
#  ----------
#  1. Open Blender 5.1.
#  2. Switch to the Scripting workspace.
#  3. Place BOTH this script AND roping-tree.stl in the same folder,
#     OR edit STL_PATH at the top of section 0.
#  4. Click Open and select this .py file (or paste it in).
#  5. Click Run Script (▶ / Alt+P).
#  6. Wait 5–20 seconds for the import and cleanup to complete.
#
#  REAL-WORLD DIMENSIONS  (Quarter Horse / ranch horse fit)
#  --------------------------------------------------------
#  Bar-to-bar width  (X) : 343.5 mm  (13.5")  — semi-QH gullet
#  Tree depth F→B    (Y) : 609.6 mm  (24.0")  — long roping tree
#  Overall height    (Z) : 235.7 mm  ( 9.3")  — tall horn + moderate cantle
#
#  COORDINATE SYSTEM  (centred at world origin 0, 0, 0)
#  ----------------------------------------------------
#  X: -171.7 → +171.7  (bar-to-bar width 343.5 mm)
#  Y: -304.8 → +304.8  (tree depth 609.6 mm; horn at negative Y)
#  Z: -117.9 → +117.9  (height 235.7 mm)
#
#  ROPING-TREE SPECIFIC FEATURES
#  ------------------------------
#  Tall, robust horn sized for dally roping.  Long 24" bars distribute
#  weight during hard stops.  Flat seat facilitates quick dismount.
#  Double-rigged: four RiggingMortise cutters for front and rear cinch.
#
#  BOOLEAN TOOL COLOUR KEY
#  -----------------------
#  Blue   (0.2, 0.6, 1.0) — standard cutters  → Apply modifier as DIFFERENCE
#  Purple (0.6, 0.4, 1.0) — rigging mortise cutters → DIFFERENCE
#  Orange (1.0, 0.5, 0.1) — seat scoop cutter → DIFFERENCE
#  Green  (0.2, 1.0, 0.4) — adders            → Apply modifier as UNION
#
#  WORKFLOW
#  --------
#  1. Select a tool in the Outliner; resize in Properties panel → Item → Scale.
#     (Scale X = half the X dimension in mm; Scale Y = half the Y dimension.)
#  2. Select the SaddleMesh object.
#  3. Properties → Modifier properties → find the Boolean for that tool.
#  4. Click the dropdown → Apply when satisfied.
#  5. For L/R symmetric changes: apply one side, then add a Mirror modifier
#     (X axis) to replicate the change to the opposite side.
#
#  SCALE REMINDER
#  --------------
#  Blender's default scene unit is metres.  This script works in millimetres.
#  If your viewport looks unusually large, go to:
#    Scene Properties → Units → Unit System: Metric → Length: Millimeters
#
#  CHANGELOG
#  ---------
#  v1.0  Initial version.
# =============================================================================

import os
import sys

# ---------------------------------------------------------------------------
# 0.  PATH SETUP — locate the shared utility module
#     os.path.dirname(__file__) returns the folder containing this script
#     when run from the Blender Text editor.  The utility module lives one
#     directory above (in trees/).
# ---------------------------------------------------------------------------
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
_TREES_ROOT = os.path.dirname(_THIS_DIR)   # one level up to trees/
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
# 1.  USER SETTINGS — edit STL_PATH if the STL is not in the same folder
# ---------------------------------------------------------------------------
STL_PATH = os.path.join(_THIS_DIR, "roping-tree.stl")

# ---------------------------------------------------------------------------
# 2.  Material palette
# ---------------------------------------------------------------------------
palette = create_material_palette()

# ---------------------------------------------------------------------------
# 3.  Import STL and clean up mesh
# ---------------------------------------------------------------------------
mesh_obj, cleanup_ok = import_and_cleanup_stl(STL_PATH)

# ---------------------------------------------------------------------------
# 4.  Create collections (SaddleSolid / BooleanTools)
# ---------------------------------------------------------------------------
coll_tools = make_collections(mesh_obj)

# ---------------------------------------------------------------------------
# 5.  Boolean tool placeholders
#
#     Bounding box of the scaled model (centred at world origin):
#       X: -171.7 → +171.7  (bar-to-bar width 343.5 mm)
#       Y: -304.8 → +304.8  (tree depth 609.6 mm)
#       Z: -117.9 → +117.9  (overall height 235.7 mm)
#
#     All L/R pairs verified perfectly symmetric about YZ plane (X=0).
#     Coordinates are identical to roping-tree.FCMacro.
# ---------------------------------------------------------------------------

# ── HORN CUTTER ─────────────────────────────────────────────────────────────
# Box around the upper horn shaft and cap.  Roping horns are stouter than
# pleasure-riding horns to withstand the lateral forces of dally roping.
# Reduce h to shorten the horn height.
# Reduce l and w to slim the neck — trade strength for lighter weight.
horn_cutter = make_box(
    coll_tools, mesh_obj, palette,
    "HornCutter",
    "HORN — cutter: reduce H to shorten; reduce L/W to slim neck",
    x=-35.6,  y=-304.8, z=60.0,
    l=71.1,   w=91.4,   h=65.0,
    color=(0.2, 0.6, 1.0),
)

# ── HORN ADDER ──────────────────────────────────────────────────────────────
# Small cylinder above the horn tip.  Union to add height or a wider cap
# for dally roping, where the rope must wrap cleanly around the cap.
horn_adder = make_cylinder(
    coll_tools, mesh_obj, palette,
    "HornAdder",
    "HORN — adder: union to raise height or widen cap for dally wrap",
    x=0.0,  y=-258.0, z=117.9,
    r=22.9, h=30.5,
    color=(0.2, 1.0, 0.4),
)

# ── SWELL / FORK CUTTER ─────────────────────────────────────────────────────
# Full-width box across the swell zone.  Roping swells are typically
# straighter and narrower — the rider needs to dismount quickly.
# Increase h to reduce swell height.  Increase w to narrow the fork.
swell_cutter = make_box(
    coll_tools, mesh_obj, palette,
    "SwellCutter",
    "SWELL/FORK — cutter: increase H to lower swell; increase W to narrow fork",
    x=-171.7, y=-213.4, z=20.0,
    l=343.5,  w=91.4,   h=60.0,
    color=(0.2, 0.6, 1.0),
)

# ── SEAT SCOOP CUTTER ───────────────────────────────────────────────────────
# Large-radius cylinder in the seat zone.  Roping seats are intentionally
# flatter to allow the rider to step off quickly.
# Increase Radius → flatter seat (roping standard).
# Decrease Radius → deeper dish, more secure but slower to exit.
seat_cutter = make_cylinder(
    coll_tools, mesh_obj, palette,
    "SeatScoopCutter",
    "SEAT — scoop cutter: increase Radius for flatter roping seat",
    x=0.0,  y=-30.5, z=-60.0,
    r=91.4, h=76.2,
    color=(1.0, 0.5, 0.1),
)

# ── BAR CURVE CUTTERS — symmetric L/R pair ──────────────────────────────────
# Long boxes along the full 24" bar length.
# Move z down to add rock (arch) along the bar.
# Rotate via Item → Rotation to introduce bar twist for shoulder clearance.
# Symmetry: right_x (111.7) = -(-171.7) - 60.0 = 111.7. Correct.
bar_l = make_box(
    coll_tools, mesh_obj, palette,
    "BarCurveCutter_L",
    "BARS — left bar cutter: move Z for rock; rotate for twist",
    x=-171.7, y=-121.9, z=-117.9,
    l=60.0,   w=426.7,  h=91.4,
    color=(0.2, 0.6, 1.0),
)
bar_r = make_box(
    coll_tools, mesh_obj, palette,
    "BarCurveCutter_R",
    "BARS — right bar cutter: mirror of left; adjust independently if needed",
    x=111.7,  y=-121.9, z=-117.9,
    l=60.0,   w=426.7,  h=91.4,
    color=(0.2, 0.6, 1.0),
)
verify_lr_symmetry(bar_l, bar_r)

# ── CANTLE CUTTER ───────────────────────────────────────────────────────────
# Full-width box across the cantle zone.  Roping cantles are moderately
# high — enough to secure the rider through hard stops, but not so tall
# they impede quick dismount.
# Reduce h to lower cantle height.
cantle_cutter = make_box(
    coll_tools, mesh_obj, palette,
    "CantleCutter",
    "CANTLE — cutter: reduce H to lower cantle; move Y to shift rise start",
    x=-171.7, y=152.4, z=30.5,
    l=343.5,  w=152.4, h=95.0,
    color=(0.2, 0.6, 1.0),
)

# ── CANTLE ADDER ────────────────────────────────────────────────────────────
# Box above the cantle crown.  Union to add height or dish to the rear face.
cantle_adder = make_box(
    coll_tools, mesh_obj, palette,
    "CantleAdder",
    "CANTLE — adder: union to raise cantle or add rear dish",
    x=-91.4, y=228.6, z=80.0,
    l=182.9, w=76.2,  h=37.9,
    color=(0.2, 1.0, 0.4),
)

# ── RIGGING RING MORTISE CUTTERS — four boxes, symmetric L/R ────────────────
# Roping saddles are double-rigged: cinch attaches at a front ring and a
# rear (flank) ring to distribute the stress of roping.  These small box
# cutters create the recesses (mortises) where rigging plates sit in the wood.
#
# Front pair (FL / FR) — full or 7/8 position, under the front of the seat.
# Rear pair  (RL / RR) — flank position, under the rear of the seat.
#
# Symmetry (all four pairs): right_x (141.2) = -(-171.7) - 30.5 = 141.2. ✓
rig_fl = make_box(
    coll_tools, mesh_obj, palette,
    "RiggingMortise_FL",
    "RIGGING — front-left mortise cutter (full/7-8 position)",
    x=-171.7, y=-152.4, z=-30.5,
    l=30.5,   w=45.7,   h=30.5,
    color=(0.6, 0.4, 1.0),
)
rig_fr = make_box(
    coll_tools, mesh_obj, palette,
    "RiggingMortise_FR",
    "RIGGING — front-right mortise cutter (full/7-8 position)",
    x=141.2,  y=-152.4, z=-30.5,
    l=30.5,   w=45.7,   h=30.5,
    color=(0.6, 0.4, 1.0),
)
verify_lr_symmetry(rig_fl, rig_fr)

rig_rl = make_box(
    coll_tools, mesh_obj, palette,
    "RiggingMortise_RL",
    "RIGGING — rear-left mortise cutter (flank position)",
    x=-171.7, y=121.9,  z=-30.5,
    l=30.5,   w=45.7,   h=30.5,
    color=(0.6, 0.4, 1.0),
)
rig_rr = make_box(
    coll_tools, mesh_obj, palette,
    "RiggingMortise_RR",
    "RIGGING — rear-right mortise cutter (flank position)",
    x=141.2,  y=121.9,  z=-30.5,
    l=30.5,   w=45.7,   h=30.5,
    color=(0.6, 0.4, 1.0),
)
verify_lr_symmetry(rig_rl, rig_rr)

# ---------------------------------------------------------------------------
# 6.  Finalise
# ---------------------------------------------------------------------------
finalise(mesh_obj, cleanup_ok)

# ---------------------------------------------------------------------------
# 7.  Print summary to the Blender console / Info editor
# ---------------------------------------------------------------------------
print()
print("=" * 62)
print("  roping-tree — Quarter Horse scale — complete")
print("=" * 62)
print()
print("  Saddle tree dimensions (real-world):")
print("    Tree depth (front->back) : 609.6 mm  (24.0\")  — long roping tree")
print("    Bar-to-bar width         : 343.5 mm  (13.5\")  — semi-QH gullet")
print("    Overall height           : 235.7 mm  ( 9.3\")  — tall horn + cantle")
print()
print("  Coordinate origin: model centred on (0, 0, 0)")
print("    Front of tree (horn end) : Y = -304.8 mm")
print("    Rear  of tree (cantle)   : Y = +304.8 mm")
print("    Bottom of bars           : Z = -117.9 mm")
print("    Top of horn              : Z = +117.9 mm")
print()
print("  Boolean tools in 'BooleanTools' collection:")
print("    HornCutter       / HornAdder")
print("    SwellCutter")
print("    SeatScoopCutter")
print("    BarCurveCutter_L / BarCurveCutter_R")
print("    CantleCutter     / CantleAdder")
print("    RiggingMortise_FL / RiggingMortise_FR  (front, full/7-8 position)")
print("    RiggingMortise_RL / RiggingMortise_RR  (rear, flank position)")
print()
print("  Colour key:")
print("    Blue   (0.2, 0.6, 1.0) -- standard cutters")
print("    Purple (0.6, 0.4, 1.0) -- rigging mortise cutters")
print("    Orange (1.0, 0.5, 0.1) -- seat scoop cutter")
print("    Green  (0.2, 1.0, 0.4) -- adders (union)")
print()
print("  WORKFLOW:")
print("  1. Select a tool in the Outliner; resize via Properties → Item → Scale.")
print("     Scale X = half the X dimension in mm.")
print("  2. Select SaddleMesh → Properties → Modifier properties.")
print("  3. Find the Boolean modifier for that tool → Apply.")
print("  4. For L/R symmetric changes: apply one side, add Mirror modifier (X).")
print()
print("  GULLET SAFETY: minimum 70 mm (2.75\") clearance at narrowest point.")
print("  Verify on the horse before use.")
