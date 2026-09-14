# Cycle UF: even leftover plus even unpaired is \(\mathrm{lo{+}unp}(k-1)+2J_k\)

For \(k\ge 2\), even leftover is leftover(\(k-1\))+ \(2J_k\) (Cycle TU)
and even unpaired is unpaired(\(k-1\)) (Cycle TZ). Cycle UE leftover
plus unpaired at \(k-1\) then gives even leftover plus even unpaired
\(\mathrm{lo{+}unp}(k-1)+2J_k=2^k(F_{k+3}-3)+2J_k\). The same closed
form holds at \(k=1\) by census. Using leftover plus unpaired at
\(k=0\) (count \(1\)) plus \(2J_1\) overcounts (\(3\) vs \(2\)).
Do **not** PREFIX leftover extra or unpaired extra separately. Do
**not** catalogue leftover \(d\). Do **not** PREFIX leftover spat
tot. Do **not** PREFIX pal-center tot. Do **not** PREFIX \(d=1\)/\(d=2\)
spat tot. Do **not** claim pal-center tot equals \(S\oplus T\). This
is **not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do
**not** catalogue leftover \(p\) one-by-one. Do **not** catalogue
further \(S\)/\(T\) subregions unless the experiment answers why
\(E_k=0\). Do **not** claim pal-left leftover xor vanishes for all
\(k\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for
all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\). Do **not**
walk \(k=11\) covering packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_uf.py --certify`.
Dump: `research/cycle_uf.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/TZ/UC/UD/UE
(even leftover plus even unpaired; no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even leftover plus even unpaired \(=\mathrm{lo{+}unp}(k-1)+2J_k\) for \(k\ge 1\))

Cycle TU: even leftover \(=\) leftover(\(k-1\))+ \(2J_k\) for
\(k\ge 2\). Cycle TZ: even unpaired \(=\) unpaired(\(k-1\)). Cycle
UE: leftover plus unpaired at \(k-1\) is \(2^k(F_{k+3}-3)\) for
\(k\ge 2\). Hence the even sum is \(2^k(F_{k+3}-3)+2J_k\). Status:
**lemma**. Algebra through \(k\le 64\); census through \(k\le 8\),
including the \(k=1\) base. **Killed:** the same formula using
leftover plus unpaired count at \(k=0\) (overcounts at \(k=1\)).
**Killed:** even leftover equals even unpaired.

## Lemma (odd leftover plus odd unpaired \(=\mathrm{lo{+}unp}-\) even sum, \(k\ge 1\))

Partition leftover plus unpaired by \(n\)-parity. Status: **lemma**.
Census through \(k\le 8\).

## Verdict

`LEMMA` (even leftover plus even unpaired
\(=\mathrm{lo{+}unp}(k-1)+2J_k\) for \(k\ge 1\); odd leftover plus
odd unpaired is the complement).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (parent leftover-plus-unpaired count plus \(2J_k\) at
\(k=1\); even leftover equals even unpaired; leftover alone equals
\(2^{k+1}(F_{k+4}-3)\); leftover plus unpaired at \(k=0\); pal-center
tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_uf.md` (this note)
- `research/cycle_uf.py`
- `research/cycle_uf.json`
