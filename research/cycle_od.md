# Cycle OD: on \(q=10\), NH's \(S\) on \(2U\le n<3U\) dies at \(k=9\)

On covering \(J_{10}\), Cycle NH's XOR of \(G(n,j+1)\) over
palindrome-right cells with \((j-n)\bmod 3=1\), \(G(n,j-1)=0\), and
\(2U\le n<3U\) (\(p=T-2j\ge 0\); no packed row) is \(1\) iff
\(k\bmod 3=2\) for \(k\le 8\), but at \(k=9\) xor \(=1\) while
want \(=0\). It also dies at \(k=10\) (xor \(=1\), want \(=0\)).
Prefix NH \(q=10\) for \(k\le 8\); walk \(k=9\) and \(k=10\).
Companion NY high \(S\), OA \(n<U\), and NZ mid still hold at
those \(k\). This is **not** empty (\(k=9\): \(n_{23}=11387\)),
**not** pointwise \(0\) (\(k=9\): \(n_{23g}=4563\)), **not** NY
high \(S\) (\(k=9\): \(1\) vs \(0\)), **not** OA \(n<U\) (\(k=9\):
\(1\) vs \(0\)), **not** rest (\(k=9\): \(1\) vs \(0\)), **not**
NA \(S\) (\(k=9\): \(1\) vs \(0\)), **not** the form through
\(k\le 10\), and **not** the form for all \(k\). Do **not** claim
\(T\) is \(1\) iff \(k=2\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim Green-only rest for all \(k\). Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_od.py --certify` (~8.57s).
Dump: `research/cycle_od.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/NH/NE/NC/OC/MJ (packed-free covering \(q=10\); prefix NH
\(2U\le n<3U\) for \(k\le 8\); walk \(k=9,10\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (\(S\) on \(2U\le n<3U\) dies at \(k=9\))

Covering \(q=10\). The walk does not read the packed row. Same
cells as Cycle NH. At \(k=8\), \(n_{23}=3216\) and xor \(=1=\)
want. At \(k=9\), \(n_{23}=11387\) and xor \(=1\neq 0=\) want,
with \(n_{23g}=4563\) fires. At \(k=10\), \(n_{23}=35196\) and xor
\(=1\neq 0=\) want. Companion high \(S\), \(n<U\), and mid vanish
still match Cycles NY, OA, and NZ.

## Killed

Holds at \(k=9\): xor \(=1\neq\) want. Holds at \(k=10\): xor
\(=1\neq\) want. The form through \(k\le 10\). Equals NY high
\(S\): \(k=9\) is \(1\) vs \(0\). Equals OA \(n<U\): \(k=9\) is
\(1\) vs \(0\). Equals NA \(S\): \(k=9\) is \(1\) vs \(0\). Equals
rest: \(k=9\) is \(1\) vs \(0\). Empty: \(k=9\) has
\(n_{23}=11387\). Pointwise \(0\): \(k=9\) has \(n_{23g}=4563\).
The form for all \(k\).

## Verdict

`LEMMA` (\(S\) on \(2U\le n<3U\) dies at \(k=9\) on \(q=10\); it
dies at \(k=10\); that form holds on \(q=10\) for \(k\le 8\);
inner \(T\) is \(1\) iff \(k>2\) and \(k\bmod 3=2\) on \(q=10\)
for \(k\le 10\); rest10 census on \(k\le 10\); \(J\) closed form
on \(k\le 6\)).
`KILLED` (holds at \(k=9\); holds at \(k=10\); the form through
\(k\le 10\); equals NY high \(S\); equals OA \(n<U\); equals NA
\(S\); equals rest; empty; pointwise \(0\); the form for all
\(k\); unique-rest xor equals \(J\); leftover equals rest on both
\(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_od.md` (this note)
- `research/cycle_od.py`
- `research/cycle_od.json`
