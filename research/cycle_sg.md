# Cycle SG: packed rest on odd \(n\), odd \(j\) is \(1\) iff \(k\in\{4,9,10\}\) through \(k\le 10\)

Covering packed rest cells split by \(n\) parity and \(j\) parity.
Even-\(n\) \(G=1\) lives only on even \(j\) (Cycle QV). Odd-\(n\)
odd-\(j\) packed rest xor is \(1\) iff \(k\in\{4,9,10\}\) through
\(k\le 10\), so odd-\(n\) even-\(j\) tot equals odd rest xor that
bit. Cycle SD consecutive Green AND xor on \(G=1\) odd-\(j\)
covering is \(0\) through \(k\le 8\), so packed odd-\(j\) tot is
**not** that Green tot (\(k=4\) is \(1\) vs \(0\)). Do **not**
claim the exception set \(\{4,9,10\}\) for all \(k\). This is
**not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do
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

Certify: `python3 research/cycle_sg.py --certify` (~9.77s).
Dump: `research/cycle_sg.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HJ/HS/HU/KH/LZ/OJ/PB/QO/QU/QV/SD/SF (packed rest on odd
\(n\), odd \(j\) is \(1\) iff \(k\in\{4,9,10\}\) through \(k\le 10\);
no Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (packed odd-\(n\) odd-\(j\) rest tot)

Through \(k\le 10\), covering packed rest xor on odd \(n\) and odd
\(j\) is \(1\) iff \(k\in\{4,9,10\}\). Odd-\(n\) even-\(j\) tot
equals odd rest xor that bit. Status: **certified** \(k\le 10\),
**prefix** all \(k\). **Killed:** identically \(0\). **Killed:**
equals Cycle SD consecutive Green AND xor. **Killed:** the set
\(\{4,9,10\}\) for all \(k\).

## Verdict

`CERTIFIED` (packed odd-\(n\) odd-\(j\) rest tot through \(k\le 10\);
odd-\(n\) even-\(j\) tot equals odd rest xor that bit; \(E_k=0\) on
odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (identically \(0\); equals SD consecutive AND xor; cellwise
2-fold packed AND).
`PREFIX` (the set \(\{4,9,10\}\) for all \(k\); even-\(n\) rest xor
at \(k\) equals odd-\(n\) rest xor at \(k-1\) for all \(k\); packed
rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for all \(k\); leftover
after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_sg.md` (this note)
- `research/cycle_sg.py`
- `research/cycle_sg.json`
