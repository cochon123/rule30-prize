# Cycle IC: both-non-cob AND xor is determined by Hamming slots

Hamming 3 AND xor is copy(\(j\)) on slots \((z,a,c)\),
\(\lnot(\mathrm{copy}\oplus\mathrm{cob})\) on \((z,b,c)\), and
copy\(\oplus\)cob on \((a,b,c)\). Together with Cycles IA/IB that
gives every both-non-cob pair. Hamming-3 XOR is **not** the Hamming-2
zab formula. It is **not** copy(\(j\)). Hamming-3 dual is **not**
reverse. Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for
all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: the both-non-cob XOR formula is still not AND along
Green ones, and the center AND plus mixed slice remain, so covering
never-fail stays open.

Helper: `ham3_and_xor`, `bn_and_xor`. Certify:
`python3 research/cycle_ic.py --certify` (~0.11s).
Dump: `research/cycle_ic.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HT/HU/HX/HY/IB (16-row table; covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (Hamming-3 AND xor slot formula)

On the three Hamming-3 non-cob slot triples, AND xor is \(b\) for
\((0,1,3)\), \(\lnot(b\oplus c)\) for \((0,2,3)\), and \(b\oplus c\)
for \((1,2,3)\). 16-row: \(24\) ordered Hamming-3 non-cob pairs.

## Lemma (both-non-cob AND xor from Hamming slots)

`bn_and_xor` stitches Hamming 0 (identically \(0\)), Hamming 1
(\(\lnot b\)), Hamming 2 (Cycle IB), and Hamming 3. 16\(\times\)16:
all \(64\) both-non-cob ordered pairs match `and_clause` xor.

## Lemma (covering both-non-cob XOR equals `bn_and_xor`)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): both-non-cob
\(2123\), XOR \(1030\), Hamming 3 \(795\) of which XOR \(372\).
Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Hamming-3 XOR equals the Hamming-2 zab formula: at \(k=3\), \(s=31\),
\(n=8\), \(j=0\) vs \(16\), fours \(0010\) vs \(1001\), Hamming-2
pred \(1\) vs XOR \(0\). Hamming-3 XOR equals copy(\(j\)): at
\(k=1\), \(s=17\), \(n=1\), \(j=0\) vs \(2\), fours \(0100\) vs
\(1111\), copy \(0\) vs XOR \(1\). Hamming-3 dual equals reverse:
same \(0100\) vs \(1111\), reverse of \(0100\) is \(0010\).

## Verdict

`LEMMA` (Hamming-3 AND xor slot formula; both-non-cob AND xor from
Hamming slots; covering bn XOR equals `bn_and_xor`).
`KILLED` (Hamming-3 equals Hamming-2 zab; Hamming-3 xor equals
copy(\(j\)); Hamming-3 equals reverse).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ic.md` (this note)
- `research/cycle_ic.py`
- `research/cycle_ic.json`
