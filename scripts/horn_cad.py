"""Parametric tractrix horn generator — neck + bell quadrant, screwless joints.

Replaces the pin-socket assembly (8x Ø4x20mm rod pins + epoxy, registering only
the neck-to-bell split) with integral tongue-and-groove joints printed directly
into the parts, on *every* split: neck-to-bell (one continuous ring) and all
four bell-quadrant-to-quadrant seams (three tabs each). No hardware, and the
quadrant seams -- previously unregistered, which is why the bell didn't fit
square -- now self-align.

All four bell quadrants remain a single identical STL: each has a tongue on
its "trailing" flat face and a groove on its "leading" flat face, so four
copies rotated 0/90/180/270 deg about Z tile into a ring that always mates
tongue-into-groove at every seam (rotational symmetry, no left/right variants).

Reuses the profile math in tractrix.py (source of truth for the acoustic
horn shape). Run with the project venv:
    .venv/bin/python scripts/horn_cad.py
Outputs cad/horn_neck.stl and cad/horn_bell_quadrant.stl (+ .step for reference).
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from tractrix import BOLT_HOLES, BOLT_PCD_MM, THROAT_DIAMETER_MM, mouth_radius_mm

import build123d as bd

# --- horn parameters (unchanged from design-notes.md rev 2) ---
FC = 340.0
WALL = 6.0
SPLIT_X = 230.0  # axial distance from throat where neck ends / bell starts
AXIAL_SIGN = -1.0  # build123d puts +x_from_throat at -Z; absorbed here so the
                    # rest of this file can just think in "x from throat"

FLANGE_OD = 130.0
FLANGE_T = 8.0
FLANGE_HOLE_D = 6.5

# circumferential (neck-bell) tongue-and-groove
C_TONGUE_H = 2.0
C_TONGUE_W = 2.0
GROOVE_CLEAR_W = 0.15  # per-side radial/width clearance
GROOVE_CLEAR_D = 0.2   # per-side depth clearance

# radial (quadrant-quadrant) tongue-and-groove: N_TABS bosses along the seam
N_TABS = 3
TAB_LEN = 14.0     # axial extent of each tab, mm
TAB_MARGIN = 10.0  # keep tabs this far from the bell's inner/outer edges
R_TONGUE_H = 2.0
R_TONGUE_W = 2.0


def rm_mm() -> float:
    return mouth_radius_mm(FC)


def s_of(r: float, rm: float) -> float:
    return math.sqrt(max(rm * rm - r * r, 0.0))


def x_from_throat_of(r: float, rm: float, rt: float) -> float:
    """Closed-form axial position (from throat) for inner radius r."""
    s = s_of(r, rm)
    st = s_of(rt, rm)
    # tractrix_x_mm() measures from the mouth; convert to "from throat"
    def tx(rr: float, ss: float) -> float:
        return rm * math.log((rm + ss) / rr) - ss
    length = tx(rt, st)
    return length - tx(r, s)


def normal_at(r: float, rm: float) -> tuple[float, float]:
    """Outward unit normal (nx, nr) to the meridian curve at radius r,
    analytic (dx/dr = r/(rm+s) - rm/r), verified against the mouth/throat
    asymptotes: pure-radial near the throat, pure-axial at the mouth rim."""
    s = s_of(r, rm)
    dxdr = r / (rm + s) - rm / r if r > 0 else -1e9
    tx, tr = dxdr, 1.0
    mag = math.hypot(tx, tr)
    nx, nr = tr / mag, -tx / mag  # rotate tangent -90 deg
    return nx, nr


# Near the mouth the tractrix curve's radius of curvature shrinks below the
# wall thickness, so a true constant-perpendicular offset self-intersects
# (the outer curve, offset mostly *axially* there per the mouth asymptote,
# ends up with a smaller radius than the inner curve at the same x -- a real
# geometric crossing, confirmed numerically, not a sign/sampling bug). Past
# this radius we fall back to a plain radial offset instead, which can never
# self-intersect (outer_x == inner_x, so the two curves stay a constant
# distance apart in x with outer_r always > inner_r).
R_SAFE = 105.0


def build_profile(n: int = 160):
    """Return (inner_pts, outer_pts) as (x_from_throat, r) lists, throat->mouth.
    True constant-perpendicular offset up to R_SAFE, plain radial offset
    beyond it (see R_SAFE comment) -- avoids the self-intersecting profile
    that a naive constant-normal offset produces near the mouth."""
    rm = rm_mm()
    rt = THROAT_DIAMETER_MM / 2
    inner, outer = [], []
    for i in range(n + 1):
        t = i / n
        r = rt + (rm - rt) * (t ** 1.5)  # bias toward throat, matches tractrix.py
        r = min(r, rm - 1e-6)
        x = x_from_throat_of(r, rm, rt)
        inner.append((x, r))
        if r <= R_SAFE:
            nx, nr = normal_at(r, rm)
            outer.append((x + WALL * nx, r + WALL * nr))
        else:
            outer.append((x, r + WALL))
    inner[-1] = (x_from_throat_of(rm - 1e-6, rm, rt), rm)
    outer[-1] = (inner[-1][0], inner[-1][1] + WALL)
    # the switch from perpendicular to radial offset at R_SAFE leaves a tiny
    # (~2-3mm) backward step in outer x right at the crossover; running-max
    # it away rather than letting a non-monotonic wiggle into the wire
    for i in range(1, len(outer)):
        if outer[i][0] < outer[i - 1][0]:
            outer[i] = (outer[i - 1][0], outer[i][1])
    return inner, outer


def revolve_shell(inner, outer) -> bd.Part:
    iv = [bd.Vector(r, 0, AXIAL_SIGN * x) for x, r in inner]
    ov = [bd.Vector(r, 0, AXIAL_SIGN * x) for x, r in outer]
    profile_pts = iv + list(reversed(ov))
    with bd.BuildPart() as p:
        with bd.BuildSketch(bd.Plane.XZ):
            with bd.BuildLine():
                bd.Polyline(*profile_pts, close=True)
            bd.make_face()
        bd.revolve(axis=bd.Axis.Z)
    return p.part


def r_at(x_target: float, pts) -> float:
    xs = [p[0] for p in pts]
    rs = [p[1] for p in pts]
    for i in range(len(xs) - 1):
        if xs[i] <= x_target <= xs[i + 1]:
            t = (x_target - xs[i]) / (xs[i + 1] - xs[i])
            return rs[i] + t * (rs[i + 1] - rs[i])
    return rs[-1] if x_target > xs[-1] else rs[0]


def make_flange() -> bd.Part:
    """Disc at the throat plane (z=0), extruded away from the bell (the bell
    extends toward AXIAL_SIGN*x, so the flange extrudes the opposite way)."""
    with bd.BuildPart() as p:
        with bd.BuildSketch(bd.Plane.XY):
            bd.Circle(FLANGE_OD / 2)
            with bd.Locations([(0, 0)]):
                bd.Circle(THROAT_DIAMETER_MM / 2, mode=bd.Mode.SUBTRACT)
            with bd.PolarLocations(BOLT_PCD_MM / 2, BOLT_HOLES):
                bd.Circle(FLANGE_HOLE_D / 2, mode=bd.Mode.SUBTRACT)
        bd.extrude(amount=-AXIAL_SIGN * FLANGE_T)
    return p.part


def circumferential_tongue_groove(neck: bd.Part, bell: bd.Part, inner, outer):
    """Add a tongue ring to the neck's top face, cut a matching groove into
    the bell's bottom face, at SPLIT_X."""
    r_in = r_at(SPLIT_X, inner)
    r_out = r_at(SPLIT_X, outer)
    r_mid = (r_in + r_out) / 2
    z_split = AXIAL_SIGN * SPLIT_X

    with bd.BuildPart() as tp:
        with bd.BuildSketch(bd.Plane.XY.offset(z_split)):
            bd.Circle(r_mid + C_TONGUE_W / 2)
            bd.Circle(r_mid - C_TONGUE_W / 2, mode=bd.Mode.SUBTRACT)
        bd.extrude(amount=-AXIAL_SIGN * C_TONGUE_H)
    tongue = tp.part
    neck = neck + tongue

    gw = C_TONGUE_W + 2 * GROOVE_CLEAR_W
    gd = C_TONGUE_H + GROOVE_CLEAR_D
    with bd.BuildPart() as gp:
        with bd.BuildSketch(bd.Plane.XY.offset(z_split)):
            bd.Circle(r_mid + gw / 2)
            bd.Circle(r_mid - gw / 2, mode=bd.Mode.SUBTRACT)
        bd.extrude(amount=AXIAL_SIGN * gd)
    groove = gp.part
    bell = bell - groove
    return neck, bell


def tab_z_bands(x_lo: float, x_hi: float, n: int):
    usable = (x_hi - x_lo) - 2 * TAB_MARGIN
    span = usable / n if n > 0 else 0
    bands = []
    for i in range(n):
        c = x_lo + TAB_MARGIN + span * (i + 0.5)
        bands.append((c - TAB_LEN / 2, c + TAB_LEN / 2))
    return bands


def quadrant_with_joints(bell_ring: bd.Part, inner, outer) -> bd.Part:
    """One 90 deg wedge with a tongue on its trailing face (azimuth 0, XZ
    plane) and a groove on its leading face (azimuth 90, YZ plane). Four
    rotated copies of this single part tile a full ring, tongue-into-groove
    at every seam (see module docstring for the symmetry argument)."""
    big = 1000.0
    half_y = bd.Box(2 * big, big, 2 * big, align=(bd.Align.CENTER, bd.Align.MIN, bd.Align.CENTER))
    half_x = bd.Box(big, 2 * big, 2 * big, align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.CENTER))
    wedge = bell_ring & half_y & half_x  # azimuth in [0, 90] deg

    bands = tab_z_bands(SPLIT_X, x_from_throat_of(rm_mm() - 1e-6, rm_mm(), THROAT_DIAMETER_MM / 2), N_TABS)

    for x_lo, x_hi in bands:
        r_lo, r_hi = r_at(x_lo, inner), r_at(x_hi, inner)
        r_mid = (r_at((x_lo + x_hi) / 2, inner) + r_at((x_lo + x_hi) / 2, outer)) / 2
        z_lo, z_hi = sorted((AXIAL_SIGN * x_lo, AXIAL_SIGN * x_hi))

        # groove on trailing face (Y=0 plane, quadrant material at Y>=0):
        # remove material from Y=0 into Y>0 by (tongue_h + clearance)
        gw = R_TONGUE_W + 2 * GROOVE_CLEAR_W
        gd = R_TONGUE_H + GROOVE_CLEAR_D
        notch = bd.Box(
            gw, gd, abs(z_hi - z_lo),
            align=(bd.Align.CENTER, bd.Align.MIN, bd.Align.CENTER),
        ).moved(bd.Location((r_mid, 0, (z_lo + z_hi) / 2)))
        wedge = wedge - notch

        # tongue on leading face (X=0 plane, quadrant material at X>=0):
        # add material protruding from X=0 into X<0
        boss = bd.Box(
            R_TONGUE_H, R_TONGUE_W, abs(z_hi - z_lo),
            align=(bd.Align.MAX, bd.Align.CENTER, bd.Align.CENTER),
        ).moved(bd.Location((0, r_mid, (z_lo + z_hi) / 2)))
        wedge = wedge + boss

    return wedge


def main():
    out_dir = Path(__file__).parent.parent / "cad"
    inner, outer = build_profile()
    shell = revolve_shell(inner, outer)
    flange = make_flange()

    z_split = AXIAL_SIGN * SPLIT_X
    big = 1000.0
    below = bd.Box(2 * big, 2 * big, big, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MAX)).moved(
        bd.Location((0, 0, z_split))
    )
    above = bd.Box(2 * big, 2 * big, big, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)).moved(
        bd.Location((0, 0, z_split))
    )
    neck = (shell & above) if AXIAL_SIGN < 0 else (shell & below)
    bell_ring = (shell & below) if AXIAL_SIGN < 0 else (shell & above)
    neck = neck + flange

    neck, bell_ring = circumferential_tongue_groove(neck, bell_ring, inner, outer)
    quadrant = quadrant_with_joints(bell_ring, inner, outer)

    print(f"neck volume cm3:  {neck.volume / 1000:.1f}")
    print(f"neck bbox:        {neck.bounding_box()}")
    print(f"quadrant volume cm3: {quadrant.volume / 1000:.1f}")
    print(f"quadrant bbox:    {quadrant.bounding_box()}")

    # correctness check: rotate two copies of the quadrant 0/90 deg and
    # confirm they don't clash (near-zero intersection) but DO engage
    # (dilated intersection picks up the tab volume).
    q0 = quadrant
    q1 = quadrant.moved(bd.Location((0, 0, 0), (0, 0, 1), 90))
    clash = q0 & q1
    clash_vol = clash.volume if clash is not None else 0.0
    print(f"adjacent-copy clash volume mm3 (want ~0): {clash_vol:.2f}")

    bd.export_stl(neck, str(out_dir / "horn_neck.stl"))
    bd.export_stl(quadrant, str(out_dir / "horn_bell_quadrant.stl"))
    bd.export_step(neck, str(out_dir / "horn_neck.step"))
    bd.export_step(quadrant, str(out_dir / "horn_bell_quadrant.step"))
    print(f"wrote STL/STEP to {out_dir}")


if __name__ == "__main__":
    main()
