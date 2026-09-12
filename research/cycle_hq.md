# Cycle HQ: fresh AND is even factors of \((001)^\omega\); CONT is the terminator

FRESH 4-tuples are the even-offset 4-factors of \((001)^\omega\)
(bit \(i\) is 1 iff \(i\bmod 3=2\)). Period-3 both-AND
\(\{001001,010010,100100\}\) are the 6-factors. The unique
non-period-3 both-AND is the continuation terminator \(010011\).
Triple/quad minus the unique \(\ldots 11\) terminator are the 8/10
factors. Period-3 AND is **not** absent on covering windows. Not
**all** consecutive AND is period-3. Period-3 AND is **not** only on
\(G=1\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for
all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: a period-3 necklace for fresh AND does not give
a closed form along Green ones, so covering never-fail stays open.

Helper: `per3_word` / `CONT_TERM`. Certify:
`python3 research/cycle_hq.py --certify`. Dump:
`research/cycle_hq.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HI/HN/HO/HP (finite tables; covering \(k\le 6\);
no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (FRESH \(=\) even factors of \((001)^\omega\))

`CONT` is not a 4-factor. Certified by matching Cycle HI `FRESH`.

## Lemma (period-3 both-AND \(=\) 6-factors; `CONT_TERM` unique terminator)

`BOTH_AND \ {010011}` are the even-offset 6-factors.
`TRIPLE_AND \ {10010011}` and `QUAD_AND \ {0010010011}` are the
8/10-factors. Certified on \(J_6,J_{10}\) for \(k\le 6\). Odd-\(s\)
\(J\) XOR matches Cycles HF/HG.

## Killed

No covering period-3 AND: at \(k=0\), \(s=3\), \(n=1\), \(j=0\),
\(p=6\), six \(100100\). All consecutive AND is period-3: at
\(k=1\), \(s=19\), \(n=0\), \(j=0\), \(p=20\), six \(010011\).
Period-3 AND only on \(G=1\): at \(k=0\), \(s=3\), \(n=3\),
\(j=2\), \(p=6\), \(G=0\).

## Verdict

`LEMMA` (FRESH \(=\) even factors of \((001)^\omega\); period-3
both-AND \(=\) 6-factors; `CONT_TERM` unique non-period-3 both-AND).
`KILLED` (no covering period-3 AND; all consecutive AND is period-3;
period-3 AND only on \(G=1\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_hq.md` (this note)
- `research/cycle_hq.py`
- `research/cycle_hq.json`
