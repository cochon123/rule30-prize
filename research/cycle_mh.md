# Cycle MH: on \(q=10\) for \(k\le 8\), leftover AND xor of \(G(n,j+1)\) is \(1\) iff \(k\) even

On covering \(J_{10}\) for \(k\le 8\), XOR of \(G(n,j+1)\) on
leftover packed AND (\(G=1\), \(p\) off \(\{4,6,14\}\) and off
the LC–LU unique-rest slots) is \(1\) iff \(k\) is even. This is
**not** rest (\(k=0\), \(q=10\): gj1 \(=1\), rest \(=0\)), **not**
identically \(0\) on \(q=10\), **not** \(k\bmod 2\) on \(q=6\)
(\(k=6\), \(q=6\) is even but xor \(=0\)), **not** Green-only
rest (still filters leftover AND by the packed row), and **not**
the form for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim a Green-only formula for rest without reading the packed
row. Do **not** record unique-slot XOR vs \(J\).

Certify: `python3 research/cycle_mh.py --certify`.
Dump: `research/cycle_mh.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/MD/ME (covering \(q=10\) for \(k\le 8\) plus the
\(k=6\), \(q=6\) kill; prefix ME for leftover=rest; no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (leftover AND xor of \(G(n,j+1)\) is \(1\) iff \(k\) even)

Covering \(q=10\), \(k\le 8\). Leftover means packed AND on
\(G=1\) off \(\{p=4,p=6,p=14\}\) and off `UNIQUE_REST`.

## Lemma (\(q=10\) leftover XOR is rest on \(k\le 8\))

Cycle ME.

## Killed

Leftover AND xor of \(G(n,j+1)\) equals rest: \(k=0\), \(q=10\)
is \(1\) vs \(0\). That xor vanishes on \(q=10\): \(k=0\) is
\(1\). That xor is \(k\bmod 2\) on \(q=6\): \(k=6\), \(q=6\) is
even but xor \(=0\). Green-only rest: the walk still filters
leftover AND by the packed row.

## Verdict

`LEMMA` (leftover AND xor of \(G(n,j+1)\) is \(1\) iff \(k\) even
on \(q=10\) for \(k\le 8\); \(q=10\) leftover split on \(k\le 8\);
unique-rest XOR vanishes at \(k=9,10\); rest10 census on
\(k\le 10\); \(J\) closed form on \(k\le 6\)).
`KILLED` (gj1 xor equals rest; gj1 xor vanishes on \(q=10\);
gj1 xor is \(k\bmod 2\) on \(q=6\); Green-only rest; the even-\(k\)
form for all \(k\); unique-rest xor equals \(J\); leftover equals
rest on both \(q\); rest8 for all \(k\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_mh.md` (this note)
- `research/cycle_mh.py`
- `research/cycle_mh.json`
