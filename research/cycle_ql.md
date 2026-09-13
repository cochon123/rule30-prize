# Cycle QL: covering leftover even-\(j\) Green xor on even \(n\) is \(1\) iff \(k\in\{0,2,4,5\}\)

Cycle QK leftover even-\(j\) odd-\(n\) tot is \(1\) iff \(k\ge 1\).
Cycle QJ leftover even-\(j\) tot is \(1\) iff \(k\le 1\) or \(k=3\)
or \(k\ge 6\). Their xor is leftover even-\(j\) even-\(n\) tot. For
\(k\ge 1\) that also equals Cycle QI even-\(n\) even-\(j\) tot
\(A(k-1)\) xor unique even tot xor Cycle PC \(p=4\) even-\(n\) xor
(which is \(1\)). Closed form: \(1\) iff \(k\in\{0,2,4,5\}\). This
is **not** rest \(=S\oplus T\) (\(k=4\): leftover even-\(n\) even-\(j\)
is \(1\), rest \(=0\); \(k=6\): \(0\) vs \(1\)). **Not** leftover
even-\(j\) even-\(n\) tot equals leftover even-\(j\) tot. **Not**
\(E_k=0\) for all \(k\). Do **not** catalogue leftover \(p\)
one-by-one. Do **not** catalogue further \(S\)/\(T\) subregions
unless the experiment answers why \(E_k=0\). Do **not** claim pal-left
leftover xor vanishes for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\). Do **not** walk \(k=11\) covering packed. Do
**not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim leftover even-\(j\) even-\(n\) tot equals leftover
even-\(j\) odd-\(n\) tot.

Certify: `python3 research/cycle_ql.py --certify`.
Dump: `research/cycle_ql.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/MD/PB/QH/QJ/QK (leftover even-\(j\) even-\(n\); doubling via
QI even-\(n\) even-\(j\) tot, unique even tot, PC \(p=4\); prefix QK
odd-\(n\) tot, QJ leftover even tot; no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (leftover even-\(j\) Green xor on even \(n\) is \(1\) iff \(k\in\{0,2,4,5\}\))

For \(k\ge 1\), leftover even-\(j\) even-\(n\) \(=\) even-\(n\)
even-\(j\) tot \(A(k-1)\) xor unique even tot xor \(p=4\) even-\(n\)
xor. Unique even-\(p\) odd-\(n\) tot vanishes, so unique even
even-\(n\) is unique even tot. Forced \(p=4\) even-\(n\) xor is \(1\).
Status: **lemma**. Checked on \(k\le 8\) by covering walk, and on
\(k\le 64\) by the closed forms. **Killed:** leftover even-\(j\)
even-\(n\) tot equals \(S\oplus T\) / packed rest (\(k=4\), \(k=6\)).
**Killed:** leftover even-\(j\) even-\(n\) tot equals leftover
even-\(j\) tot (\(k=2\), \(k=7\)).

## Verdict

`LEMMA` (leftover even-\(j\) even-\(n\) tot is \(1\) iff
\(k\in\{0,2,4,5\}\); QK leftover even-\(j\) odd-\(n\); QJ leftover
even tot; QI even-\(n\) even-\(j\) tot \(A(k-1)\)).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (leftover even-\(j\) even-\(n\) tot equals \(S\oplus T\) /
packed rest; leftover even-\(j\) even-\(n\) tot equals leftover
even-\(j\) tot).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ql.md` (this note)
- `research/cycle_ql.py`
- `research/cycle_ql.json`
