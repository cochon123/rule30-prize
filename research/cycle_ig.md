# Cycle IG: \(G=1\) AND is determined by Hamming slots vs \(\mathrm{green4}(n,j)\)

On \(G(n,j)=1\), \(\mathrm{green4}=(G(j+1),\lnot G(j+1),1,\lnot G(j-1))\).
Packed AND is \(G(j+1)\) on error slots \((z)\) and \((z,c)\);
\(\lnot G(j+1)\) on \((a)\) and \((a,c)\); \(G(j+1)\oplus G(j-1)\) on
\((b)\) and \((z,a,b,c)\); \(G(j+1)=G(j-1)\) on \((b,c)\) and
\((z,a,b)\); else \(0\). Cycle IF is the center case
\(G(j+1)=G(j-1)\). \(G=1\) AND is **not** \(G(j+1)\). It is **not**
\(G(j-1)\). It is **not** identically 1. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: the slot formula still reads the packed 4-tuple,
so covering never-fail stays open.

Helper: `g1_green4`, `g1_and_from_slots`. Certify:
`python3 research/cycle_ig.py --certify` (~0.14s).
Dump: `research/cycle_ig.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HJ/HU/IF (\(n<64\) plus 4\(\times\)16-row; covering
\(k\le 6\); no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (\(G=1\) \(\mathrm{green4}\) shape)

For \(n<64\) and \(G(n,j)=1\),
\(\mathrm{green4}(n,j)=(G(n,j+1),\lnot G(n,j+1),1,\lnot G(n,j-1))\).

## Lemma (\(G=1\) AND from \(\mathrm{green4}\) Hamming slots)

`g1_and_from_slots` on the four \(G=1\) Green 4-tuples matches
`and_clause` on all \(16\) packed 4-tuples (\(64\) rows).

## Lemma (covering \(G=1\) AND equals the slot formula)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): \(G=1\) columns
\(22659\), AND \(4522\). Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

\(G=1\) AND equals \(G(j+1)\): at \(k=0\), \(s=5\), \(n=0\), \(j=0\),
fours \(0100\) vs green \(0111\), AND \(1\) vs \(G(j+1)=0\). \(G=1\)
AND equals \(G(j-1)\): at \(k=0\), \(s=3\), \(n=1\), \(j=0\), fours
\(0100\) vs green \(1011\), AND \(1\) vs \(G(j-1)=0\). \(G=1\) AND
identically 1: at \(k=0\), \(s=3\), \(n=3\), \(j=0\), fours \(0000\)
vs green \(1011\), AND \(0\).

## Verdict

`LEMMA` (\(G=1\) \(\mathrm{green4}\) shape; \(G=1\) AND from
\(\mathrm{green4}\) Hamming slots; covering \(G=1\) AND equals the
slot formula).
`KILLED` (\(G=1\) AND equals \(G(j+1)\); equals \(G(j-1)\);
identically 1).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ig.md` (this note)
- `research/cycle_ig.py`
- `research/cycle_ig.json`
