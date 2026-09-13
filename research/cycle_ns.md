# Cycle NS: on \(q=10\) through \(k\le 10\), inner palindrome-right even-\(d\) \(G(j+1)\) vanishes

On covering \(J_{10}\) through \(k\le 10\), XOR of \(G(n,j+1)\) over
covering \(G=1\) cells with \(n<j\le n+\lfloor n/2\rfloor\) and
\((j-n)\) even (\(p=T-2j\ge 0\); no packed row) is \(0\). Lift of
Cycle MV (\(k\le 8\), both covering \(q\)). Prefix MV \(q=10\) for
\(k\le 8\); walk \(k=9\) and \(k=10\). Companion of Cycle NR's
outer identically-\(1\) lift: inner even-\(d\) still vanishes at
those \(k\). This is **not** a death at \(k=9\), **not** a death
at \(k=10\), **not** rest (\(k=2\): \(0\) vs \(1\)), **not** NR
outer identically \(1\) (\(k=9\): \(0\) vs \(1\)), **not** empty
(\(k=9\): \(n_{\mathrm{ine}}=47906\)), **not** pointwise \(0\)
(\(k=9\): \(n_{G(j+1)=1}=14872\)), and **not** the form for all
\(k\). Do **not** claim \(T\) is \(1\) iff \(k=2\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim Green-only rest for all \(k\). Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_ns.py --certify` (runtime to be
recorded in the dump commit).
Dump: `research/cycle_ns.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/MV/NR/MJ (packed-free covering \(q=10\); prefix MV inner
even-\(d\) for \(k\le 8\); walk \(k=9,10\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (inner palindrome-right even-\(d\) \(G(j+1)\) vanishes through \(k\le 10\))

Covering \(q=10\), \(k\le 10\). The walk does not read the packed
row. Same cells as Cycle MV's \(q=10\) slice. At \(k=2\),
\(n_{\mathrm{ine}}=5\) and \(G(j+1)\) fires twice. At \(k=9\),
\(n_{\mathrm{ine}}=47906\) and \(n_{G(j+1)=1}=14872\). Inner
\(G(j-1)\) xor also vanishes at \(k=9,10\) (Cycle MK companion;
not recorded here).

## Killed

Dies at \(k=9\): xor \(=0\). Dies at \(k=10\): xor \(=0\). Equals
rest: \(k=2\) is \(0\) vs \(1\). Equals NR outer identically \(1\):
\(k=9\) is \(0\) vs \(1\). Empty: \(k=9\) has
\(n_{\mathrm{ine}}=47906\). Pointwise \(0\): \(k=9\) has
\(n_{G(j+1)=1}=14872\). The form for all \(k\).

## Verdict

`LEMMA` (inner palindrome-right even-\(d\) \(G(j+1)\) vanishes on
\(q=10\) for \(k\le 10\); that vanish holds on both covering \(q\)
for \(k\le 8\); outer palindrome-right \(G(j+1)\) is identically
\(1\) on \(q=10\) for \(k\le 10\); rest10 census on \(k\le 10\);
\(J\) closed form on \(k\le 6\)).
`KILLED` (dies at \(k=9\); dies at \(k=10\); equals rest; equals
NR outer identically \(1\); empty; pointwise \(0\); the form for
all \(k\); unique-rest xor equals \(J\); leftover equals rest on
both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ns.md` (this note)
- `research/cycle_ns.py`
- `research/cycle_ns.json`
