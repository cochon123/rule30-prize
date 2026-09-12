# Cycle EI: leftover after extra 57888 cannot hold odd 87468

The 57888 second-even group lands from \(k=8\) entirely in annulus
\(k=15\) at packed \((58144,58399]\). Remaining extra to 87468 is
29580. That is strictly less than worst-case leftover
\(2^{15}=32768\), so \(\mathrm{threshold}(29580)=15\) equals the
landing \(k\) and a later odd can fit in the worst case. Actual
leftover after the image is at most \(65536-58144=7392<29580\), so
87468 cannot sit in the same \(k=15\) high half on this path. Kills:
remaining after 57888 exceeds \(2^{15}\). Do **not** claim leftover
empty at \(k=16\). Do **not** claim packed 58287. Do **not** claim a
closed form for 29580/87468. Do **not** claim an 11-bit gap. Do
**not** compute \(\varphi^{(3,5,9)}\) at \(k=16\).

Not a prize claim: an actual-leftover gap on one extra does not force
the next odd into a 2-power high half for every later \(k\).

Helper: `python3 research/cycle_ei.py --certify`. Dump:
`research/cycle_ei.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles ED, EH (no new packed run, no Fermat table, no
\(n_0=16\) window bump).

## Lemma (remaining 29580; \(\mathrm{threshold}=15\))

\(87468-57888=29580\). Then \(2^{14}<29580\le 2^{15}\), so
\(\mathrm{threshold}(29580)=15\), equal to the landing annulus of extra
57888 from \(k=8\).

## Lemma (worst-case \(k=15\) leftover can fit 29580)

Worst-case leftover is \(2^{15}=32768\ge 29580\). Cycle ED’s
skip-becomes-dangerous pattern applies to this post-second-even gap:
if the second even sat at packed \(2^{15}+1\), a later odd of extra
29580 would fit in the same high half.

## Lemma (actual 57888-image leftover cannot fit 87468)

The image of \((2^8,2^9]\) under extra 57888 is
\((58144,58399]\subset(2^{15},2^{16}]\). Leftover after the right
endpoint is \(65536-58399=7137\); after the left endpoint 7392. Both
are \(<29580\). On the 57888 path, 87468 therefore lands in \(k=16\),
not in the \(k=15\) leftover.

## Killed

Remaining extra after 57888 does not exceed \(2^{15}\). Worst-case
leftover at the landing annulus can fit the next odd; only the actual
late landing of extra 57888 keeps \(k=15\) free of a later odd.

## Verdict

`LEMMA` (remaining 29580; threshold 15; worst-case \(k=15\) leftover
can fit 29580; actual 57888-image leftover cannot).
`KILLED` (remaining after 57888 exceeds \(2^{15}\)).
`PREFIX` (leftover empty at \(k=16\); packed 58287; closed form for
29580; at-most-one-odd for all \(k\); period-\(H\) seed; \(\pi\)
formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ei.md` (this note)
- `research/cycle_ei.py`
- `research/cycle_ei.json`
