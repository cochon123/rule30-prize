# Cycle IF: covering center AND is determined by Hamming slots vs \(\mathrm{green4}(n,n)\)

\(\mathrm{green4}(n,n)=(w,1-w,1,1-w)\) with \(w=v_2(n+1)\bmod 2\).
Packed center AND is \(1\) on error slots \((z,a,b)\) and \((b,c)\);
equals \(w\) on \((z)\) and \((z,c)\); equals \(1-w\) on \((a)\) and
\((a,c)\); else \(0\). Center AND is **not** \(w\). It is **not**
\(1-w\). Mixed-with-\(\mathrm{green4}\) is **not** always AND. Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: the slot formula still reads the packed 4-tuple,
so covering never-fail stays open.

Helper: `center_green4`, `center_and_from_slots`. Certify:
`python3 research/cycle_if.py --certify` (~0.09s).
Dump: `research/cycle_if.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HJ/HT/HU/IE (\(n<64\) plus 16-row; covering
\(k\le 6\); no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (\(\mathrm{green4}\) at the center is \(v_2\))

For \(n<64\), \(\mathrm{green4}(n,n)=(w,1-w,1,1-w)\) with
\(w=v_2(n+1)\bmod 2\), equal to \(G(n,n\pm 1)\). The two values are
cob \(0111\) (\(w=0\)) and cob \(1010\) (\(w=1\)).

## Lemma (center AND from \(\mathrm{green4}\) Hamming slots)

`center_and_from_slots` on those two Green 4-tuples matches
`and_clause` on all \(16\) packed 4-tuples.

## Lemma (covering center AND equals the slot formula)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): centers \(762\), AND
\(232\), packed\(=\mathrm{green4}\) on \(32\). Odd-\(s\) \(J\) XOR
matches Cycles HF/HG.

## Killed

Center AND equals \(w\): at \(k=0\), \(s=5\), \(n=0\), fours \(0100\)
vs green \(0111\), AND \(1\) vs \(w=0\). Center AND equals \(1-w\):
at \(k=0\), \(s=3\), \(n=1\), fours \(1001\) vs green \(1010\), AND
\(1\) vs \(1-w=0\). Mixed-with-\(\mathrm{green4}\) always AND: at
\(k=1\), \(s=15\), \(n=2\), fours \(1000\) vs \(0111\), Hamming 4,
AND \(0\).

## Verdict

`LEMMA` (\(\mathrm{green4}\) at the center is \(v_2\); center AND
from \(\mathrm{green4}\) Hamming slots; covering center AND equals
the slot formula).
`KILLED` (center AND equals \(w\); equals \(1-w\); mixed-with-green
always AND).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_if.md` (this note)
- `research/cycle_if.py`
- `research/cycle_if.json`
