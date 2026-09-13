# Cycle NK: on \(q=10\) through \(k\le 10\), NI \(S\) on \(2U\le n<5U/2\) is \(1\) iff \(k\bmod 4\in\{2,3\}\)

On covering \(J_{10}\) through \(k\le 10\), XOR of \(G(n,j+1)\) over
palindrome-right cells with \((j-n)\bmod 3=1\), \(G(n,j-1)=0\), and
\(2U\le n<5U/2\) (\(p=T-2j\ge 0\); no packed row) is \(1\) iff
\(k\bmod 4\in\{2,3\}\). Prefix Cycle NI for \(k\le 8\); walk
\(k=9\) and \(k=10\). This is **not** a death at \(k=9\) (xor
\(=0=\) want), **not** a death at \(k=10\) (xor \(=1=\) want; the
nontrivial lift), **not** Cycle NH through \(k\le 10\) (dies at
\(k=9\): xor \(=1\), want \(=0\)), **not** Cycle NJ through
\(k\le 10\) (dies at \(k=9\): xor \(=1\), want \(=0\)), **not**
rest (\(k=10\): xor \(=1\), rest \(=0\)), **not** NE high
(\(k=10\): \(1\) vs \(0\)), **not** empty (\(k=9\):
\(n_{\mathrm{lo}}=4372\)), **not** the form on \(q=6\), and
**not** the form for all \(k\). Do **not** claim \(T\) is \(1\)
iff \(k=2\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim Green-only rest for all \(k\). Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_nk.py --certify`.
Dump: `research/cycle_nk.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/NI/NJ/NH/NE/MD (packed-free covering \(q=10\) for
\(k=9,10\); prefix NI \(2U\le n<5U/2\) on \(k\le 8\); no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (\(S\) on \(2U\le n<5U/2\) is \(1\) iff \(k\bmod 4\in\{2,3\}\) through \(k\le 10\))

Covering \(q=10\), \(k\le 10\). Cycle NI's form holds at \(k=9\)
(\(0=0\)) and \(k=10\) (\(1=1\)). The walk does not read the packed
row. Together with Cycle NI that is the \(2U\le n<5U/2\) slice of
NA \(S\) on the full Cycle MD rest10 range. Cycle NH's
\(k\bmod 3=2\) form and Cycle NJ's \(k\bmod 8\in\{5,6\}\) form both
die at \(k=9\).

## Killed

Dies at \(k=9\): xor \(=0=\) want. Dies at \(k=10\): xor \(=1=\)
want. NH through \(k\le 10\): \(k=9\) is \(1\) vs \(0\). NJ
through \(k\le 10\): \(k=9\) is \(1\) vs \(0\). Equals rest:
\(k=10\), \(q=10\) is \(1\) vs \(0\). Equals NE high: \(k=10\) is
\(1\) vs \(0\). Empty at \(k=9\): \(n_{\mathrm{lo}}=4372\). The
form on \(q=6\). The form for all \(k\).

## Verdict

`LEMMA` (\(S\) on \(2U\le n<5U/2\) is \(1\) iff \(k\bmod 4\in\{2,3\}\)
on \(q=10\) for \(k\le 10\); \(S\) on \(2U\le n<5U/2\) on \(k\le 8\);
\(S\) on \(2U\le n<3U\) is \(1\) iff \(k\bmod 3=2\) on \(k\le 8\);
\(S\) on \(n\ge 7U/2\) is \(1\) iff \(k\bmod 8\in\{5,6\}\) on
\(k\le 8\); high \(S\) is \(1\) iff \(k\bmod 8\in\{4,6\}\) on
\(q=10\); rest10 census on \(k\le 10\); \(J\) closed form on
\(k\le 6\)).
`KILLED` (dies at \(k=9\); dies at \(k=10\); NH through \(k\le 10\);
NJ through \(k\le 10\); equals rest; equals NE high; empty at
\(k=9\); the form on \(q=6\); the form for all \(k\); unique-rest
xor equals \(J\); leftover equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_nk.md` (this note)
- `research/cycle_nk.py`
- `research/cycle_nk.json`
