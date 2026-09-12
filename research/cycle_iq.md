# Cycle IQ: consecutive \(G=1\) kind is determined by the parent half-run

On odd \(n=2m+1\), every \(G=1\) pair sits in a half-run image.
Parent run-1 gives left/right of a triple; parent run-2 or run-3
gives isolated pairs. Isolated pairs do **not** come from run-1.
Triples do **not** come from run-2. \(n\equiv 3\pmod{4}\) triples
**do** come from run-1. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: parent-run kind still leaves packed AND on those
pairs and triples, so covering never-fail stays open.

Helper: `g11_parent`. Certify:
`python3 research/cycle_iq.py --certify` (~0.20s).
Dump: `research/cycle_iq.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IN/IP (\(n<64\); covering \(k\le 6\); no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (\(G=1\) kind from parent run length)

For odd \(n<64\), `g11_parent` hits every consecutive \(G=1\) pair.
Parent \(r=1\) is left \(141\) / right \(141\); parent \(r=2\) is
isolated \(140\); parent \(r=3\) is isolated \(90\).

## Lemma (isolated pairs are parent run-2 or run-3)

Iso iff \(r\in\{2,3\}\). Left/right of a triple iff \(r=1\).

## Lemma (covering clocks parent-kind)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): consecutive \(G=1\)
\(8577\) split as parent-\(r=1\) left \(2380\) / right \(2380\),
parent-\(r=2\) iso \(2339\), parent-\(r=3\) iso \(1478\). Odd-\(s\)
\(J\) XOR matches Cycles HF/HG.

## Killed

Isolated pair comes from parent run-1: at \(k=0\), \(s=3\), \(n=3\),
\(j=0\), parent \((0,3)\), iso, \(p=10\). Triple left/right comes
from parent run-2: at \(k=0\), \(s=3\), \(n=1\), parent \((0,1)\),
left, \(p=6\). \(n\equiv 3\pmod{4}\) triple comes from parent
run-2: at \(k=1\), \(s=5\), \(n=7\), \(j=6\), parent \((3,1)\),
left, \(p=8\).

## Verdict

`LEMMA` (\(G=1\) kind from parent run length; isolated pairs are
parent run-2 or run-3; covering clocks parent-kind).
`KILLED` (isolated pair comes from parent run-1; triple left/right
comes from parent run-2; \(n\equiv 3\) triple comes from parent
run-2).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_iq.md` (this note)
- `research/cycle_iq.py`
- `research/cycle_iq.json`
