# Cycle PF: packed bits \(7,8,9\) freeze; covering \(p=8\) and \(p=10\) silent

Cycle PD froze bits \(1..6\) on even \(t\ge 2\). Bit \(7\) reads
bits \(5,6,7\): with those already \(0\) on even \(t\) and
\(t\bmod 2\) on odd \(t\ge 3\), bit \(7\) stays \(0\) for every
\(t\). Then bit \(8(t+1)=\) bit \(6(t)\oplus\) bit \(8(t)\), so
for \(t\ge 4\) bit \(8=1\) iff \(t\bmod 4\in\{0,1\}\). Bit \(9\)
is then \(1\) for every \(t\ge 5\) (it becomes \(1\) at \(t=5\)
and the \(b_7=0\) update is an OR with bit \(8\)).

The \(p=8\) 4-tuple is therefore never an AND-one, so AND at
\(p=8\) is \(0\) for every \(t\) and covering \(p=8\) is silent
for every \(k\). For \(t\ge 5\) the \(p=10\) 4-tuple is an
AND-one iff \(t\bmod 4\in\{2,3\}\). Covering even \(s\ge 8\)
has that AND iff \(n\) is even, but \(j=5U-5\) is odd, so even
\(n\) have \(G=0\). Covering \(p=10\) is silent for \(k\ge 2\).
Scale \(k=0\) still has two \(p=10\) AND-ones (finite).

**Not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\).
Do **not** claim covering \(p=12\) silent for all \(k\). Do
**not** catalogue further \(S\)/\(T\) subregions unless the
experiment answers why \(E_k=0\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).

Certify: `python3 research/cycle_pf.py --certify` (~0.14s).
Dump: `research/cycle_pf.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/PE/PD/GU/HG/HH/HU (frozen bits \(7,8,9\), thin silent
\(p=8,10\); prefix PE right-edge duals, PD forced xor; no Fermat
table, no extra window, no \(n_0=16\) window, no packed covering
\(k=11\)).

## Lemma (bits \(7,8,9\))

Bit \(7=0\) for every \(t\). Bit \(8=1\) iff \(t\bmod 4\in\{0,1\}\)
for \(t\ge 4\). Bit \(9=1\) for every \(t\ge 5\). Status:
**lemma**. Checked on \(0\le t\le 64\).

## Lemma (AND at \(p=8\) is \(0\))

The \(p=8\) 4-tuple is never an AND-one. Covering \(p=8\) is
silent for every \(k\). Status: **lemma**. Thin packed check on
\(k\le 8\).

## Lemma (covering \(p=10\) silent for \(k\ge 2\))

For \(t\ge 5\), AND at \(p=10\) fires iff \(t\bmod 4\in\{2,3\}\).
Covering even \(s\ge 8\) therefore fires iff \(n\) is even, which
cannot meet \(G=1\) at the odd column \(5U-5\). Status:
**lemma**. Thin packed check on \(k\le 8\); \(k=0\) has two
AND-ones.

## Verdict

`LEMMA` (bits \(7,8,9\); AND \(p=8=0\); covering \(p=8\) silent;
covering \(p=10\) silent for \(k\ge 2\); PE right-edge; PD forced
xor).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); covering \(p=12\) silent for all \(k\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_pf.md` (this note)
- `research/cycle_pf.py`
- `research/cycle_pf.json`
