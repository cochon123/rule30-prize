# Cycle OA: on \(q=10\) through \(k\le 10\), NA's \(S\) on \(n<U\) is \(1\) iff \(k>0\) and \(k\bmod 4=0\)

On covering \(J_{10}\) through \(k\le 10\), XOR of \(G(n,j+1)\) over
palindrome-right cells with \((j-n)\bmod 3=1\), \(G(n,j-1)=0\), and
\(n<U\) (\(p=T-2j\ge 0\); no packed row) is \(1\) iff \(k>0\) and
\(k\bmod 4=0\). Lift of Cycle NC (\(k\le 8\)). Prefix NC \(q=10\)
for \(k\le 8\); walk \(k=9\) and \(k=10\). Companion NZ mid vanish
and NY high \(S\) still hold at those \(k\). This is **not** a
death at \(k=9\), **not** a death at \(k=10\), **not** rest
(\(k=4\): \(1\) vs \(0\)), **not** NY high \(S\) (\(k=6\): \(0\) vs
\(1\)), **not** NZ mid (\(k=4\): \(1\) vs \(0\)), **not** NA \(S\)
(\(k=6\): \(0\) vs \(1\)), **not** Green d31 (\(k=0\): \(0\) vs
\(1\)), **not** MQ \(d31\) \(G(j+1)\) (\(k=4\): \(1\) vs \(0\)),
**not** \(j>n\) even-\(k\) (\(k=2\): \(0\) vs \(1\)), **not**
identically \(0\) (\(k=4\): \(1\)), **not** empty (\(k=9\):
\(n_S=4372\)), **not** pointwise \(0\) (\(k=9\): \(n_{\mathrm{sg}}=1728\)),
and **not** the form for all \(k\). Do **not** claim \(T\) is \(1\)
iff \(k=2\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\)
for all \(k\). Do **not** push the even-spine scan past \(k=18\).
Do **not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\). Do **not**
walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim Green-only rest for all \(k\). Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_oa.py --certify` (~8.84s).
Dump: `research/cycle_oa.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/NC/NZ/NE/MJ/MM/MQ (packed-free covering \(q=10\); prefix NC
\(S\) on \(n<U\) for \(k\le 8\); walk \(k=9,10\); no Fermat table,
no extra window, no \(n_0=16\) window).

## Lemma (\(S\) on \(n<U\) is \(1\) iff \(k>0\) and \(k\bmod 4=0\) through \(k\le 10\))

Covering \(q=10\), \(k\le 10\). The walk does not read the packed
row. Same cells as Cycle NC. At \(k=4\), \(n_S=6\) and xor \(=1\)
with \(n_{\mathrm{sg}}=3\) fires. At \(k=9\), \(n_S=4372\) and xor
\(=0\) with \(n_{\mathrm{sg}}=1728\) fires. Companion mid vanish
and high \(S\) still match Cycles NZ and NY.

## Killed

Dies at \(k=9\): xor \(=0=\) want. Dies at \(k=10\): xor \(=0=\)
want. Equals rest: \(k=4\) is \(1\) vs \(0\). Equals NY high
\(S\): \(k=6\) is \(0\) vs \(1\). Equals NZ mid: \(k=4\) is \(1\)
vs \(0\). Equals NA \(S\): \(k=6\) is \(0\) vs \(1\). Equals Green
d31: \(k=0\) is \(0\) vs \(1\). Equals MQ \(d31\) \(G(j+1)\):
\(k=4\) is \(1\) vs \(0\). Equals \(j>n\) even-\(k\): \(k=2\) is
\(0\) vs \(1\). Vanishes identically: \(k=4\) is \(1\). Empty:
\(k=9\) has \(n_S=4372\). Pointwise \(0\): \(k=9\) has
\(n_{\mathrm{sg}}=1728\). The form for all \(k\).

## Verdict

`LEMMA` (\(S\) on \(n<U\) is \(1\) iff \(k>0\) and \(k\bmod 4=0\)
on \(q=10\) for \(k\le 10\); that form holds on both covering \(q\)
for \(k\le 8\); \(S\) on \(U\le n<3U/2\) vanishes on \(q=10\) for
\(k\le 10\); rest10 census on \(k\le 10\); \(J\) closed form on
\(k\le 6\)).
`KILLED` (dies at \(k=9\); dies at \(k=10\); equals rest; equals
NY high \(S\); equals NZ mid; equals NA \(S\); equals Green d31;
equals MQ \(d31\) \(G(j+1)\); equals jgtn; vanishes identically;
empty; pointwise \(0\); the form for all \(k\); unique-rest xor
equals \(J\); leftover equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_oa.md` (this note)
- `research/cycle_oa.py`
- `research/cycle_oa.json`
