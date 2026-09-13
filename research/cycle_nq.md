# Cycle NQ: on both covering \(q\) through \(k\le 10\), \(T\)-cell \(d\bmod 3=1\) \(G(j+1)\) is \(1\) iff \(k>2\) and \(k\) is even

On covering \(J_6,J_{10}\) through \(k\le 10\), XOR of \(G(n,j+1)\)
over palindrome-right \(G=1\) cells with \(n<U/2\) and
\(d=j-n\equiv 1\pmod{3}\) (\(p=T-2j\ge 0\); no packed row) is \(1\)
iff \(k>2\) and \(k\) is even. Residue split of Cycle NN's
\(T\)-cell \(G(j+1)\) after Cycle NP's odd-\(d\) vanish. Prefix NN
\(n_T\) / \(\mathrm{xor}_{jp1}\) and NP \(\mathrm{xor}_{odd}\) for
\(k\le 8\); walk \(k=9\) and \(k=10\) on \(q=10\). The \(k=10\) bit
is nontrivial (\(1=1\)). This is **not** a death at \(k=9\),
**not** a death at \(k=10\), **not** NN \(G(j+1)\) (\(k=3\): \(0\)
vs \(1\)), **not** NP vanish (\(k=4\): \(1\) vs \(0\)), **not**
\(T\) (\(k=4\): \(1\) vs \(0\)), **not** rest (\(k=4\), \(q=10\):
\(1\) vs \(0\)), **not** NO outer \(G(j+1)\) (\(k=3\): \(0\) vs
\(1\)), **not** identically \(0\), **not** identically \(1\),
**not** empty (\(k=2\): \(n_{d31}=1\)), **not** pointwise \(0\)
(\(k=4\): \(n_{d31,G(j+1)=1}=1\)), **not** a death on \(q=6\),
**not** \(T\)-cell \(d\bmod 3=0\) as a standalone cycle (same xor),
**not** \(T\)-cell \(d\bmod 3=2\) as a standalone cycle, and
**not** the form for all \(k\). Do **not** claim \(T\) is \(1\)
iff \(k=2\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim Green-only rest for all \(k\). Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_nq.py --certify` (~8.47s).
Dump: `research/cycle_nq.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/MJ/NN/NP/NO (packed-free covering both \(q\) for
\(k\le 8\) and \(q=10\) for \(k=9,10\); prefix NN \(T\)-cell
\(G(j+1)\) and NP odd-\(d\) vanish; no Fermat table, no extra
window, no \(n_0=16\) window).

## Lemma (\(T\)-cell \(d\bmod 3=1\) \(G(j+1)\) is \(1\) iff \(k>2\) and \(k\) is even)

Both covering \(q\), \(k\le 10\). The walk does not read the packed
row. Same cells as Cycle NN's \(T\), restricted to \(d\bmod 3=1\).
At \(k=2\) the unique \(d\bmod 3=1\) cell has \(G(j+1)=0\). At
\(k=4\), \(n_{d31}=8\) and \(G(j+1)\) fires once. At \(k=10\),
\(n_{d31}=7780\) and \(n_{d31,G(j+1)=1}=2573\).

## Killed

Dies at \(k=9\): xor \(=0=\) want. Dies at \(k=10\): xor \(=1=\)
want. Equals NN \(G(j+1)\): \(k=3\) is \(0\) vs \(1\). Equals NP
vanish: \(k=4\) is \(1\) vs \(0\). Equals \(T\): \(k=4\) is \(1\)
vs \(0\). Equals rest: \(k=4\), \(q=10\) is \(1\) vs \(0\). Equals
NO outer \(G(j+1)\): \(k=3\) is \(0\) vs \(1\). Vanishes: \(k=4\)
is \(1\). Identically \(1\): \(k=2\) is \(0\). Empty: \(k=2\) has
\(n_{d31}=1\). Pointwise \(0\): \(k=4\) has
\(n_{d31,G(j+1)=1}=1\). Dies on \(q=6\): \(k=4\) xor \(=1=\) want.
The form for all \(k\).

## Verdict

`LEMMA` (\(T\)-cell \(d\bmod 3=1\) \(G(j+1)\) is \(1\) iff \(k>2\)
and \(k\) is even on both covering \(q\) for \(k\le 10\);
\(T\)-cell \(G(j+1)\) is \(1\) iff \(k>2\); odd-\(d\) \(T\)-cell
\(G(j+1)\) vanishes; rest10 census on \(k\le 10\); \(J\) closed
form on \(k\le 6\)).
`KILLED` (dies at \(k=9\); dies at \(k=10\); equals NN \(G(j+1)\);
equals NP vanish; equals \(T\); equals rest; equals NO outer
\(G(j+1)\); vanishes; identically \(1\); empty; pointwise \(0\);
dies on \(q=6\); the form for all \(k\); unique-rest xor equals
\(J\); leftover equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_nq.md` (this note)
- `research/cycle_nq.py`
- `research/cycle_nq.json`
