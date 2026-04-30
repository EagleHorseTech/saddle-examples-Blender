# =============================================================================
#  split-cantle-horn-tree.py
#  Blender 5.1 compatible  (converted from split-cantle-horn-tree.FCMacro v1.1)
#
#  WHAT THIS SCRIPT DOES
#  ---------------------
#  1. Imports split-cantle-horn-tree.stl.  13.3" gullet, 22" depth,
#     ranch/trail hybrid with split cantle AND horn.  Centred at origin.
#  2. Mesh cleanup.
#  3. Full set of 14 named, colour-coded boolean-tool primitives as
#     non-destructive Boolean modifier previews — NOT applied automatically.
#
#  HOW TO RUN — Blender 5.1 Scripting workspace → Run Script (▶)
#
#  REAL-WORLD DIMENSIONS
#  ----------------------
#  Bar-to-bar width (X) : 338.9 mm  (13.3")  — semi-QH gullet
#  Tree depth F→B   (Y) : 558.8 mm  (22.0")  — general ranch/trail
#  Overall height   (Z) : 208.0 mm  ( 8.2")  — moderate horn + split cantle
#
#  COORDINATE SYSTEM  (centred at world origin 0, 0, 0)
#  ----------------------------------------------------
#  X: -169.45 → +169.45   Y: -279.40 → +279.40   Z: -103.98 → +103.98
#  Horn/pommel at NEGATIVE Y; cantle wings at POSITIVE Y.
#
#  SADDLE REGION MAP  (mm)
#  -------------------------
#  Horn               : Y -279.4 → -140.0   top Z ~ +104.0
#  Swell / fork       : Y -140.0 →  -56.0
#  Seat / gullet      : Y  -56.0 →  +56.0   min Z ~ -104.0
#  Cantle body        : Y  +56.0 → +168.0
#  Cantle split wings : Y +168.0 → +279.4   (two wings, centre open)
#
#  BOOLEAN TOOL COLOUR KEY  (all 5 colours used in this tree)
#  -----------------------------------------------------------
#  Red    (0.9, 0.2, 0.2) — CantleSplitCutter (apply FIRST)  → DIFFERENCE
#  Blue   (0.2, 0.6, 1.0) — standard cutters                 → DIFFERENCE
#  Teal   (0.4, 0.8, 1.0) — gullet-width cutters (safety)    → DIFFERENCE
#  Purple (0.6, 0.4, 1.0) — rigging mortise cutters          → DIFFERENCE
#  Orange (1.0, 0.5, 0.1) — seat scoop cutter (cylinder)     → DIFFERENCE
#  Green  (0.2, 1.0, 0.4) — adders                           → UNION
#
#  RECOMMENDED WORKFLOW (apply modifiers in this order)
#  ----------------------------------------------------
#  1. CantleSplitCutter (RED) — central cantle slot.
#  2. CantleWingCutter_L / _R — shape wings.
#  3. CantleBodyCutter — lower cantle wall.
#  4. CantleAdder (optional) — raise or dish cantle.
#  5. HornCutter — shorten / slim horn.
#  6. HornAdder (optional) — extend / widen horn cap.
#  7. SwellCutter — fork height and profile.
#  8. SeatScoopCutter — seat dish depth.
#  9. BarCurveCutter_L → apply → Mirror modifier (X) for right bar.
# 10. RiggingMortise FL/FR/RL/RR — four hardware plate recesses.
# 11. Green adders — union as needed.
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
STL_PATH = os.path.join(_THIS_DIR, "split-cantle-horn-tree.stl")

# ---------------------------------------------------------------------------
# 1–3.  Setup
# ---------------------------------------------------------------------------
palette    = create_material_palette()
mesh_obj, cleanup_ok = import_and_cleanup_stl(STL_PATH)
coll_tools = make_collections(mesh_obj)

# ---------------------------------------------------------------------------
# 4.  Boolean tool placeholders
#     Bounding box: X ±169.45  Y ±279.40  Z ±103.98  (all mm)
#     All L/R pairs verified symmetric (right_x == -left_x - left_L).
# ---------------------------------------------------------------------------

# ── CANTLE SPLIT CUTTER — RED — APPLY FIRST ─────────────────────────────────
# Signature cut defining this tree type.  Tall narrow box centred on X=0.
# Widen l for wider slot; deepen w; increase h to extend slot downward.
# MUST be applied before CantleWingCutter_L / _R.
make_box(
    coll_tools, mesh_obj, palette,
    "CantleSplitCutter",
    "CANTLE SPLIT -- RED -- Apply FIRST: widen L; deepen W; increase H for deeper slot",
    x=-20.0,  y=168.0, z=-15.0,
    l=40.0,   w=111.4, h=119.0,
    color=(0.9, 0.2, 0.2),
)

# ── CANTLE WING CUTTERS — symmetric L/R ─────────────────────────────────────
# Apply after CantleSplitCutter.  Reduce h to shorten wings.
# Shift x outward to slim wings.
# Symmetry: right_x (25.0) = -(-169.45) - 144.45 = 25.0. ✓
wing_l = make_box(
    coll_tools, mesh_obj, palette,
    "CantleWingCutter_L",
    "CANTLE WING LEFT -- Apply after SplitCutter: reduce H to shorten; shift X outward to slim",
    x=-169.45, y=168.0, z=50.0,
    l=144.45,  w=111.4, h=60.0,
    color=(0.2, 0.6, 1.0),
)
wing_r = make_box(
    coll_tools, mesh_obj, palette,
    "CantleWingCutter_R",
    "CANTLE WING RIGHT -- mirror of left; adjust independently for asymmetric rider fit",
    x=25.0,    y=168.0, z=50.0,
    l=144.45,  w=111.4, h=60.0,
    color=(0.2, 0.6, 1.0),
)
verify_lr_symmetry(wing_l, wing_r)

# ── CANTLE BODY CUTTER ──────────────────────────────────────────────────────
# Full-width box for the lower cantle wall below the wing split.
make_box(
    coll_tools, mesh_obj, palette,
    "CantleBodyCutter",
    "CANTLE BODY -- Cut: increase H to lower overall cantle wall below the wing split",
    x=-169.45, y=56.0,  z=35.0,
    l=338.9,   w=112.0, h=55.0,
    color=(0.2, 0.6, 1.0),
)

# ── CANTLE ADDER ────────────────────────────────────────────────────────────
# Wide low box at the cantle top.  Union to raise height or add rear-face dish.
make_box(
    coll_tools, mesh_obj, palette,
    "CantleAdder",
    "CANTLE ADDER -- Union: raise cantle height or add rear-face dish after body cutter",
    x=-84.7,  y=140.0, z=103.98,
    l=169.45, w=60.0,  h=25.0,
    color=(0.2, 1.0, 0.4),
)

# ── HORN CUTTER ─────────────────────────────────────────────────────────────
# Box around the upper horn shaft.  Reduce h to shorten; reduce l/w to slim.
make_box(
    coll_tools, mesh_obj, palette,
    "HornCutter",
    "HORN -- Cut: reduce H to shorten horn; reduce L and W equally to slim neck",
    x=-35.0,  y=-279.4, z=45.0,
    l=70.0,   w=85.0,   h=65.0,
    color=(0.2, 0.6, 1.0),
)

# ── HORN ADDER ──────────────────────────────────────────────────────────────
# Small cylinder at the horn tip.  Union to raise or widen the cap.
make_cylinder(
    coll_tools, mesh_obj, palette,
    "HornAdder",
    "HORN ADDER -- Union: increase R to widen cap for dally wrap; increase H to raise horn",
    x=0.0,  y=-237.0, z=103.98,
    r=22.0, h=25.0,
    color=(0.2, 1.0, 0.4),
)

# ── SWELL / FORK CUTTER ─────────────────────────────────────────────────────
# Full-width box.  Increase h to lower swell; increase w to narrow fork.
make_box(
    coll_tools, mesh_obj, palette,
    "SwellCutter",
    "SWELL/FORK -- Cut: increase H to lower swell height; increase W to narrow fork profile",
    x=-169.45, y=-140.0, z=10.0,
    l=338.9,   w=84.0,   h=55.0,
    color=(0.2, 0.6, 1.0),
)

# ── SEAT SCOOP CUTTER ───────────────────────────────────────────────────────
# Vertical cylinder centred at X=0, Y=0.  Increase Radius → flatter seat.
make_cylinder(
    coll_tools, mesh_obj, palette,
    "SeatScoopCutter",
    "SEAT -- Cut: increase Radius for flatter seat; decrease for deeper dish; shift Y to move dish centre",
    x=0.0,  y=0.0, z=-60.0,
    r=80.0, h=65.0,
    color=(1.0, 0.5, 0.1),
)

# ── BAR CURVE CUTTERS — symmetric L/R ───────────────────────────────────────
# Move z down to add rock.  Rotate via Item → Rotation for twist.
# Symmetry: right_x (114.45) = -(-169.45) - 55.0 = 114.45. ✓
bar_l = make_box(
    coll_tools, mesh_obj, palette,
    "BarCurveCutter_L",
    "BARS LEFT -- Cut: move Z for rock; rotate for twist; mirror result for right bar",
    x=-169.45, y=-200.0, z=-103.98,
    l=55.0,    w=400.0,  h=80.0,
    color=(0.2, 0.6, 1.0),
)
bar_r = make_box(
    coll_tools, mesh_obj, palette,
    "BarCurveCutter_R",
    "BARS RIGHT -- Cut: mirror of left bar; adjust independently for asymmetric horse fit",
    x=114.45,  y=-200.0, z=-103.98,
    l=55.0,    w=400.0,  h=80.0,
    color=(0.2, 0.6, 1.0),
)
verify_lr_symmetry(bar_l, bar_r)

# ── GULLET WIDTH CUTTERS — symmetric L/R ────────────────────────────────────
# SAFETY-CRITICAL.  Minimum safe gullet width: 70 mm (2.75").
# Shift x toward 0 to widen gullet.  Never narrow without horse measurement.
# Symmetry: right_x (25.0) = -(-45.0) - 20.0 = 25.0. ✓
gul_l = make_box(
    coll_tools, mesh_obj, palette,
    "GulletCutter_L",
    "GULLET LEFT -- SAFETY-CRITICAL: shift X toward 0 to widen gullet; verify 70mm+ on horse",
    x=-45.0,  y=-279.4, z=-103.98,
    l=20.0,   w=100.0,  h=207.96,
    color=(0.4, 0.8, 1.0),
)
gul_r = make_box(
    coll_tools, mesh_obj, palette,
    "GulletCutter_R",
    "GULLET RIGHT -- SAFETY-CRITICAL: shift X toward 0 to widen gullet; mirror left change",
    x=25.0,   y=-279.4, z=-103.98,
    l=20.0,   w=100.0,  h=207.96,
    color=(0.4, 0.8, 1.0),
)
verify_lr_symmetry(gul_l, gul_r)

# ── RIGGING MORTISE CUTTERS — four boxes, symmetric L/R ─────────────────────
# Front pair (FL / FR) — 3/4 or 7/8 rigging position.
# Rear pair  (RL / RR) — flank (rear cinch) position.
# Resize l, w, h to match your actual rigging hardware plate dimensions.
# Symmetry: right_x (138.95) = -(-169.45) - 30.5 = 138.95. ✓  (all four)
rig_fl = make_box(
    coll_tools, mesh_obj, palette,
    "RiggingMortise_FL",
    "RIGGING FRONT-LEFT -- Cut: resize to match hardware plate; shift Y for 3/4 or 7/8 position",
    x=-169.45, y=-112.0, z=-30.5,
    l=30.5,    w=45.7,   h=30.5,
    color=(0.6, 0.4, 1.0),
)
rig_fr = make_box(
    coll_tools, mesh_obj, palette,
    "RiggingMortise_FR",
    "RIGGING FRONT-RIGHT -- Cut: mirror of front-left; resize to match hardware plate",
    x=138.95,  y=-112.0, z=-30.5,
    l=30.5,    w=45.7,   h=30.5,
    color=(0.6, 0.4, 1.0),
)
verify_lr_symmetry(rig_fl, rig_fr)

rig_rl = make_box(
    coll_tools, mesh_obj, palette,
    "RiggingMortise_RL",
    "RIGGING REAR-LEFT -- Cut: resize to match flank cinch hardware; shift Y for flank position",
    x=-169.45, y=84.0,   z=-30.5,
    l=30.5,    w=45.7,   h=30.5,
    color=(0.6, 0.4, 1.0),
)
rig_rr = make_box(
    coll_tools, mesh_obj, palette,
    "RiggingMortise_RR",
    "RIGGING REAR-RIGHT -- Cut: mirror of rear-left; resize to match flank cinch hardware",
    x=138.95,  y=84.0,   z=-30.5,
    l=30.5,    w=45.7,   h=30.5,
    color=(0.6, 0.4, 1.0),
)
verify_lr_symmetry(rig_rl, rig_rr)

# ---------------------------------------------------------------------------
# 5.  Finalise
# ---------------------------------------------------------------------------
finalise(mesh_obj, cleanup_ok)

print()
print("=" * 62)
print("  split-cantle-horn-tree — Quarter Horse scale — complete")
print("=" * 62)
print()
print("  Tree type: Split-cantle WITH horn (hybrid ranch / trail)")
print()
print("  Bar-to-bar width : 338.9 mm  (13.3\")  — semi-QH gullet")
print("  Tree depth F->B  : 558.8 mm  (22.0\")  — general ranch/trail")
print("  Overall height   : 208.0 mm  ( 8.2\")  — moderate horn + cantle")
print()
print("  Horn end (front) : Y = -279.4 mm")
print("  Cantle (rear)    : Y = +279.4 mm")
print()
print("  Tools (14 total):")
print("    CantleSplitCutter (RED — apply first)")
print("    CantleWingCutter_L/R · CantleBodyCutter · CantleAdder")
print("    HornCutter · HornAdder · SwellCutter · SeatScoopCutter")
print("    BarCurveCutter_L/R")
print("    GulletCutter_L/R  (SAFETY-CRITICAL)")
print("    RiggingMortise_FL/FR/RL/RR")
print()
print("  GULLET SAFETY: minimum 70 mm (2.75\") clearance.")
print("  Verify gullet width on the horse before extended riding.")
