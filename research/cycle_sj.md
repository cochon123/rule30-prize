# Cycle SJ: covering Green \(p=0\) xor on odd \(n\) is \(1\) iff \(k=0\) through \(k\le 12\)

Cycle QI clip-edge packed \(p=0\) tot is \(1\) for every \(k\). Split
by \(n\) parity: odd-\(n\) xor is \(1\) iff \(k=0\) and even-\(n\) xor
is \(1\) iff \(k\ge 1\) through \(k\le 12\) (Cycle QI's \(k_{\mathrm{hi}}\)).
Many odd \(n\) still fire for \(k\ge 1\); they cancel, so the column
is **not** empty. Cycle QI odd-\(n\) even-\(j\) clipped \(G=1\) equals
\(p=0\) at \(k-1\), so \(n\bmod 4=3\) even-\(j\) clip equals parent
odd \(p=0\) (\(1\) iff \(k=1\) for \(k\ge 1\)) through \(k\le 8\).
That clip bit is **not** Cycle SI's Green rest on the same cells
(forced remains). Do **not** claim those identities for all \(k\).
This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\).
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
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_sj.py --certify` (~0.49s).
Dump: `research/cycle_sj.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/KH/OJ/PC/QG/QI/QV/SI (covering Green \(p=0\) xor on odd \(n\)
is \(1\) iff \(k=0\) through \(k\le 12\); even \(n\) is \(1\) iff
\(k\ge 1\); no Fermat table, no extra window, no \(n_0=16\) window,
no packed covering \(k=11\)).

## Lemma (clip-edge \(p=0\) odd \(n\))

Through \(k\le 12\), covering Green \(G=1\) xor at packed \(p=0\)
on odd \(n\) is \(1\) iff \(k=0\), and on even \(n\) is \(1\) iff
\(k\ge 1\). Through \(k\le 8\), clipped \(G=1\) on \(n\bmod 4=3\)
even \(j\) equals parent odd \(p=0\). Status: **certified**
\(k\le 12\) / \(k\le 8\), **prefix** all \(k\). **Killed:** odd \(n\)
at \(p=0\) empty for \(k\ge 1\). **Killed:** clip \(n\bmod 4=3\)
even-\(j\) equals Green rest on those cells.

## Verdict

`CERTIFIED` (covering Green \(p=0\) odd-\(n\) xor is \(1\) iff \(k=0\)
through \(k\le 12\); even-\(n\) is \(1\) iff \(k\ge 1\); \(n\bmod 4=3\)
even-\(j\) clip equals parent odd \(p=0\) through \(k\le 8\);
\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (odd \(n\) at \(p=0\) empty for \(k\ge 1\); clip equals rest
on \(n\bmod 4=3\) even \(j\); cellwise 2-fold packed AND).
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

- `research/cycle_sj.md` (this note)
- `research/cycle_sj.py`
- `research/cycle_sj.json`
