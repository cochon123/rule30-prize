# Cycle SP: packed n1e equals \(1\) xor UNIQUE_EVEN packed tot through \(k\le 10\)

Cycle SH packed rest on \(n\bmod 4=1\) even \(j\) is \(1\) iff
\(k\notin\{3,4,5\}\). Cycle QP UNIQUE_EVEN packed tot is \(1\) iff
\(k\in\{3,4,5\}\) for all \(k\), so n1e equals \(1\) xor that tot
through \(k\le 10\). The same bit is UNIQUE_ODD packed tot and
UNIQUE_REST Green tot. If this lifts with Cycle SO's odd form, then
\(n0\oplus oo\) must be \(1\) at \(k=11\) (the SH/SN/SG helpers xor
to \(0\) there). Do **not** claim n1e for all \(k\). Packed n1e is
**not** UNIQUE_EVEN packed tot. This is **not** rest \(=S\oplus T\).
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

Certify: `python3 research/cycle_sp.py --certify`.
Dump: `research/cycle_sp.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/PB/QG/QJ/QP/QV/SG/SH/SN/SO (packed n1e equals \(1\) xor
UNIQUE_EVEN packed tot through \(k\le 10\); no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (packed n1e equals \(1\) xor UNIQUE_EVEN packed tot)

Through \(k\le 10\), covering packed rest xor on \(n\bmod 4=1\) even
\(j\) equals \(1\) xor Cycle QP's UNIQUE_EVEN packed tot, hence is
\(0\) iff \(k\in\{3,4,5\}\). The same bit is UNIQUE_ODD packed tot
and UNIQUE_REST Green tot. Status: **certified** \(k\le 10\),
**prefix** all \(k\). **Killed:** equals UNIQUE_EVEN packed tot.
**Killed:** equals Green unique even tot. **Killed:** identically
\(1\).

## Verdict

`CERTIFIED` (packed n1e equals \(1\) xor UNIQUE_EVEN packed tot
through \(k\le 10\); \(E_k=0\) on odd-\(s\) rest for \(q=10\),
\(k\le 10\)).
`LEMMA` (QP UNIQUE_EVEN/ODD packed tots \(1\) iff \(k\in\{3,4,5\}\);
QG unique Green tot the same bit).
`KILLED` (n1e equals UNIQUE_EVEN packed tot; n1e equals Green unique
even tot; n1e identically \(1\); cellwise 2-fold packed AND).
`PREFIX` (n1e for all \(k\); even-\(n\) rest xor at \(k\) equals
odd-\(n\) rest xor at \(k-1\) for all \(k\); packed rest \(=S\oplus T\)
for all \(k\); \(E_k=0\) for all \(k\); leftover after classified
columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_sp.md` (this note)
- `research/cycle_sp.py`
- `research/cycle_sp.json`
