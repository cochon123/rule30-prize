# Cycle OM: pal-right \(S\) on \(n=8t+7\) equals \(S(2t+1)\)

If \(n=8t+7\), then \(n=4s+3\) with \(s=2t+1\) odd. Palindrome-right
\(S(4s+3)=S(s)\) through \(t<128\) (\(n\le 1023\)). Each fold
strictly decreases the odd argument, so every \(n\equiv 7\pmod{8}\)
below that bound reduces to Cycle OL’s even-parent residue xor or
to an \(n=8u+3\) off-residue-\(0\) row.

This is **not** \(S(8t+7)=0\) (\(t=4\), \(n=39\): xor \(=1\)),
**not** \(S(8t+7)=S(8t+3)\) (\(n=23\) is \(0\), \(n=19\) is \(1\)),
and **not** the fold for all \(t\). Do **not** claim a closed
odd-\(n\) \(S\) without the fold. Do **not** claim \(E_k=0\) for all
\(k\). Do **not** catalogue further \(S\)/\(T\) subregions unless
the experiment answers why \(E_k=0\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\). Do **not** walk \(k=11\) covering packed. Do
**not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).

Certify: `python3 research/cycle_om.py --certify`.
Dump: `research/cycle_om.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OK/OL/OJ/OG (fold \(S(8t+7)=S(2t+1)\); prefix OL even-parent
and \(n=8t+3\), OJ covering \(T_k\), OG \(E_k\); no Fermat table,
no extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Certificate (\(S(8t+7)=S(2t+1)\) for \(t<128\))

Green doubling of \(n=2(2s+1)+1\) with odd \(s\) maps pal-right
\(S\)-cells of \(s\) into the child; the identity holds on
\(t=0,\ldots,127\). At \(t=0\), \(S(7)=S(1)=0\). At \(t=4\),
\(S(39)=S(9)=1\). Status: **certified** on this range, not a lemma
for all \(t\).

## Killed

\(S(8t+7)=0\): \(n=39\) has xor \(=1\). Equals the \(n=8t+3\) class:
\(S(23)=0\) and \(S(19)=1\). The fold for all \(t\). Closed odd-\(n\)
\(S\) without the fold. \(E_k=0\) for all \(k\).

## Verdict

`LEMMA` (even-parent residue xor; \(n=8t+3\) pal-right off residue
\(0\); covering \(T_k=1\) iff \(k=2\)).
`CERTIFIED` (\(S(8t+7)=S(2t+1)\) for \(t<128\); \(E_k=0\) on
odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (\(S(8t+7)=0\); \(S(8t+7)=S(8t+3)\)).
`PREFIX` (fold for all \(t\); closed odd-\(n\) \(S\); \(E_k=0\) for
all \(k\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all
\(k\); seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_om.md` (this note)
- `research/cycle_om.py`
- `research/cycle_om.json`
