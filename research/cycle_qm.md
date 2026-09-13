# Cycle QM: covering leftover even-\(j\) Green xor on \(n\equiv 0\pmod{4}\) is \(1\) iff \(k\in\{0,1,3,5\}\)

For \(k\ge 2\), \(G(4t,\mathrm{even}\ j)\) vanishes unless \(j\equiv 0\pmod{4}\),
and \(G(4t,4r)=G(t,r)\) maps the covering \(n\equiv 0\pmod{4}\) window
onto the parent covering window at \(k-2\), so all even-\(j\)
\(n\equiv 0\pmod{4}\) tot is \(A(k-2)\). Cycle PC \(p=4\) even \(n\)
is \(3U-2\), which is \(2\pmod{4}\), so forced even-\(j\)
\(n\equiv 0\pmod{4}\) tot vanishes. UNIQUE_EVEN \(p\equiv 0\pmod{8}\)
columns \(16,32,72,88\) double to Green \(p=4,8,18,22\) at \(k-2\)
(\(n\equiv 0\) xor \(1\) iff \(k\ge 2\), \(k\ge 4\), \(k\ge 5\),
\(k\ge 6\)), so unique even \(n\equiv 0\pmod{4}\) tot is \(1\) iff
\(k\in\{2,3,5\}\). Leftover \(n\equiv 0\pmod{4}\) tot is \(A(k-2)\)
xor that bit. Cycle QL leftover even-\(j\) even-\(n\) tot xor this
bit is leftover even-\(j\) on \(n\equiv 2\pmod{4}\), which is \(1\)
iff \(k\in\{1,2,3,4\}\). This is **not** rest \(=S\oplus T\)
(\(k=3\): leftover \(n\equiv 0\) is \(1\), rest \(=0\); \(k=6\):
\(0\) vs \(1\)). **Not** leftover \(n\equiv 0\pmod{4}\) tot equals
leftover even-\(j\) even-\(n\) tot. **Not** \(E_k=0\) for all \(k\).
Do **not** catalogue leftover \(p\) one-by-one. Do **not** catalogue
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
Do **not** claim leftover even-\(j\) \(n\equiv 0\pmod{4}\) tot
equals leftover even-\(j\) tot.

Certify: `python3 research/cycle_qm.py --certify` (~0.39s).
Dump: `research/cycle_qm.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/LZ/MD/PB/PC/PT/QA/QH/QJ/QK/QL (leftover even-\(j\)
\(n\equiv 0\pmod{4}\); 4-fold doubling to \(A(k-2)\) and unique
\(p=16,32,72,88\); prefix QL leftover even-\(n\), QH clip tot; no
Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (leftover even-\(j\) Green xor on \(n\equiv 0\pmod{4}\) is \(1\) iff \(k\in\{0,1,3,5\}\))

For \(k\ge 2\), leftover even-\(j\) \(n\equiv 0\) \(=\) even-\(j\)
\(n\equiv 0\) tot \(A(k-2)\) xor unique even \(n\equiv 0\) tot.
Forced \(p=4\) even \(n\) is \(3U-2\equiv 2\pmod{4}\). Status:
**lemma**. Checked on \(k\le 8\) by covering walk, unique columns
on \(k\le 12\), and on \(k\le 64\) by the closed forms.
**Killed:** leftover even-\(j\) \(n\equiv 0\) tot equals \(S\oplus T\)
/ packed rest (\(k=3\), \(k=6\)). **Killed:** leftover even-\(j\)
\(n\equiv 0\) tot equals leftover even-\(j\) even-\(n\) tot (\(k=2\)).

## Lemma (leftover even-\(j\) Green xor on \(n\equiv 2\pmod{4}\) is \(1\) iff \(k\in\{1,2,3,4\}\))

Xor of Cycle QL leftover even-\(j\) even-\(n\) tot with the
\(n\equiv 0\) tot. Status: **lemma**.

## Lemma (UNIQUE_EVEN Green xor on \(n\equiv 0\pmod{4}\) is \(1\) iff \(k\in\{2,3,5\}\))

Columns \(p\equiv 4\pmod{8}\) have odd \(j/2\), so \(G(4t,j)=0\).
Columns \(16,32,72,88\) are Green \(p=4,8,18,22\) at \(k-2\).
Status: **lemma**.

## Verdict

`LEMMA` (leftover even-\(j\) \(n\equiv 0\pmod{4}\) tot is \(1\) iff
\(k\in\{0,1,3,5\}\); leftover even-\(j\) \(n\equiv 2\pmod{4}\) tot
is \(1\) iff \(k\in\{1,2,3,4\}\); unique even \(n\equiv 0\) tot is
\(1\) iff \(k\in\{2,3,5\}\); QL leftover even-\(n\); QH \(A(k)\)).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (leftover even-\(j\) \(n\equiv 0\) tot equals \(S\oplus T\)
/ packed rest; leftover even-\(j\) \(n\equiv 0\) tot equals leftover
even-\(j\) even-\(n\) tot).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_qm.md` (this note)
- `research/cycle_qm.py`
- `research/cycle_qm.json`
