# Cycle PI: bits \(17,18\) freeze; covering \(p=18\) silent for \(k\ge 2\)

Cycle PH froze bits \(13..16\) and showed covering packed AND xor
at \(p=16\) is \(1\) for \(k\ge 3\). Bit \(17=1\) iff
\(t\bmod 4=3\) for \(t\ge 20\); bit \(18=1\) iff
\(t\bmod 4\in\{1,2\}\) for \(t\ge 20\). The left 19 bits are
autonomous, and the word at \(t=20\) equals \(t=24\), so even
\(t\ge 20\) has the \(p=18\) 4-tuple \(1100\) (\(t\bmod 4=0\)) or
\(0101\) (\(t\bmod 4=2\)), never an AND-one. Even \(t\) with AND at
\(p=18\) are only \(8,12,14,18\). Covering \(k\ge 4\) starts at
\(2U\ge 32\), so misses them. \(k=3\) has only \(s=18\), even \(n\),
odd column, \(G=0\). \(k=2\) has \(G(13,11)=G(15,11)=0\). Hence
covering \(p=18\) is silent for \(k\ge 2\). Even \(t\ge 24\) has the
\(p=20\) 4-tuple \(0001\) or \(0110\), so covering \(p=20\) is silent
for \(k\ge 4\). **Killed:** covering \(p=18\) silent for all \(k\)
(\(k=1\) has two AND-ones).

**Not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do
**not** claim covering \(p=22\) silent for all \(k\). Do **not**
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

Certify: `python3 research/cycle_pi.py --certify`.
Dump: `research/cycle_pi.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/PF/PG/PH/PD/GU/HG/HH/HU (bits \(17,18\), even-\(t\)
\(p=18\) 4-tuple; prefix PH \(p=16\) xor, PG silent \(p=12\); no
Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (bits \(17,18\))

For \(t\ge 20\): bit \(17=1\) iff \(t\bmod 4=3\), bit \(18=1\) iff
\(t\bmod 4\in\{1,2\}\). Status: **lemma**. Checked on
\(0\le t\le 64\).

## Lemma (left 19-bit period \(4\) from \(t=20\))

Bits \(0..18\) are autonomous. The word at \(t=20\) equals \(t=24\),
so even \(t\ge 20\) is period \(4\). Status: **lemma**.

## Lemma (AND at \(p=18\) on even \(t\ge 20\))

Even \(t\ge 20\): the \(p=18\) 4-tuple is \(1100\) or \(0101\),
AND \(=0\). Early even AND-ones are exactly \(t\in\{8,12,14,18\}\).
Status: **lemma**.

## Lemma (covering \(p=18\) silent for \(k\ge 2\))

Covering \(k\ge 4\) misses the four early AND-ones.
\(k=3\) has only \(s=18\) (even \(n\), odd \(j\), \(G=0\)).
\(k=2\) has \(G(13,11)=G(15,11)=0\). Status: **lemma**. Thin packed
check on \(k\le 8\). **Killed:** silent for all \(k\) (\(k=1\) has
two AND-ones).

## Lemma (covering \(p=20\) silent for \(k\ge 4\))

Even \(t\ge 24\): the \(p=20\) 4-tuple is \(0001\) or \(0110\),
AND \(=0\). Covering even \(s\) starts at \(2U\ge 32\) for
\(k\ge 4\). Status: **lemma**. Thin packed check on \(k\le 8\).

## Verdict

`LEMMA` (bits \(17,18\); left-19 period \(4\); AND \(p=18=0\) on
even \(t\ge 20\); covering \(p=18\) silent for \(k\ge 2\); covering
\(p=20\) silent for \(k\ge 4\); PH \(p=16\) xor).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (covering \(p=18\) silent for all \(k\)).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); covering \(p=22\) silent for all \(k\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_pi.md` (this note)
- `research/cycle_pi.py`
- `research/cycle_pi.json`
