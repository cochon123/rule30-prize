# Cycle MS: on \(q=6\) for \(k\le 8\), palindrome-right \(d\bmod 3=1\) xor of \(G(n,j-1)\) is \(1\) iff \(k\bmod 4\in\{0,1,2\}\)

On covering \(J_6\) for \(k\le 8\), XOR of \(G(n,j-1)\) over covering
\(G=1\) cells with \(j>n\) and \((j-n)\bmod 3=1\) (\(p=T-2j\ge 0\);
no packed row) is \(1\) iff \(k\bmod 4\in\{0,1,2\}\). Companion of
Cycle MM's \(q=10\) d31 \(=1_{k\bmod 4=0}\). This is **not** rest
(\(q=6\) rest \(=0\), \(k=0\) xor \(=1\)), **not** the MM form
(\(k=1\): xor \(=1\), \(\mathrm{want}_{d31}=0\)), **not** Cycle MR
d30 (\(k=0\): d31 \(=1\), d30 \(=0\)), **not** \(j>n\) even-\(k\)
(\(k=1\): d31 \(=1\), jgtn \(=0\)), **not** the \(\{0,1,2\}\) form
on \(q=10\) (\(k=1\) d31 \(=0\)), **not** Green-only rest, and
**not** the form for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim a Green-only formula for rest. Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_ms.py --certify`.
Dump: `research/cycle_ms.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/MM/MJ/MR (packed-free covering \(q=6\) for \(k\le 8\);
prefix MR q=6 walk sizes and MM \(q=10\) d31 kill; no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (palindrome-right \(d\bmod 3=1\) xor of \(G(n,j-1)\) is \(1\) iff \(k\bmod 4\in\{0,1,2\}\))

Covering \(q=6\), \(k\le 8\). The walk does not read the packed
row.

## Killed

q=6 d31 xor equals rest: \(k=0\) is \(1\) vs \(0\). Equals MM
\(k\bmod 4=0\): \(k=1\) is \(1\) vs \(0\). Equals MR d30: \(k=0\)
d31 \(=1\) and d30 \(=0\). Equals \(j>n\) even-\(k\): \(k=1\) d31
\(=1\) and jgtn \(=0\). The \(\{0,1,2\}\) form on \(q=10\):
\(k=1\) d31 \(=0\). Green-only rest: this xor is not rest.

## Verdict

`LEMMA` (palindrome-right \(d\bmod 3=1\) xor of \(G(n,j-1)\) is
\(1\) iff \(k\bmod 4\in\{0,1,2\}\) on \(q=6\) for \(k\le 8\);
d30 xor is \(1\) iff \(k\bmod 4\in\{1,2\}\) on both covering \(q\);
Green d31 is \(1\) iff \(k\bmod 4=0\) on \(q=10\); \(j>n\) xor is
\(1\) iff \(k\) even on both covering \(q\); rest10 census on
\(k\le 10\); \(J\) closed form on \(k\le 6\)).
`KILLED` (q=6 d31 equals rest; q=6 d31 equals MM form; q=6 d31
equals d30; q=6 d31 equals jgtn; \(\{0,1,2\}\) form on \(q=10\);
Green-only rest; the form for all \(k\); unique-rest xor equals
\(J\); leftover equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ms.md` (this note)
- `research/cycle_ms.py`
- `research/cycle_ms.json`
