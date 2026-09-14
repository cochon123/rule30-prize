# Cycle SU: covering packed AND is next-row consecutive bits at \(2(n-j)\)

On \(q=10\), even snapshot \(s=10U-2n-2\) and packed \(p=10U-2j\),
so \(p-(s+1)=2(n-j)+1\). Cycle HH packed AND is odd-\(s\) bits
\(p\) and \(p-1\), hence AND \(= x(s+1,2d)\land x(s+1,2d+1)\) with
\(d=n-j\). Pal-center is the \(d=0\) case (Cycle ST). Pal-pair raw
AND-mismatch is that predicate at \(d\) xor at \(-d\). Do **not**
claim pal-center tot equals \(S\oplus T\). Do **not** claim AND
equals the left spat bit alone. Do **not** claim AND identically
\(0\). This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\) for
all \(k\). Do **not** catalogue leftover \(p\) one-by-one. Do
**not** catalogue further \(S\)/\(T\) subregions unless the
experiment answers why \(E_k=0\). Do **not** claim pal-left leftover
xor vanishes for all \(k\). Do **not** claim
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

Certify: `python3 research/cycle_su.py --certify`.
Dump: `research/cycle_su.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/OJ/PB/QV/SO/SS/ST (covering packed AND is next-row
consecutive bits at \(2(n-j)\); no Fermat table, no extra window,
no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (covering packed AND \(= x(s+1,2d)\land x(s+1,2d+1)\))

On \(q=10\), \(s=10U-2n-2\) and \(p=10U-2j\), so
\(p-(s+1)=2d+1\) with \(d=n-j\). Cycle HH packed AND is the
odd-row bits \(p\) and \(p-1\). Two-sided coords give
\(x(s+1,2d)=\) packed bit \(s+1+2d\) and \(x(s+1,2d+1)=\) packed
bit \(s+2+2d\). Hence covering packed AND \(= x(s+1,2d)\land
x(s+1,2d+1)\). Pal-center is \(d=0\). Status: **lemma**. Cellwise
through \(k\le 8\); algebra through \(k\le 64\). **Killed:** AND
equals the left spat bit alone. **Killed:** AND identically \(0\).

## Lemma (pal-pair raw AND-mismatch is spat(\(d\)) xor spat(\(-d\)))

A clipped pal-pair has partners at \(d\) and \(-d\). Raw packed
AND-mismatch is covering spat at \(d\) xor at \(-d\). Rest
mismatch differs when a side is forced. Status: **lemma**.
**Killed:** pal-center tot equals \(S\oplus T\).

## Verdict

`LEMMA` (covering packed AND \(= x(s+1,2d)\land x(s+1,2d+1)\);
pal-center is \(d=0\); pal-pair raw AND-mismatch is spat(\(d\))
xor spat(\(-d\))).
`CERTIFIED` (spatial identity through \(k\le 8\); \(E_k=0\) on
odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (pal-center tot equals \(S\oplus T\); AND equals the
left spat bit alone; AND identically \(0\); cellwise 2-fold packed
AND).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_su.md` (this note)
- `research/cycle_su.py`
- `research/cycle_su.json`
