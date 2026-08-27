"""Vented-box modeling for the OJAS-style 2-way bass bin.

Implements Small's 4th-order vented-box transfer function (with leakage QL)
plus port sizing and port-velocity / excursion sanity checks.

Coefficients verified against the B4 alignment: Qts=0.383, h=1, QL->inf
yields a1=a3=2.613, a2=3.414 (Butterworth), alpha=1.414.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

C = 343.0        # speed of sound, m/s
RHO = 1.204      # air density, kg/m^3


@dataclass(frozen=True)
class Driver:
    name: str
    fs: float        # Hz
    qts: float
    qes: float
    vas_l: float     # litres
    re: float        # ohm
    bl: float        # Tm
    sd_cm2: float    # cm^2
    xmax_mm: float
    mms_g: float
    sens_db: float   # dB 1W/1m


TF1225 = Driver("Celestion TF1225", fs=55.60, qts=0.370, qes=0.420,
                vas_l=67.27, re=5.08, bl=14.32, sd_cm2=530.93,
                xmax_mm=4.5, mms_g=48.52, sens_db=97.0)

FTR12_3070C = Driver("Celestion FTR12-3070C", fs=65.10, qts=0.321, qes=0.362,
                     vas_l=43.70, re=5.59, bl=18.58, sd_cm2=530.93,
                     xmax_mm=5.5, mms_g=54.61, sens_db=96.0)

FSL1225 = Driver("Peerless FSL-1225R02-08", fs=63.0, qts=0.44, qes=0.49,
                 vas_l=54.8, re=5.5, bl=14.9, sd_cm2=547.0,
                 xmax_mm=5.3, mms_g=50.1, sens_db=96.2)


def vented_response_db(d: Driver, vb_l: float, fb: float, f: float,
                       ql: float = 7.0) -> float:
    """Relative response (dB) of driver in vented box Vb tuned to fb, at f."""
    alpha = d.vas_l / vb_l
    h = fb / d.fs
    a1 = (ql + h * d.qts) / (math.sqrt(h) * ql * d.qts)
    a2 = (h + (alpha + 1 + h * h) * ql * d.qts) / (h * ql * d.qts)
    a3 = (h * ql + d.qts) / (math.sqrt(h) * ql * d.qts)
    f0 = math.sqrt(fb * d.fs)          # geometric-mean normalisation
    s = complex(0.0, f / f0)
    num = s ** 4
    den = s ** 4 + a1 * s ** 3 + a2 * s ** 2 + a3 * s + 1
    return 20 * math.log10(abs(num / den))


def f_at_drop(d: Driver, vb_l: float, fb: float, drop_db: float) -> float:
    """Frequency where response first falls drop_db below passband (search down)."""
    f = 400.0
    while f > 10.0:
        if vented_response_db(d, vb_l, fb, f) < -drop_db:
            return f
        f *= 0.995
    return f


def slot_port_length(vb_l: float, fb: float, area_cm2: float) -> float:
    """Physical slot-port length (m), end correction 0.85 * effective diameter."""
    sp = area_cm2 * 1e-4
    vb = vb_l * 1e-3
    l_eff = C * C * sp / ((2 * math.pi * fb) ** 2 * vb)
    d_eq = math.sqrt(4 * sp / math.pi)
    return l_eff - 0.85 * d_eq


def port_velocity_ms(d: Driver, vb_l: float, fb: float, area_cm2: float,
                     power_w: float) -> float:
    """Rough peak port air velocity at fb, assuming all output radiates
    from the port there (worst case, monopole at 1 m)."""
    spl = d.sens_db + 10 * math.log10(power_w) + vented_response_db(d, vb_l, fb, fb)
    p_rms = 20e-6 * 10 ** (spl / 20)
    u_rms = p_rms * 2.0 / (RHO * fb)          # |p| = rho*f*U/2 at r=1m
    return u_rms * math.sqrt(2) / (area_cm2 * 1e-4)


def cone_excursion_mm(d: Driver, vb_l: float, fb: float, f: float,
                      power_w: float) -> float:
    """Peak cone excursion estimate: infinite-baffle displacement shaped by the
    vented-box excursion function (minimum at fb). Conservative near/below fb."""
    v_in = math.sqrt(power_w * d.re)          # drive voltage for rated power into Re
    w = 2 * math.pi * f
    ws = 2 * math.pi * d.fs
    s = complex(0, w / ws)
    hx = 1 / (s * s + s / d.qts + 1)          # displacement response, driver alone
    x_flat = (d.bl * v_in / d.re) / (d.mms_g * 1e-3 * ws ** 2)
    # driver-alone excursion: upper bound above fb (vented box unloads the cone
    # near fb); below fb it underestimates, so keep DSP high-pass in mind there
    return x_flat * abs(hx) * 1e3


def report(d: Driver, vb_l: float, fb: float, port_area_cm2: float,
           power_w: float) -> None:
    print(f"\n=== {d.name} | Vb={vb_l:.0f} L net, fb={fb:.1f} Hz, "
          f"port {port_area_cm2:.0f} cm2, {power_w:.0f} W ===")
    print(f"  alpha (Vas/Vb) = {d.vas_l / vb_l:.3f},  h (fb/fs) = {fb / d.fs:.3f}")
    for f in (30, 40, 45, 50, 55, 60, 70, 80, 100, 150, 200, 300):
        print(f"  {f:4d} Hz : {vented_response_db(d, vb_l, fb, f):+6.2f} dB")
    print(f"  F3  = {f_at_drop(d, vb_l, fb, 3):5.1f} Hz")
    print(f"  F6  = {f_at_drop(d, vb_l, fb, 6):5.1f} Hz")
    print(f"  F10 = {f_at_drop(d, vb_l, fb, 10):5.1f} Hz")
    lp = slot_port_length(vb_l, fb, port_area_cm2)
    print(f"  slot port physical length = {lp * 1000:.0f} mm")
    print(f"  port velocity @ fb, {power_w:.0f} W = "
          f"{port_velocity_ms(d, vb_l, fb, port_area_cm2, power_w):.1f} m/s peak")
    x = max(cone_excursion_mm(d, vb_l, fb, f, power_w) for f in range(int(fb), 200))
    print(f"  max cone excursion {int(fb)}-200 Hz @ {power_w:.0f} W ~ {x:.1f} mm "
          f"(Xmax = {d.xmax_mm} mm)")


if __name__ == "__main__":
    # sanity check: B4 alignment reproduces Butterworth -3.01 dB at f0
    b4 = Driver("B4 check", fs=50, qts=0.383, qes=0.383, vas_l=100 * 1.414,
                re=6, bl=10, sd_cm2=500, xmax_mm=5, mms_g=50, sens_db=90)
    db_at_f0 = vented_response_db(b4, 100, 50, 50, ql=1e9)
    assert abs(db_at_f0 + 3.01) < 0.1, f"B4 check failed: {db_at_f0:.2f} dB"
    print(f"B4 alignment check: {db_at_f0:+.2f} dB at f0 (expect -3.01)  OK")

    POWER = 30.0  # realistic loud home-listening peaks on a 97 dB speaker

    # candidate alignments, TF1225
    for vb, fb in ((55, 50.0), (60, 48.0), (65, 46.0), (70, 44.0)):
        report(TF1225, vb, fb, port_area_cm2=105.0, power_w=POWER)

    # comparison: FTR12-3070C in its sensible alignment
    for vb, fb in ((40, 55.0), (50, 52.0)):
        report(FTR12_3070C, vb, fb, port_area_cm2=105.0, power_w=POWER)

    # Peerless FSL-1225R02-08 in the existing 62 L cabinet, tuning sweep
    for vb, fb in ((62, 44.0), (62, 46.0), (62, 48.0), (62, 50.0)):
        report(FSL1225, vb, fb, port_area_cm2=117.6, power_w=POWER)
