# Cycle QJ: covering Green leftover even-\(j\) / odd-\(j\) xor closed forms

For \(k\ge 1\), covering \(10U\equiv 0\pmod{4}\), so even \(j\) is
packed \(p\equiv 0\pmod{4}\). Cycle QI even-\(j\) tot xor Cycle PC
\(p=4\) xor Cycle QG UNIQUE_REST even-\(p\) tot is leftover even-\(j\)
tot. That equals unique even-\(p\) tot for \(k\ge 2\), hence leftover
even-\(j\) is \(1\) iff \(k\le 1\) or \(k=3\) or \(k\ge 6\). Odd-\(j\)
tot xor \(p=6\) xor \(p=14\) xor unique odd-\(p\) tot is leftover
odd-\(j\) tot, which is \(1\) iff \(k\le 1\) or \(k=3\). Xor of the
two is Cycle QH leftover tot (\(1\) iff \(k\ge 6\)). Unique even-\(p\)
tot is \(1\) iff \(k=3\) or \(k\ge 6\); unique odd-\(p\) tot is \(1\)
iff \(k\ge 4\). This is **not** rest \(=S\oplus T\) (leftover even-\(j\)
is \(1\) at \(k=7\)). **Not** leftover even-\(j\) tot equals packed
leftover / rest. **Not** leftover odd-\(j\) tot equals unique odd-\(p\)
tot (\(k=3\): leftover odd \(=1\), unique odd \(=0\)). **Not** \(E_k=0\)
for all \(k\). Do **not** catalogue leftover \(p\) one-by-one. Do
**not** catalogue further \(S\)/\(T\) subregions unless the experiment
answers why \(E_k=0\). Do **not** claim pal-left leftover xor vanishes
for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\). Do **not** walk \(k=11\) covering packed. Do
**not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim leftover even-\(j\) tot equals even-\(j\) tot.

Certify: `python3 research/cycle_qj.py --certify`.
Dump: `research/cycle_qj.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/LZ/MD/PB/PC/QG/QH/QI (leftover even/odd \(j\); unique
even/odd \(p\); prefix QI clip-edge, QG unique tot; no Fermat table,
no extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (UNIQUE_REST even-\(p\) tot is \(1\) iff \(k=3\) or \(k\ge 6\); odd-\(p\) tot is \(1\) iff \(k\ge 4\))

Even unique columns \(\{16,32,52,60,72,76,88\}\); odd unique
columns the other nine. Xor is Cycle QG tot. Status: **lemma**.
Checked on \(k\le 64\) via Cycle QG doubling.

## Lemma (leftover even-\(j\) tot is \(1\) iff \(k\le 1\) or \(k=3\) or \(k\ge 6\))

For \(k\ge 1\), leftover even-\(j\) \(=\) even-\(j\) tot xor \(p=4\)
xor unique even-\(p\). For \(k\ge 2\) that equals unique even-\(p\).
Status: **lemma**. Checked on \(k\le 8\) by covering walk.
**Killed:** leftover even-\(j\) tot equals \(S\oplus T\) / packed
rest (\(k=7\)).

## Lemma (leftover odd-\(j\) tot is \(1\) iff \(k\le 1\) or \(k=3\))

For \(k\ge 1\), leftover odd-\(j\) \(=\) odd-\(j\) tot xor \(p=6\)
xor \(p=14\) xor unique odd-\(p\). Status: **lemma**. **Killed:**
leftover odd-\(j\) tot equals unique odd-\(p\) tot.

## Verdict

`LEMMA` (unique even/odd Green tot; leftover even-\(j\) / odd-\(j\)
tots; QI even/odd \(j\); QG unique tot; QH leftover tot).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (leftover even-\(j\) tot equals \(S\oplus T\) / packed rest;
leftover odd-\(j\) tot equals unique odd-\(p\) tot).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_qj.md` (this note)
- `research/cycle_qj.py`
- `research/cycle_qj.json`
