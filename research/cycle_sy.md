# Cycle SY: odd pal-pair rest equals raw for \(k\ge 3\)

Pal-left never forced for \(k\ge 3\). Odd pal-right forced AND tot
is \(0\) at \(p=4\) (even Green count after dropping unique even
\(n=3U-2\), all fire), \(1\) at \(p=6\) (odd count, bits \(5,6\)
fire on odd \(t\ge 3\)), and \(1\) at \(p=14\) (odd count; Cycle PD
fires on odd \(n\)). Those \(p=14\) covering times are
\(t\equiv 1\pmod{4}\), so the even snapshot sits in Cycle PD's
\(0011\) class. Odd corr vanishes, so odd pal-pair rest tot equals
pal-pair raw tot for every \(k\ge 3\). Do **not** claim pal-center
tot equals \(k\bmod 2\) (dies at \(k=12\)). Do **not** claim
pal-center tot equals \(S\oplus T\). This is **not** rest
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

Certify: `python3 research/cycle_sy.py --certify` (~0.26s).
Dump: `research/cycle_sy.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/LC/LD/LF/OJ/PB/PC/PD/QV/SO/SV/SW/SX (odd pal-pair rest
equals raw for \(k\ge 3\); no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (odd pal-right \(p=14\) times are \(t\equiv 1\pmod{4}\))

Cycle SX's covering times \(2U+5\), \(4U+1\), \(4U+5\) if \(k\) odd,
and \(4U+5+2^{i+1}\) are all \(1\bmod 4\) for \(k\ge 3\). The even
snapshot \(s=t-1\) is \(\equiv 0\pmod{4}\) and \(s\ge 2U+4\ge 20\).
Cycle PD: even \(t\ge 12\) has bits \(11..14=0011\) iff
\(t\equiv 0\pmod{4}\), hence AND at \(p=14\). Status: **lemma**.
Algebra through \(k\le 64\); period through even \(t<256\).

## Lemma (odd forced corr \(=0\) for \(k\ge 3\))

Pal-left never forced (Cycle SV). Odd pal-right AND tot: \(p=4\)
has even count \(k+(k\bmod 2)\) after dropping unique even
\(n=3U-2\), and Cycle SV fires on odd \(t\ge 3\), tot \(0\); \(p=6\)
has odd count and Cycle SW fires, tot \(1\); \(p=14\) has odd count
(Cycle PC) and Cycle PD fires on odd \(n\), tot \(1\). Xor \(0\).
Status: **lemma**. Green sets Cycles PC/SW; freezes Cycles SV/SW/PD.

## Lemma (odd pal-pair rest equals raw for \(k\ge 3\))

Pal-pair rest xor raw is the forced-side AND tot. That tot is \(0\),
so odd pal-pair rest tot equals pal-pair raw tot. Odd rest tot is
pal-center tot xor pal-pair raw tot. Status: **lemma**. **Killed:**
pal-center tot equals \(k\bmod 2\) (even \(n\) dies at \(k=12\)).
**Killed:** pal-center even tot equals odd tot (dies at \(k=10,12\)).

## Verdict

`LEMMA` (odd pal-right \(p=14\) times \(t\equiv 1\pmod{4}\); odd
forced corr \(0\) for \(k\ge 3\); odd pal-pair rest equals raw for
\(k\ge 3\); listed \(p=14\) cells all fire for all \(k\ge 3\)).
`CERTIFIED` (pal-center AP of \(c_t\land x(t,1)\) through \(k\le 12\);
\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (pal-center tot equals \(k\bmod 2\); pal-center even tot
equals odd tot; pal-center tot equals \(S\oplus T\); AND at \(p=14\)
on all odd \(t\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_sy.md` (this note)
- `research/cycle_sy.py`
- `research/cycle_sy.json`
