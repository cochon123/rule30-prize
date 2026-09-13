# Cycle NW: on \(q=10\) through \(k\le 10\), palindrome-right \(d\bmod 3=0\) \(G(j-1)\) is \(1\) iff \(k\bmod 4\in\{1,2\}\)

On covering \(J_{10}\) through \(k\le 10\), XOR of \(G(n,j-1)\) over
covering \(G=1\) cells with \(j>n\) and \((j-n)\bmod 3=0\)
(\(p=T-2j\ge 0\); no packed row) is \(1\) iff \(k\bmod 4\in\{1,2\}\).
Lift of Cycle MR (\(k\le 8\), both covering \(q\)). Prefix MR
\(q=10\) for \(k\le 8\); walk \(k=9\) and \(k=10\). On \(q=10\) this
xor equals Cycle NU's d31 \(G(j+1)\) (same want; different
cells). Companion Green d31 still equals Cycle NV. This is
**not** a death at \(k=9\), **not** a death at \(k=10\), **not**
rest (\(k=1\): \(1\) vs \(0\)), **not** NV Green d31 (\(k=9\):
\(1\) vs \(0\)), **not** NU as the same cells (\(k=9\):
\(n_{d30}=52103\) vs \(n_{d31}=50742\)), **not** MQ on \(q=6\)
(\(k=1\): d30 \(=1\), jp1 \(=0\)), **not** identically \(0\),
**not** empty (\(k=9\): \(n_{d30}=52103\)), and **not** the form
for all \(k\). Do **not** claim \(T\) is \(1\) iff \(k=2\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim Green-only rest for all \(k\). Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_nw.py --certify`.
Dump: `research/cycle_nw.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/MR/NV/NU/MQ/MM/MJ (packed-free covering \(q=10\); prefix MR
d30 \(G(j-1)\) for \(k\le 8\); walk \(k=9,10\); no Fermat table,
no extra window, no \(n_0=16\) window).

## Lemma (palindrome-right \(d\bmod 3=0\) \(G(j-1)\) is \(1\) iff \(k\bmod 4\in\{1,2\}\) through \(k\le 10\))

Covering \(q=10\), \(k\le 10\). The walk does not read the packed
row. Same cells as Cycle MR's \(q=10\) slice. At \(k=1\),
\(n_{d30}=3\) and xor \(=1\). At \(k=9\), \(n_{d30}=52103\) and
xor \(=1\). On \(q=10\) the xor equals Cycle NU (same
\(1_{k\bmod 4\in\{1,2\}}\)). Companion d31 \(G(j-1)\) is \(1\) iff
\(k\bmod 4=0\).

## Killed

Dies at \(k=9\): xor \(=1=\) want. Dies at \(k=10\): xor \(=1=\)
want. Equals rest: \(k=1\) is \(1\) vs \(0\). Equals NV Green
d31: \(k=9\) is \(1\) vs \(0\). Equals NU as the same cells:
\(k=9\) has \(n_{d30}\ne n_{d31}\). Equals MQ on \(q=6\): \(k=1\)
d30 \(=1\) and MQ jp1 \(=0\). Vanishes: \(k=9\) is \(1\). Empty:
\(k=9\) has \(n_{d30}=52103\). The form for all \(k\).

## Verdict

`LEMMA` (palindrome-right \(d\bmod 3=0\) xor of \(G(j-1)\) is \(1\)
iff \(k\bmod 4\in\{1,2\}\) on \(q=10\) for \(k\le 10\); that form
holds on both covering \(q\) for \(k\le 8\); palindrome-right
\(d\bmod 3=1\) xor of \(G(j+1)\) is that form on \(q=10\) for
\(k\le 10\); Green d31 \(G(j-1)\) is \(1\) iff \(k\bmod 4=0\) on
\(q=10\) for \(k\le 10\); rest10 census on \(k\le 10\); \(J\)
closed form on \(k\le 6\)).
`KILLED` (dies at \(k=9\); dies at \(k=10\); equals rest; equals
NV Green d31; equals NU as the same cells; equals MQ on \(q=6\);
vanishes; empty; the form for all \(k\); unique-rest xor equals
\(J\); leftover equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_nw.md` (this note)
- `research/cycle_nw.py`
- `research/cycle_nw.json`
