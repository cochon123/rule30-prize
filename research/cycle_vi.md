# Cycle VI: leftover-parent xor tot minus leftover extra xor tot is \(4(\mathrm{lo}_e(k-1)-\mathrm{lo}_e(k-2))-(\mathrm{UM}(k)-\mathrm{UM}(k-1))-\mathrm{named}_{lo}(k-1)\)

Leftover extra except \(j=0\) each produce one leftover-parent xor
child, count \(\mathrm{xor\_lo}(k-1)\). Leftover-parent xor tot is
\(4\,\mathrm{lo}_e(k-1)\) minus Cycle UM difference. Their gap is
four times the even leftover first difference, minus the UM first
difference, minus named leftover extra at the parent, for every
\(k\) (\(\mathrm{lo}_e\), UM, and \(\mathrm{named}_{lo}\) vanish at
negative arguments). Dies at \(k=2\) if \(\mathrm{named}_{lo}\) at
the parent is replaced by the \(k\ge 2\) closed form
\(2^{k-1}+2 J_{k-1}-2\) (got \(1\), form \(0\)). Dies at \(k=8\) for
the even leftover difference alone (got \(11662\), not \(11992\)).
Census \(k=8\): gap \(11662\). Do **not** PREFIX pal-center tot from
small \(k\). Do **not** PREFIX leftover spat tot. Do **not** PREFIX
\(d=1\)/\(d=2\) spat tot. Do **not** catalogue leftover \(d\). Do
**not** claim pal-center tot equals \(S\oplus T\). This is **not**
rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
catalogue leftover \(p\) one-by-one. Do **not** catalogue further
\(S\)/\(T\) subregions unless the experiment answers why \(E_k=0\).
Do **not** claim pal-left leftover xor vanishes for all \(k\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\)
covering packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_vi.py --certify`.
Dump: `research/cycle_vi.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LZ/OJ/QV/SO/SV/SY/TA/TB/TD/TE/TT/TU/UC/UD/UE/UL/UM/UO/UP/UQ/UR/UU/UV/UW/UZ/VA/VH
(xor count gap; no Fermat table, no extra window, no \(n_0=16\)
window, no packed covering \(k=11\)).

## Lemma (leftover-parent xor tot minus leftover extra xor tot is \(4(\mathrm{lo}_e(k-1)-\mathrm{lo}_e(k-2))-(\mathrm{UM}(k)-\mathrm{UM}(k-1))-\mathrm{named}_{lo}(k-1)\))

Equals \(\mathrm{lo\_parent\_sum}-\mathrm{xor\_lo}(k-1)\) for
\(k\ge 1\). Status: **lemma**. Algebra through \(k\le 64\); census
through \(k\le 8\). **Killed** at \(k=2\) for the named closed form
at the parent.

## Lemma (that gap equals leftover-parent xor tot minus leftover extra xor tot)

Census through \(k\le 8\). Status: **lemma**. **Killed** even leftover
difference alone at \(k=8\). Do **not** PREFIX pal-center tot.

## Verdict

`LEMMA` (xor count gap is \(4(\mathrm{lo}_e(k-1)-\mathrm{lo}_e(k-2))-(\mathrm{UM}(k)-\mathrm{UM}(k-1))-\mathrm{named}_{lo}(k-1)\);
equals leftover-parent xor tot minus leftover extra xor tot).
`CERTIFIED` (census through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (named closed parent at \(k=2\); even leftover difference
alone at \(k=8\); pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_vi.md` (this note)
- `research/cycle_vi.py`
- `research/cycle_vi.json`
