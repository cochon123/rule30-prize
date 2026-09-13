# Cycle NA: on \(q=10\) for \(k\le 8\), Green-only \((d31\ G(j+1)\) on \(G(j-1)=0)\) xor (palindrome-right \(G(j-1)\) on \(n<U/2)\) equals rest

On covering \(J_{10}\) for \(k\le 8\), XOR of \(G(n,j+1)\) over
palindrome-right cells with \((j-n)\bmod 3=1\) and \(G(n,j-1)=0\),
xor XOR of \(G(n,j-1)\) over palindrome-right cells with
\(n<U/2\) (\(p=T-2j\ge 0\); no packed row) equals rest. This closes
Cycle MN's \(k=8\) proxy miss. This is **not** MN proxy (\(k=8\):
xor \(=1\), proxy \(=0\)), **not** \(j>n\) even-\(k\), **not** Green
d31, **not** identically \(0\), **not** empty (\(k=2\):
\(n_T=1\)), **not** the form on \(q=6\) (\(k=2\) xor \(=1\), rest
\(=0\)), and **not** the form for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
record unique-slot XOR vs \(J\).

Certify: `python3 research/cycle_na.py --certify`.
Dump: `research/cycle_na.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/MJ/MM/MN/MZ (packed-free covering \(q=10\) for \(k\le 8\);
prefix MN proxy-except-\(k=8\) and MJ \(j>n\); \(k=2\), \(q=6\)
kill; no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (Green-only rest)

Covering \(q=10\), \(k\le 8\). Let \(S\) be the XOR of \(G(n,j+1)\)
on palindrome-right \(d\bmod 3=1\) cells with \(G(n,j-1)=0\), and
let \(T\) be the XOR of \(G(n,j-1)\) on palindrome-right cells with
\(n<U/2\). Then \(S\oplus T\) equals rest. The walk does not read
the packed row. At \(k=8\), \(S=1\) and \(T=0\) close MN's proxy
miss; at \(k=2\), \(S=0\) and \(T=1\).

## Killed

Equals MN proxy: \(k=8\) is \(1\) vs \(0\). Equals \(j>n\)
even-\(k\): \(k=0\) is \(0\) vs \(1\). Equals Green d31: \(k=0\) is
\(0\) vs \(1\). Vanishes: \(k=2\) is \(1\). \(n<U/2\) empty:
\(k=2\) has \(n_T=1\). The form on \(q=6\): \(k=2\) xor \(=1\) and
rest \(=0\). The form for all \(k\).

## Verdict

`LEMMA` (Green-only \(S\oplus T\) equals rest on \(q=10\) for
\(k\le 8\); MN proxy equals rest except \(k=8\); inner \(G=1\)
count is odd iff \(k\) odd on \(q=10\); \(j>n\) xor is \(1\) iff
\(k\) even on both covering \(q\); rest10 census on \(k\le 10\);
\(J\) closed form on \(k\le 6\)).
`KILLED` (equals MN proxy; equals jgtn; equals Green d31;
vanishes; \(n<U/2\) empty; the form on \(q=6\); the form for all
\(k\); unique-rest xor equals \(J\); leftover equals rest on both
\(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_na.md` (this note)
- `research/cycle_na.py`
- `research/cycle_na.json`
