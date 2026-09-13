# Cycle MR: on \(q=6\) and \(q=10\) for \(k\le 8\), palindrome-right \(d\bmod 3=0\) xor of \(G(n,j-1)\) is \(1\) iff \(k\bmod 4\in\{1,2\}\)

On covering \(J_6,J_{10}\) for \(k\le 8\), XOR of \(G(n,j-1)\) over
covering \(G=1\) cells with \(j>n\) and \((j-n)\bmod 3=0\)
(\(p=T-2j\ge 0\); no packed row) is \(1\) iff \(k\bmod 4\in\{1,2\}\).
Holds on both covering \(q\). Dual of Cycle MM's \(d\bmod 3=1\)
\(G(j-1)\) and Cycle MQ's \(d\bmod 3=1\) \(G(j+1)\) (those two are
\(q=10\) only). This is **not** rest (\(k=1\): d30 \(=1\), rest
\(=0\)), **not** identically \(0\), **not** Green d31, **not** MQ
\(G(j+1)\) on \(q=6\) (\(k=1\): d30 \(=1\), MQ jp1 \(=0\)), **not**
empty on \(q=10\) (\(k=1\): \(n_{d30}=3\)), **not** Green-only rest,
and **not** the form for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim a Green-only formula for rest. Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_mr.py --certify`.
Dump: `research/cycle_mr.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/MM/MQ (packed-free covering both \(q\) for \(k\le 8\);
prefix MM \(G(j-1)\) d31 and MQ \(G(j+1)\) d31; \(k=1\), \(q=6\)
MQ-unequal kill; no Fermat table, no extra window, no \(n_0=16\)
window).

## Lemma (palindrome-right \(d\bmod 3=0\) xor of \(G(n,j-1)\) is \(1\) iff \(k\bmod 4\in\{1,2\}\))

Covering \(q=6\) and \(q=10\), \(k\le 8\). The walk does not read
the packed row. Same \((k\bmod 4)\) form as Cycle MQ on \(q=10\),
but this xor also holds on \(q=6\).

## Killed

d30 xor equals rest: \(k=1\), \(q=10\) is \(1\) vs \(0\). That xor
vanishes: \(k=1\) both \(q\) are \(1\). Equals Green d31: \(k=0\),
\(q=10\) has d30 \(=0\) and d31 \(=1\). Equals MQ \(G(j+1)\) d31
on \(q=6\): \(k=1\) d30 \(=1\) and MQ jp1 \(=0\). Empty on
\(q=10\): \(k=1\) has \(n_{d30}=3\). Green-only rest: this xor is
not rest.

## Verdict

`LEMMA` (palindrome-right \(d\bmod 3=0\) xor of \(G(n,j-1)\) is
\(1\) iff \(k\bmod 4\in\{1,2\}\) on both covering \(q\) for
\(k\le 8\); palindrome-right \(d\bmod 3=1\) xor of \(G(n,j+1)\) is
that form on \(q=10\); Green d31 \(G(j-1)\) is \(1\) iff
\(k\bmod 4=0\); rest10 census on \(k\le 10\); \(J\) closed form on
\(k\le 6\)).
`KILLED` (d30 xor equals rest; d30 xor vanishes; d30 equals Green
d31; d30 equals MQ \(G(j+1)\) on \(q=6\); d30 empty on \(q=10\);
Green-only rest; the form for all \(k\); unique-rest xor equals
\(J\); leftover equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_mr.md` (this note)
- `research/cycle_mr.py`
- `research/cycle_mr.json`
