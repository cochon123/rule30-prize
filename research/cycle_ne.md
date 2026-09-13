# Cycle NE: on \(q=10\) for \(k\le 8\), NA's \(S\) on \(n\ge 3U/2\) is \(1\) iff \(k\bmod 8\in\{4,6\}\)

On covering \(J_{10}\) for \(k\le 8\), XOR of \(G(n,j+1)\) over
palindrome-right cells with \((j-n)\bmod 3=1\), \(G(n,j-1)=0\), and
\(n\ge 3U/2\) (\(p=T-2j\ge 0\); no packed row) is \(1\) iff
\(k\bmod 8\in\{4,6\}\). Companion of Cycle NC's \(n<U\) form:
Cycle ND's mid-band vanish leaves this high slice. This is **not**
rest (\(k=4\): xor \(=1\), rest \(=0\)), **not** NC \(n<U\)
(\(k=6\): \(1\) vs \(0\)), **not** NA \(S\) (\(k=4\): \(1\) vs
\(0\)), **not** ND mid (\(k=4\): \(1\) vs \(0\)), **not**
identically \(0\), **not** empty (\(k=2\): \(n_{\mathrm{hi}}=4\)),
**not** the form on \(q=6\) (\(k=3\) xor \(=1\), want \(=0\)),
**not** Green-only rest, and **not** the form for all \(k\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim Green-only rest for all \(k\). Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_ne.py --certify`.
Dump: `research/cycle_ne.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/MJ/ND/NC/NA (packed-free covering \(q=10\) for \(k\le 8\);
prefix ND mid vanish, NC \(n<U\), and NA \(S\); \(k=3\), \(q=6\)
kill; no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (\(S\) on \(n\ge 3U/2\) is \(1\) iff \(k\bmod 8\in\{4,6\}\))

Covering \(q=10\), \(k\le 8\). The walk does not read the packed
row. Together with Cycles NC and ND, Cycle NA's \(S\) on \(q=10\)
is \(1_{k>0,\,k\bmod 4=0}\oplus 1_{k\bmod 8\in\{4,6\}}\).

## Killed

Equals rest: \(k=4\), \(q=10\) is \(1\) vs \(0\). Equals NC
\(n<U\): \(k=6\) is \(1\) vs \(0\). Equals NA \(S\): \(k=4\) is
\(1\) vs \(0\). Equals ND mid: \(k=4\) is \(1\) vs \(0\).
Vanishes: \(k=4\) is \(1\). Empty: \(k=2\) has \(n_{\mathrm{hi}}=4\).
The form on \(q=6\): \(k=3\) xor \(=1\) and want \(=0\). The form
for all \(k\).

## Verdict

`LEMMA` (\(S\) on \(n\ge 3U/2\) is \(1\) iff \(k\bmod 8\in\{4,6\}\)
on \(q=10\) for \(k\le 8\); \(S\) on \(U\le n<3U/2\) vanishes on
both covering \(q\); \(S\) on \(n<U\) is \(1\) iff \(k>0\) and
\(k\bmod 4=0\); Green-only rest on \(q=10\) for \(k\le 8\); rest10
census on \(k\le 10\); \(J\) closed form on \(k\le 6\)).
`KILLED` (equals rest; equals NC \(n<U\); equals NA \(S\); equals
ND mid; vanishes; empty; the form on \(q=6\); the form for all
\(k\); unique-rest xor equals \(J\); leftover equals rest on both
\(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ne.md` (this note)
- `research/cycle_ne.py`
- `research/cycle_ne.json`
