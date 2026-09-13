# Cycle PJ: bits \(19..22\) freeze; covering \(p=22\) silent for every \(k\)

Cycle PI froze bits \(17,18\) and showed covering \(p=18\) silent
for \(k\ge 2\). Bit \(19=1\) iff \(t\bmod 4\in\{2,3\}\) for
\(t\ge 28\); bit \(20=1\) iff \(t\bmod 4\in\{0,1\}\); bit \(21=1\)
iff \(t\bmod 4\neq 3\); bit \(22=1\) iff \(t\bmod 4\in\{0,3\}\).
The left 23 bits are autonomous, and the word at \(t=26\) equals
\(t=30\), so even \(t\ge 26\) has the \(p=22\) 4-tuple \(1010\)
(\(t\bmod 4=2\)) or \(0111\) (\(t\bmod 4=0\)), never an AND-one.
Even \(t\) with AND at \(p=22\) are only \(10,12\). Covering
\(k\ge 3\) starts at \(2U\ge 16\), so misses them. \(k=2\) has
\(G(13,9)=G(14,9)=0\). \(k=0,1\) have \(j<0\). Hence covering
\(p=22\) is silent for every \(k\). **Killed:** covering \(p=24\)
silent for all \(k\) (\(k=2\) has one AND-one).

**Not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do
**not** claim covering \(p=24\) silent for all \(k\). Do **not**
catalogue further \(S\)/\(T\) subregions unless the experiment
answers why \(E_k=0\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).

Certify: `python3 research/cycle_pj.py --certify` (~0.14s).
Dump: `research/cycle_pj.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/PF/PG/PH/PI/PD/GU/HG/HH/HU (bits \(19..22\), even-\(t\)
\(p=22\) 4-tuple; prefix PI silent \(p=18,20\), PH \(p=16\) xor; no
Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (bits \(19..22\))

For \(t\ge 28\): bit \(19=1\) iff \(t\bmod 4\in\{2,3\}\), bit
\(20=1\) iff \(t\bmod 4\in\{0,1\}\), bit \(21=1\) iff
\(t\bmod 4\neq 3\), bit \(22=1\) iff \(t\bmod 4\in\{0,3\}\).
Status: **lemma**. Checked on \(0\le t\le 64\).

## Lemma (left 23-bit period \(4\) from \(t=26\))

Bits \(0..22\) are autonomous. The word at \(t=26\) equals \(t=30\),
so even \(t\ge 26\) is period \(4\). Status: **lemma**.

## Lemma (AND at \(p=22\) on even \(t\ge 26\))

Even \(t\ge 26\): the \(p=22\) 4-tuple is \(1010\) or \(0111\),
AND \(=0\). Early even AND-ones are exactly \(t\in\{10,12\}\).
Status: **lemma**.

## Lemma (covering \(p=22\) silent for every \(k\))

Covering \(k\ge 3\) misses the two early AND-ones. \(k=2\) has
\(G(13,9)=G(14,9)=0\). \(k=0,1\) have \(j<0\). Status: **lemma**.
Thin packed check on \(k\le 8\). **Killed:** covering \(p=24\)
silent for all \(k\).

## Verdict

`LEMMA` (bits \(19..22\); left-23 period \(4\); AND \(p=22=0\) on
even \(t\ge 26\); covering \(p=22\) silent for every \(k\); PI
\(p=18,20\) silent).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (covering \(p=24\) silent for all \(k\)).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); covering \(p=26\) silent for all \(k\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_pj.md` (this note)
- `research/cycle_pj.py`
- `research/cycle_pj.json`
