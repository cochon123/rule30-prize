# Cycle KG: packed vs \(\mathrm{green4}\) on \(G=1\) fills all 64 cells

Covering \(G=1\) packed 4-tuples take all 16 values on each of the
four \(\mathrm{g1\_green4}\) shapes. Packed is **not** always
\(\mathrm{green4}\). Packed is **not** a function of
\(\mathrm{green4}\). Cob packed is **not** only on \(0111\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: there is no pointwise Green constraint on the
packed 4-tuple, so covering never-fail stays open.

Certify: `python3 research/cycle_kg.py --certify`.
Dump: `research/cycle_kg.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HJ/HT/HU/IG/IR/KB/KF (\(n<64\); covering \(k\le 6\);
no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (\(G=1\) \(\mathrm{green4}\) has four shapes)

For \(n<64\), every \(G=1\) column has
\(\mathrm{green4}=\mathrm{g1\_green4}\) in
\(\{0110,0111,1010,1011\}\). Isolated ones are exactly \(0111\)
(\(461\), including seed). (Cycle KB.)

## Lemma (covering packed vs \(\mathrm{green4}\) fills all 64)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): \(G=1\) columns
\(22659\), split \(0111\) \(7785\), \(1011\) \(6297\), \(0110\)
\(6197\), \(1010\) \(2380\). Each shape takes all \(16\) packed
4-tuples (\(64\) cells). Cob packed \(13628\), on all four shapes.
Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Packed always equals \(\mathrm{green4}\): at \(k=0\), \(s=7\),
\(n=1\), \(j=1\), packed \(0000\) vs \(\mathrm{green4}\) \(1010\),
\(p=8\). Packed is a function of \(\mathrm{green4}\): isolated
\(\mathrm{green4}\) \(0111\) takes packed \(0010\) at \(k=2\),
\(s=39\), \(n=0\), \(j=0\), \(p=40\) and packed \(0100\) at \(k=1\),
\(s=5\), \(n=3\), \(j=3\), \(p=6\). Cob packed only on \(0111\): the
\(0000\) vs \(1010\) witness is cob-shaped.

## Verdict

`LEMMA` (\(G=1\) \(\mathrm{green4}\) has four shapes; covering packed
vs \(\mathrm{green4}\) fills all \(64\)).
`KILLED` (packed always equals \(\mathrm{green4}\); packed is a
function of \(\mathrm{green4}\); cob packed only on \(0111\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_kg.md` (this note)
- `research/cycle_kg.py`
- `research/cycle_kg.json`
