# Cycle IE: mixed Hamming-1 AND xor is a slot formula

Flip \(z\): XOR is \(a\oplus(b\lor c)\). Flip \(a\): cob-bit
\((z\oplus b)\) equals \((b\lor c)\). Flip \(b\):
\(a\oplus((a=z)\lor c)\). `mix_and_xor` stitches Hamming 1–4 so
every mixed pair is determined. Mixed Hamming-1 XOR is **not**
always 1. It is **not** the left AND factor. It is **not** NOT
copy(\(j\)). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\)
for all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: the mixed XOR formula is still not AND along
Green ones, and the center AND remains, so covering never-fail stays
open.

Helper: `mix_ham1_and_xor`, `mix_and_xor`. Certify:
`python3 research/cycle_ie.py --certify` (~0.12s).
Dump: `research/cycle_ie.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HT/HU/HY/ID (16-row table; covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (mixed Hamming-1 AND xor slot formula)

On the three mixed Hamming-1 slots, AND xor is \(a\oplus(b\lor c)\)
for \((z)\), \((z\oplus b)=(b\lor c)\) for \((a)\), and
\(a\oplus((a=z)\lor c)\) for \((b)\). 16-row: \(48\) ordered mixed
Hamming-1 pairs.

## Lemma (mixed AND xor from Hamming slots)

`mix_and_xor` stitches Hamming 1 (cob-free) with Hamming 2–4
(cob-bit of the left 4-tuple). 16\(\times\)16: all \(128\) mixed
ordered pairs match `and_clause` xor.

## Lemma (covering mixed XOR equals `mix_and_xor`)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): mixed \(4383\), XOR
\(2216\), Hamming 1 \(1666\) of which XOR \(846\). Odd-\(s\) \(J\)
XOR matches Cycles HF/HG.

## Killed

Mixed Hamming-1 XOR always 1: at \(k=2\), \(s=23\), \(n=8\),
\(j=0\) vs \(16\), fours \(1000\) vs \(0000\), XOR \(0\). Mixed
Hamming-1 XOR equals left \(a\oplus(b\lor c)\): at \(k=2\),
\(s=9\), \(n=15\), \(j=13\) vs \(17\), fours \(0000\) vs \(0100\),
XOR \(1\) vs factor \(0\). Mixed Hamming-1 XOR equals NOT
copy(\(j\)): at \(k=1\), \(s=13\), \(n=3\), \(j=1\) vs \(5\), fours
\(0011\) vs \(0111\), XOR \(1\) vs NOT copy \(0\).

## Verdict

`LEMMA` (mixed Hamming-1 AND xor slot formula; mixed AND xor from
Hamming slots; covering mix XOR equals `mix_and_xor`).
`KILLED` (mixed Hamming-1 xor always 1; equals left AND factor;
equals NOT copy(\(j\))).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ie.md` (this note)
- `research/cycle_ie.py`
- `research/cycle_ie.json`
