# Cycle MK: on \(q=10\) for \(k\le 8\), inner palindrome-right xor of \(G(n,j-1)\) on \(G=1\) vanishes

On covering \(J_{10}\) for \(k\le 8\), XOR of \(G(n,j-1)\) over
covering \(G=1\) cells with \(n<j\le n+\lfloor n/2\rfloor\)
(\(p=T-2j\ge 0\); no packed row) is \(0\), so Cycle MJ's even-\(k\)
\(j>n\) xor is the outer slice \(j>n+\lfloor n/2\rfloor\). This is
**not** rest, **not** inner empty (\(k\ge 1\) has inner \(G=1\)),
**not** inner vanish on \(q=6\) (\(k=3\), \(q=6\) xor \(=1\)),
**not** Green-only rest, and **not** the form for all \(k\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim a Green-only formula for rest. Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_mk.py --certify` (~0.65s).
Dump: `research/cycle_mk.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/MJ (packed-free covering \(q=10\) for \(k\le 8\); prefix
MJ \(j>n\) xor; \(k=3\), \(q=6\) kill; no Fermat table, no extra
window, no \(n_0=16\) window).

## Lemma (inner palindrome-right xor vanishes on \(q=10\))

Covering \(k\le 8\). Inner means \(n<j\le n+\lfloor n/2\rfloor\).
The walk does not read the packed row.

## Lemma (outer slice equals Cycle MJ even-\(k\) xor)

Same \(q=10\), \(k\le 8\) census: \(j>n+\lfloor n/2\rfloor\) xor
of \(G(n,j-1)\) on \(G=1\) is \(1\) iff \(k\) even.

## Killed

Inner xor vanishes on \(q=6\): \(k=3\), \(q=6\) is \(1\). Inner
xor equals rest: inner is \(0\) and rest is \(1\) at \(k=2\),
\(q=10\). Inner \(G=1\) empty: \(k=1\) has \(n_{\mathrm{in}}>0\).
Green-only rest: this xor is not rest.

## Verdict

`LEMMA` (inner palindrome-right xor vanishes on \(q=10\) for
\(k\le 8\); outer slice equals MJ even-\(k\) xor; \(j>n\) xor is
\(1\) iff \(k\) even on both covering \(q\); \(j=n\) xor of
\(G(n,n-1)\) is \(1\); Green-only xor of \(G(n,j-1)\) on \(G=1\) is
\(1\) iff \(k\) even on \(q=10\); rest10 census on \(k\le 10\);
\(J\) closed form on \(k\le 6\)).
`KILLED` (inner vanish on \(q=6\); inner xor equals rest; inner
empty; Green-only rest; the even-\(k\) form for all \(k\);
unique-rest xor equals \(J\); leftover equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_mk.md` (this note)
- `research/cycle_mk.py`
- `research/cycle_mk.json`
