# Cycle GI: at cone-hi hit \(q\), cone-hi sits \(4U(Q-1-q)\) left of \(r_*\)

Cycle GG’s hits \(s=t_0+1+q\cdot 2U\) have cone-hi \(\chi=2U+2+4U q\).
The dual column is \(r_*=W-2U+2\), so \(r_*-\chi=4U(Q-1-q)\). The gap
vanishes iff \(q=Q-1\) (the in-cone collapse at \(s=W+1\)). Gap is
**not** 0 on pre-cone hits and is **not** independent of \(q\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: a formula for the cone-hi/\(r_*\) gap at the \(Q\)
hits does not prove covering never-fail.

Helper: `python3 research/cycle_gi.py --certify` (~0.01s). Dump:
`research/cycle_gi.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles CA/GB/GG/GH (algebraic \(k\le 11\); no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (\(\chi=2U+2+4U q\); gap \(4U(Q-1-q)\))

Certified \(k\le 11\), \(W\in\{4U,8U,16U\}\). Gap 0 iff \(q=Q-1\).

## Killed

Gap 0 on pre-cone: at \(k=2\), \(W=8U\), \(q=0\), gap \(=4U\). Gap
independent of \(q\): \(4U\) vs \(0\). \(\chi=r_*\) at \(t_0+1\) for
\(W=8U\): \(2U+2\neq 6U+2\).

## Verdict

`LEMMA` (\(\chi=2U+2+4U q\); gap \(4U(Q-1-q)\); zero iff last hit).
`KILLED` (gap 0 on pre-cone; gap independent of \(q\); \(\chi=r_*\) at
\(t_0+1\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_gi.md` (this note)
- `research/cycle_gi.py`
- `research/cycle_gi.json`
