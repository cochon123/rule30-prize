# Cycle MV: on \(q=6\) and \(q=10\) for \(k\le 8\), inner palindrome-right even-\(d\) xor of \(G(n,j+1)\) vanishes

On covering \(J_6,J_{10}\) for \(k\le 8\), XOR of \(G(n,j+1)\) over
covering \(G=1\) cells with \(n<j\le n+\lfloor n/2\rfloor\) and
\((j-n)\) even (\(p=T-2j\ge 0\); no packed row) is \(0\). Dual of
Cycle MK's inner \(G(j-1)\) vanish (\(q=10\) only): Cycle MU's
\(k\)-odd even-\(d\) \(G(j+1)\) on \(q=6\) is the outer even-\(d\)
slice. This is **not** rest (\(k=2\), \(q=10\): xor \(=0\), rest
\(=1\)), **not** empty (\(k=2\), \(q=10\): \(n_{\mathrm{ine}}=5\)),
**not** pointwise \(0\) (\(k=2\), \(q=10\): \(n_{G(j+1)=1}=2\)),
**not** MU even-\(d\) \(G(j+1)\) (\(k=3\), \(q=6\): \(0\) vs \(1\)),
**not** MK inner \(G(j-1)\) (\(k=3\), \(q=6\): jm1 \(=1\)), **not**
Green-only rest, and **not** the form for all \(k\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim a Green-only formula for rest. Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_mv.py --certify`.
Dump: `research/cycle_mv.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/MJ/MK/MU (packed-free covering both \(q\) for \(k\le 8\);
prefix MU even-\(d\) \(G(j+1)\) and MK inner \(G(j-1)\) vanish; no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (inner palindrome-right even-\(d\) xor of \(G(n,j+1)\) vanishes)

Both covering \(q\), \(k\le 8\). The walk does not read the packed
row. On \(q=6\), Cycle MU's \(k\)-odd even-\(d\) xor is the
outer even-\(d\) slice.

## Killed

Inner even-\(d\) \(G(j+1)\) xor equals rest: \(k=2\), \(q=10\) is
\(0\) vs \(1\). Empty: \(k=2\), \(q=10\) has \(n_{\mathrm{ine}}=5\).
Pointwise \(0\): \(k=2\), \(q=10\) has two \(G(j+1)=1\) cells.
Equals MU even-\(d\) \(G(j+1)\): \(k=3\), \(q=6\) is \(0\) vs \(1\).
Equals MK inner \(G(j-1)\): \(k=3\), \(q=6\) jm1 \(=1\). Green-only
rest: this xor is not rest.

## Verdict

`LEMMA` (inner palindrome-right even-\(d\) xor of \(G(n,j+1)\)
vanishes on both covering \(q\) for \(k\le 8\); even-\(d\)
\(G(j+1)\) xor is \(1\) iff \(k\) odd on \(q=6\); inner
\(G(j-1)\) xor vanishes on \(q=10\); \(j>n\) xor is \(1\) iff
\(k\) even on both covering \(q\); rest10 census on \(k\le 10\);
\(J\) closed form on \(k\le 6\)).
`KILLED` (inner even-\(d\) \(G(j+1)\) equals rest; inner even-\(d\)
empty; inner even-\(d\) pointwise \(0\); inner even-\(d\) equals
MU; inner even-\(d\) equals MK inner \(G(j-1)\); Green-only rest;
the form for all \(k\); unique-rest xor equals \(J\); leftover
equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_mv.md` (this note)
- `research/cycle_mv.py`
- `research/cycle_mv.json`
