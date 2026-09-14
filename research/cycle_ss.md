# Cycle SS: clip-unpaired packed AND is \(0\) for all \(k\)

Unpaired covering cells have pal-partner \(2n-j>5U\), so
\(p-(2s+6)=2(2n-j-5U-1)\ge 0\) with \(s=10U-2n-2\) the even
snapshot. Thus \(p\ge 2s+6\) and \(p-3>2s\). Packed support at time
\(s\) is bits \(0..2s\) (right edge bit \(2s=1\)), so the 4-tuple is
`0000`, not an AND-one. Clip-unpaired packed AND vanishes for every
\(k\), even and odd \(n\). Rest tot is pal-center AND xor pal-pair
AND-mismatch for all \(k\). Do **not** claim pal-center tot equals
\(S\oplus T\). This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\)
for all \(k\). Do **not** catalogue leftover \(p\) one-by-one. Do
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

Certify: `python3 research/cycle_ss.py --certify` (~0.18s).
Dump: `research/cycle_ss.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/GE/HH/KH/OJ/PB/QV/SO/SR (clip-unpaired packed AND is \(0\) for
all \(k\); no Fermat table, no extra window, no \(n_0=16\) window,
no packed covering \(k=11\)).

## Lemma (unpaired columns sit past packed bit \(2s\))

On \(q=10\), covering even snapshot \(s=10U-2n-2\) and packed
\(p=10U-2j\). Clip-unpaired means \(2n-j>5U\), hence
\(p-(2s+6)=2(2n-j-5U-1)\ge 0\). Packed support at time \(s\) is
bits \(0..2s\). The 4-tuple at \(p-3..p\) is `0000`, which is not
an AND-one. Status: **lemma**. Cellwise unpaired bound through
\(k\le 8\); support width through \(s<128\); algebra through
\(k\le 64\). **Killed:** `0000` is an AND-one. **Killed:** even rest
equals \(S\oplus T\).

## Lemma (rest tot is pal-center xor pal-pair mismatch, all \(k\))

Every clipped \(G=1\) cell is a pal-center, a pal-pair, or
clip-unpaired. Unpaired packed AND is \(0\) for all \(k\), so rest
tot equals pal-center packed rest xor pal-pair AND-mismatch, for
every \(k\). Cycle SR certified that split through \(k\le 10\).
Status: **lemma**. **Killed:** pal-center tot equals \(S\oplus T\).

## Verdict

`LEMMA` (packed support bits \(0..2s\); unpaired \(p\) past \(2s\);
unpaired packed AND is \(0\) for all \(k\); rest tot is pal-center
xor pal-pair mismatch for all \(k\)).
`CERTIFIED` (unpaired bound through \(k\le 8\); support through
\(s<128\); \(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (`0000` is an AND-one; even rest equals \(S\oplus T\);
pal-center tot equals \(S\oplus T\); cellwise 2-fold packed AND).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ss.md` (this note)
- `research/cycle_ss.py`
- `research/cycle_ss.json`
