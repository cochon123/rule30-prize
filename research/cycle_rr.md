# Cycle RR: covering \(n\bmod 4=2\) rest tot equals parent odd tot except \(k\in\{2,4,8\}\)

Cycle QU even-\(n\) rest tot equals parent odd tot through \(k\le 10\).
Parent odd \(n\) 2-folds onto child \(n\bmod 4=2\), so cellwise 2-fold
AND would make \(n\bmod 4=2\) tot equal parent odd tot. The 2-fold
AND-mismatch tot on \(n\bmod 4=2\) is 1 iff \(k\in\{2,4,8\}\) through
\(k\le 10\), and \(n\bmod 4=2\) tot equals parent odd xor that bit.
Dual: mismatch on \(n\bmod 4=0\) is 1 iff \(k\in\{1,3,4,9\}\), and
the two mismatch tots xor to parent even tot (Cycle QV). Unique
\(n\bmod 4=2\) tot is 0, so leftover \(n\bmod 4=2\) tot is the same
fold. This is **not** \(n\bmod 4=2\) tot equals parent odd for all
\(k\le 10\). **Not** the exception sets for all \(k\). This is
**not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do
**not** catalogue leftover \(p\) one-by-one. Do **not** catalogue
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
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_rr.py --certify`.
Dump: `research/cycle_rr.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/PB/QO/QU/QV/RB/RC/RQ (\(n\bmod 4=2\) rest tot equals parent
odd tot except \(k\in\{2,4,8\}\) through \(k\le 10\); mismatch on
\(n\bmod 4=0\) is 1 iff \(k\in\{1,3,4,9\}\); prefixes QO dump rather
than re-walking; no Fermat table, no extra window, no \(n_0=16\)
window, no packed covering \(k=11\)).

## Lemma (n2 rest tot equals parent odd tot except \(k\in\{2,4,8\}\), \(k\le 10\))

2-fold AND-mismatch tot on \(n\bmod 4=2\) is 1 iff \(k\in\{2,4,8\}\)
through \(k\le 10\). Dual mismatch on \(n\bmod 4=0\) is 1 iff
\(k\in\{1,3,4,9\}\). Status: **certified** \(k\le 10\). **Killed:**
n2 tot equals parent odd for all \(k\le 10\). **Prefix:** those
exception sets for all \(k\).

## Verdict

`CERTIFIED` (\(n\bmod 4=2\) rest tot equals parent odd tot except
\(k\in\{2,4,8\}\) through \(k\le 10\); mismatch on \(n\bmod 4=2\) is
1 iff \(k\in\{2,4,8\}\); mismatch on \(n\bmod 4=0\) is 1 iff
\(k\in\{1,3,4,9\}\); \(E_k=0\) on odd-\(s\) rest for \(q=10\),
\(k\le 10\)).
`KILLED` (n2 tot equals parent odd for all \(k\le 10\); cellwise
2-fold packed AND).
`PREFIX` (mismatch on \(n\bmod 4=2\) is 1 iff \(k\in\{2,4,8\}\) for
all \(k\); even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_rr.md` (this note)
- `research/cycle_rr.py`
- `research/cycle_rr.json`
