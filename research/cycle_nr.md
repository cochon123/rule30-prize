# Cycle NR: on \(q=10\) through \(k\le 10\), outer palindrome-right \(G(j+1)\) is identically \(1\)

On covering \(J_{10}\) through \(k\le 10\), XOR of \(G(n,j+1)\) over
covering \(G=1\) cells with \(j>n+\lfloor n/2\rfloor\)
(\(p=T-2j\ge 0\); no packed row) is \(1\). Lift of Cycle MW
(\(k\le 8\)). Walk \(k=9\) and \(k=10\). The \(k=9\) and \(k=10\)
bits are nontrivial (\(1=1\)). Companion inner even-\(d\)
\(G(j+1)\) xor still vanishes at those \(k\). This is **not** a
death at \(k=9\), **not** a death at \(k=10\), **not** rest
(\(k=0\): \(1\) vs \(0\)), **not** NN \(T\)-cell \(G(j+1)\)
(\(k=0\): \(1\) vs \(0\)), **not** NO outer \(T\)-cell \(G(j+1)\)
(\(k=0\): \(1\) vs \(0\)), **not** MV inner even vanish (\(k=9\):
\(1\) vs \(0\)), **not** identically \(0\), **not** empty (\(k=9\):
\(n_{\mathrm{out}}=73657\)), **not** pointwise \(0\) (\(k=9\):
\(n_{G(j+1)=1}=28139\)), **not** identically \(1\) on \(q=6\), and
**not** the form for all \(k\). Do **not** claim \(T\) is \(1\)
iff \(k=2\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim Green-only rest for all \(k\). Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_nr.py --certify` (~8.83s).
Dump: `research/cycle_nr.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/MW/MV/MJ/NN/NO (packed-free covering \(q=10\); prefix MW
outer \(G(j+1)\) for \(k\le 8\); walk \(k=9,10\); no Fermat table,
no extra window, no \(n_0=16\) window).

## Lemma (outer palindrome-right \(G(j+1)\) is identically \(1\) through \(k\le 10\))

Covering \(q=10\), \(k\le 10\). The walk does not read the packed
row. Same cells as Cycle MW. At \(k=0\), \(n_{\mathrm{out}}=3\) and
\(G(j+1)\) fires once. At \(k=9\), \(n_{\mathrm{out}}=73657\) and
\(n_{G(j+1)=1}=28139\).

## Killed

Dies at \(k=9\): xor \(=1=\) want. Dies at \(k=10\): xor \(=1=\)
want. Equals rest: \(k=0\) is \(1\) vs \(0\). Equals NN
\(T\)-cell \(G(j+1)\): \(k=0\) is \(1\) vs \(0\). Equals NO outer
\(T\)-cell \(G(j+1)\): \(k=0\) is \(1\) vs \(0\). Equals MV inner
even vanish: \(k=9\) is \(1\) vs \(0\). Vanishes: \(k=9\) is \(1\).
Empty: \(k=9\) has \(n_{\mathrm{out}}=73657\). Pointwise \(0\):
\(k=9\) has \(n_{G(j+1)=1}=28139\). Identically \(1\) on \(q=6\):
\(k=4\) xor \(=0\). The form for all \(k\).

## Verdict

`LEMMA` (outer palindrome-right \(G(j+1)\) is identically \(1\) on
\(q=10\) for \(k\le 10\); inner even-\(d\) \(G(j+1)\) vanishes on
both covering \(q\) for \(k\le 8\); rest10 census on \(k\le 10\);
\(J\) closed form on \(k\le 6\)).
`KILLED` (dies at \(k=9\); dies at \(k=10\); equals rest; equals
NN \(T\)-cell \(G(j+1)\); equals NO outer \(T\)-cell \(G(j+1)\);
equals MV inner even vanish; vanishes; empty; pointwise \(0\);
identically \(1\) on \(q=6\); the form for all \(k\); unique-rest
xor equals \(J\); leftover equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_nr.md` (this note)
- `research/cycle_nr.py`
- `research/cycle_nr.json`
