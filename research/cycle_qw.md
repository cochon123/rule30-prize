# Cycle QW: covering Green even-\(n\) rest is \(1\) iff \(k\neq 1\)

Cycle QV's 2-fold sends even-\(n\) clipped \(G=1\) at \(k\) to all
clipped \(G=1\) at \(k-1\), so even-\(n\) \(G=1\) xor equals Cycle QH's
clip xor at \(k-1\), which is \(1\) iff \(k=1\). For \(k\ge 1\) forced
\(p=6\) and \(p=14\) have odd \(j\), hence vanish on even \(n\), and
Cycle PC's even-\(n\) \(p=4\) is the unique cell \(n=3U-2\), xor \(1\).
Green even-\(n\) rest off forced is therefore \(1\) iff \(k\neq 1\).
Green odd-\(n\) rest is \(1\) iff \(k\in\{0,2\}\); for \(k\ge 3\) the
Green residual lives only on even \(n\) (Cycle QH tot \(1\) iff
\(k\ge 3\)). Packed even-\(n\) rest is **not** this bit (\(k=1\): packed
\(1\) vs Green \(0\); \(k=3\): packed \(0\) vs Green \(1\)). This is
**not** rest \(=S\oplus T\) for all \(k\). **Not** \(E_k=0\) for all
\(k\). Do **not** catalogue leftover \(p\) one-by-one. Do **not**
catalogue further \(S\)/\(T\) subregions unless the experiment answers
why \(E_k=0\). Do **not** claim pal-left leftover xor vanishes for all
\(k\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all
\(k\). Do **not** push the even-spine scan past \(k=18\). Do **not**
bump all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim Green even-\(n\) rest equals packed even-\(n\) rest.
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\) for
all \(k\).

Certify: `python3 research/cycle_qw.py --certify` (~0.50s).
Dump: `research/cycle_qw.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/LZ/PC/QH/QO/QU/QV (Green even/odd rest through \(k\le 8\);
even-\(n\) \(p=4\) unique through \(k\le 8\); packed kill from QO
\(k\le 10\); no Fermat table, no extra window, no \(n_0=16\) window,
no packed covering \(k=11\)).

## Certificate (Green even-\(n\) rest is \(1\) iff \(k\neq 1\))

For \(k\ge 2\): even-\(n\) \(G=1\) xor vanishes by Cycle QV plus clip
xor \(A(k-1)=0\); even-\(n\) forced xor is the unique \(p=4\) cell, so
Green even-\(n\) rest is \(1\). Green odd-\(n\) rest is \(1\) only at
\(k=2\) among \(k\ge 1\). Status: **lemma**. **Killed:** Green even-\(n\)
rest equals packed even-\(n\) rest.

## Verdict

`LEMMA` (covering Green even-\(n\) rest off forced is \(1\) iff
\(k\neq 1\); Green odd-\(n\) rest is \(1\) iff \(k\in\{0,2\}\)).
`CERTIFIED` (Green split through \(k\le 8\); even-\(n\) \(p=4\) unique
through \(k\le 8\); \(E_k=0\) on odd-\(s\) rest for \(q=10\),
\(k\le 10\)).
`KILLED` (Green even-\(n\) rest equals packed even-\(n\) rest; cellwise
2-fold packed AND; even-\(n\) rest equals \(S\oplus T\) at \(k-1\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_qw.md` (this note)
- `research/cycle_qw.py`
- `research/cycle_qw.json`
