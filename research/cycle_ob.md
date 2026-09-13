# Cycle OB: on \(q=10\) through \(k\le 10\), outer NA \(T\) xor of \(G(n,j-1)\) is \(1\) iff \(k\bmod 3=2\)

On covering \(J_{10}\) through \(k\le 10\), XOR of \(G(n,j-1)\) over
palindrome-right \(G=1\) cells with \(n<U/2\) and
\(j>n+\lfloor n/2\rfloor\) (\(p=T-2j\ge 0\); no packed row) is \(1\)
iff \(k\bmod 3=2\). Lift of Cycle NF (\(k\le 8\)). Prefix NF
\(q=10\) for \(k\le 8\); walk \(k=9\) and \(k=10\). Companion NG
inner still holds at those \(k\). This is **not** a death at
\(k=9\), **not** a death at \(k=10\), **not** \(T\) (\(k=5\):
\(1\) vs \(0\)), **not** rest (\(k=5\): \(1\) vs \(0\)), **not**
inner \(T\) (\(k=2\): \(1\) vs \(0\)), **not** NN \(T\)-cell
\(G(j+1)\) (\(k=9\): \(0\) vs \(1\)), **not** identically \(0\)
(\(k=5\): \(1\)), **not** empty (\(k=9\): \(n_{\mathrm{out}}=4296\)),
**not** pointwise \(0\) (\(k=9\): \(n_{\mathrm{outg}}=1650\)), and
**not** the form for all \(k\). Do **not** claim \(T\) is \(1\) iff
\(k=2\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for
all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\). Do **not**
walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim Green-only rest for all \(k\). Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_ob.py --certify` (~8.88s).
Dump: `research/cycle_ob.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/NF/NG/NN/OA/MJ (packed-free covering \(q=10\); prefix NF
outer \(T\) for \(k\le 8\); walk \(k=9,10\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (outer \(T\) is \(1\) iff \(k\bmod 3=2\) through \(k\le 10\))

Covering \(q=10\), \(k\le 10\). The walk does not read the packed
row. Same cells as Cycle NF. At \(k=2\), \(n_{\mathrm{out}}=1\) and
xor \(=1\). At \(k=9\), \(n_{\mathrm{out}}=4296\) and xor \(=0\)
with \(n_{\mathrm{outg}}=1650\) fires. Companion inner \(T\) still
matches Cycle NG.

## Killed

Dies at \(k=9\): xor \(=0=\) want. Dies at \(k=10\): xor \(=0=\)
want. Equals \(T\): \(k=5\) is \(1\) vs \(0\). Equals rest:
\(k=5\) is \(1\) vs \(0\). Equals inner \(T\): \(k=2\) is \(1\) vs
\(0\). Equals NN \(T\)-cell \(G(j+1)\): \(k=9\) is \(0\) vs \(1\).
Vanishes identically: \(k=5\) is \(1\). Empty: \(k=9\) has
\(n_{\mathrm{out}}=4296\). Pointwise \(0\): \(k=9\) has
\(n_{\mathrm{outg}}=1650\). The form for all \(k\).

## Verdict

`LEMMA` (outer \(T\) xor of \(G(n,j-1)\) is \(1\) iff
\(k\bmod 3=2\) on \(q=10\) for \(k\le 10\); that form holds on both
covering \(q\) for \(k\le 8\); \(S\) on \(n<U\) is \(1\) iff
\(k>0\) and \(k\bmod 4=0\) on \(q=10\) for \(k\le 10\); rest10
census on \(k\le 10\); \(J\) closed form on \(k\le 6\)).
`KILLED` (dies at \(k=9\); dies at \(k=10\); equals \(T\); equals
rest; equals inner \(T\); equals NN \(T\)-cell \(G(j+1)\); vanishes
identically; empty; pointwise \(0\); the form for all \(k\);
unique-rest xor equals \(J\); leftover equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ob.md` (this note)
- `research/cycle_ob.py`
- `research/cycle_ob.json`
