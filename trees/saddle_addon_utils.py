# =============================================================================
#  saddle_addon_utils.py
#  Shared utility module for saddle-examples-Blender scripts.
#  Blender 5.1 compatible  (bpy / bmesh / Python 3.11+)
#
#  USAGE
#  -----
#  At the top of any tree script in this collection:
#
#      import sys, os
#      sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
#      from saddle_addon_utils import (
#          create_material_palette,
#          import_and_cleanup_stl,
#          make_collections,
#          make_box,
#          make_cylinder,
#          finalise,
#          verify_lr_symmetry,
#      )
#
#  WHY THIS MODULE EXISTS
#  ----------------------
#  A single shared
#  module means bug fixes and API updates need to be made in only one place.
#
#  COORDINATE CONVENTION
#  -------------------------------------------------------
#  X : Left (negative) → Right (positive), centred at 0
#  Y : Front / horn end (negative) → Rear / cantle (positive)
#  Z : Down / bar underside (negative) → Up / horn tip (positive)
#  All trees centred at world origin (0, 0, 0).
#
#  PLACEMENT CONVENTION DIFFERENCE  (critical)
#  --------------------------------------------
#  Input convention  : (x, y, z) = minimum corner of the box.
#  Blender cube add   : location  = centre of the object.
#
#  make_box() accepts min-corner + dimensions (same convention as the
#  original CAD source) and converts internally to Blender centre:
#  internally, so tree scripts copy coordinates from the FCMacro source
#  without recalculation:
#    location = (x + l/2,  y + w/2,  z + h/2)
#    scale    = (l/2,       w/2,       h/2)
#
#  For cylinders, (x,y,z) = centre of bottom disk:
#    location = (x,  y,  z + h/2)
#    scale    = (r,  r,  h/2)
#
#  COLOUR KEY  (shared materials, consistent across all five scripts)
#  -----------------------------------------------------------------
#  Material name     RGB                Meaning            Operation
#  ----------------  -----------------  -----------------  ----------
#  Cutter_Red        (0.9, 0.2, 0.2)   CantleSplitCutter  Difference
#  Cutter_Blue       (0.2, 0.6, 1.0)   Standard cutters   Difference
#  Cutter_Teal       (0.4, 0.8, 1.0)   Gullet cutters     Difference
#  Cutter_Purple     (0.6, 0.4, 1.0)   Rigging mortises   Difference
#  Cutter_Orange     (1.0, 0.5, 0.1)   Seat scoop         Difference
#  Adder_Green       (0.2, 1.0, 0.4)   Adders             Union
#
#  Alpha 0.3 (70% transparent) via diffuse_color[3].
#  Note: mat.blend_method was removed in Blender 4.2 and is not set here.
#
#  CHANGELOG
#  ---------
#  v1.0  Initial version. Five tree scripts, shared utility module.
#  v1.1  Phase 3 static-analysis fixes (rev-002):
#        - Removed unused 'from mathutils import Vector' in make_box.
#        - Removed deprecated mat.blend_method (dropped Blender 4.2).
#        - Added _safe_unlink_from_all_collections() — replaces every
#          fragile scene.collection.objects.unlink() call so the scripts
#          work regardless of which collection was active at run time.
#        - Added default scene clear in import_and_cleanup_stl() to remove
#          Blender's default Cube / Camera / Light for a clean start.
#        - Repo name finalised as saddle-examples-Blender.
# =============================================================================

import os


# ---------------------------------------------------------------------------
# COLOUR PALETTE
# ---------------------------------------------------------------------------

#: Canonical material definitions.
#: Value = (R, G, B, A) with A = 0.3 for 70% transparency.
MATERIAL_PALETTE = {
    "Cutter_Red":    (0.9, 0.2, 0.2, 0.3),
    "Cutter_Blue":   (0.2, 0.6, 1.0, 0.3),
    "Cutter_Teal":   (0.4, 0.8, 1.0, 0.3),
    "Cutter_Purple": (0.6, 0.4, 1.0, 0.3),
    "Cutter_Orange": (1.0, 0.5, 0.1, 0.3),
    "Adder_Green":   (0.2, 1.0, 0.4, 0.3),
}

#: Map from source RGB tuples to material names.
_COLOR_TO_MAT = {
    (0.9, 0.2, 0.2): "Cutter_Red",
    (0.2, 0.6, 1.0): "Cutter_Blue",
    (0.4, 0.8, 1.0): "Cutter_Teal",
    (0.6, 0.4, 1.0): "Cutter_Purple",
    (1.0, 0.5, 0.1): "Cutter_Orange",
    (0.2, 1.0, 0.4): "Adder_Green",
}


def create_material_palette():
    """
    Create (or reuse) the six standard saddle-tool materials in bpy.data.

    On first call materials are created with the correct diffuse colour and
    alpha.  On subsequent calls existing materials are reused — no duplicates.

    In Blender 5.x with use_nodes=False, transparency is driven entirely by
    diffuse_color[3].  The deprecated blend_method property is not set.

    Returns
    -------
    dict  —  material name → bpy.types.Material
    """
    import bpy

    palette = {}
    for name, (r, g, b, a) in MATERIAL_PALETTE.items():
        if name in bpy.data.materials:
            palette[name] = bpy.data.materials[name]
        else:
            mat = bpy.data.materials.new(name=name)
            mat.use_nodes     = False
            mat.diffuse_color = (r, g, b, a)   # [3] = alpha
            palette[name]     = mat

    # Set viewport colour mode so tool colours are visible in Solid shading
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            for space in area.spaces:
                if space.type == "VIEW_3D":
                    space.shading.color_type = "MATERIAL"
                    break

    return palette


def _get_material(color_tuple, palette):
    """
    Resolve an (R, G, B) tuple to a Blender material from the palette.
    Falls back to Cutter_Blue on an unrecognised colour.
    """
    mat_name = _COLOR_TO_MAT.get(tuple(color_tuple), "Cutter_Blue")
    return palette[mat_name]


# ---------------------------------------------------------------------------
# COLLECTION HELPER
# ---------------------------------------------------------------------------

def _safe_unlink_from_all_collections(obj):
    """
    Unlink obj from every collection it currently belongs to.

    Blender links newly created primitives to the *active* collection,
    which may not be the scene root collection.  Calling
    scene.collection.objects.unlink() on an object that lives in a child
    collection raises RuntimeError.  This helper iterates a copy of
    obj.users_collection (copying is required because the list mutates
    during unlinking) and removes the object from each, so the caller can
    safely link it into a specific target collection.

    Parameters
    ----------
    obj : bpy.types.Object
    """
    for coll in list(obj.users_collection):
        coll.objects.unlink(obj)


# ---------------------------------------------------------------------------
# STL IMPORT AND MESH CLEANUP
# ---------------------------------------------------------------------------

def import_and_cleanup_stl(stl_path, merge_distance=0.01):
    """
    Clear the default scene, import an STL, and run a mesh cleanup pass.

    Imports the STL and runs a bmesh cleanup pass (merge doubles + fill holes).
    The result is a polygon mesh, sufficient for Boolean modifier operations.

    Scene clear: removes Blender's default Cube / Camera / Light before
    importing.  Safe on re-runs — an empty scene is a no-op.

    Parameters
    ----------
    stl_path       : str   — Absolute path to the binary STL file.
    merge_distance : float — Max vertex-weld distance in mm (default 0.01).

    Returns
    -------
    mesh_obj   : bpy.types.Object — Imported and cleaned mesh.
    cleanup_ok : bool             — True if bmesh cleanup completed.

    Raises
    ------
    FileNotFoundError  — stl_path does not exist.
    ValueError         — Fewer than 1000 polygons after import.
    RuntimeError       — Import succeeded but active_object is None.
    """
    import bpy
    import bmesh

    if not os.path.isfile(stl_path):
        raise FileNotFoundError(
            f"STL not found at:\n  {stl_path}\n"
            "Edit STL_PATH at the top of the script."
        )

    # Clear the default Blender scene objects (Cube, Camera, Light).
    # Safe on re-runs: empty bpy.data.objects skips this block entirely.
    if bpy.data.objects:
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete(use_global=False)

    # Set scene units to millimetres so the STL imports at the correct scale
    # regardless of the user's default scene-unit preference.  Without this,
    # a scene left in metres would import the mesh 1000× too large.
    scene = bpy.context.scene
    scene.unit_settings.system      = "METRIC"
    scene.unit_settings.length_unit = "MILLIMETERS"
    scene.unit_settings.scale_length = 0.001

    # Deselect so only the newly imported object will be selected/active
    bpy.ops.object.select_all(action="DESELECT")

    # Blender 5.1 STL import — bpy.ops.import_mesh.stl removed in Blender 4.0
    bpy.ops.wm.stl_import(filepath=stl_path)

    mesh_obj = bpy.context.active_object
    if mesh_obj is None:
        raise RuntimeError("STL import succeeded but no active object was set.")

    mesh_obj.name      = "SaddleMesh"
    mesh_obj.data.name = "SaddleMesh_data"

    poly_count = len(mesh_obj.data.polygons)
    if poly_count < 1000:
        raise ValueError(
            f"STL imported only {poly_count} polygons — file may be corrupt.\n"
            f"Path: {stl_path}"
        )

    print(f"[1/5] Mesh imported — {poly_count} polygons")
    print("[2/5] Running mesh cleanup (remove doubles + fill holes)…")

    cleanup_ok = False
    try:
        bm = bmesh.new()
        bm.from_mesh(mesh_obj.data)

        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=merge_distance)

        boundary_edges = [e for e in bm.edges if e.is_boundary]
        if boundary_edges:
            bmesh.ops.holes_fill(bm, edges=boundary_edges, sides=0)

        bm.to_mesh(mesh_obj.data)
        bm.free()
        mesh_obj.data.update()
        cleanup_ok = True

        print(f"[3/5] Cleanup done — {len(mesh_obj.data.polygons)} polygons")

    except Exception as exc:
        print(f"[3/5] WARNING: mesh cleanup failed ({exc})")
        print("      Mesh is available; boolean results may vary.")
        print("      Manual fix: Edit Mode → Mesh → Clean Up → Merge by Distance")
        print("      then Mesh → Clean Up → Fill Holes.")

    return mesh_obj, cleanup_ok


# ---------------------------------------------------------------------------
# COLLECTIONS
# ---------------------------------------------------------------------------

def make_collections(mesh_obj):
    """
    Create the standard two-collection structure and return BooleanTools.

    Creates the standard two-collection Outliner structure.

    Collections created:
      SaddleSolid
        └── SaddleMesh          ← working mesh object

      BooleanTools (cutters & adders)
        └── (tool objects added by make_box / make_cylinder)

    Parameters
    ----------
    mesh_obj : bpy.types.Object

    Returns
    -------
    coll_tools : bpy.types.Collection
    """
    import bpy

    scene = bpy.context.scene

    coll_solid = bpy.data.collections.new("SaddleSolid")
    scene.collection.children.link(coll_solid)

    # The STL importer links mesh_obj to the *active* collection, which may
    # not be the scene root.  _safe_unlink handles both cases.
    _safe_unlink_from_all_collections(mesh_obj)
    coll_solid.objects.link(mesh_obj)

    coll_tools = bpy.data.collections.new("BooleanTools (cutters & adders)")
    scene.collection.children.link(coll_tools)

    print("[4/5] Collections created")
    return coll_tools


# ---------------------------------------------------------------------------
# BOOLEAN TOOL FACTORY FUNCTIONS
# ---------------------------------------------------------------------------

def make_box(coll_tools, mesh_obj, palette,
             name, label, x, y, z, l, w, h,
             color=(0.2, 0.6, 1.0)):
    """
    Create a named, coloured box tool, link it into BooleanTools, and add
    a non-destructive Boolean modifier to the saddle mesh.

    COORDINATE CONVENTION:
      x, y, z — min-corner position (mm).  l = X, w = Y, h = Z dimension.

    Blender conversion (internal):
      location = (x + l/2,  y + w/2,  z + h/2)
      scale    = (l/2,       w/2,       h/2)

    Parameters
    ----------
    coll_tools : bpy.types.Collection
    mesh_obj   : bpy.types.Object
    palette    : dict
    name       : str    — Outliner display name.
    label      : str    — stored in obj["label"] custom property.
    x, y, z    : float  — min-corner position (mm).
    l, w, h    : float  — X, Y, Z dimensions (mm).
    color      : tuple  — (R, G, B) from the colour key above.

    Returns
    -------
    obj : bpy.types.Object
    """
    import bpy

    cx = x + l / 2.0
    cy = y + w / 2.0
    cz = z + h / 2.0

    bpy.ops.mesh.primitive_cube_add(size=2.0, location=(cx, cy, cz))
    obj        = bpy.context.active_object
    obj.name   = name
    obj["label"] = label
    obj.scale  = (l / 2.0, w / 2.0, h / 2.0)
    # Scale is intentionally NOT applied (bpy.ops.object.transform_apply).
    # The Boolean modifier works correctly with un-applied scale in Blender 4+.
    # Leaving scale un-applied means Blender's N-panel Dimensions readout
    # shows the correct real-world mm values directly.

    mat = _get_material(color, palette)
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    obj.display_type = "WIRE"

    _safe_unlink_from_all_collections(obj)
    coll_tools.objects.link(obj)

    is_adder = (tuple(color) == (0.2, 1.0, 0.4))
    op = "UNION" if is_adder else "DIFFERENCE"

    mod           = mesh_obj.modifiers.new(name=name, type="BOOLEAN")
    mod.operation = op
    mod.object    = obj
    mod.solver    = "EXACT"

    return obj


def make_cylinder(coll_tools, mesh_obj, palette,
                  name, label, x, y, z, r, h,
                  color=(1.0, 0.5, 0.1)):
    """
    Create a named, coloured cylinder tool, link it into BooleanTools, and
    add a non-destructive Boolean modifier to the saddle mesh.

    COORDINATE CONVENTION:
      x, y, z — centre of the BOTTOM disk (mm).
      r       — radius (mm).
      h       — height along +Z (mm).

    Blender conversion (internal):
      location = (x,  y,  z + h/2)
      scale    = (r,  r,  h/2)
      (default cylinder: radius=1, depth=2 along Z)

    Parameters
    ----------
    coll_tools : bpy.types.Collection
    mesh_obj   : bpy.types.Object
    palette    : dict
    name       : str
    label      : str
    x, y, z    : float  — centre of bottom disk (mm).
    r          : float  — radius (mm).
    h          : float  — height (mm).
    color      : tuple  — (R, G, B).

    Returns
    -------
    obj : bpy.types.Object
    """
    import bpy

    cz = z + h / 2.0

    bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=2.0,
                                        location=(x, y, cz))
    obj          = bpy.context.active_object
    obj.name     = name
    obj["label"] = label
    obj.scale    = (r, r, h / 2.0)
    # Scale intentionally un-applied — see make_box comment above.

    mat = _get_material(color, palette)
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    obj.display_type = "WIRE"

    _safe_unlink_from_all_collections(obj)
    coll_tools.objects.link(obj)

    is_adder = (tuple(color) == (0.2, 1.0, 0.4))
    op = "UNION" if is_adder else "DIFFERENCE"

    mod           = mesh_obj.modifiers.new(name=name, type="BOOLEAN")
    mod.operation = op
    mod.object    = obj
    mod.solver    = "EXACT"

    return obj


# ---------------------------------------------------------------------------
# FINALISE
# ---------------------------------------------------------------------------

def finalise(mesh_obj, cleanup_ok):
    """
    Update the dependency graph, activate the saddle mesh, fit the viewport.

    Parameters
    ----------
    mesh_obj   : bpy.types.Object
    cleanup_ok : bool
    """
    import bpy

    bpy.context.view_layer.update()
    bpy.context.evaluated_depsgraph_get().update()

    bpy.ops.object.select_all(action="DESELECT")
    mesh_obj.select_set(True)
    bpy.context.view_layer.objects.active = mesh_obj

    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            with bpy.context.temp_override(area=area):
                bpy.ops.view3d.view_all()
            break

    if not cleanup_ok:
        print(
            "\n  WARNING: Mesh cleanup did not complete.\n"
            "  Boolean results may vary.\n"
            "  Manual fix: Edit Mode → Mesh → Clean Up → Merge by Distance,\n"
            "  then Mesh → Clean Up → Fill Holes."
        )

    print("[5/5] Setup complete")


# ---------------------------------------------------------------------------
# UTILITY: L/R SYMMETRY CHECK
# ---------------------------------------------------------------------------

def verify_lr_symmetry(left_obj, right_obj, tolerance=0.01):
    """
    Verify  right_centre_x == -left_centre_x  for a L/R tool pair.

    Prints a warning if drift > tolerance mm.  Returns True if symmetric.

    Parameters
    ----------
    left_obj  : bpy.types.Object
    right_obj : bpy.types.Object
    tolerance : float  — mm
    """
    lx    = left_obj.location.x
    rx    = right_obj.location.x
    drift = abs(rx + lx)
    if drift > tolerance:
        print(
            f"  SYMMETRY WARNING: {left_obj.name} / {right_obj.name}\n"
            f"    Expected right_centre_x = {-lx:.4f} mm\n"
            f"    Actual   right_centre_x = {rx:.4f} mm\n"
            f"    Drift = {drift:.4f} mm  (tolerance {tolerance} mm)"
        )
    return drift <= tolerance
