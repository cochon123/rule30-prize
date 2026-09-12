# Cycle JY: covering center packed 4-tuples take all 16 values

\(G(n,n)=1\). Covering packed centers hit every 16-row on both
\(w=0\) isolated centers and \(w=1\) run-3 middles; AND fires all
four `AND_ONES`. Center packed is **not** always \(\mathrm{green4}\).
Center packed is **not** always cob-shaped. Center AND does **not**
vanish. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: covering-center packed 4-tuples still fire AND on
every `AND_ONES` pattern (the Cycle HW fold's center term still
reads the packed row), so covering never-fail stays open.

Certify: `python3 research/cycle_jy.py --certify` (~0.10s).
Dump: `research/cycle_jy.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HJ/HT/HU/IF/IR/JX (\(n<64\); covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (center \(\mathrm{green4}\) is \(w\); isolated iff \(w=0\))

For \(n<64\), \(\mathrm{green4}(n,n)=\mathrm{center\_green4}(n)\)
and the center is isolated iff \(w=v_2(n+1)\bmod 2\) is \(0\).
Census \(64\): isolated \(43\) (seed \(1\)), run-3 middles \(21\).

## Lemma (covering centers hit all 16 rows)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): centers \(762\);
isolated \(508\) and middles \(254\) each hit all \(16\) even-\(s\)
4-tuples; \(0000\) is \(50\); packed equals \(\mathrm{green4}\) on
\(32\). Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Lemma (center AND fires all four `AND_ONES`)

Center AND \(232\): \(0010\) \(85\), \(0011\) \(53\), \(0100\)
\(68\), \(1001\) \(26\).

## Killed

Center packed always equals \(\mathrm{green4}\): at \(k=0\),
\(s=3\), \(n=1\), \(j=1\), packed \(1001\) vs \(\mathrm{green4}\)
\(1010\), \(p=4\). Center packed is always cob-shaped: the same
witness is not cob-shaped. Center AND vanishes: the same witness is
in `AND_ONES`.

## Verdict

`LEMMA` (center \(\mathrm{green4}\) is \(w\); covering centers hit
all \(16\) rows; center AND fires all four `AND_ONES`).
`KILLED` (center packed always equals \(\mathrm{green4}\); center
packed is always cob-shaped; center AND vanishes).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_jy.md` (this note)
- `research/cycle_jy.py`
- `research/cycle_jy.json`
