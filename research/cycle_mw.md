# Cycle MW: on \(q=10\) for \(k\le 8\), outer palindrome-right xor of \(G(n,j+1)\) on \(G=1\) is identically \(1\)

On covering \(J_{10}\) for \(k\le 8\), XOR of \(G(n,j+1)\) over
covering \(G=1\) cells with \(j>n+\lfloor n/2\rfloor\)
(\(p=T-2j\ge 0\); no packed row) is \(1\). Companion of Cycle MV's
inner even-\(d\) \(G(j+1)\) vanish and Cycle MK's inner \(G(j-1)\)
vanish. This is **not** rest (\(k=0\): out \(=1\), rest \(=0\)),
**not** identically \(0\), **not** empty (\(k=0\):
\(n_{\mathrm{out}}=3\)), **not** pointwise \(0\) (\(k=0\):
\(n_{G(j+1)=1}=1\)), **not** identically \(1\) on \(q=6\) (\(k=4\)
xor \(=0\)), **not** \(j>n\) even-\(k\), **not** MV inner even
vanish, **not** Green-only rest, and **not** the form for all
\(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim a Green-only formula for rest. Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_mw.py --certify`.
Dump: `research/cycle_mw.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/MJ/MK/MV (packed-free covering \(q=10\) for \(k\le 8\);
prefix MV inner even-\(d\) vanish and MK inner \(G(j-1)\) vanish;
\(k=4\), \(q=6\) kill; no Fermat table, no extra window, no
\(n_0=16\) window).

## Lemma (outer palindrome-right xor of \(G(n,j+1)\) is identically \(1\))

Covering \(q=10\), \(k\le 8\). The walk does not read the packed
row.

## Killed

Outer \(G(j+1)\) xor equals rest: \(k=0\), \(q=10\) is \(1\) vs
\(0\). Vanishes on \(q=10\): \(k=0\) is \(1\). Empty: \(k=0\) has
\(n_{\mathrm{out}}=3\). Pointwise \(0\): \(k=0\) has one
\(G(j+1)=1\) cell. Identically \(1\) on \(q=6\): \(k=4\) xor
\(=0\) with \(n_{\mathrm{out}}=100\). Equals \(j>n\) even-\(k\):
\(k=1\) out \(=1\) and jgtn \(=0\). Equals MV inner even vanish:
\(k=0\) out \(=1\) and ine \(=0\). Green-only rest: this xor is
not rest.

## Verdict

`LEMMA` (outer palindrome-right xor of \(G(n,j+1)\) is identically
\(1\) on \(q=10\) for \(k\le 8\); inner even-\(d\) \(G(j+1)\) xor
vanishes on both covering \(q\); inner \(G(j-1)\) xor vanishes on
\(q=10\); \(j>n\) xor is \(1\) iff \(k\) even on both covering
\(q\); rest10 census on \(k\le 10\); \(J\) closed form on
\(k\le 6\)).
`KILLED` (outer \(G(j+1)\) equals rest; outer \(G(j+1)\) vanishes;
outer empty; outer pointwise \(0\); identically \(1\) on \(q=6\);
outer equals jgtn; outer equals MV inner even; Green-only rest;
the form for all \(k\); unique-rest xor equals \(J\); leftover
equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_mw.md` (this note)
- `research/cycle_mw.py`
- `research/cycle_mw.json`
