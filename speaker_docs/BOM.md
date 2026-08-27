# Bill of Materials — MP-H1 (OJAS-Style 2-Way, pair)

Prices checked July 2026; confirm stock at order time — small-run pro-audio
stock moves fast.

## Drivers — Wagner Online (rev 2, July 2026)

Both confirmed listed at [Wagner Online](https://www.wagneronline.com.au)
(Sydney; AU distributor for SB Audience / Peerless / Dayton). Wagner's site
blocks price scraping — check the product page or call (02) 9798 9233 for
current pricing; estimates below are from US street prices + typical AU markup.

| Qty | Item | Source | Est. AUD | Stock (checked) |
|---|---|---|---|---|
| 2 | Peerless by Tymphany FSL-1225R02-08 12" pro woofer, 8 Ω | [Wagner product page](https://www.wagneronline.com.au/product/peerless-by-tymphany-12-woofer-driver-994241?sku=fsl-1225) | ~$150–190 ea (US$74 at DigiKey) | Listed; Parts-Express has it on clearance — if Wagner is out, order 2 spares-worth while it lasts |
| 2 | SB Audience ROSSO-65CD-T 1.4" compression driver, 8 Ω | [Wagner product page](https://www.wagneronline.com.au/product/sb-audience-1-4-compression-driver-1005231?sku=rosso-65cd-t) | ~$260–320 ea (US$156 at Madisound) | **In stock** per Wagner listing |

Driver subtotal ≈ **$850–1,000** — back inside the original budget tier.

**Superseded (rev 1):** Celestion TF1225 + CDX14-3050 — TF1225 out of stock
at every AU stockist checked; CDX14-3050 $499 ea at the single stockist
(Crossfader). The Celestion pair remains a valid drop-in if stock returns:
same cabinet, same horn flange; use the rev-1 L-pad values in git history.

## Crossover (per speaker: C + L + 2 resistors)

| Qty | Item | Notes | Est. AUD |
|---|---|---|---|
| 2 | 12 µF MKP film capacitor, ≥400 V | **as built: PB-MKP-FC 12 µF 400 V**. Jantzen Cross-Cap / Dayton PMPC also fine (≥250 V); 10 µF + 2.2 µF parallel works too | ~$15 ea |
| 2 | 1.5 mH air-core inductor, ≥0.9 mm (20 AWG) wire | Jantzen air core; DCR ≤0.6 Ω | ~$25 ea |
| 2 | 6.8 Ω 10 W wirewound resistor | **L-pad series, as built** (6.8 Ω = −12.8 dB; 6.2 Ω nominal was −12.2 dB). Buy 5.6 Ω and 8.2 Ω too for ±1.5 dB trim (cheap) — see below | ~$4 ea |
| 2 | 2.7 Ω 5 W wirewound resistor | **L-pad shunt, as built** (5 W is fine — the shunt leg dissipates ~¼ of the series leg; 3.3 Ω / 2.2 Ω alternates) | ~$3 ea |

Mount parts on a small ply board on the cabinet floor. Subtotal ≈ **$100**

## Timber & cabinet hardware

| Qty | Item | Notes | Est. AUD |
|---|---|---|---|
| 2 sheets | 18 mm Baltic birch plywood, 2400×1200 | ~1.3 sheets needed; spare covers mistakes. AA/BB grade for exposed edges | ~$140 ea |
| 1 | Solid timber for feet, ~90×90 mm section, 1.6 m (e.g. Vic ash / oak) | 4 blocks per photo style | ~$60 |
| 8 | Binding posts (4 per speaker) | rear pair = amp input, top pair = external-horn feed through the lid (bed in sealant) | ~$4 ea |
| 4 | Wago 221 lever-nuts | join the negative rail (amp / woofer / crossover-in) — 2 per speaker | ~$2 ea |
| 8 | M6 T-nuts + M6×35 hex bolts (woofer) | 4 per woofer | ~$15 |
| 8 | M6×25 bolts + washers (CD to horn flange) | 4 per driver | ~$8 |
| 2 m² | Polyester/wool acoustic wadding | line rear + side walls | ~$25 |
| — | Foam gasket tape, wood glue, screws | | ~$25 |
| 4 m | Internal cable 1.5 mm² + spade terminals for CD | | ~$15 |

Subtotal ≈ **$440**

## Horn & finish

| Qty | Item | Notes | Est. AUD |
|---|---|---|---|
| ~5 kg | PETG or PLA+ filament | ~2–2.5 kg per horn incl. supports/stand; PETG preferred (sanding + heat resistance) | ~$150 |
| 2 | M5 × 30 bolt + nyloc nut (stand clamp) + 8 × 4 mm wood screws (stand base) | stand is fully printed | ~$8 |
| — | 4 mm rod or filament offcuts for horn joint pins (16 × 20 mm pins) | | ~$0 |
| — | Body filler / spot putty, sandpaper 120–600 | seam finishing | ~$40 |
| — | High-build primer + white satin/gloss acrylic spray | the seamless white look | ~$50 |

Subtotal ≈ **$255**

## Measurement (if not already owned)

| Qty | Item | Notes | Est. AUD |
|---|---|---|---|
| 1 | miniDSP UMIK-1 USB measurement mic | for REW; used for DSP tuning | ~$150 |

## Total ≈ **$1,650–1,850** for the pair (excl. mic)

Rev-2 drivers (~$850–1,000 via Wagner) bring the build back inside the
original ~$800–1000 driver tier. Wagner also stocks the crossover parts
(Jantzen/Dayton caps & coils, resistors) and speaker terminals — most of
this BOM can ship in one box; plywood and timber are the only local buys.
