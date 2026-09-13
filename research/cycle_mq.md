# Cycle MQ: on \(q=10\) for \(k\le 8\), palindrome-right \(d\bmod 3=1\) xor of \(G(n,j+1)\) on \(G=1\) is \(1\) iff \(k\bmod 4\in\{1,2\}\)

On covering \(J_{10}\) for \(k\le 8\), XOR of \(G(n,j+1)\) over
covering \(G=1\) cells with \(j>n\) and \((j-n)\bmod 3=1\)
(\(p=T-2j\ge 0\); no packed row) is \(1\) iff \(k\bmod 4\in\{1,2\}\).
Dual of Cycle MM's Green \(d31=1_{k\bmod 4=0}\) on \(G(n,j-1)\). This
is **not** rest (\(k=1\): jp1 \(=1\), rest \(=0\)), **not**
identically \(0\), **not** \(k\bmod 4\in\{1,2\}\) on \(q=6\)
(\(k=1\), \(q=6\) jp1 \(=0\)), **not** Green d31, **not** leftover
d31 \(G(j-1)\), **not** Green-only rest, and **not** the form for
all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim a Green-only formula for rest. Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_mq.py --certify`.
Dump: `research/cycle_mq.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/MM/MP (packed-free covering \(q=10\) for \(k\le 8\);
prefix MM \(G(j-1)\) d31 and MP leftover \(G(j-1)\) d31; \(k=1\),
\(q=6\) kill; no Fermat table, no extra window, no \(n_0=16\)
window).

## Lemma (palindrome-right \(d\bmod 3=1\) xor of \(G(n,j+1)\) is \(1\) iff \(k\bmod 4\in\{1,2\}\))

Covering \(q=10\), \(k\le 8\). The walk does not read the packed
row.

## Killed

d31 \(G(j+1)\) xor equals rest: \(k=1\), \(q=10\) is \(1\) vs
\(0\). That xor vanishes on \(q=10\): \(k=1\) is \(1\). Equals
Green d31 \(G(j-1)\): \(k=1\) jp1 \(=1\) and jm1 \(=0\). Equals
leftover d31 \(G(j-1)\): leftover is rest, same \(k=1\) cell. The
\(\{1,2\}\) form on \(q=6\): \(k=1\), \(q=6\) jp1 \(=0\).
Green-only rest: this xor is not rest.

## Verdict

`LEMMA` (palindrome-right \(d\bmod 3=1\) xor of \(G(n,j+1)\) is
\(1\) iff \(k\bmod 4\in\{1,2\}\) on \(q=10\) for \(k\le 8\);
leftover d31 \(G(j-1)\) equals rest; Green d31 \(G(j-1)\) is \(1\)
iff \(k\bmod 4=0\); rest10 census on \(k\le 10\); \(J\) closed form
on \(k\le 6\)).
`KILLED` (d31 \(G(j+1)\) equals rest; d31 \(G(j+1)\) vanishes; d31
\(G(j+1)\) equals Green d31 \(G(j-1)\); d31 \(G(j+1)\) equals
leftover d31 \(G(j-1)\); \(\{1,2\}\) form on \(q=6\); Green-only
rest; the form for all \(k\); unique-rest xor equals \(J\);
leftover equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_mq.md` (this note)
- `research/cycle_mq.py`
- `research/cycle_mq.json`
