# Cycle SH: packed rest on \(n\bmod 4=0\) equals \(n\bmod 4=3\) even-\(j\) through \(k\le 10\)

Covering packed rest split by \(n\bmod 4\) and \(j\) parity.
Even-\(n\) \(G=1\) lives only on even \(j\) (Cycle QV). Packed rest
on \(n\bmod 4=0\) equals packed rest on \(n\bmod 4=3\) even \(j\)
through \(k\le 10\), **not** \(n\bmod 4=3\) tot (odd \(j\) is
extra). Packed rest on \(n\bmod 4=1\) even \(j\) is \(1\) iff
\(k\notin\{3,4,5\}\) through \(k\le 10\); that is **not**
identically \(1\), **not** parent even tot (Cycle RU packed
analogue dies at \(k=3\)), and **not** Green \(n\bmod 4=1\) rest.
Do **not** claim those identities for all \(k\). This is **not**
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

Certify: `python3 research/cycle_sh.py --certify` (~9.58s).
Dump: `research/cycle_sh.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HJ/HS/HU/KH/LZ/OJ/PB/QO/QU/QV/QX/SG (packed rest on
\(n\bmod 4=0\) equals \(n\bmod 4=3\) even \(j\) through \(k\le 10\);
packed rest on \(n\bmod 4=1\) even \(j\) is \(1\) iff
\(k\notin\{3,4,5\}\); no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (packed \(n\bmod 4=0\) equals \(n\bmod 4=3\) even-\(j\))

Through \(k\le 10\), covering packed rest xor on \(n\bmod 4=0\)
equals packed rest xor on \(n\bmod 4=3\) even \(j\). Packed rest
on \(n\bmod 4=1\) even \(j\) is \(1\) iff \(k\notin\{3,4,5\}\).
Status: **certified** \(k\le 10\), **prefix** all \(k\).
**Killed:** \(n\bmod 4=0\) tot equals \(n\bmod 4=3\) tot.
**Killed:** \(n\bmod 4=1\) even-\(j\) identically \(1\).
**Killed:** equals parent even tot. **Killed:** equals Green
\(n\bmod 4=1\) rest.

## Verdict

`CERTIFIED` (packed \(n\bmod 4=0\) tot equals \(n\bmod 4=3\)
even-\(j\) tot through \(k\le 10\); packed \(n\bmod 4=1\) even-\(j\)
is \(1\) iff \(k\notin\{3,4,5\}\) through \(k\le 10\); \(E_k=0\) on
odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (\(n\bmod 4=0\) equals \(n\bmod 4=3\) tot; \(n1e\)
identically \(1\); \(n1e\) equals parent even tot; \(n1e\) equals
Green \(n\bmod 4=1\) rest; cellwise 2-fold packed AND).
`PREFIX` (those identities for all \(k\); even-\(n\) rest xor at
\(k\) equals odd-\(n\) rest xor at \(k-1\) for all \(k\); packed
rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for all \(k\); leftover
after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_sh.md` (this note)
- `research/cycle_sh.py`
- `research/cycle_sh.json`
