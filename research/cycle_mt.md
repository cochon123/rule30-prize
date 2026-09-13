# Cycle MT: on \(q=6\) for \(k\le 8\), palindrome-right even-\(d\) xor of \(G(n,j-1)\) on \(G=1\) vanishes

On covering \(J_6\) for \(k\le 8\), XOR of \(G(n,j-1)\) over covering
\(G=1\) cells with \(j>n\) and \((j-n)\) even (\(p=T-2j\ge 0\); no
packed row) is \(0\), so Cycle MJ's even-\(k\) \(j>n\) xor is the
odd-\(d\) slice on \(q=6\). Dual of Cycle MK's inner vanish on
\(q=10\). This is **not** rest (\(k=2\), \(q=10\): even \(=0\), rest
\(=1\)), **not** vanish on \(q=10\) (\(k=1\) xor \(=1\)), **not**
empty (\(k=1\): \(n_{\mathrm{even}}=2\)), **not** pointwise \(0\)
(\(k=2\): \(n_{G(j-1)=1}=2\)), **not** \(j>n\) even-\(k\), **not**
Green-only rest, and **not** the form for all \(k\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim a Green-only formula for rest. Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_mt.py --certify` (~0.23s).
Dump: `research/cycle_mt.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/MJ/MS (packed-free covering \(q=6\) for \(k\le 8\);
prefix MJ \(j>n\) xor; \(k=1\) and \(k=2\), \(q=10\) kills; no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (palindrome-right even-\(d\) xor of \(G(n,j-1)\) vanishes)

Covering \(q=6\), \(k\le 8\). The walk does not read the packed
row. Odd-\(d\) xor equals Cycle MJ's even-\(k\) \(j>n\) xor.

## Killed

Even-\(d\) xor vanishes on \(q=10\): \(k=1\) is \(1\). Equals rest:
\(k=2\), \(q=10\) is \(0\) vs \(1\). Empty on \(q=6\): \(k=1\) has
\(n_{\mathrm{even}}=2\). Pointwise \(0\): \(k=2\) has two
\(G(j-1)=1\) cells. Equals \(j>n\) even-\(k\): \(k=0\), \(q=6\) is
\(0\) vs \(1\). Green-only rest: this xor is not rest.

## Verdict

`LEMMA` (palindrome-right even-\(d\) xor of \(G(n,j-1)\) vanishes
on \(q=6\) for \(k\le 8\), so \(j>n\) even-\(k\) is the odd-\(d\)
slice; q=6 d31 is \(1\) iff \(k\bmod 4\in\{0,1,2\}\); \(j>n\) xor
is \(1\) iff \(k\) even on both covering \(q\); rest10 census on
\(k\le 10\); \(J\) closed form on \(k\le 6\)).
`KILLED` (even-\(d\) vanish on \(q=10\); even-\(d\) equals rest;
even-\(d\) empty; even-\(d\) pointwise \(0\); even-\(d\) equals
jgtn; Green-only rest; the form for all \(k\); unique-rest xor
equals \(J\); leftover equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_mt.md` (this note)
- `research/cycle_mt.py`
- `research/cycle_mt.json`
