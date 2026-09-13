# Cycle OC: on \(q=10\) through \(k\le 10\), inner NA \(T\) xor of \(G(n,j-1)\) is \(1\) iff \(k>2\) and \(k\bmod 3=2\)

On covering \(J_{10}\) through \(k\le 10\), XOR of \(G(n,j-1)\) over
palindrome-right \(G=1\) cells with \(n<U/2\) and
\(j\le n+\lfloor n/2\rfloor\) (\(p=T-2j\ge 0\); no packed row) is
\(1\) iff \(k>2\) and \(k\bmod 3=2\). Lift of Cycle NG (\(k\le 8\)).
Prefix NG \(q=10\) for \(k\le 8\); walk \(k=9\) and \(k=10\).
Companion OB outer still holds at those \(k\). This is **not** a
death at \(k=9\), **not** a death at \(k=10\), **not** \(T\)
(\(k=5\): \(1\) vs \(0\)), **not** rest (\(k=5\): \(1\) vs \(0\)),
**not** outer \(T\) (\(k=2\): \(0\) vs \(1\)), **not** NN \(T\)-cell
\(G(j+1)\) (\(k=9\): \(0\) vs \(1\)), **not** identically \(0\)
(\(k=5\): \(1\)), **not** empty (\(k=9\): \(n_{\mathrm{in}}=2616\)),
**not** pointwise \(0\) (\(k=9\): \(n_{\mathrm{ing}}=1038\)), and
**not** the form for all \(k\). Do **not** claim \(T\) is \(1\) iff
\(k=2\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for
all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\). Do **not**
walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim Green-only rest for all \(k\). Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_oc.py --certify`.
Dump: `research/cycle_oc.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/NG/NF/NN/OB/MJ (packed-free covering \(q=10\); prefix NG
inner \(T\) for \(k\le 8\); walk \(k=9,10\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (inner \(T\) is \(1\) iff \(k>2\) and \(k\bmod 3=2\) through \(k\le 10\))

Covering \(q=10\), \(k\le 10\). The walk does not read the packed
row. Same cells as Cycle NG. At \(k=4\), \(n_{\mathrm{in}}=3\) and
xor \(=0\) with \(n_{\mathrm{ing}}=2\) fires. At \(k=9\),
\(n_{\mathrm{in}}=2616\) and xor \(=0\) with \(n_{\mathrm{ing}}=1038\)
fires. Companion outer \(T\) still matches Cycle OB.

## Killed

Dies at \(k=9\): xor \(=0=\) want. Dies at \(k=10\): xor \(=0=\)
want. Equals \(T\): \(k=5\) is \(1\) vs \(0\). Equals rest:
\(k=5\) is \(1\) vs \(0\). Equals outer \(T\): \(k=2\) is \(0\) vs
\(1\). Equals NN \(T\)-cell \(G(j+1)\): \(k=9\) is \(0\) vs \(1\).
Vanishes identically: \(k=5\) is \(1\). Empty: \(k=9\) has
\(n_{\mathrm{in}}=2616\). Pointwise \(0\): \(k=9\) has
\(n_{\mathrm{ing}}=1038\). The form for all \(k\).

## Verdict

`LEMMA` (inner \(T\) xor of \(G(n,j-1)\) is \(1\) iff \(k>2\) and
\(k\bmod 3=2\) on \(q=10\) for \(k\le 10\); that form holds on both
covering \(q\) for \(k\le 8\); outer \(T\) is \(1\) iff
\(k\bmod 3=2\) on \(q=10\) for \(k\le 10\); rest10 census on
\(k\le 10\); \(J\) closed form on \(k\le 6\)).
`KILLED` (dies at \(k=9\); dies at \(k=10\); equals \(T\); equals
rest; equals outer \(T\); equals NN \(T\)-cell \(G(j+1)\); vanishes
identically; empty; pointwise \(0\); the form for all \(k\);
unique-rest xor equals \(J\); leftover equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_oc.md` (this note)
- `research/cycle_oc.py`
- `research/cycle_oc.json`
