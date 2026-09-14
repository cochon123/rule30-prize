# Cycle SL: covering Green \(p=0\) on even \(n\) at \(k\) equals tot at \(k-1\)

For \(k\ge 1\), \(G(2m,5\cdot 2^k)=G(m,5\cdot 2^{k-1})\) and the
covering even-\(n\) window at packed \(p=0\) is exactly the parent
covering window, so even-\(n\) xor equals Cycle QI tot at \(k-1\).
That tot is \(1\) for every \(k\), hence even-\(n\) xor is \(1\) for
\(k\ge 1\) and odd-\(n\) xor is \(0\). At \(k=0\), \(j=5\) is odd,
even \(n\) vanish, tot is \(1\), odd-\(n\) is \(1\). This lifts
Cycle SJ's split to all \(k\). Many odd \(n\) still fire for
\(k\ge 1\); they cancel, so the column is **not** empty. Cycle SI
rest on \(n\bmod 4=3\) even \(j\) remains PREFIX (the clip fold
is still certified \(k\le 8\)). Do **not** claim that rest identity
for all \(k\). Packed rest is **not** this bit. This is **not**
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

Certify: `python3 research/cycle_sl.py --certify`.
Dump: `research/cycle_sl.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/KH/OJ/PC/QG/QI/QV/SI/SJ/SK (covering Green \(p=0\) xor on
odd \(n\) is \(1\) iff \(k=0\) for all \(k\); even \(n\) equals
parent tot; no Fermat table, no extra window, no \(n_0=16\)
window, no packed covering \(k=11\)).

## Lemma (clip-edge \(p=0\) doubling)

For \(k\ge 1\), covering Green \(G=1\) xor at packed \(p=0\) on
even \(n\) equals tot at \(k-1\) (hence \(1\)). Odd-\(n\) xor is
\(1\) iff \(k=0\). Status: **lemma**. Walked \(k\le 12\); cellwise
doubling on \(1\le k\le 8\). **Killed:** odd \(n\) at \(p=0\) empty
for \(k\ge 1\).

## Verdict

`LEMMA` (covering Green \(p=0\) even-\(n\) xor at \(k\) equals tot
at \(k-1\); odd-\(n\) xor is \(1\) iff \(k=0\); Cycle QI tot \(1\);
Cycle AL doubling).
`CERTIFIED` (those xors through \(k\le 12\); doubling window
through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest for \(q=10\),
\(k\le 10\)).
`KILLED` (odd \(n\) at \(p=0\) empty for \(k\ge 1\); cellwise
2-fold packed AND).
`PREFIX` (Cycle SI rest n3 even-\(j\) for all \(k\); even-\(n\)
rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\) for all
\(k\); packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_sl.md` (this note)
- `research/cycle_sl.py`
- `research/cycle_sl.json`
