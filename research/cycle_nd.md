# Cycle ND: on \(q=6\) and \(q=10\) for \(k\le 8\), NA's \(S\) on \(U\le n<3U/2\) vanishes

On covering \(J_6,J_{10}\) for \(k\le 8\), XOR of \(G(n,j+1)\) over
palindrome-right cells with \((j-n)\bmod 3=1\), \(G(n,j-1)=0\), and
\(U\le n<3U/2\) (\(p=T-2j\ge 0\); no packed row) is \(0\). So
Cycle NA's \(S\) on \(n\ge U\) is the \(n\ge 3U/2\) slice. Both
covering \(q\) agree on xor and on \(n_{\mathrm{mid}}\). This is
**not** rest (\(k=2\), \(q=10\): xor \(=0\), rest \(=1\)), **not**
empty (\(k=2\): \(n_{\mathrm{mid}}=1\)), **not** pointwise \(0\)
(\(k=4\): \(n_{\mathrm{mid},G(j+1)=1}=4\)), **not** NC \(n<U\)
(\(k=4\): \(0\) vs \(1\)), **not** NA \(S\) (\(k=6\), \(q=10\):
\(0\) vs \(1\)), **not** \(S\) on \(n\ge U\) (\(k=3\), \(q=6\):
\(0\) vs \(1\)), **not** Green-only rest, and **not** the form for
all \(k\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\)
for all \(k\). Do **not** push the even-spine scan past \(k=18\).
Do **not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\). Do **not**
walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim Green-only rest for all \(k\). Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_nd.py --certify` (~0.61s).
Dump: `research/cycle_nd.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/MJ/NC/NA (packed-free covering both \(q\) for \(k\le 8\);
prefix NC \(S\) on \(n<U\), NA \(S\), and MJ \(j>n\); no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (\(S\) on \(U\le n<3U/2\) vanishes)

Both covering \(q\), \(k\le 8\). The walk does not read the packed
row. At \(k=4\), \(n_{\mathrm{mid}}=13\) and \(G(j+1)\) fires four
times. The mid-band counts agree on \(q=6\) and \(q=10\).

## Killed

Equals rest: \(k=2\), \(q=10\) is \(0\) vs \(1\). Empty: \(k=2\)
has \(n_{\mathrm{mid}}=1\). Pointwise \(0\): \(k=4\) has
\(n_{\mathrm{mid},G(j+1)=1}=4\). Equals NC \(n<U\): \(k=4\) is
\(0\) vs \(1\). Equals NA \(S\): \(k=6\), \(q=10\) is \(0\) vs
\(1\). Equals \(S\) on \(n\ge U\): \(k=3\), \(q=6\) is \(0\) vs
\(1\). Dies on \(q=6\): \(k=4\) xor \(=0\) with
\(n_{\mathrm{mid}}=13\). The form for all \(k\).

## Verdict

`LEMMA` (\(S\) on \(U\le n<3U/2\) vanishes on both covering \(q\)
for \(k\le 8\); \(S\) on \(n<U\) is \(1\) iff \(k>0\) and
\(k\bmod 4=0\); Green-only rest on \(q=10\) for \(k\le 8\);
\(j>n\) xor is \(1\) iff \(k\) even; rest10 census on \(k\le 10\);
\(J\) closed form on \(k\le 6\)).
`KILLED` (equals rest; empty; pointwise \(0\); equals NC \(n<U\);
equals NA \(S\); equals \(S\) on \(n\ge U\); dies on \(q=6\); the
form for all \(k\); unique-rest xor equals \(J\); leftover equals
rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_nd.md` (this note)
- `research/cycle_nd.py`
- `research/cycle_nd.json`
