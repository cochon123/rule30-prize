# Cycle RF: covering 2-fold of forced columns is silent \(\{8,12,28\}\)

Forced packed columns are \(\{4,6,14\}\). Doubling the packed index
sends them to \(\{8,12,28\}\). Cycle PF covering \(p=8\) is silent
for every \(k\), Cycle PG covering \(p=12\) is silent for \(k\ge 2\),
and Cycle PL covering \(p=28\) is silent for every \(k\). For child
\(k\ge 2\) the 2-fold image of forced \(G=1\) therefore has packed
AND \(0\), so parent forced AND does not leak into child rest. This
is **not** the 2-fold of forced being forced (\(\{8,12,28\}\) is
disjoint from \(\{4,6,14\}\)). **Not** cellwise 2-fold packed AND.
**Not** even-\(n\) rest equals parent rest tot. This is **not** rest
\(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not** catalogue
leftover \(p\) one-by-one. Do **not** catalogue further \(S\)/\(T\)
subregions unless the experiment answers why \(E_k=0\). Do **not**
claim pal-left leftover xor vanishes for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\). Do **not** walk \(k=11\) covering packed. Do
**not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim the 2-fold of forced is forced. Do **not** claim
cellwise 2-fold packed AND. Do **not** claim even-\(n\) rest xor at
\(k\) equals odd-\(n\) rest xor at \(k-1\) for all \(k\). Do **not**
claim silent xor leftover is \((1,1,1,0)\) for all \(k\). Do **not**
claim silent equals leftover on all residues for \(k\ge 6\).

Certify: `python3 research/cycle_rf.py --certify`.
Dump: `research/cycle_rf.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/LZ/PF/PG/PL/QV/RE (2-fold of FORCED is silent
\(\{8,12,28\}\) for child \(k\ge 2\); no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (covering 2-fold of forced columns is silent \(\{8,12,28\}\) for child \(k\ge 2\))

Packed column doubling is \(p\mapsto 2p\). Forced
\(\{4,6,14\}\mapsto\{8,12,28\}\). Those three columns are covering
silent (PF all \(k\); PG for \(k\ge 2\); PL all \(k\)). Status:
**lemma**. **Killed:** the 2-fold of forced is forced. **Killed:**
cellwise 2-fold packed AND.

## Verdict

`LEMMA` (covering 2-fold of forced columns is silent
\(\{8,12,28\}\) for child \(k\ge 2\); PF \(p=8\) silent; PG \(p=12\)
silent for \(k\ge 2\); PL \(p=28\) silent; QV 2-fold geometry).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\);
2-fold image AND \(0\) on forced \(G=1\) through \(k\le 6\)).
`KILLED` (2-fold of forced is forced; cellwise 2-fold packed AND).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_rf.md` (this note)
- `research/cycle_rf.py`
- `research/cycle_rf.json`
