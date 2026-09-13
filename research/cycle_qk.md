# Cycle QK: covering leftover even-\(j\) Green xor on odd \(n\) is \(1\) for \(k\ge 1\)

Each UNIQUE_REST even-\(p\) column has Green parents \(p/2\) and
\(p/2+2\) with the same xor closed form, so Cycle QG's odd-\(n\) tot
(those two xor'd) vanishes: unique even-\(p\) Green xor lives only
on even \(n\). Cycle PC's \(p=4\) on odd \(n\) also vanishes for
\(k\ge 1\) (the unique even \(n\) is \(3U-2\)). Cycle QI odd-\(n\)
even-\(j\) tot is clip-edge \(p=0\) at \(k-1\), hence \(1\) for
\(k\ge 1\). Leftover even-\(j\) on odd \(n\) is that bit, so \(1\)
for every \(k\ge 1\). Leftover even-\(j\) on even \(n\) is leftover
even-\(j\) tot xor \(1\) for \(k\ge 1\). This is **not** rest
\(=S\oplus T\) (odd-\(n\) leftover even-\(j\) is \(1\) at \(k=7\)).
**Not** unique even-\(p\) odd-\(n\) tot equals unique even tot.
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
Do **not** claim leftover even-\(j\) odd-\(n\) tot equals leftover
even-\(j\) tot.

Certify: `python3 research/cycle_qk.py --certify` (~0.53s).
Dump: `research/cycle_qk.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/LZ/MD/PB/PC/PH/PM/PT/PV/PY/QC/QD/QE/QG/QI/QJ (unique
even-\(p\) odd-\(n\) vanish; parent pairs; leftover even-\(j\) odd-\(n\);
prefix QJ leftover even tot, QI clip-edge; no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (UNIQUE_REST even-\(p\) Green xor on odd \(n\) vanishes)

Parent pairs \((p/2,p/2+2)\) are \((8,10)\), \((16,18)\),
\((26,28)\), \((30,32)\), \((36,38)\), \((38,40)\), \((44,46)\),
each with identical Green xor closed forms. Status: **lemma**.
Checked on \(k\le 12\) by covering walk, and on \(k\le 64\) by the
closed forms.

## Lemma (leftover even-\(j\) Green xor on odd \(n\) is \(1\) iff \(k\ge 1\))

Forced even-\(j\) odd-\(n\) tot is \(0\) (\(p=4\) even \(n\) is
\(3U-2\)). Unique even-\(p\) odd-\(n\) tot is \(0\). All even-\(j\)
odd-\(n\) tot is clip-edge \(p=0\) at \(k-1\). Status: **lemma**.
Checked on \(k\le 8\). **Killed:** leftover even-\(j\) odd-\(n\) tot
equals \(S\oplus T\) / packed rest (\(k=7\)).

## Verdict

`LEMMA` (unique even-\(p\) odd-\(n\) Green xor vanishes; parent pairs
equal; leftover even-\(j\) odd-\(n\) tot is \(1\) for \(k\ge 1\); QJ
leftover even tot; QI clip-edge \(p=0\)).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (leftover even-\(j\) odd-\(n\) tot equals \(S\oplus T\) /
packed rest).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_qk.md` (this note)
- `research/cycle_qk.py`
- `research/cycle_qk.json`
