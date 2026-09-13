# Cycle MI: on \(q=10\) for \(k\le 8\), Green-only xor of \(G(n,j-1)\) on \(G=1\) is \(1\) iff \(k\) even

On covering \(J_{10}\) for \(k\le 8\), XOR of \(G(n,j-1)\) over
covering cells with \(G(n,j)=1\) (\(p=T-2j\ge 0\); no packed row)
is \(1\) iff \(k\) is even. Equals Cycle MH leftover AND xor of
\(G(n,j+1)\). This is **not** rest (\(k=0\), \(q=10\): jm1 \(=1\),
rest \(=0\)), **not** identically \(0\) on \(q=10\), **not**
\(k\bmod 2\) on \(q=6\) (\(k=0\), \(q=6\) is even but xor \(=0\)),
**not** leftover \(G(j+1)\) xor on \(q=6\) (\(k=6\), \(q=6\):
jm1 \(=1\), leftover \(=0\)), **not** Green-only rest, and **not**
the form for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim a Green-only formula for rest. Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_mi.py --certify`.
Dump: `research/cycle_mi.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/MH (packed-free covering \(q=10\) for \(k\le 8\); prefix
MH leftover \(G(j+1)\) xor; no Fermat table, no extra window, no
\(n_0=16\) window).

## Lemma (Green-only xor of \(G(n,j-1)\) on \(G=1\) is \(1\) iff \(k\) even)

Covering \(q=10\), \(k\le 8\). The walk does not read the packed
row.

## Lemma (equals Cycle MH leftover AND xor of \(G(n,j+1)\))

Same \(q=10\), \(k\le 8\) census.

## Killed

Green-only \(G(n,j-1)\) xor equals rest: \(k=0\), \(q=10\) is
\(1\) vs \(0\). That xor vanishes on \(q=10\): \(k=0\) is \(1\).
That xor is \(k\bmod 2\) on \(q=6\): \(k=0\), \(q=6\) is even but
xor \(=0\). Equals leftover \(G(j+1)\) xor on \(q=6\): \(k=6\),
\(q=6\) has jm1 \(=1\) and leftover \(=0\). Green-only rest:
this xor is not rest.

## Verdict

`LEMMA` (Green-only xor of \(G(n,j-1)\) on \(G=1\) is \(1\) iff
\(k\) even on \(q=10\) for \(k\le 8\); equals MH leftover
\(G(j+1)\) xor; leftover AND xor of \(G(n,j+1)\) is \(1\) iff \(k\)
even; \(q=10\) leftover split on \(k\le 8\); rest10 census on
\(k\le 10\); \(J\) closed form on \(k\le 6\)).
`KILLED` (jm1 xor equals rest; jm1 xor vanishes on \(q=10\);
jm1 xor is \(k\bmod 2\) on \(q=6\); jm1 equals leftover jp1 on
\(q=6\); Green-only rest; the even-\(k\) form for all \(k\);
unique-rest xor equals \(J\); leftover equals rest on both \(q\);
rest8 for all \(k\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_mi.md` (this note)
- `research/cycle_mi.py`
- `research/cycle_mi.json`
