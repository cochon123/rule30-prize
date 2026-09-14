# Cycle SI: Green rest on \(n\bmod 4=3\) even-\(j\) is \(1\) iff \(k\neq 1\) through \(k\le 10\)

Covering Green rest split by \(n\bmod 4\) and \(j\) parity.
Even-\(n\) \(G=1\) lives only on even \(j\) (Cycle QV). Green rest
on \(n\bmod 4=3\) even \(j\) is \(1\) iff \(k\neq 1\) through
\(k\le 10\), and odd \(j\) is \(1\) iff \(k=1\), refining Cycle
QY's \(n\bmod 4=3\) tot \(1\). Green rest on \(n\bmod 4=1\) even
\(j\) is \(1\) iff \(k\le 1\), and odd \(j\) is \(1\) iff \(k=0\)
or \(k\ge 3\). Green \(n\bmod 4=0\) tot is **not** Green
\(n\bmod 4=3\) even-\(j\) (Cycle SH analogue dies at \(k=1\)).
Packed \(n\bmod 4=3\) even-\(j\) is **not** this bit. Do **not**
claim those identities for all \(k\). This is **not** rest
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

Certify: `python3 research/cycle_si.py --certify` (~6.68s).
Dump: `research/cycle_si.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/KH/LZ/OJ/QV/QX/QY/QW/SH (Green rest on \(n\bmod 4=3\) even
\(j\) is \(1\) iff \(k\neq 1\) through \(k\le 10\); odd \(j\) is
\(1\) iff \(k=1\); no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (Green \(n\bmod 4=3\) even-\(j\) rest)

Through \(k\le 10\), covering Green rest xor on \(n\bmod 4=3\)
even \(j\) is \(1\) iff \(k\neq 1\), and odd \(j\) is \(1\) iff
\(k=1\). Green rest on \(n\bmod 4=1\) even \(j\) is \(1\) iff
\(k\le 1\), and odd \(j\) is \(1\) iff \(k=0\) or \(k\ge 3\).
Status: **certified** \(k\le 10\), **prefix** all \(k\).
**Killed:** Green \(n\bmod 4=0\) tot equals Green \(n\bmod 4=3\)
even-\(j\). **Killed:** packed \(n\bmod 4=3\) even-\(j\) equals
Green \(n\bmod 4=3\) even-\(j\). **Killed:** Green \(n\bmod 4=3\)
even-\(j\) identically \(1\).

## Verdict

`CERTIFIED` (Green \(n\bmod 4=3\) even-\(j\) is \(1\) iff \(k\neq 1\)
through \(k\le 10\); odd \(j\) is \(1\) iff \(k=1\); Green
\(n\bmod 4=1\) even-/odd-\(j\) closed forms through \(k\le 10\);
\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (Green \(n\bmod 4=0\) equals Green \(n\bmod 4=3\) even-\(j\);
packed \(n3e\) equals Green \(n3e\); Green \(n3e\) identically \(1\);
cellwise 2-fold packed AND).
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

- `research/cycle_si.md` (this note)
- `research/cycle_si.py`
- `research/cycle_si.json`
