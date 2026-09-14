# Cycle RG: covering packed doubling spine \(2\to 4\to 8\to 16\to 32\to 64\); \(p=2\) silent

Packed column doubling is \(p\mapsto 2p\). The spine is
\((2,4,8,16,32,64)\). Covering \(p=2\) is silent for every \(k\):
even \(t\ge 2\) has bits \((-1,0,1,2)=(0,1,1,0)\), not an AND-one
(Cycle PD freeze). It 2-folds onto forced \(p=4\). Forced \(p=4\)
2-folds onto silent \(p=8\) (Cycle RF). Silent \(p=8\) 2-folds onto
unique \(p=16\). Unique \(p=16\) 2-folds onto unique \(p=32\). Unique
\(p=32\) 2-folds onto leftover \(p=64\), silent for \(k\ge 6\)
(Cycle PO). This is **not** \(p=2\) unique-rest. **Not** \(p=64\)
unique-rest. **Not** \(p=2\) 2-folds onto unique. This is **not**
rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
catalogue leftover \(p\) one-by-one. Do **not** catalogue further
\(S\)/\(T\) subregions unless the experiment answers why \(E_k=0\).
Do **not** claim pal-left leftover xor vanishes for all \(k\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim the 2-fold of forced is forced. Do **not** claim
cellwise 2-fold packed AND. Do **not** claim even-\(n\) rest xor at
\(k\) equals odd-\(n\) rest xor at \(k-1\) for all \(k\). Do **not**
claim \(p=2\) is unique-rest. Do **not** claim \(p=64\) is
unique-rest.

Certify: `python3 research/cycle_rg.py --certify` (~0.14s).
Dump: `research/cycle_rg.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/LZ/MD/PD/PF/PH/PK/PO/RF (spine \(2\to 4\to 8\to 16\to 32\to 64\);
covering \(p=2\) silent; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (covering \(p=2\) silent for every \(k\))

Even \(t\ge 2\) has the \(p=2\) 4-tuple \(0110\), not an AND-one.
Covering even \(s\) starts at \(2U\ge 2\). Status: **lemma**. Thin
packed check on \(k\le 8\): one live \(G=1\), AND \(0\). **Killed:**
\(p=2\) unique-rest. **Killed:** \(p=2\) 2-folds onto unique.

## Lemma (covering packed doubling spine \(2\to 4\to 8\to 16\to 32\to 64\))

Column doubling is \(p\mapsto 2p\). Labels: \(p=2\) silent; \(p=4\)
forced; \(p=8\) silent; \(p=16\) and \(p=32\) unique-rest; \(p=64\)
leftover, silent for \(k\ge 6\). Status: **lemma**. **Killed:**
\(p=64\) unique-rest.

## Verdict

`LEMMA` (covering \(p=2\) silent for every \(k\); packed doubling
spine \(2\to 4\to 8\to 16\to 32\to 64\); PD freeze; RF forced
2-fold; PH \(p=16\); PK \(p=32\); PO \(p=64\)).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\);
covering \(p=2\) AND \(0\) through \(k\le 8\)).
`KILLED` (\(p=2\) unique-rest; \(p=64\) unique-rest; \(p=2\) 2-folds
onto unique; cellwise 2-fold packed AND).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_rg.md` (this note)
- `research/cycle_rg.py`
- `research/cycle_rg.json`
