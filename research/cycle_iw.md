# Cycle IW: center \(G=1\) slot is \(v_2\) of the odd core

For \(n>0\), the center is `(m,1,1)` iff \(v_2(\mathrm{odd\_core}(n)+1)\)
is odd, else `(m-1,3,3)` with \(m=\mathrm{core}//2\). \(n=0\) stays
**seed**. Even-\(n\) type is **not** \(v_2(n+1)\). Center `(1,1)` is
**not** always \(w=1\). The center is **not** never `(3,3)`. Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: the center-slot formula still leaves packed AND
on both types (and the seed), so covering never-fail stays open.

Helper: `center_core_slot`. Certify:
`python3 research/cycle_iw.py --certify` (~0.11s).
Dump: `research/cycle_iw.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IT/IV (\(n<64\); covering \(k\le 6\); no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (center slot is `center_core_slot`)

For \(0\le n<64\), `g1_core_slot(n,n)==center_core_slot(n)`. Census
\(64\): seed \(1\), type `(1,1)` \(42\), type `(3,3)` \(21\). Never
run-2.

## Lemma (odd-\(n\) center is \(v_2(n+1)\bmod 2\))

On odd \(n\), the core is \(n\), so `(1,1)` iff \(v_2(n+1)\) is odd
and `(3,3)` iff it is even. Algebra odd \(n<64\): `(1,1)` \(21\),
`(3,3)` \(11\).

## Lemma (covering center slots)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): in-support centers
\(762\) split as seed \(14\), `(1,1)` \(501\), `(3,3)` \(247\), AND
\(232\). Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Even-\(n\) type is \(v_2(n+1)\): at \(k=1\), \(s=7\), \(n=2\), slot
`(0,1,1)`, naive `(0,3,3)`, \(w=0\), \(p=8\). Center `(1,1)` always
has \(w=1\): same witness, \(w=0\). Center is never `(3,3)`: at
\(k=1\), \(s=5\), \(n=3\), slot `(0,3,3)`, \(p=6\).

## Verdict

`LEMMA` (center slot is `center_core_slot`; odd-\(n\) center is
\(v_2(n+1)\bmod 2\); covering center slots).
`KILLED` (even-\(n\) type is \(v_2(n+1)\); center `(1,1)` always has
\(w=1\); center is never `(3,3)`).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_iw.md` (this note)
- `research/cycle_iw.py`
- `research/cycle_iw.json`
