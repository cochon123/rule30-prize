# Cycle RN: unique Green \(n\bmod 4\) is \((0,1,1,0)\) for every \(k\ge 6\)

Cycle QX/QY Green rest \(n\bmod 4\) is \((0,1,1,1)\) for \(k\ge 3\).
Cycle RM leftover Green \(n\bmod 4\) is \((0,0,0,1)\) for \(k\ge 6\).
Unique Green is Green xor leftover, so the tuple is \((0,1,1,0)\):
unique Green lives on \(n\bmod 4\in\{1,2\}\). Dual of RM. This is
**not** that tuple for all \(k\) (\(k=0\) is \((0,0,0,0)\); \(k=5\)
is \((1,0,1,1)\)). **Not** unique Green \(n\bmod 4\) equals packed
unique \(n\bmod 4\) (packed \(k\ge 6\) is \((1,0,0,1)\)). This is
**not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do
**not** catalogue leftover \(p\) one-by-one. Do **not** catalogue
further \(S\)/\(T\) subregions unless the experiment answers why
\(E_k=0\). Do **not** claim pal-left leftover xor vanishes for all
\(k\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all
\(k\). Do **not** push the even-spine scan past \(k=18\). Do **not**
bump all \(n_0=16\) past 414990. Do **not** increment consecutive
`11` to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\)
covering packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_rn.py --certify`.
Dump: `research/cycle_rn.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/QX/QY/RB/RM (unique Green \(n\bmod 4=(0,1,1,0)\) for
\(k\ge 6\); prefixes Cycle RM green walk rather than re-walking;
no Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (unique Green \(n\bmod 4\) is \((0,1,1,0)\) for \(k\ge 6\))

Green rest \(n\bmod 4\) xor leftover Green \(n\bmod 4\). Status:
**lemma**. **Killed:** that tuple for all \(k\). **Killed:** unique
Green \(n\bmod 4\) equals packed unique \(n\bmod 4\).

## Verdict

`LEMMA` (unique Green \(n\bmod 4\) is \((0,1,1,0)\) for every
\(k\ge 6\); dual of RM leftover \((0,0,0,1)\); QX/QY Green
\((0,1,1,1)\) for \(k\ge 3\)).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (unique Green \(n\bmod 4=(0,1,1,0)\) for all \(k\);
unique Green \(n\bmod 4\) equals packed unique \(n\bmod 4\);
cellwise 2-fold packed AND).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_rn.md` (this note)
- `research/cycle_rn.py`
- `research/cycle_rn.json`
