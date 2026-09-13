# Cycle NP: on both covering \(q\) through \(k\le 10\), odd-\(d\) \(T\)-cell \(G(j+1)\) vanishes

On covering \(J_6,J_{10}\) through \(k\le 10\), XOR of \(G(n,j+1)\)
over palindrome-right \(G=1\) cells with \(n<U/2\) and \(d=j-n\)
odd (\(p=T-2j\ge 0\); no packed row) is \(0\). So Cycle NN's
\(T\)-cell \(G(j+1)\) xor lives on even \(d\). Prefix NN \(n_T\) /
\(\mathrm{xor}_{jp1}\) and NO outer \(G(j+1)\) for \(k\le 8\); walk
\(k=9\) and \(k=10\) on \(q=10\). The \(k=9\) and \(k=10\) bits
match want \(0\) on a nonempty slice. This is **not** a death at
\(k=9\), **not** a death at \(k=10\), **not** NN \(G(j+1)\)
(\(k=3\): \(0\) vs \(1\)), **not** \(T\) (\(k=2\): \(0\) vs \(1\)),
**not** outer \(T\) (\(k=2\): \(0\) vs \(1\)), **not** inner \(T\)
(\(k=5\): \(0\) vs \(1\)), **not** rest (\(k=2\), \(q=10\): \(0\)
vs \(1\)), **not** NO outer \(G(j+1)\) (\(k=3\): \(0\) vs \(1\)),
**not** identically \(1\), **not** empty (\(k=2\):
\(n_{\mathrm{odd}}=1\)), **not** pointwise \(0\) (\(k=4\):
\(n_{\mathrm{odd},G(j+1)=1}=2\)), **not** a death on \(q=6\),
**not** even-\(d\) as a standalone cycle (tautology of this vanish
plus NN), and **not** the form for all \(k\). Do **not** claim
\(T\) is \(1\) iff \(k=2\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim Green-only rest for all \(k\). Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_np.py --certify` (~8.52s).
Dump: `research/cycle_np.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/MJ/NN/NO/NF/NG (packed-free covering both \(q\) for
\(k\le 8\) and \(q=10\) for \(k=9,10\); prefix NN \(T\)-cell
\(G(j+1)\) and NO outer \(G(j+1)\); no Fermat table, no extra
window, no \(n_0=16\) window).

## Lemma (odd-\(d\) \(T\)-cell \(G(j+1)\) vanishes)

Both covering \(q\), \(k\le 10\). The walk does not read the packed
row. Same cells as Cycle NN's \(T\), restricted to odd \(d\). At
\(k=2\) the unique \(T\) cell is odd-\(d\) with \(G(j+1)=0\). At
\(k=4\), \(n_{\mathrm{odd}}=8\) and \(G(j+1)\) fires twice. At
\(k=9\), \(n_{\mathrm{odd}}=2688\) and \(n_{\mathrm{odd},G(j+1)=1}=1280\).

## Killed

Dies at \(k=9\): xor \(=0=\) want. Dies at \(k=10\): xor \(=0=\)
want. Equals NN \(G(j+1)\): \(k=3\) is \(0\) vs \(1\). Equals
\(T\): \(k=2\) is \(0\) vs \(1\). Equals outer \(T\): \(k=2\) is
\(0\) vs \(1\). Equals inner \(T\): \(k=5\) is \(0\) vs \(1\).
Equals rest: \(k=2\), \(q=10\) is \(0\) vs \(1\). Equals NO outer
\(G(j+1)\): \(k=3\) is \(0\) vs \(1\). Equals even-\(d\): \(k=3\)
is \(0\) vs \(1\). Identically \(1\): \(k=2\) is \(0\). Empty:
\(k=2\) has \(n_{\mathrm{odd}}=1\). Pointwise \(0\): \(k=4\) has
\(n_{\mathrm{odd},G(j+1)=1}=2\). Dies on \(q=6\): \(k=4\) xor
\(=0=\) want. The form for all \(k\).

## Verdict

`LEMMA` (odd-\(d\) \(T\)-cell \(G(j+1)\) vanishes on both covering
\(q\) for \(k\le 10\); \(T\)-cell \(G(j+1)\) is \(1\) iff \(k>2\);
outer \(T\)-cell \(G(j+1)\) is \(1\) iff \(k>0\) and
\(k\bmod 3=0\); rest10 census on \(k\le 10\); \(J\) closed form on
\(k\le 6\)).
`KILLED` (dies at \(k=9\); dies at \(k=10\); equals NN \(G(j+1)\);
equals \(T\); equals outer \(T\); equals inner \(T\); equals rest;
equals NO outer \(G(j+1)\); equals even-\(d\); identically \(1\);
empty; pointwise \(0\); dies on \(q=6\); the form for all \(k\);
unique-rest xor equals \(J\); leftover equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_np.md` (this note)
- `research/cycle_np.py`
- `research/cycle_np.json`
