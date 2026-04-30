#!/usr/bin/env python3
"""
validate_stl.py — Pre-submission STL validator for saddle-examples-Blender.

Usage
-----
    python tools/validate_stl.py <path/to/tree.stl>
    python tools/validate_stl.py --help

Requirements
------------
    pip install numpy-stl

Checks performed
----------------
  1. File exists and is readable.
  2. Valid binary STL format (not ASCII — binary is preferred for speed).
  3. Facet count > 10,000 (degenerate mesh guard).
  4. No degenerate (zero-area) triangles.
  5. Bounding-box centre within 0.5 mm of (0, 0, 0) on all three axes.
  6. Reports bar-to-bar width (X span), depth (Y span), height (Z span)
     in mm and inches for manual sanity check.
  7. Estimates gullet width at X = 0 cross-section (informational).

Exit codes
----------
  0  All required checks passed.
  1  One or more checks failed (details printed to stdout).
  2  Usage error or missing dependency.
"""

import argparse
import os
import sys

MM_PER_INCH = 25.4
ORIGIN_TOLERANCE_MM = 0.5  # bounding-box centre must be within this of (0,0,0)
MIN_FACET_COUNT = 10_000


def check_numpy_stl():
    try:
        import numpy as np
        from stl import mesh as stl_mesh
        return np, stl_mesh
    except ImportError:
        print("ERROR: numpy-stl is required but not installed.")
        print("       Run:  pip install numpy-stl")
        sys.exit(2)


def load_stl(path, stl_mesh_module):
    """Load STL and return the mesh object, or exit with error."""
    try:
        m = stl_mesh.Mesh.from_file(path)
        return m
    except Exception as e:
        print(f"ERROR: Could not load STL file: {e}")
        sys.exit(1)


def check_binary_format(path):
    """Return True if the file is binary STL, False if ASCII."""
    with open(path, "rb") as f:
        header = f.read(80)
    # ASCII STL starts with "solid " (possibly with whitespace)
    try:
        text = header.decode("utf-8", errors="ignore").strip().lower()
        if text.startswith("solid"):
            # Could still be binary if the header happens to start with "solid"
            # Check for the facet count field (bytes 80–83) as a second signal
            with open(path, "rb") as f:
                f.seek(80)
                facet_count_bytes = f.read(4)
            if len(facet_count_bytes) < 4:
                return False
            import struct
            facet_count = struct.unpack("<I", facet_count_bytes)[0]
            file_size = os.path.getsize(path)
            expected_size = 80 + 4 + facet_count * 50
            # If sizes match, it's binary despite the "solid" header
            return abs(file_size - expected_size) < 200
    except Exception:
        pass
    return True  # assume binary if we can't determine


def validate(stl_path):
    np, stl_mesh_module = check_numpy_stl()

    results = []
    passed = 0
    failed = 0

    def ok(msg):
        nonlocal passed
        passed += 1
        results.append(f"  [PASS] {msg}")

    def fail(msg):
        nonlocal failed
        failed += 1
        results.append(f"  [FAIL] {msg}")

    def info(msg):
        results.append(f"  [INFO] {msg}")

    print(f"\nValidating: {stl_path}\n")

    # Check 1 — file exists
    if not os.path.isfile(stl_path):
        print(f"  [FAIL] File not found: {stl_path}")
        sys.exit(1)
    ok(f"File exists ({os.path.getsize(stl_path) / 1e6:.1f} MB)")

    # Check 2 — binary format
    if check_binary_format(stl_path):
        ok("Binary STL format")
    else:
        fail("ASCII STL format detected — convert to binary before submitting. "
             "Binary STL loads significantly faster at 500k+ triangle counts.")

    # Load mesh
    m = load_stl(stl_path, stl_mesh_module)
    vectors = m.vectors  # shape: (n_facets, 3 vertices, 3 coords)
    n_facets = len(vectors)

    # Check 3 — facet count
    if n_facets >= MIN_FACET_COUNT:
        ok(f"Facet count: {n_facets:,} (minimum {MIN_FACET_COUNT:,})")
    else:
        fail(f"Facet count: {n_facets:,} — below minimum {MIN_FACET_COUNT:,}. "
             "Mesh may be too coarse for reliable solid conversion.")

    # Check 4 — degenerate triangles (zero-area facets)
    v0 = vectors[:, 0, :]
    v1 = vectors[:, 1, :]
    v2 = vectors[:, 2, :]
    cross = np.cross(v1 - v0, v2 - v0)
    areas = np.linalg.norm(cross, axis=1) / 2.0
    zero_area = np.sum(areas < 1e-10)
    if zero_area == 0:
        ok("No degenerate (zero-area) triangles found")
    else:
        fail(f"{zero_area:,} degenerate triangles found — these can cause "
             "mesh-to-solid conversion failures.")

    # Compute bounding box from all vertices
    all_verts = vectors.reshape(-1, 3)
    x_min, y_min, z_min = all_verts.min(axis=0)
    x_max, y_max, z_max = all_verts.max(axis=0)

    cx = (x_min + x_max) / 2.0
    cy = (y_min + y_max) / 2.0
    cz = (z_min + z_max) / 2.0

    x_span = x_max - x_min
    y_span = y_max - y_min
    z_span = z_max - z_min

    # Check 5 — origin centring
    origin_drift = max(abs(cx), abs(cy), abs(cz))
    if origin_drift <= ORIGIN_TOLERANCE_MM:
        ok(f"Bounding-box centre: ({cx:.3f}, {cy:.3f}, {cz:.3f}) mm — "
           f"within {ORIGIN_TOLERANCE_MM} mm of origin")
    else:
        fail(
            f"Bounding-box centre: ({cx:.3f}, {cy:.3f}, {cz:.3f}) mm — "
            f"maximum drift {origin_drift:.3f} mm exceeds {ORIGIN_TOLERANCE_MM} mm tolerance.\n"
            "         The STL must be recentred to the world origin before submission.\n"
            "         Recentre by computing the bounding-box midpoint offset and\n"
            "         applying it via your modelling tool's transform function."
        )

    # Informational — dimensions
    info(f"Bar-to-bar width (X span): {x_span:.1f} mm  ({x_span / MM_PER_INCH:.2f}\")")
    info(f"Tree depth F→B  (Y span): {y_span:.1f} mm  ({y_span / MM_PER_INCH:.2f}\")")
    info(f"Overall height  (Z span): {z_span:.1f} mm  ({z_span / MM_PER_INCH:.2f}\")")
    info(f"Bounding box: X [{x_min:.1f} → {x_max:.1f}]  "
         f"Y [{y_min:.1f} → {y_max:.1f}]  Z [{z_min:.1f} → {z_max:.1f}]")

    # Informational — approximate gullet width at the pommel end
    # Estimate: find all vertices near Y = y_min (front of tree, pommel end)
    # and measure the X span of vertices near Z = cz (midplane, gullet channel)
    pommel_mask = all_verts[:, 1] < (y_min + y_span * 0.15)
    if pommel_mask.sum() > 10:
        pommel_verts = all_verts[pommel_mask]
        mid_z_mask = np.abs(pommel_verts[:, 2] - cz) < z_span * 0.25
        if mid_z_mask.sum() > 4:
            channel_verts = pommel_verts[mid_z_mask]
            est_gullet = channel_verts[:, 0].max() - channel_verts[:, 0].min()
            flag = "" if est_gullet >= 70 else "  ← BELOW 70 mm MINIMUM — verify on horse!"
            info(f"Estimated gullet width at pommel: {est_gullet:.1f} mm "
                 f"({est_gullet / MM_PER_INCH:.2f}\"){flag}")
        else:
            info("Gullet width estimate: insufficient midplane vertices at pommel — check manually.")
    else:
        info("Gullet width estimate: insufficient pommel-region vertices — check manually.")

    # Print results
    print("\n".join(results))
    print()
    if failed == 0:
        print(f"Result: ALL {passed} checks PASSED — ready to submit.\n")
        return 0
    else:
        print(f"Result: {failed} check(s) FAILED, {passed} passed — "
              f"fix failures before opening a pull request.\n")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="Validate an STL file for submission to saddle-examples-Blender.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("stl_path", nargs="?", help="Path to the STL file to validate.")
    args = parser.parse_args()

    if not args.stl_path:
        parser.print_help()
        sys.exit(2)

    sys.exit(validate(args.stl_path))


if __name__ == "__main__":
    main()
