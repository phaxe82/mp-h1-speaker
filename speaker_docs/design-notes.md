# Design Notes — MP-H1 (OJAS-Style 2-Way Horn Speaker)

**MP-H1** — Mornington Peninsula, Horn, rev 1: round-tractrix, single-amp,
high-sensitivity 2-way. (MP-H2 reserved for the elliptical R-OSSE waveguide swap.)

All the acoustic math behind the build, with sources. Scripts that produced
these numbers: `scripts/box_model.py`, `scripts/tractrix.py`.

## 1. Concept

Two-way, high-efficiency: 12" reflex bass bin + compression driver on a
3D-printed round tractrix horn sitting on top. Modeled on the OJAS (Devon
Turnbull) two-way — the real kit uses a FaitalPRO 15PR400 + HF10AK on a long
tractrix; the Klipsch×OJAS kO-R2 crosses at 760 Hz with 97 dB sensitivity.
Drivers here are Celestion for Australian availability.

Amplification: 2-channel amp with DSP. So: **woofer runs direct** (no series
parts), **compression driver gets a passive 2nd-order high-pass + L-pad**,
and all voicing is DSP PEQ. This mirrors OJAS practice (minimal passive
parts, high-efficiency drivers, low amplifier power).

## 2. Drivers (datasheet values)

> **Revision 2 (July 2026):** design re-based on Wagner Online stock —
> Celestion proved unobtainable in Australia (TF1225 out of stock at the
> stockists checked; CDX14-3050 $499 at the one that had it). Both
> replacement drivers below are stocked by
> [Wagner Online](https://www.wagneronline.com.au) (Australian
> SB Audience / Peerless / Dayton distributor). Original Celestion figures
> remain in `box_model.py` for reference.

### Woofer — Peerless by Tymphany FSL-1225R02-08 (8 Ω), chosen
| Fs | Qts | Qes | Vas | Re | BL | Sd | Xmax | Mms | Le | Sens | Power |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 63.0 Hz | 0.44 | 0.49 | 54.8 L | 5.5 Ω | 14.9 Tm | 547 cm² | 5.3 mm | 50.1 g | 0.54 mH | 96.2 dB | 233 W AES |

Pro-style pressed-steel 12", paper cone, 65 mm voice coil, spec'd by
Tymphany as "extremely flat response up to 3,000 Hz" — the same recipe as
the TF1225 it replaces, with more Xmax. Frame Ø313.5 mm, depth ~96 mm
(shallower than the TF1225's 130 mm — more brace clearance). **Baffle
cut-out: nominal Ø285 mm — verify against the delivered driver before
routing** (the cutout/bolt-PCD page of the datasheet isn't in any public
mirror; 12" pro frames land 283–287 mm).

*(Earlier candidates: Celestion TF1225 — unobtainable in AU;
FTR12-3070C — rejected, higher Fs / smaller Vas = less extension.)*

### Compression driver — SB Audience ROSSO-65CD-T (8 Ω)
- **108 dB** 1W/1m, 70 W AES (140 W max), RDC 6.2 Ω
- Frequency range 500–20,000 Hz; **recommended crossover 1 kHz**
- Throat exit **35.6 mm (1.4")**, fitting **4 × M6 at 90° on Ø102 mm PCD** —
  identical to the Celestion CDX14-3050 it replaces, so **the printed horn
  flange in `cad/` fits unchanged** (36.0 mm bore vs 35.6 mm exit is a
  0.2 mm/side step; give the throat entry a light chamfer when finishing)
- 65 mm titanium diaphragm, ferrite motor, annular phase plug, copper-cap
  demodulation, 18.4° conical exit angle
- Body **Ø156 mm, depth 65.9 mm, 3.76 kg** — bigger and heavier than the
  Celestion (Ø125 mm / 1.7 kg): driver stand resized accordingly
  (Ø157 mm clamp ring, 50×50 column, 110×110×10 base)

## 3. Bass bin alignment (box_model.py)

Model: Small's 4th-order vented transfer function, QL = 7. Code sanity-checked
against the textbook B4 alignment (reproduces −3.01 dB at f0 with
Qts = 0.383, α = 1.414).

**Chosen: Vb = 62 L net (the as-modeled cabinet), fb = 48 Hz**
(FSL-1225R02-08: α = 0.88, h = 0.76). The cabinet was designed around the
TF1225 at the same tuning, and the FSL-1225 lands in the same place — with
the unchanged 150 mm duct the actual tuning computes to ~47 Hz. **No cabinet
or port change was needed for the driver swap.**

| f (Hz) | 40 | 45 | 50 | 55 | 60 | 70 | 80 | 100 | 150 | 200 |
|---|---|---|---|---|---|---|---|---|---|---|
| dB | −9.0 | −6.7 | −5.3 | −4.4 | −3.7 | −2.7 | −2.0 | −1.2 | −0.4 | −0.2 |

F3 = 67 Hz, F6 = 47 Hz, F10 = 38 Hz — essentially identical extension to the
original Celestion alignment. The rolloff is intentionally shallow (QB3-ish
pro-driver alignment): a gentle DSP low-shelf (+3–4 dB below ~100 Hz) plus
normal room gain gives flat in-room response into the mid-40s.

**Excursion:** ~2.5 mm peak at 30 W across 48–200 Hz vs Xmax 5.3 mm — fine.
Below fb the cone unloads, so **set a DSP high-pass at 40 Hz (24 dB/oct)**,
especially if using the low-shelf boost.

**Port:** full-width slot at the bottom of the front baffle (as in the
reference photo), formed by a shelf above the cabinet floor:
- Slot: **420 mm wide × 28 mm high** (Sp = 117.6 cm²)
- Physical duct length (front-to-back): **150 mm** (end correction 0.85·d_eq)
- Port velocity at fb, 30 W: ≈ 16.5 m/s peak — under the ~17 m/s chuffing
  threshold at realistically loud levels (30 W on 97 dB = ~112 dB peaks).

**Cabinet internal:** 420 W × 500 H × 330 D mm = 69.3 L gross.
Deductions: driver ≈ 3 L, port duct air 1.8 L, port shelf wood 1.1 L,
bracing ≈ 1 L → **net ≈ 62 L** (within 5% of target; tuning shifts <1 Hz).
External with 18 mm Baltic birch: **456 W × 536 H × 366 D mm**
(H/W = 1.18, matching the photo's proportions).

## 4. Horn (tractrix.py)

Tractrix with mouth radius r_m = c/(2π·fc); profile closed form
x(r) = r_m·ln((r_m + √(r_m²−r²))/r) − √(r_m²−r²).

**Chosen: fc = 340 Hz** → mouth **Ø321 mm**, axial length **303 mm** from
36 mm throat. Loading is effective from ~450 Hz, i.e. > 1.5 octaves below
the 1.15 kHz crossover — generous margin. (fc = 400 Hz / Ø273 was computed
as the smaller alternative; 340 Hz matches the photo scale and loads lower.)
Profile CSV for CAD: `cad/horn_profile_340.csv`.

**Print sectioning (235 × 235 × 250 mm bed) — as modeled in `cad/`:**
- **Neck** (throat → split at x = 230 mm): one vertical piece,
  167.5 × 167.5 × 238 mm, integrated CDX14/ROSSO bolt flange (Ø130 × 8 mm,
  4 × M6 on Ø102 PCD, Ø6.5 clearance holes).
- **Bell** (x 230–303 mm): 4 identical quadrants, 168.6 × 166.6 × 72.6 mm each.
- Wall 6 mm throughout.

> **Rev 3 (Aug 2026): screwless joints.** The rev-2 print run showed the bell
> quadrants fitting poorly — the only registration feature was 8 × Ø4×20mm
> pin sockets across the *neck-to-bell* split; the four quadrant-to-quadrant
> seams (where the visible misalignment actually was) had no registration at
> all, just a butt joint held square by hand while the epoxy set. Replaced
> the pins with **integral tongue-and-groove joints printed directly into
> the parts, on every split**: a continuous ring at the neck-bell interface,
> plus 3 tabs per quadrant-to-quadrant seam (tongue on one radial face,
> groove on the other — all 4 quadrants stay a single identical STL, since
> a part with tongue on its "trailing" face and groove on its "leading"
> face self-tiles into a ring under 90° rotation). No hardware, no drilling;
> assembly is dry-fit → epoxy in the grooves → tape/clamp → cure. Joint
> clearance is 0.15mm/side (width) and 0.2mm (depth) — tune in
> `scripts/horn_cad.py` (`GROOVE_CLEAR_W`/`GROOVE_CLEAR_D`) if your printer
> runs tighter or looser than that.
>
> **`scripts/horn_cad.py` (build123d, headless) is now the source of truth
> for `cad/horn_neck.stl` and `cad/horn_bell_quadrant.stl`** — regenerate
> with `.venv/bin/python scripts/horn_cad.py` after any profile/joint
> change. `speaker-full-design.f3d` still owns the cabinet and driver
> stand; it was not updated for this revision and is stale for the horn
> specifically.

## 5. Crossover / electrical

Both drivers hang on one amp channel. Woofer direct. CD chain:
**2nd-order Butterworth high-pass → L-pad → driver.**

- Target corner ≈ **1.2 kHz** acoustic (ROSSO recommended min is 1.0 kHz; the
  horn's own rolloff below ~450 Hz adds protection).
- Into 8 Ω: **C = 12 µF** (series, film/MKP 250 V) and **L = 1.5 mH**
  (shunt, air core, ≥0.7 mm wire). fc = 1/(2π√(LC)) = 1.19 kHz, Q ≈ 0.72. ✓
- **L-pad −12 dB** (ROSSO 108 → woofer 96.2 dB): series **6.2 Ω**, shunt
  **2.7 Ω** (10 W wirewound each; gives −12.2 dB into ~8.2 Ω). Keeps ~8 Ω
  load and damps horn impedance peaks. Alternates: −10.5 dB = 5.6 Ω/3.3 Ω;
  −13.5 dB = 6.8 Ω/2.2 Ω. Final trim by ear / REW after measuring actual
  sensitivity on *this* horn (spec sensitivity is on SB's H280 horn, ±~2 dB
  on ours).
- System impedance minimum ≈ 4.4 Ω near crossover (woofer ~9.6 Ω at 1.5 kHz
  in parallel with padded network) — safe for any 4 Ω-rated amp channel.
- DSP does the rest: 40 Hz HP, low-shelf, baffle-step/room EQ, and any
  top-octave lift (above ~5 kHz global EQ only affects the horn anyway).

## 6. References

- SB Audience ROSSO-65CD-T spec + dimension sheets (sbaudience.com)
- Peerless FSL-1225R02-08 T/S set (loudspeakerdatabase.com; Tymphany product page)
- Celestion TF1225 / CDX14-3050 / FTR12-3070C datasheets (rev-1 design, for reference)
- Small, R. "Vented-Box Loudspeaker Systems" JAES 1973 (transfer function)
- Klipsch × OJAS kO-R2 product page (reference: 760 Hz crossover, 97 dB)
- OJAS 2-way DIY kit (FaitalPRO 15PR400 + HF10AK, long tractrix)
