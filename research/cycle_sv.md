# Cycle SV: even pal-pair rest is raw xor \(1\) for \(k\ge 1\)

Pal-left packed \(p\) exceeds pal-center min \(2U+2\), so pal-left is
never forced for \(k\ge 3\). Even \(n\) only meets forced pal-right at
\(p=4\), \(j=5U-2\). That Green cell is unique: \(n=3U-2\). Packed AND
at \(p=4\) is bits \(3\) and \(4\) on the odd row; bit \(4\) is \(1\)
for \(t\ge 2\) and bit \(3\) equals \(t\bmod 2\) for \(t\ge 2\), so
AND \(=1\) on every odd \(t\ge 3\). Even pal-pair rest tot is
therefore raw spat-mismatch xor \(1\) for every \(k\ge 1\). Do
**not** claim odd pal-pair rest equals raw for all \(k\). Do **not**
claim pal-center tot equals \(S\oplus T\). This is **not** rest
\(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not** catalogue
leftover \(p\) one-by-one. Do **not** catalogue further \(S\)/\(T\)
subregions unless the experiment answers why \(E_k=0\). Do **not**
claim pal-left leftover xor vanishes for all \(k\). Do **not** claim
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

Certify: `python3 research/cycle_sv.py --certify`.
Dump: `research/cycle_sv.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/BV/HH/HU/KH/LZ/OJ/PB/QV/SO/SR/ST/SU (even pal-pair rest is
raw xor \(1\) for \(k\ge 1\); no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (pal-left never forced for \(k\ge 3\))

Pal-left \(j<n\) has packed \(p>\) pal-center \(p\ge 2U+2\). For
\(k\ge 3\) that min sits past \(\{4,6,14\}\). Pal-pair rest xor raw
is therefore pal-right forced AND tot. Status: **lemma**.

## Lemma (unique even pal-right at \(p=4\) is \(n=3U-2\))

Even \(n\) visits only even \(j\), so among forced pal-right
\(j\in\{5U-2,5U-3,5U-7\}\) only \(p=4\). After folding, Green ones
at that column are \(t=q\cdot 2^{k-2}-1\) with \(q\) odd; covering
range forces \(q=3\), hence \(n=3U-2\). \(G(3U-2,5U-2)=1\) by
\(k\) even/odd folds to \(G(2,4)=1\). Status: **lemma**. Cellwise
through \(k\le 12\); \(q\)-range through \(k\le 64\). **Killed:**
even \(p=4\) pal-right empty.

## Lemma (packed AND at \(p=4\) is \(1\) on odd \(t\ge 3\))

Packed bit \(4\) is \(1\) for \(t\ge 2\) (Cycle BV). Bit \(3\)
updates as \(1\oplus\) bit \(3\) once bits \(1,2\) freeze, so bit
\(3=t\bmod 2\) for \(t\ge 2\). On odd \(t\ge 3\), bits \(3\) and
\(4\) are both \(1\), hence AND at \(p=4\) is \(1\). The unique
even pal-right therefore contributes \(1\). Even pal-pair rest tot
equals raw spat-mismatch xor \(1\) for every \(k\ge 1\). Status:
**lemma**. Left freeze through \(t<128\); forced pal-right AND walk
through \(k\le 10\). **Killed:** even pair rest equals raw. **Killed:**
AND at \(p=4\) identically \(1\) (fails at \(t=0\)).

## Verdict

`LEMMA` (pal-left never forced for \(k\ge 3\); unique even \(p=4\)
pal-right is \(n=3U-2\); packed AND at \(p=4\) is \(1\) on odd
\(t\ge 3\); even pal-pair rest is raw xor \(1\) for \(k\ge 1\)).
`CERTIFIED` (Green unique through \(k\le 12\); forced pal-right AND
through \(k\le 10\); odd pal-right AND tot \(0\) for \(3\le k\le 10\);
\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (pal-center tot equals \(S\oplus T\); even pair rest equals
raw; AND at \(p=4\) identically \(1\); cellwise 2-fold packed AND).
`PREFIX` (odd pal-pair rest equals raw for all \(k\ge 3\); even-\(n\)
rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\) for all \(k\);
packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for all \(k\);
leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_sv.md` (this note)
- `research/cycle_sv.py`
- `research/cycle_sv.json`
