# Cycle NB: on \(q=10\) for \(k\le 10\), NA Green-only two-piece xor equals rest

On covering \(J_{10}\) through \(k\le 10\), XOR of \(G(n,j+1)\) over
palindrome-right cells with \((j-n)\bmod 3=1\) and \(G(n,j-1)=0\),
xor XOR of \(G(n,j-1)\) over palindrome-right cells with
\(n<U/2\) (\(p=T-2j\ge 0\); no packed row) equals rest. Prefix
Cycle NA for \(k\le 8\); walk \(k=9\) and \(k=10\). This is **not**
a death at \(k=9\) (xor \(=0=\) rest), **not** a death at
\(k=10\), **not** \(S\) alone (\(k=2\): \(S=0\), rest \(=1\)),
**not** \(T\) alone (\(k=8\): \(T=0\), rest \(=1\)), **not** the
form on \(q=6\), and **not** the form for all \(k\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. This is
Green-only rest on the certified range \(q=10\), \(k\le 10\); do
**not** claim the form on \(q=6\), and do **not** claim Green-only
rest for all \(k\). Do **not** record unique-slot XOR vs \(J\).

Certify: `python3 research/cycle_nb.py --certify` (~8.72s).
Dump: `research/cycle_nb.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/NA/MD (packed-free covering \(q=10\) for \(k=9,10\);
prefix NA Green-only rest on \(k\le 8\) and MD rest10; no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (Green-only rest through \(k\le 10\))

Covering \(q=10\), \(k\le 10\). Cycle NA's \(S\oplus T\) equals
rest at \(k=9\) and \(k=10\) (both \(0\)). The walk does not read
the packed row. Together with Cycle NA that is Green-only rest on
the full Cycle MD rest10 range.

## Killed

Dies at \(k=9\): xor \(=0=\) rest. Dies at \(k=10\): xor \(=0=\)
rest. \(S\) alone equals rest through \(k\le 10\): \(k=2\) is
\(0\) vs \(1\). \(T\) alone equals rest through \(k\le 10\):
\(k=8\) is \(0\) vs \(1\). Empty at \(k=9\): \(n_S=29820\). The
form on \(q=6\). The form for all \(k\).

## Verdict

`LEMMA` (Green-only \(S\oplus T\) equals rest on \(q=10\) for
\(k\le 10\); Cycle NA Green-only rest on \(k\le 8\); rest10 census
on \(k\le 10\); \(J\) closed form on \(k\le 6\)).
`KILLED` (dies at \(k=9\); dies at \(k=10\); \(S\) alone; \(T\)
alone; empty at \(k=9\); the form on \(q=6\); the form for all
\(k\); unique-rest xor equals \(J\); leftover equals rest on both
\(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_nb.md` (this note)
- `research/cycle_nb.py`
- `research/cycle_nb.json`
