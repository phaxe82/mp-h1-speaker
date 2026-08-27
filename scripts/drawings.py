"""Generate dimensioned build drawings (cad/drawings.pdf).

Three sheets: cabinet front elevation, cabinet vertical section, horn section.
All dimensions in mm. Run with the project venv: .venv/bin/python scripts/drawings.py
"""

from __future__ import annotations

import math

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Circle, Rectangle

INK = "#222222"
DIM = "#B0432E"


def dim_h(ax, x0: float, x1: float, y: float, text: str, offset: float = 0) -> None:
    ax.annotate("", (x0, y), (x1, y), arrowprops=dict(arrowstyle="<->", color=DIM, lw=0.9))
    ax.text((x0 + x1) / 2, y + 8 + offset, text, ha="center", va="bottom",
            color=DIM, fontsize=8)


def dim_v(ax, y0: float, y1: float, x: float, text: str) -> None:
    ax.annotate("", (x, y0), (x, y1), arrowprops=dict(arrowstyle="<->", color=DIM, lw=0.9))
    ax.text(x + 8, (y0 + y1) / 2, text, ha="left", va="center",
            color=DIM, fontsize=8, rotation=90)


def sheet_front(pdf: PdfPages) -> None:
    fig, ax = plt.subplots(figsize=(8.27, 11.69))
    ax.set_title("Sheet 1 — Cabinet front elevation (mm)", fontsize=11)
    # outline
    ax.add_patch(Rectangle((0, 0), 456, 536, fill=False, ec=INK, lw=1.4))
    # side panel edges (visible ply, 18 each side)
    for x in (18, 438):
        ax.plot([x, x], [0, 536], color=INK, lw=0.6, ls=":")
    # top/bottom edges
    for y in (18, 518):
        ax.plot([18, 438], [y, y], color=INK, lw=0.6, ls=":")
    # baffle lower edge -> port slot 18..46
    ax.add_patch(Rectangle((18, 18), 420, 28, fill=True, fc="#dddddd", ec=INK, lw=0.8))
    ax.text(228, 32, "port slot 420 × 28", ha="center", va="center", fontsize=7)
    # woofer
    ax.add_patch(Circle((228, 346), 142.5, fill=False, ec=INK, lw=1.2))
    ax.text(228, 346, "cutout Ø285 nom.\n(FSL-1225 — verify vs driver)", ha="center", va="center", fontsize=8)
    for k in range(4):
        a = math.radians(45 + 90 * k)
        ax.add_patch(Circle((228 + 148.5 * math.cos(a), 346 + 148.5 * math.sin(a)),
                            3.5, fill=False, ec=INK, lw=0.8))
    ax.text(228, 480, "bolt holes: match FSL-1225 frame (T-nuts behind)", ha="center", fontsize=7)
    # feet
    for x0 in (55, 311):
        ax.add_patch(Rectangle((x0, -90), 90, 90, fill=False, ec=INK, lw=1.0))
    ax.text(228, -45, "feet 90 × 90 × 366 solid timber", ha="center", va="center", fontsize=7)
    # dims
    dim_h(ax, 0, 456, 570, "456")
    dim_v(ax, 0, 536, 500, "536")
    dim_v(ax, 18, 46, -40, "28")
    dim_v(ax, 46, 346, -40, "300 (slot top to woofer centre)")
    dim_h(ax, 0, 228, -130, "228")
    ax.set_xlim(-160, 620)
    ax.set_ylim(-180, 640)
    ax.set_aspect("equal")
    ax.axis("off")
    pdf.savefig(fig)
    plt.close(fig)


def sheet_section(pdf: PdfPages) -> None:
    fig, ax = plt.subplots(figsize=(8.27, 11.69))
    ax.set_title("Sheet 2 — Vertical section, side view (mm)", fontsize=11)
    # y = depth (0 front), z = height
    ax.add_patch(Rectangle((0, 0), 366, 536, fill=False, ec=INK, lw=1.4))
    # panels (hatched)
    panels = [
        ("baffle", (0, 46), 18, 472),
        ("back", (348, 18), 18, 500),
        ("bottom", (0, 0), 366, 18),
        ("top", (0, 518), 366, 18),
        ("port shelf", (18, 46), 132, 18),
        ("brace", (18, 160), 330, 18),
    ]
    for name, (y, z), w, h in panels:
        ax.add_patch(Rectangle((y, z), w, h, fill=True, fc="#e8e0d0",
                               ec=INK, lw=0.8, hatch="///"))
    ax.text(84, 55, "port shelf", fontsize=7, va="bottom")
    ax.text(180, 169, "window brace 420×330, 300×210 cutout", fontsize=7, va="center")
    # duct arrow
    ax.annotate("", (10, 32), (140, 32),
                arrowprops=dict(arrowstyle="<-", color=DIM, lw=1.2))
    ax.text(75, 20, "duct 150 deep × 28 high", color=DIM, fontsize=7, ha="center")
    # woofer (side profile): baffle rear at y=18, depth 130
    ax.add_patch(Rectangle((18, 346 - 156.75), 96, 313.5, fill=False, ec=INK, lw=1.0))
    ax.text(66, 346, "FSL-1225\ndepth ~96", ha="center", va="center", fontsize=7)
    # terminal
    ax.add_patch(Rectangle((348, 70), 18, 60, fill=False, ec=INK, lw=0.8))
    ax.text(340, 100, "terminal Ø60 @ z=100", ha="right", fontsize=7)
    # cable exit
    ax.add_patch(Rectangle((178, 518), 10, 18, fill=False, ec=INK, lw=0.8))
    ax.text(183, 545, "CD cable exit Ø10 @ y=183", ha="center", fontsize=7)
    dim_h(ax, 0, 366, 570, "366")
    dim_v(ax, 0, 536, 400, "536")
    dim_v(ax, 18, 46, -40, "28 duct")
    dim_h(ax, 18, 150, -60, "132 shelf")
    ax.set_xlim(-120, 520)
    ax.set_ylim(-120, 640)
    ax.set_aspect("equal")
    ax.axis("off")
    pdf.savefig(fig)
    plt.close(fig)


def sheet_horn(pdf: PdfPages) -> None:
    import csv
    fig, ax = plt.subplots(figsize=(11.69, 8.27))
    ax.set_title("Sheet 3 — Horn section, tractrix fc = 340 Hz (mm)", fontsize=11)
    with open("cad/horn_profile_340.csv") as fh:
        rows = [(float(a), float(b)) for a, b in list(csv.reader(fh))[1:]]
    xs = [x for x, _ in rows]
    rs = [r for _, r in rows]
    for sign in (1, -1):
        ax.plot(xs, [sign * r for r in rs], color=INK, lw=1.3)
        # outer wall approx (visual only, +6)
        ax.plot(xs, [sign * (r + 6) for r in rs], color=INK, lw=0.7, ls="--")
    # flange
    ax.add_patch(Rectangle((-8, -65), 8, 130, fill=False, ec=INK, lw=1.0))
    ax.text(-30, 0, "flange Ø130×8\n4×M6 on Ø102 PCD\n(ROSSO-65CD-T)",
            ha="right", va="center", fontsize=8)
    # split plane
    ax.plot([230, 230], [-170, 170], color=DIM, lw=0.9, ls="-.")
    ax.text(232, 150, "split z=230\n8 × Ø4×20 pin sockets\n(30°,75°,…,345°)",
            color=DIM, fontsize=7)
    ax.plot([0, 0], [-170, 170], color=INK, lw=0.5, ls=":")
    dim_h(ax, 0, 302.6, -200, "302.6")
    dim_v(ax, -160.6, 160.6, 330, "Ø321 mouth")
    dim_v(ax, -18, 18, -60, "Ø36 throat")
    ax.text(150, -240, "wall 6 mm · neck prints vertical (174×174×238) · "
                       "bell = 4 identical quadrants (161×161×73)",
            ha="center", fontsize=8)
    ax.set_xlim(-120, 420)
    ax.set_ylim(-260, 220)
    ax.set_aspect("equal")
    ax.axis("off")
    pdf.savefig(fig)
    plt.close(fig)


def main() -> None:
    with PdfPages("cad/drawings.pdf") as pdf:
        sheet_front(pdf)
        sheet_section(pdf)
        sheet_horn(pdf)
    print("wrote cad/drawings.pdf (3 sheets)")


if __name__ == "__main__":
    main()
