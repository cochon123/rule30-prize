# Cycle NN: on both covering \(q\) through \(k\le 10\), palindrome-right \(G(j+1)\) on \(n<U/2\) is \(1\) iff \(k>2\)

On covering \(J_6,J_{10}\) through \(k\le 10\), XOR of \(G(n,j+1)\)
over palindrome-right \(G=1\) cells with \(n<U/2\) (\(p=T-2j\ge 0\);
no packed row) is \(1\) iff \(k>2\). Same cells as Cycle NA's \(T\).
Prefix Cycle NF for \(k\le 8\) \(n_T\) / inner / outer; walk \(k=9\)
and \(k=10\) on \(q=10\) (\(T\) cells are \(q\)-independent). The
\(k=9\) and \(k=10\) bits are nontrivial (\(1=1\)). This is **not**
a death at \(k=9\), **not** a death at \(k=10\), **not** \(T\)
(\(k=2\): \(0\) vs \(1\)), **not** rest (\(k=3\), \(q=10\): \(1\)
vs \(0\)), **not** outer \(T\) (\(k=3\): \(1\) vs \(0\)), **not**
inner \(T\) (\(k=3\): \(1\) vs \(0\)), **not** identically \(0\),
**not** identically \(1\), **not** empty (\(k=2\): \(n_T=1\)),
**not** pointwise \(0\) (\(k=3\): \(n_{T,G(j+1)=1}=1\)), **not** a
death on \(q=6\), and **not** the form for all \(k\). Do **not**
claim \(T\) is \(1\) iff \(k=2\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim Green-only rest for all \(k\). Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_nn.py --certify`.
Dump: `research/cycle_nn.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/MJ/NA/NF/NG (packed-free covering both \(q\) for \(k\le 8\)
and \(q=10\) for \(k=9,10\); prefix NF outer \(T\) and NG inner
\(T\); no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (palindrome-right \(G(j+1)\) on \(n<U/2\) is \(1\) iff \(k>2\))

Both covering \(q\), \(k\le 10\). The walk does not read the packed
row. At \(k=2\) the unique \(T\) cell has \(G(j+1)=0\). At \(k=3\),
\(n_T=4\) and \(G(j+1)\) fires once. The two covering \(q\) agree on
xor and on \(n_T\) through \(k\le 8\); \(k=9,10\) use the same
\(n<U/2\) cells as \(q=6\) (never clipped).

## Killed

Dies at \(k=9\): xor \(=1=\) want. Dies at \(k=10\): xor \(=1=\)
want. Equals \(T\): \(k=2\) is \(0\) vs \(1\). Equals rest:
\(k=3\), \(q=10\) is \(1\) vs \(0\). Equals outer \(T\): \(k=3\) is
\(1\) vs \(0\). Equals inner \(T\): \(k=3\) is \(1\) vs \(0\).
Vanishes: \(k=3\) is \(1\). Identically \(1\): \(k=2\) is \(0\).
Empty: \(k=2\) has \(n_T=1\). Pointwise \(0\): \(k=3\) has
\(n_{T,G(j+1)=1}=1\). Dies on \(q=6\): \(k=3\) xor \(=1=\) want.
The form for all \(k\).

## Verdict

`LEMMA` (palindrome-right \(G(j+1)\) on \(n<U/2\) is \(1\) iff
\(k>2\) on both covering \(q\) for \(k\le 10\); outer \(T\) is \(1\)
iff \(k\bmod 3=2\); inner \(T\) is \(1\) iff \(k>2\) and
\(k\bmod 3=2\); Green-only rest on \(q=10\) for \(k\le 8\); rest10
census on \(k\le 10\); \(J\) closed form on \(k\le 6\)).
`KILLED` (dies at \(k=9\); dies at \(k=10\); equals \(T\); equals
rest; equals outer \(T\); equals inner \(T\); vanishes; identically
\(1\); empty; pointwise \(0\); dies on \(q=6\); the form for all
\(k\); unique-rest xor equals \(J\); leftover equals rest on both
\(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_nn.md` (this note)
- `research/cycle_nn.py`
- `research/cycle_nn.json`
