# Cycle JW: isolated-one packed 4-tuples take all 16 values

On isolated ones \(\mathrm{green4}=0111\). Covering packed 4-tuples
hit every 16-row; AND fires all four `AND_ONES`. Isolated packed is
**not** always \(0000\). Isolated packed is **not** always cob-shaped.
Isolated AND does **not** vanish. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: isolated-one packed 4-tuples still fire AND on
every `AND_ONES` pattern (and on every iso3 class), so covering
never-fail stays open.

Certify: `python3 research/cycle_jw.py --certify` (~0.16s).
Dump: `research/cycle_jw.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HJ/HT/HU/IR/JV (\(n<64\); covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (isolated-one \(\mathrm{green4}\) is \(0111\))

For \(n<64\), every isolated one has
\(\mathrm{green4}(n,j)=0111\). Census \(n_{\mathrm{iso}}=461\)
(seed \(1\)).

## Lemma (covering isolated 4-tuples hit all 16 rows)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): isolated ones
\(7785\); all \(16\) even-\(s\) 4-tuples occur; \(0000\) is \(1892\);
packed equals \(\mathrm{green4}\) on \(356\). Odd-\(s\) \(J\) XOR
matches Cycles HF/HG.

## Lemma (isolated AND fires all four `AND_ONES`)

Isolated AND \(1489\): \(0010\) \(354\), \(0011\) \(343\), \(0100\)
\(385\), \(1001\) \(407\).

## Killed

Isolated packed is always \(0000\): at \(k=1\), \(s=5\), \(n=3\),
\(j=3\), packed \(0100\), \(p=6\). Isolated packed is always
cob-shaped: the same witness is not cob-shaped. Isolated AND
vanishes: the same witness is in `AND_ONES`.

## Verdict

`LEMMA` (isolated-one \(\mathrm{green4}\) is \(0111\); covering
isolated 4-tuples hit all \(16\) rows; isolated AND fires all four
`AND_ONES`).
`KILLED` (isolated packed is always \(0000\); isolated packed is
always cob-shaped; isolated AND vanishes).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_jw.md` (this note)
- `research/cycle_jw.py`
- `research/cycle_jw.json`
