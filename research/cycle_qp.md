# Cycle QP: covering UNIQUE_EVEN packed AND xor tot is \(1\) iff \(k\in\{3,4,5\}\)

Xor of the seven UNIQUE_EVEN packed formulas (\(p=16,32,52,60,72,76,88\))
is \(1\) iff \(k\in\{3,4,5\}\): five ones at \(k=3\), three at \(k=4\)
and at \(k=5\), four for every \(k\ge 6\). UNIQUE_ODD packed tot equals
the same bit, and they xor to Cycle QF's unique tot \(0\). The closed
form equals Cycle QG's Green UNIQUE_REST tot, **not** Cycle QJ's Green
unique even tot (\(k=4\): packed even \(=1\), Green even \(=0\);
\(k\ge 6\): packed even \(=0\), Green even \(=1\)). Leftover even-\(n\)
tot is even-\(n\) rest xor this bit, so leftover even-\(n\) equals
even-\(n\) rest except at \(k=3,4,5\). This is **not** rest
\(=S\oplus T\) (\(k=3\): unique even packed \(=1\), rest \(=0\)).
**Not** \(E_k=0\) for all \(k\). Do **not** catalogue leftover \(p\)
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
Do **not** claim packed rest on \(n\equiv 0\pmod{4}\) equals
\(S\oplus T\) at \(k-2\). Do **not** claim packed unique even tot
equals Green unique even tot.

Certify: `python3 research/cycle_qp.py --certify`.
Dump: `research/cycle_qp.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/MD/PB/QF/QG/QJ/QN/QO (UNIQUE_EVEN packed tot via QF
`PACK`; equals QG Green unique tot; not QJ Green unique even;
prefix QO \(n\equiv 0\) tot kill, QN unique packed \(n\equiv 0\);
no Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (UNIQUE_EVEN packed AND xor tot is \(1\) iff \(k\in\{3,4,5\}\))

The seven even unique packed formulas xor as: \(k\le 2\) empty;
\(k=3\) five ones; \(k=4,5\) three ones; \(k\ge 6\) four ones
(\(p=16,32,76,88\)). UNIQUE_ODD packed tot equals the same bit.
Equals Cycle QG Green UNIQUE_REST tot. Status: **lemma**. Closed
forms on \(k\le 64\). **Killed:** packed unique even tot equals
Green unique even tot. **Killed:** packed unique even tot equals
\(S\oplus T\) / packed rest.

## Verdict

`LEMMA` (UNIQUE_EVEN packed tot is \(1\) iff \(k\in\{3,4,5\}\);
UNIQUE_ODD packed tot is the same bit; QF unique tot \(0\); QG
Green unique tot).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (packed unique even tot equals Green unique even tot;
packed unique even tot equals \(S\oplus T\) / packed rest;
packed rest on \(n\equiv 0\pmod{4}\) equals \(S\oplus T\) at
\(k-2\)).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_qp.md` (this note)
- `research/cycle_qp.py`
- `research/cycle_qp.json`
