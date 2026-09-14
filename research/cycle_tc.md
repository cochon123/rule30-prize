# Cycle TC: clip-edge pal-pair packed AND is \(0\) on both sides

Clip-edge pal-right is \(j=5U\), packed \(p=0\). Packed AND at
\(p=0\) is bits \(0\) and \(-1\); bit \(-1\) is \(0\), and the
4-tuple `0001` is not an AND-one. Clip-edge distance \(d=5U-n\)
satisfies \(2d=t+1\) at covering time \(t=10U-2n-1\), so spat(\(d\))
reads packed bits \(2t+1\) and \(2t+2\), past the support \(0..2t\).
Both sides vanish, so clip-edge pal-pair raw is \(0\) cellwise and
does not contribute to pal-pair raw tot. Do **not** claim clip-edge
raw tot is \(1\). Do **not** claim odd pal-pairs 2-fold all parent
pal-pairs. Do **not** claim pal-center tot equals \(S\oplus T\).
This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all
\(k\). Do **not** catalogue leftover \(p\) one-by-one. Do **not**
catalogue further \(S\)/\(T\) subregions unless the experiment
answers why \(E_k=0\). Do **not** claim pal-left leftover xor
vanishes for all \(k\). Do **not** claim
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

Certify: `python3 research/cycle_tc.py --certify`.
Dump: `research/cycle_tc.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/OJ/PB/QV/SO/SS/SU/SV/SX/SY/TB (clip-edge pal-pair packed
AND is \(0\) on both sides; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (clip-edge pal-right is packed \(p=0\), AND \(=0\))

On \(q=10\), packed \(p=10U-2j\), so \(j=5U\) has \(p=0\). Packed
AND at \(p=0\) is odd-row bits \(0\) and \(-1\). Negative bits are
\(0\), and the 4-tuple `0001` is not an AND-one. Status: **lemma**.
Algebra through \(k\le 64\); freeze through \(t<256\).

## Lemma (clip-edge pal-left spat sits past packed bit \(2t\))

Clip-edge distance is \(d=5U-n\). Covering time \(t=10U-2n-1\)
gives \(2d=t+1\), hence spat(\(d\)) reads bits \(2t+1\) and
\(2t+2\). Packed support at time \(t\) is bits \(0..2t\) (Cycle
SS). Status: **lemma**. Algebra through \(k\le 64\); support through
\(t<256\).

## Lemma (clip-edge pal-pair raw is \(0\) cellwise)

Both spat sides vanish, so clip-edge pal-pair AND-mismatch is \(0\)
on every such cell. Those \(J_{k+2}\) pairs do not contribute to
pal-pair raw tot. Status: **lemma**. Cellwise through \(k\le 8\).
**Killed:** clip-edge raw tot is \(1\).

## Verdict

`LEMMA` (clip-edge pal-right is packed \(p=0\); packed AND at
\(p=0\) is \(0\); clip-edge pal-left spat sits past \(2t\);
clip-edge pal-pair raw is \(0\) cellwise).
`CERTIFIED` (clip-edge AND through \(k\le 8\); \(p=0\) freeze
through \(t<256\); \(E_k=0\) on odd-\(s\) rest for \(q=10\),
\(k\le 10\)).
`KILLED` (clip-edge raw tot is \(1\); odd pal-pairs 2-fold all
parent pal-pairs; pal-center even tot period \(8\); pal-center tot
equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_tc.md` (this note)
- `research/cycle_tc.py`
- `research/cycle_tc.json`
