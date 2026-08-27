"""Tractrix horn profile generator for the Celestion CDX14-3050 (1.4" exit).

The tractrix curve: a horn whose mouth radius r_m sets the flare cutoff
    r_m = c / (2 * pi * fc)
and whose axial coordinate for a given radius r is the closed form
    x(r) = r_m * ln((r_m + sqrt(r_m^2 - r^2)) / r) - sqrt(r_m^2 - r^2)
with x measured from the mouth plane (x=0 at mouth, increasing toward throat).

Outputs a CSV profile (axial position from throat, inner radius) for CAD
import, plus a printed summary. Wall thickness is added in CAD.
"""

from __future__ import annotations

import csv
import math
import sys

C = 343.0  # speed of sound, m/s

# Celestion CDX14-3050 interface (datasheet)
THROAT_DIAMETER_MM = 36.0          # 1.4" exit
BOLT_HOLES = 4                     # M6
BOLT_PCD_MM = 102.0
DRIVER_BODY_DIAMETER_MM = 125.0


def mouth_radius_mm(fc_hz: float) -> float:
    return C / (2 * math.pi * fc_hz) * 1000


def tractrix_x_mm(r_mm: float, rm_mm: float) -> float:
    """Axial distance from the mouth plane for inner radius r (both mm)."""
    root = math.sqrt(rm_mm * rm_mm - r_mm * r_mm)
    return rm_mm * math.log((rm_mm + root) / r_mm) - root


def generate_profile(fc_hz: float, throat_d_mm: float = THROAT_DIAMETER_MM,
                     n_points: int = 200) -> list[tuple[float, float]]:
    """(axial position from throat, inner radius) pairs, throat -> mouth, mm."""
    rm = mouth_radius_mm(fc_hz)
    rt = throat_d_mm / 2
    if rt >= rm:
        raise ValueError("throat radius must be smaller than mouth radius")
    length = tractrix_x_mm(rt, rm)  # total axial length throat->mouth
    pts: list[tuple[float, float]] = []
    for i in range(n_points + 1):
        # sample radius; bias sampling toward the throat where curvature is high
        t = i / n_points
        r = rt + (rm - rt) * (t ** 1.5)
        r = min(r, rm - 1e-9)
        x_from_throat = length - tractrix_x_mm(r, rm)
        pts.append((x_from_throat, r))
    pts[-1] = (length, rm)  # exact mouth point (tangent is axial here)
    return pts


def main() -> None:
    fc = float(sys.argv[1]) if len(sys.argv) > 1 else 340.0
    out = sys.argv[2] if len(sys.argv) > 2 else "cad/horn_profile.csv"

    rm = mouth_radius_mm(fc)
    pts = generate_profile(fc)
    length = pts[-1][0]

    # closed-form validation
    assert abs(pts[0][1] * 2 - THROAT_DIAMETER_MM) < 1e-6
    assert abs(pts[-1][1] - rm) < 1e-6
    mid_r = (THROAT_DIAMETER_MM / 2 + rm) / 2
    x_mid = length - tractrix_x_mm(mid_r, rm)
    assert 0 < x_mid < length

    with open(out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["x_from_throat_mm", "inner_radius_mm"])
        for x, r in pts:
            w.writerow([f"{x:.3f}", f"{r:.3f}"])

    print(f"Tractrix horn, fc = {fc:.0f} Hz")
    print(f"  throat diameter : {THROAT_DIAMETER_MM:.1f} mm "
          f"(1.4\" exit: ROSSO-65CD-T 35.6 mm / CDX14-3050 36 mm)")
    print(f"  mouth diameter  : {2 * rm:.1f} mm")
    print(f"  axial length    : {length:.1f} mm (throat plane to mouth plane)")
    print(f"  driver flange   : {BOLT_HOLES} x M6 on {BOLT_PCD_MM:.0f} mm PCD, "
          f"body {DRIVER_BODY_DIAMETER_MM:.0f} mm dia")
    print(f"  profile written : {out} ({len(pts)} points)")
    for probe in (0.25, 0.5, 0.75):
        r = THROAT_DIAMETER_MM / 2 + (rm - THROAT_DIAMETER_MM / 2) * probe
        x = length - tractrix_x_mm(r, rm)
        print(f"    r = {r:6.1f} mm at x = {x:6.1f} mm from throat")


if __name__ == "__main__":
    main()
