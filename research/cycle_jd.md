# Cycle JD: isolated Green ones lift from the four `LIFT1` 5-windows

The 5-windows that trinomial-lift to \(010\) are
`LIFT1` \(=\{11000,01110,10101,00011\}\). Five of \(16\) parity
cases are freshman-sat; only \(10101\) is sat on even \(n\). Every
isolated one with \(n>0\) lifts from `LIFT1`. Odd-\(n\) isolated
ones all lift from \(10101\). Odd iso is **not** from \(01110\).
Even iso is **not** all \(10101\). Seed \(n=0\) has **no** parent
window. Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for
all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: isolated-one parent windows still leave packed
AND on those columns (and on pairs), so covering never-fail stays
open.

Helper: `LIFT1`, `trinomial3`, `iso1_lift5`, `lift1_extend_sat`.
Certify:
`python3 research/cycle_jd.py --certify`.
Dump: `research/cycle_jd.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IL/IM/IR (\(n<64\); covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (`LIFT1` has five freshman-sat cases)

Exactly four 5-windows map to \(010\). Of \(16\) `LIFT1` \(\times\)
parity cases, five are freshman-sat: \(11000/01110/00011\) on odd
\(n\), odd \(j\), and \(10101\) on even \(n\), even \(j\) and on
odd \(n\), odd \(j\).

## Lemma (every isolated one with \(n>0\) lifts from `LIFT1`)

For \(n<64\), isolated ones \(461\): seed \(1\), odd \(45\) all
\(10101\), even \(415\) split \(01110\) \(141\), \(00011\) \(115\),
\(11000\) \(115\), \(10101\) \(44\). Completes the lift dictionary
with Cycles IK/IM/JA (`LIFT4`/`LIFT3`/`LIFT2`).

## Lemma (covering isolated-one `LIFT1`)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): isolated ones
\(7785\) (seed \(14\), odd \(741\) all \(10101\), even \(7030\)).
Window census \(01110\) \(2373\), \(00011\) \(2011\), \(11000\)
\(1912\), \(10101\) \(1475\). Odd-\(s\) \(J\) XOR matches Cycles
HF/HG.

## Killed

Odd iso from \(01110\): at \(k=0\), \(s=3\), \(n=3\), \(j=3\),
parent \(10101\), \(p=4\). Even iso all from \(10101\): at \(k=0\),
\(s=5\), \(n=2\), \(j=0\), parent \(00011\), \(p=10\). Seed is a
`LIFT1` window: at \(k=0\), \(s=5\), \(n=0\), \(j=0\), no parent,
\(p=6\).

## Verdict

`LEMMA` (`LIFT1` has five freshman-sat cases; every isolated one
with \(n>0\) lifts from `LIFT1`; covering isolated-one `LIFT1`).
`KILLED` (odd iso from \(01110\); even iso all from \(10101\);
seed is a `LIFT1` window).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_jd.md` (this note)
- `research/cycle_jd.py`
- `research/cycle_jd.json`
