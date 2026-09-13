# Cycle NG: on \(q=6\) and \(q=10\) for \(k\le 8\), inner NA \(T\) xor of \(G(n,j-1)\) is \(1\) iff \(k>2\) and \(k\bmod 3=2\)

On covering \(J_6,J_{10}\) for \(k\le 8\), XOR of \(G(n,j-1)\) over
palindrome-right \(G=1\) cells with \(n<U/2\) and \(j\le n+\lfloor n/2\rfloor\)
(\(p=T-2j\ge 0\); no packed row) is \(1\) iff \(k>2\) and
\(k\bmod 3=2\). Both covering \(q\) agree on xor and on
\(n_{\mathrm{in}}\). This is the inner slice of Cycle NA's \(T\),
the companion of Cycle NF's outer \(k\bmod 3=2\) form. This is
**not** \(T\) (\(k=5\): xor \(=1\), \(T=0\)), **not** rest
(\(k=5\), \(q=10\): \(1\) vs \(0\)), **not** outer \(T\)
(\(k=2\): \(0\) vs \(1\)), **not** identically \(0\), **not**
empty (\(k=4\): \(n_{\mathrm{in}}=3\)), **not** Green-only rest,
and **not** the form for all \(k\). Do **not** claim \(T\) is
\(1\) iff \(k=2\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim Green-only rest for all \(k\). Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_ng.py --certify`.
Dump: `research/cycle_ng.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/MJ/NA/NF (packed-free covering both \(q\) for \(k\le 8\);
prefix NF outer \(T\), NA \(T\), and MJ \(j>n\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (inner \(T\) is \(1\) iff \(k>2\) and \(k\bmod 3=2\))

Both covering \(q\), \(k\le 8\). The walk does not read the packed
row. At \(k=2\), inner is empty. At \(k=4\), inner is nonempty with
xor \(=0\). The inner counts agree on \(q=6\) and \(q=10\).

## Killed

Equals \(T\): \(k=5\) is \(1\) vs \(0\). Equals rest: \(k=5\),
\(q=10\) is \(1\) vs \(0\). Equals outer \(T\): \(k=2\) is \(0\) vs
\(1\). Vanishes: \(k=5\) is \(1\). Empty: \(k=4\) has
\(n_{\mathrm{in}}=3\). Dies on \(q=6\): \(k=5\) xor \(=1\) equals
the form. \(T\) is \(1\) iff \(k=2\). The form for all \(k\).

## Verdict

`LEMMA` (inner palindrome-right \(n<U/2\) xor of \(G(j-1)\) is \(1\)
iff \(k>2\) and \(k\bmod 3=2\) on both covering \(q\) for \(k\le 8\);
outer \(T\) is \(1\) iff \(k\bmod 3=2\); Green-only rest on
\(q=10\) for \(k\le 8\); \(j>n\) xor is \(1\) iff \(k\) even; rest10
census on \(k\le 10\); \(J\) closed form on \(k\le 6\)).
`KILLED` (equals \(T\); equals rest; equals outer \(T\); vanishes;
empty; dies on \(q=6\); \(T\) iff \(k=2\); the form for all \(k\);
unique-rest xor equals \(J\); leftover equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ng.md` (this note)
- `research/cycle_ng.py`
- `research/cycle_ng.json`
