# Cycle SO: odd-\(n\) packed rest tot matches the QU+\(S\oplus T\) recurrence through \(k\le 10\)

If even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
and rest \(=S\oplus T\), the odd tot is forced: \(\mathrm{odd}(0)=1\)
and \(\mathrm{odd}(k)=\mathrm{odd}(k-1)\oplus\mathrm{ST}(k)\). The
closed form is \(1\) iff \(k\le 1\) or (\(k\ge 6\) and
\(k\bmod 8\in\{6,7\}\)). Covering packed odd tot matches through
\(k\le 10\), and equals \(n1e\oplus n0\oplus oo\) (Cycles SH/SN/SG).
Those three exception-set helpers cannot all hold at \(k=11\) if
this form lifts (they xor to \(1\); the form is \(0\)). Do **not**
claim the form for all \(k\). This is **not** rest \(=S\oplus T\).
**Not** \(E_k=0\) for all \(k\). Do **not** catalogue leftover \(p\)
one-by-one. Do **not** catalogue further \(S\)/\(T\) subregions
unless the experiment answers why \(E_k=0\). Do **not** claim
pal-left leftover xor vanishes for all \(k\). Do **not** claim
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

Certify: `python3 research/cycle_so.py --certify` (~0.13s).
Dump: `research/cycle_so.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/PB/QV/SG/SH/SN (odd-\(n\) packed rest tot matches the
QU+\(S\oplus T\) recurrence through \(k\le 10\); no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (helper: \(\mathrm{odd}(k)\oplus\mathrm{odd}(k-1)=\mathrm{ST}(k)\))

Write \(\mathrm{odd}(k)=1\) iff \(k\le 1\) or (\(k\ge 6\) and
\(k\bmod 8\in\{6,7\}\)), and \(\mathrm{ST}(k)=1\) iff \(k=2\) or
(\(k\ge 6\) and \(k\bmod 8\in\{0,6\}\)). For \(k\ge 1\),
\(\mathrm{odd}(k)\oplus\mathrm{odd}(k-1)=\mathrm{ST}(k)\). Even tot
is parent odd. Status: **lemma**.

## Lemma (packed odd tot equals that form through \(k\le 10\))

Covering packed rest xor on odd \(n\) equals the helper through
\(k\le 10\), hence equals \(n1e\oplus n0\oplus oo\), and xor the
parent odd tot equals \(S\oplus T\). Status: **certified**
\(k\le 10\), **prefix** all \(k\). **Killed:** equals \(S\oplus T\).
**Killed:** identically \(0\). **Killed:** SH/SN/SG exception-set
helpers xor to this bit at \(k=11\).

## Verdict

`LEMMA` (helper odd xor parent odd equals \(S\oplus T\) for all
\(k\); helper even tot is parent odd).
`CERTIFIED` (packed odd tot equals the helper through \(k\le 10\);
equals \(n1e\oplus n0\oplus oo\); \(E_k=0\) on odd-\(s\) rest for
\(q=10\), \(k\le 10\)).
`KILLED` (odd tot equals \(S\oplus T\); odd tot identically \(0\);
SH/SN/SG exception-set helpers xor equals the odd form at \(k=11\);
cellwise 2-fold packed AND).
`PREFIX` (that odd form for all \(k\); even-\(n\) rest xor at
\(k\) equals odd-\(n\) rest xor at \(k-1\) for all \(k\); packed
rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for all \(k\); leftover
after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_so.md` (this note)
- `research/cycle_so.py`
- `research/cycle_so.json`
