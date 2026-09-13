# Cycle NV: on \(q=10\) through \(k\le 10\), palindrome-right \(d\bmod 3=1\) \(G(j-1)\) is \(1\) iff \(k\bmod 4=0\)

On covering \(J_{10}\) through \(k\le 10\), XOR of \(G(n,j-1)\) over
covering \(G=1\) cells with \(j>n\) and \((j-n)\bmod 3=1\)
(\(p=T-2j\ge 0\); no packed row) is \(1\) iff \(k\bmod 4=0\).
Lift of Cycle MM (\(k\le 8\)). Prefix MM \(q=10\) for \(k\le 8\);
walk \(k=9\) and \(k=10\). Dual of Cycle NU's
\(G(n,j+1)\) \(d31=1_{k\bmod 4\in\{1,2\}}\). Companion \(j>n\) xor
still equals Cycle MJ's even-\(k\) form. This is **not** a death
at \(k=9\), **not** a death at \(k=10\), **not** rest (\(k=0\):
\(1\) vs \(0\)), **not** NU d31 \(G(j+1)\) (\(k=9\): \(0\) vs
\(1\)), **not** NT inner vanish (\(k=0\): \(1\) vs \(0\)), **not**
the \(j>n\) even-\(k\) xor (\(k=2\): \(0\) vs \(1\)), **not**
identically \(0\), **not** empty (\(k=9\): \(n_{\mathrm{d31}}=50742\)),
**not** the form on \(q=6\), and **not** the form for all \(k\).
Do **not** claim \(T\) is \(1\) iff \(k=2\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim Green-only rest for all \(k\). Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_nv.py --certify`.
Dump: `research/cycle_nv.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/MM/NU/NT/MQ/MJ (packed-free covering \(q=10\); prefix MM
d31 \(G(j-1)\) for \(k\le 8\); walk \(k=9,10\); no Fermat table,
no extra window, no \(n_0=16\) window).

## Lemma (palindrome-right \(d\bmod 3=1\) \(G(j-1)\) is \(1\) iff \(k\bmod 4=0\) through \(k\le 10\))

Covering \(q=10\), \(k\le 10\). The walk does not read the packed
row. Same cells as Cycle MM. At \(k=0\), \(n_{\mathrm{d31}}=1\) and
xor \(=1\). At \(k=9\), \(n_{\mathrm{d31}}=50742\) and xor \(=0\).
Companion \(j>n\) xor of \(G(n,j-1)\) is \(1\) iff \(k\) even
(Cycle MJ form).

## Killed

Dies at \(k=9\): xor \(=0=\) want. Dies at \(k=10\): xor \(=0=\)
want. Equals rest: \(k=0\) is \(1\) vs \(0\). Equals NU d31
\(G(j+1)\): \(k=9\) is \(0\) vs \(1\). Equals NT inner vanish:
\(k=0\) is \(1\) vs \(0\). Equals \(j>n\) even-\(k\): \(k=2\) has
jgtn \(=1\) and d31 \(=0\). Vanishes: \(k=0\) is \(1\). Empty:
\(k=9\) has \(n_{\mathrm{d31}}=50742\). The form on \(q=6\):
\(k=1\), \(q=6\) d31 \(=1\). The form for all \(k\).

## Verdict

`LEMMA` (palindrome-right \(d\bmod 3=1\) xor of \(G(j-1)\) is \(1\)
iff \(k\bmod 4=0\) on \(q=10\) for \(k\le 10\); that form holds on
\(q=10\) for \(k\le 8\); palindrome-right \(d\bmod 3=1\) xor of
\(G(j+1)\) is \(1\) iff \(k\bmod 4\in\{1,2\}\) on \(q=10\) for
\(k\le 10\); inner palindrome-right \(G(j-1)\) vanishes on
\(q=10\) for \(k\le 10\); rest10 census on \(k\le 10\); \(J\)
closed form on \(k\le 6\)).
`KILLED` (dies at \(k=9\); dies at \(k=10\); equals rest; equals
NU d31 \(G(j+1)\); equals NT inner vanish; equals \(j>n\)
even-\(k\); vanishes; empty; form on \(q=6\); the form for all
\(k\); unique-rest xor equals \(J\); leftover equals rest on both
\(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_nv.md` (this note)
- `research/cycle_nv.py`
- `research/cycle_nv.json`
