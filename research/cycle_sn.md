# Cycle SN: packed rest on \(n\bmod 4=0\) equals n2 AND-mismatch tot through \(k\le 10\)

Cycle RR packed rest on \(n\bmod 4=0\) is parent even xor
\(\mathrm{mis}_{n0}\). Cycle QV mismatch xor equals parent even, so
that tot equals \(\mathrm{mis}_{n2}\): \(1\) iff \(k\in\{2,4,8\}\)
through \(k\le 10\). Cycle SH packed rest on \(n\bmod 4=3\) even \(j\)
equals \(n\bmod 4=0\), hence the same bit. Do **not** claim those
identities for all \(k\). Packed \(n0\) is **not** \(S\oplus T\).
Packed \(n3e\) is **not** Green \(n3e\). This is **not** rest
\(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
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

Certify: `python3 research/cycle_sn.py --certify` (~0.14s).
Dump: `research/cycle_sn.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/PB/QV/QX/RR/SH/SI/SM (packed rest on \(n\bmod 4=0\) equals
n2 AND-mismatch tot through \(k\le 10\); no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (packed \(n0\) tot equals \(\mathrm{mis}_{n2}\))

Through \(k\le 10\), covering packed rest xor on \(n\bmod 4=0\)
equals Cycle RR's 2-fold AND-mismatch tot on \(n\bmod 4=2\), hence
is \(1\) iff \(k\in\{2,4,8\}\). The same bit is packed rest on
\(n\bmod 4=3\) even \(j\). Status: **certified** \(k\le 10\),
**prefix** all \(k\). **Killed:** identically \(0\). **Killed:**
equals \(S\oplus T\). **Killed:** equals Green \(n0\). **Killed:**
packed n3 even-\(j\) equals Green n3 even-\(j\).

## Verdict

`CERTIFIED` (packed rest on \(n\bmod 4=0\) equals n2 AND-mismatch
tot through \(k\le 10\); packed n3 even-\(j\) is the same bit;
\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (packed n0 identically \(0\); packed n0 equals \(S\oplus T\);
packed n0 equals Green n0; packed n3e equals Green n3e; cellwise
2-fold packed AND).
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

- `research/cycle_sn.md` (this note)
- `research/cycle_sn.py`
- `research/cycle_sn.json`
