# Cycle NH: on \(q=10\) for \(k\le 8\), NA's \(S\) on \(2U\le n<3U\) is \(1\) iff \(k\bmod 3=2\)

On covering \(J_{10}\) for \(k\le 8\), XOR of \(G(n,j+1)\) over
palindrome-right cells with \((j-n)\bmod 3=1\), \(G(n,j-1)=0\), and
\(2U\le n<3U\) (\(p=T-2j\ge 0\); no packed row) is \(1\) iff
\(k\bmod 3=2\). Same modulus as Cycle NF's outer \(T\); a different
slice. This is **not** rest (\(k=5\): xor \(=1\), rest \(=0\)),
**not** NE high (\(k=2\): \(1\) vs \(0\)), **not** NA \(S\)
(\(k=2\): \(1\) vs \(0\)), **not** NC \(n<U\) (\(k=2\): \(1\) vs
\(0\)), **not** \(T\) (\(k=5\): \(1\) vs \(0\)), **not**
identically \(0\), **not** empty (\(k=1\): \(n_{23}=1\)), **not**
the form on \(q=6\) (empty; \(k=2\) xor \(=0\), want \(=1\)),
**not** Green-only rest, and **not** the form for all \(k\). Do
**not** claim \(T\) is \(1\) iff \(k=2\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim Green-only rest for all \(k\). Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_nh.py --certify`.
Dump: `research/cycle_nh.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/MJ/NA/NC/NE (packed-free covering \(q=10\) for \(k\le 8\);
prefix NE high \(S\), NC \(n<U\), and NA \(S\); \(k=2\), \(q=6\)
empty kill; no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (\(S\) on \(2U\le n<3U\) is \(1\) iff \(k\bmod 3=2\))

Covering \(q=10\), \(k\le 8\). The walk does not read the packed
row. The band is unclipped on \(q=10\) (\(j\le 2n<6U\),
\(p\ge 4U\)). On \(q=6\) the band is empty (\(n<2U\)).

## Killed

Equals rest: \(k=5\), \(q=10\) is \(1\) vs \(0\). Equals NE high:
\(k=2\) is \(1\) vs \(0\). Equals NA \(S\): \(k=2\) is \(1\) vs
\(0\). Equals NC \(n<U\): \(k=2\) is \(1\) vs \(0\). Equals \(T\):
\(k=5\) is \(1\) vs \(0\). Vanishes: \(k=2\) is \(1\). Empty:
\(k=1\) has \(n_{23}=1\). The form on \(q=6\): empty at \(k=2\),
xor \(=0\) and want \(=1\). The form for all \(k\).

## Verdict

`LEMMA` (\(S\) on \(2U\le n<3U\) is \(1\) iff \(k\bmod 3=2\) on
\(q=10\) for \(k\le 8\); high \(S\) is \(1\) iff
\(k\bmod 8\in\{4,6\}\) on \(q=10\); Green-only rest on \(q=10\)
for \(k\le 8\); \(j>n\) xor is \(1\) iff \(k\) even; rest10 census
on \(k\le 10\); \(J\) closed form on \(k\le 6\)).
`KILLED` (equals rest; equals NE high; equals NA \(S\); equals NC
\(n<U\); equals \(T\); vanishes; empty; the form on \(q=6\); the
form for all \(k\); unique-rest xor equals \(J\); leftover equals
rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_nh.md` (this note)
- `research/cycle_nh.py`
- `research/cycle_nh.json`
