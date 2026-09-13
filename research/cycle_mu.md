# Cycle MU: on \(q=6\) for \(k\le 8\), palindrome-right even-\(d\) xor of \(G(n,j+1)\) on \(G=1\) is \(1\) iff \(k\) odd

On covering \(J_6\) for \(k\le 8\), XOR of \(G(n,j+1)\) over covering
\(G=1\) cells with \(j>n\) and \((j-n)\) even (\(p=T-2j\ge 0\); no
packed row) is \(1\) iff \(k\) is odd. Dual of Cycle MT's even-\(d\)
\(G(j-1)\) vanish. This is **not** rest (\(k=1\), \(q=6\): jp1
\(=1\), rest \(=0\)), **not** identically \(0\), **not** \(j>n\)
even-\(k\), **not** MT vanish, **not** \(k\) odd on \(q=10\)
(\(k=0\) jp1 \(=1\)), **not** Green-only rest, and **not** the form
for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim a Green-only formula for rest. Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_mu.py --certify` (~0.23s).
Dump: `research/cycle_mu.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/MJ/MT (packed-free covering \(q=6\) for \(k\le 8\);
prefix MT even-\(d\) \(G(j-1)\) vanish and MJ \(j>n\); \(k=0\),
\(q=10\) kill; no Fermat table, no extra window, no \(n_0=16\)
window).

## Lemma (palindrome-right even-\(d\) xor of \(G(n,j+1)\) is \(1\) iff \(k\) odd)

Covering \(q=6\), \(k\le 8\). The walk does not read the packed
row.

## Killed

Even-\(d\) \(G(j+1)\) xor equals rest: \(k=1\), \(q=6\) is \(1\) vs
\(0\). Vanishes on \(q=6\): \(k=1\) is \(1\). Equals \(j>n\)
even-\(k\): \(k=1\) jp1 \(=1\) and jgtn \(=0\). Equals MT
\(G(j-1)\) vanish: \(k=1\) jp1 \(=1\) and jm1 \(=0\). The \(k\)-odd
form on \(q=10\): \(k=0\) jp1 \(=1\). Green-only rest: this xor is
not rest.

## Verdict

`LEMMA` (palindrome-right even-\(d\) xor of \(G(n,j+1)\) is \(1\)
iff \(k\) odd on \(q=6\) for \(k\le 8\); even-\(d\) \(G(j-1)\) xor
vanishes on \(q=6\); \(j>n\) xor is \(1\) iff \(k\) even on both
covering \(q\); rest10 census on \(k\le 10\); \(J\) closed form on
\(k\le 6\)).
`KILLED` (even-\(d\) \(G(j+1)\) equals rest; even-\(d\) \(G(j+1)\)
vanishes; even-\(d\) \(G(j+1)\) equals jgtn; even-\(d\) \(G(j+1)\)
equals MT vanish; \(k\)-odd form on \(q=10\); Green-only rest; the
form for all \(k\); unique-rest xor equals \(J\); leftover equals
rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_mu.md` (this note)
- `research/cycle_mu.py`
- `research/cycle_mu.json`
