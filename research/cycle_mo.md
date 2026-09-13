# Cycle MO: on \(q=10\) for \(k\le 8\), leftover AND xor on \(j>n\) with \(d\bmod 3=1\) is \(1\) iff \(k\bmod 4\in\{2,3\}\)

On covering \(J_{10}\) for \(k\le 8\), XOR of leftover packed AND
(\(G=1\), \(p\) off \(\{4,6,14\}\) and the LC–LU unique-rest slots)
with \(j>n\) and \((j-n)\bmod 3=1\) is \(1\) iff \(k\bmod 4\in\{2,3\}\).
Dual of Cycle MM's Green \(d31=1_{k\bmod 4=0}\). At \(k=8\) leftover
d31 \(=0\) while Green d31 \(=1\), so Cycle MN's proxy misses rest.
This is **not** rest (\(k=3\): \(1\) vs \(0\); \(k=8\): \(0\) vs
\(1\)), **not** Green d31, **not** \(k\bmod 4\in\{2,3\}\) on
\(q=6\) (\(k=4\) leftover d31 \(=1\)), **not** Green-only rest, and
**not** the form for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim a Green-only formula for rest. Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_mo.py --certify`.
Dump: `research/cycle_mo.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/MD/ME/MM/MN (covering \(q=10\) for \(k\le 8\); prefix ME
leftover=rest and MN proxy; \(k=4\), \(q=6\) kill; no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (leftover palindrome-right \(d\bmod 3=1\) xor is \(1\) iff \(k\bmod 4\in\{2,3\}\))

Covering \(q=10\), \(k\le 8\).

## Killed

Leftover d31 xor equals rest: \(k=3\) is \(1\) vs \(0\) and
\(k=8\) is \(0\) vs \(1\). Equals Green d31: \(k=2\) leftover
\(=1\) and Green \(=0\). The \(\{2,3\}\) form on \(q=6\): \(k=4\),
\(q=6\) leftover d31 \(=1\). Green-only rest: leftover still
reads the packed row.

## Verdict

`LEMMA` (leftover palindrome-right \(d\bmod 3=1\) xor is \(1\) iff
\(k\bmod 4\in\{2,3\}\) on \(q=10\) for \(k\le 8\); Green proxy
equals rest except \(k=8\); Green d31 is \(1\) iff \(k\bmod 4=0\);
\(q=10\) leftover split on \(k\le 8\); rest10 census on
\(k\le 10\); \(J\) closed form on \(k\le 6\)).
`KILLED` (leftover d31 equals rest; leftover d31 equals Green
d31; \(\{2,3\}\) form on \(q=6\); Green-only rest; the form for
all \(k\); unique-rest xor equals \(J\); leftover equals rest on
both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_mo.md` (this note)
- `research/cycle_mo.py`
- `research/cycle_mo.json`
