# Cycle SK: covering Green forced on \(n\bmod 4=3\) even \(j\) is \(1\) iff \(k\ge 1\)

Covering forced columns are \(j=5U-2,5U-3,5U-7\) (\(p=4,6,14\)).
For \(k\ge 1\), \(U\) is even, so those \(j\) are even, odd, odd:
even-\(j\) forced is \(p=4\). Cycle PC's \(p=4\) set on
\(n\bmod 4=3\) has odd count for \(k\ge 1\) (closed count
\(k-1+(k\bmod 2)\)), xor \(1\); at \(k=0\) even-\(j\) is \(p=6\)
on \(\{1,2\}\), so \(n\bmod 4=3\) even-\(j\) is \(0\). Odd-\(j\)
is \(1\) iff \(k\le 2\), recovering Cycle RV's n3 tot. Even-\(j\)
on \(n\bmod 4=1\) is \(1\) for every \(k\); odd-\(j\) is \(0\).
Cycle SI rest n3 even-\(j\) is Cycle SJ's clipped \(G=1\) xor this
bit (PREFIX all \(k\) via the clip-edge lift). Do **not** claim
that rest identity for all \(k\) without Cycle SJ's \(p=0\) odd-\(n\)
lift. Packed \(n\bmod 4=3\) even-\(j\) rest is **not** this bit.
Do **not** claim those identities for all \(k\) as packed rest.
This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all
\(k\). Do **not** catalogue leftover \(p\) one-by-one. Do **not**
catalogue further \(S\)/\(T\) subregions unless the experiment
answers why \(E_k=0\). Do **not** claim pal-left leftover xor
vanishes for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\)
covering packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_sk.py --certify` (~0.17s).
Dump: `research/cycle_sk.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/KH/OJ/PC/QV/QX/RV/SI/SJ (Green forced on \(n\bmod 4=3\)
even \(j\) is \(1\) iff \(k\ge 1\); odd \(j\) is \(1\) iff
\(k\le 2\); no Fermat table, no extra window, no \(n_0=16\)
window, no packed covering \(k=11\)).

## Lemma (Green forced \(n\bmod 4=3\) even-\(j\))

Green forced xor on \(n\bmod 4=3\) even \(j\) is \(1\) iff
\(k\ge 1\), and odd \(j\) is \(1\) iff \(k\le 2\). Green forced
on \(n\bmod 4=1\) even \(j\) is \(1\) for every \(k\); odd \(j\)
is \(0\). Status: **lemma**. Walked \(k\le 12\). **Killed:**
identically \(1\). **Killed:** Green \(n\bmod 4=0\) tot equals
this even-\(j\) bit.

## Verdict

`LEMMA` (Green forced on \(n\bmod 4=3\) even \(j\) is \(1\) iff
\(k\ge 1\); odd \(j\) is \(1\) iff \(k\le 2\); Green forced on
\(n\bmod 4=1\) even \(j\) is \(1\) and odd \(j\) is \(0\);
Cycle PC \(p=4\) set; Cycle RV n3 tot).
`CERTIFIED` (those xors through \(k\le 12\); \(E_k=0\) on
odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (forced n3 even-\(j\) identically \(1\); Green n0 tot
equals forced n3 even-\(j\); cellwise 2-fold packed AND).
`PREFIX` (Cycle SI rest n3 even-\(j\) for all \(k\) via
\(g_1\oplus\) forced; even-\(n\) rest xor at \(k\) equals
odd-\(n\) rest xor at \(k-1\) for all \(k\); packed rest
\(=S\oplus T\) for all \(k\); \(E_k=0\) for all \(k\); leftover
after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_sk.md` (this note)
- `research/cycle_sk.py`
- `research/cycle_sk.json`
