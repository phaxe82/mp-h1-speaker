# Build Guide — OJAS-Style 2-Way

Read `design-notes.md` first for the why; this is the how. Dimensioned
drawings and cut list live in `cad/`.

## 1. Cabinet (per speaker) — 18 mm Baltic birch

External 456 W × 536 H × 366 D mm. Butt joints, glued and screwed (screws
hidden on bottom/back or plugged); the photo look leaves ply edges exposed
on the sides, with the front baffle set flush between them.

### Cut list (per cabinet, 18 mm ply)
| Panel | Size (mm) | Qty | Notes |
|---|---|---|---|
| Sides | 536 × 366 | 2 | edges exposed front + top |
| Top / Bottom | 420 × 366 | 2 | fit between sides |
| Back | 420 × 500 | 1 | fits between sides, top, bottom |
| Front baffle | 420 × 472 | 1 | stops 28 mm above the bottom panel → the port slot |
| Port shelf | 420 × 132 | 1 | butts against baffle rear, 28 mm above bottom; with the baffle it forms the 150 mm duct |
| Window brace | 420 × 330 (cut ~60% out) | 1 | mid-height, ties sides/back |
| Crossover board | ~150 × 200 | 1 | screwed to floor after wiring |

*(Exact sizes and the woofer cutout position come from the CAD drawings —
`cad/` is authoritative if anything differs.)*

### Assembly order
1. Cut all panels; cut the woofer hole (nominal Ø285 mm for the FSL-1225 —
   **verify against the delivered driver**) in the baffle with a router
   trammel. Woofer centre is on the vertical centreline, 300 mm up from the
   baffle's bottom edge (i.e. above mid-height, per the photo).
2. Mark the woofer mounting holes from the driver frame itself and fit M6
   T-nuts from the rear.
3. Glue the port shelf between the sides, 28 mm above the bottom panel
   (rest it on temporary 28 mm spacer offcuts during glue-up) — the duct is
   open at the front (the slot) and opens into the box at the back, 150 mm
   deep in total (18 mm baffle + 132 mm shelf), full 420 mm width.
4. Box glue-up: bottom + sides + top around the back panel, then the window
   brace at mid-height (glued to sides and back, clear of the woofer magnet
   by ≥20 mm — check interference drawing).
5. Fit the baffle flush. Seal every internal seam with a glue fillet.
6. Binding posts: back pair low on the back (amp input), top pair through the
   top panel (horn feed) — bed both top posts in sealant. Wire to the crossover
   board before mounting drivers.
7. Wadding on back and side walls (not in the port path, not stuffed).
8. Crossover board on the floor; woofer wired direct off the back posts, CD
   high-pass/L-pad output run up to the sealed top posts (see §3).
9. Gasket tape on the woofer frame; bolt in the woofer.
10. Feet: two solid blocks ~90 × 90 × 366 mm under the cabinet, set in from
    the sides as in the photo (glued dowels or screwed from inside).

### Finish
Sand to 180, exposed ply left natural (hardwax oil or matte poly). Baffle
painted light warm grey (as in the photo) before final assembly if you want
the crisp two-tone look.

## 2. Horn — 3D print (per speaker)

Parts (STLs in `cad/`): 1 neck (with CDX14 flange), 4 bell quadrants,
driver stand parts.

**Print settings:** PETG, 0.2 mm layers, 6 mm walls printed as ~8 perimeters
or 30%+ gyroid with 3 mm shells — the horn must be *dead* (knuckle-rap test:
a dull thock, not a ring). Neck prints vertically, flange down, no supports
except under the flange bolt bosses. Quadrants print bell-face up with
tree supports on the outer flare.

**Assembly:**
1. Bolt-check the neck flange against the ROSSO-65CD-T (4 × M6 on Ø102 PCD)
   before gluing anything.
2. Glue quadrants to each other and to the neck with 2-part epoxy. The
   neck↔bell joint face has 8 × Ø4 × 10 mm deep pin sockets (at 30°, 75°,
   120° … 345°) — cut 20 mm pins from 4 mm rod/filament to register the
   parts. Dry-fit the whole bell first, then epoxy, pin, and tape/strap
   until cured. Run an epoxy fillet around the outside of every seam
   (it disappears under filler).
3. Fill seams (spot putty), sand 120 → 400, high-build primer, sand 600,
   white satin/gloss topcoats. Inside of the bell matters visually;
   inside of the *neck* matters acoustically — keep it smooth.
4. Mount the CD to the neck flange with a thin gasket (supplied with driver
   or cut from 1 mm foam).

**Stand:** the CD + horn (~5 kg total: ~1.3 kg print + 3.76 kg ROSSO driver)
hangs from the printed stand (`cad/driver_stand.stl`): a Ø157 mm clamp ring
that grips the driver body, closed with an M5 × 30 bolt + nyloc across the
top slot, on a 50 × 50 column and 110 × 110 × 10 base screwed to the cabinet
top with 4 × 4 mm wood screws. Ring centre is 188 mm above the cabinet top,
which floats the bell ~20 mm clear of the lid as in the photo. Print it
lying on its side (177 × 110 × 277 mm — fits a 235 mm bed on the diagonal),
50%+ infill and 6 perimeters — it carries 5 kg, it's structural.

## 3. Electrical

**Terminals: 4 binding posts per speaker** (not a terminal cup). The horn is
external on top, so its feed exits the box:
- **Back pair** = amp input.
- **Top pair** = the CD high-pass + L-pad *output*, up through the top panel
  to the horn via twisted flex. Bed both top posts in sealant (they pierce
  the ported box near ear height).

Signal path (one amp channel):
```
Amp ──► BACK posts ──┬──► Woofer            (direct, no parts)
                     │
                     └──► 12µF series ──●A──► 6.8Ω series ──●B──► TOP posts ──► Horn
                                        │                  │
                                     1.5mH              2.7Ω
                                        │                  │
          negative rail ───────────────┴──────────────────┴─── (all shunt returns + horn − + amp − + woofer −)
```
- **Woofer taps directly off the back posts**, in parallel with the crossover
  input — it must not run through any crossover part.
- Join the negative rail with **two Wago 221 lever-nuts** (one for +, one for
  −): amp / woofer / crossover-in all land together. Anchor the Wagos so they
  don't rattle.
- **L-pad is as-built 6.8 Ω series / 2.7 Ω shunt** (≈ −12.8 dB; nominal spec
  was 6.2 Ω / 2.7 Ω = −12.2 dB — the horn lands ~0.6 dB quieter, recovered in
  DSP). Leave the L-pad resistor leads long / on a Wago so they're swappable —
  you re-trim by ear/REW once you measure *this* horn (see below).
- **Polarity: start with the CD inverted** (common for a 2nd-order HP at these
  spacings); confirm by measuring the crossover null/sum in REW. Mark the top
  posts' +/− clearly so you can flip deliberately.

> **Field note (Sep 2026): the shared negative rail is a single point of
> failure — keep it reachable through the woofer cutout.** After repainting a
> baffle, both drivers went dead. The horn's own terminal measured fine, but
> nothing reached it: a spade had lifted off the **negative-rail Wago**. Because
> the woofer taps the back posts directly *and* horn−/woofer−/amp− all land on
> that one Wago, a single loose negative kills the woofer **and** the horn at
> once — the symptom looks like a dead amp input, not a crossover fault. Fix was
> a 5-minute re-terminate (confirm back −post → woofer − and back −post → horn −
> both ≈ 0 Ω). **Lesson: the woofer is the service hatch — site the ± Wagos
> within reach of the Ø285 cutout so you never pull the (glued) baffle.**
> Removing the baffle to reach the terminal destroyed it and forced a remake
> (420 × 472, woofer front-mounted, M6 T-nuts pressed into the **rear** face
> before glue-up).

### L-pad trim (do this during voicing, not the build)
Full procedure is `dsp-tuning-guide.md` step 3 (level-match). In short:
1. Measure horn-band vs woofer-band level at 1 m (pink noise, 2–8 kHz vs
   200–800 Hz).
2. If the horn is **>±1.5 dB** off, change the **series** resistor rather than
   burning DSP headroom: **larger = quieter horn** (6.8 → 8.2 Ω), **smaller =
   louder** (6.8 → 6.2 → 5.6 Ω). Leave the 2.7 Ω shunt unless you need a big
   swing.
3. Re-confirm polarity/sum after any resistor change, then hand the last dB
   to DSP.

Then follow `dsp-tuning-guide.md`.
