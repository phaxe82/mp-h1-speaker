# DSP Tuning Guide

Goal: take the finished speakers from "assembled" to "voiced" using a
measurement mic and your amp's DSP. Budget an afternoon.

## Kit
- **miniDSP UMIK-1** USB mic (calibrated) — or any calibrated measurement mic
- **REW (Room EQ Wizard)** — free, macOS
- Mic stand, tape measure

## Baseline settings (before measuring)

Enter these first — they're from the design math, not taste:

| DSP block | Setting | Why |
|---|---|---|
| High-pass | 40 Hz, 24 dB/oct (Butterworth) | protects the woofer below fb = 48 Hz where the vented box unloads the cone |
| Low-shelf | +3 dB below 100 Hz, Q 0.7 | compensates the shallow QB3-style rolloff (design F6 = 47 Hz) |
| Peak EQ | −2 dB at 1.6 kHz, Q 2 (placeholder) | typical woofer/horn overlap bump; refine by measurement |

## Measurement session

1. **Nearfield sanity check** (mic 10 cm from woofer cone, then port):
   confirm the port output peaks around 48 Hz — that verifies box tuning.
   If it's off by more than ~3 Hz, adjust port depth (each −10 mm of duct
   raises fb ~1 Hz) before any EQ.
2. **Crossover polarity check**: measure at 1 m on the horn axis. Flip CD
   polarity (swap leads at the driver) and keep whichever gives a smooth
   sum through 1–1.5 kHz; the wrong one shows a deep suckout.
3. **Level match**: play pink noise band-limited 2–8 kHz vs 200–800 Hz.
   The horn band should sit level with the woofer band. If it's >±1.5 dB
   off, change the L-pad series resistor rather than burning DSP headroom.
   As-built is **6.8 Ω**: smaller = hotter horn (6.2 → 5.6 Ω), larger =
   quieter (8.2 Ω). Leave the 2.7 Ω shunt unless you need a big swing.
4. **Listening-position sweep** (mic at ear height, main seat, 3–5 spatially
   averaged positions): let REW's EQ tool generate corrections **below
   500 Hz only** (room modes). Above 500 Hz, correct only broad trends
   (Q ≤ 2, cuts preferred), never narrow dips.
5. **House curve**: aim for flat 200 Hz–2 kHz, then a gentle downward tilt,
   roughly −4 dB by 10 kHz at the listening position. Horns sound right
   with a slight top-octave shelf-down; trust your ears for the last dB.

## Notes specific to this design

- Both drivers share one amp channel, so every PEQ is global. That's fine:
  below 1 kHz only the woofer radiates, above ~5 kHz only the horn does —
  the overlap region 1–3 kHz is where to be gentle.
- The 12 µF/1.5 mH/L-pad network was designed for ~1.2 kHz into a nominal
  8 Ω horn load. If REW shows the acoustic crossover sitting far from
  1.2 kHz, adjust in DSP (shelf filters around the overlap), not by
  swapping passive parts, unless the error exceeds ~1/3 octave.
- Save the final DSP preset and export the REW session; keep both in
  `docs/measurements/` for the day you move rooms or rebuild something.
