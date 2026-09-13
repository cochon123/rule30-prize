# Cycle MP: on \(q=10\) for \(k\le 8\), leftover AND xor of \(G(n,j-1)\) on \(j>n\) with \(d\bmod 3=1\) equals rest

On covering \(J_{10}\) for \(k\le 8\), XOR of \(G(n,j-1)\) on leftover
packed AND (\(G=1\), \(p\) off \(\{4,6,14\}\) and the LC–LU unique-rest
slots) with \(j>n\) and \((j-n)\bmod 3=1\) equals rest. Dual of Cycle
MM's Green \(d31=1_{k\bmod 4=0}\) and Cycle MO's leftover AND d31
(\(1\) iff \(k\bmod 4\in\{2,3\}\)). This is **not** leftover AND d31
xor (\(k=3\): \(0\) vs \(1\); \(k=8\): \(1\) vs \(0\)), **not** Green
d31, **not** leftover all \(G(j-1)\) (\(k=3\): all \(=1\), d31
\(=0\)), **not** rest on \(q=6\) (\(k=5\) leftover d31 \(G(j-1)=1\)),
**not** Green-only rest, and **not** the form for all \(k\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim a Green-only formula for rest. Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_mp.py --certify` (~1.59s).
Dump: `research/cycle_mp.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/MD/ME/MM/MO (covering \(q=10\) for \(k\le 8\); prefix ME
leftover=rest and MO leftover AND d31; \(k=5\), \(q=6\) kill; no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (leftover palindrome-right \(d\bmod 3=1\) xor of \(G(n,j-1)\) equals rest)

Covering \(q=10\), \(k\le 8\). Leftover means packed AND on \(G=1\)
off \(\{p=4,p=6,p=14\}\) and off `UNIQUE_REST`.

## Killed

Leftover d31 \(G(j-1)\) xor equals leftover AND d31 xor: \(k=3\) is
\(0\) vs \(1\) and \(k=8\) is \(1\) vs \(0\). Equals Green d31:
\(k=2\) leftover \(=1\) and Green \(=0\). Leftover all \(G(j-1)\)
equals rest: \(k=3\) all \(=1\) while d31 \(=0\). The rest form on
\(q=6\): \(k=5\), \(q=6\) leftover d31 \(G(j-1)=1\). Green-only
rest: leftover still reads the packed row.

## Verdict

`LEMMA` (leftover palindrome-right \(d\bmod 3=1\) xor of
\(G(n,j-1)\) equals rest on \(q=10\) for \(k\le 8\); leftover AND
d31 is \(1\) iff \(k\bmod 4\in\{2,3\}\); Green d31 is \(1\) iff
\(k\bmod 4=0\); \(q=10\) leftover split on \(k\le 8\); rest10 census
on \(k\le 10\); \(J\) closed form on \(k\le 6\)).
`KILLED` (leftover d31 \(G(j-1)\) equals leftover AND d31; leftover
d31 \(G(j-1)\) equals Green d31; leftover all \(G(j-1)\) equals
rest; rest form on \(q=6\); Green-only rest; the form for all
\(k\); unique-rest xor equals \(J\); leftover equals rest on both
\(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_mp.md` (this note)
- `research/cycle_mp.py`
- `research/cycle_mp.json`
