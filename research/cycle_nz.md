# Cycle NZ: on \(q=10\) through \(k\le 10\), NA's \(S\) on \(U\le n<3U/2\) vanishes

On covering \(J_{10}\) through \(k\le 10\), XOR of \(G(n,j+1)\) over
palindrome-right cells with \((j-n)\bmod 3=1\), \(G(n,j-1)=0\), and
\(U\le n<3U/2\) (\(p=T-2j\ge 0\); no packed row) is \(0\). Lift of
Cycle ND (\(k\le 8\)). Prefix ND \(q=10\) for \(k\le 8\); walk
\(k=9\) and \(k=10\). Companion NC \(n<U\) and NY high \(S\) still
hold at those \(k\). This is **not** a death at \(k=9\), **not** a
death at \(k=10\), **not** rest (\(k=2\): \(0\) vs \(1\)), **not**
NC \(n<U\) (\(k=4\): \(0\) vs \(1\)), **not** NA \(S\) (\(k=6\):
\(0\) vs \(1\)), **not** NY high \(S\) (\(k=4\): \(0\) vs \(1\)),
**not** empty (\(k=9\): \(n_{\mathrm{mid}}=4203\)), **not**
pointwise \(0\) (\(k=9\): \(n_{\mathrm{midg}}=2032\)), and **not**
the form for all \(k\). Do **not** claim \(T\) is \(1\) iff
\(k=2\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for
all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\). Do **not**
walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim Green-only rest for all \(k\). Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_nz.py --certify` (~8.74s).
Dump: `research/cycle_nz.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/ND/NY/NC/NE/MJ (packed-free covering \(q=10\); prefix ND
mid \(S\) for \(k\le 8\); walk \(k=9,10\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (\(S\) on \(U\le n<3U/2\) vanishes through \(k\le 10\))

Covering \(q=10\), \(k\le 10\). The walk does not read the packed
row. Same cells as Cycle ND. At \(k=4\), \(n_{\mathrm{mid}}=13\)
and \(G(j+1)\) fires four times. At \(k=9\),
\(n_{\mathrm{mid}}=4203\) and xor \(=0\) with
\(n_{\mathrm{midg}}=2032\) fires. Companion \(S\) on \(n<U\) and on
\(n\ge 3U/2\) still match Cycles NC and NY.

## Killed

Dies at \(k=9\): xor \(=0\). Dies at \(k=10\): xor \(=0\). Equals
rest: \(k=2\) is \(0\) vs \(1\). Equals NC \(n<U\): \(k=4\) is
\(0\) vs \(1\). Equals NA \(S\): \(k=6\) is \(0\) vs \(1\). Equals
NY high \(S\): \(k=4\) is \(0\) vs \(1\). Empty: \(k=9\) has
\(n_{\mathrm{mid}}=4203\). Pointwise \(0\): \(k=9\) has
\(n_{\mathrm{midg}}=2032\). The form for all \(k\).

## Verdict

`LEMMA` (\(S\) on \(U\le n<3U/2\) vanishes on \(q=10\) for
\(k\le 10\); that vanish holds on both covering \(q\) for
\(k\le 8\); \(S\) on \(n\ge 3U/2\) is \(1\) iff
\(k\bmod 8\in\{4,6\}\) on \(q=10\) for \(k\le 10\); rest10 census
on \(k\le 10\); \(J\) closed form on \(k\le 6\)).
`KILLED` (dies at \(k=9\); dies at \(k=10\); equals rest; equals
NC \(n<U\); equals NA \(S\); equals NY high \(S\); empty;
pointwise \(0\); the form for all \(k\); unique-rest xor equals
\(J\); leftover equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_nz.md` (this note)
- `research/cycle_nz.py`
- `research/cycle_nz.json`
