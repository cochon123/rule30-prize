# Cycle SQ: \(n0\oplus oo\) matches the SO+SP remainder through \(k\le 10\)

Cycle SO odd tot equals \(n1e\oplus n0\oplus oo\) through \(k\le 10\).
Cycle SP n1e equals \(1\) xor UNIQUE_EVEN packed tot. The remainder
\(n0\oplus oo\) is \(1\) iff \(k=2\) or (\(k\ge 8\) and
\(k\bmod 8\notin\{6,7\}\)) through \(k\le 10\). Helpers
\(\mathrm{odd}\oplus n1e\) equal that form for all \(k\). Cycles
SN/SG exception-set helpers xor to \(0\) at \(k=11\), so they cannot
both lift if this form lifts. Do **not** claim the form for all
\(k\). This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\) for
all \(k\). Do **not** catalogue leftover \(p\) one-by-one. Do
**not** catalogue further \(S\)/\(T\) subregions unless the
experiment answers why \(E_k=0\). Do **not** claim pal-left leftover
xor vanishes for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\). Do **not** walk \(k=11\) covering packed. Do
**not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_sq.py --certify` (~0.13s).
Dump: `research/cycle_sq.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/PB/QV/SG/SH/SN/SO/SP ( \(n0\oplus oo\) matches the SO+SP
remainder through \(k\le 10\); no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (helper: \(n0\oplus oo=\mathrm{odd}\oplus n1e\))

Write \(n0\oplus oo=1\) iff \(k=2\) or (\(k\ge 8\) and
\(k\bmod 8\notin\{6,7\}\)). Then this equals Cycle SO odd xor Cycle
SP n1e for every \(k\). Status: **lemma**.

## Lemma (packed \(n0\oplus oo\) equals that form through \(k\le 10\))

Covering packed rest xor on \(n\bmod 4=0\), xor odd-\(n\) odd-\(j\),
equals the helper through \(k\le 10\). Status: **certified**
\(k\le 10\), **prefix** all \(k\). **Killed:** identically \(0\).
**Killed:** equals \(S\oplus T\). **Killed:** SN/SG exception-set
helpers xor to this bit at \(k=11\).

## Verdict

`LEMMA` (helper \(n0\oplus oo\) equals odd xor n1e for all \(k\)).
`CERTIFIED` (packed \(n0\oplus oo\) equals the helper through
\(k\le 10\); \(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (\(n0\oplus oo\) identically \(0\); equals \(S\oplus T\);
SN/SG exception-set helpers xor equals this form at \(k=11\);
cellwise 2-fold packed AND).
`PREFIX` (that form for all \(k\); even-\(n\) rest xor at \(k\)
equals odd-\(n\) rest xor at \(k-1\) for all \(k\); packed rest
\(=S\oplus T\) for all \(k\); \(E_k=0\) for all \(k\); leftover
after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_sq.md` (this note)
- `research/cycle_sq.py`
- `research/cycle_sq.json`
