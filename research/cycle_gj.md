# Cycle GJ: at cone-hi hit \(q\), Green clock \(m=2U(Q-q)-2\)

Cycle GG’s hits \(s=t_0+1+q\cdot 2U\) have Green clock
\(m=T-s-1=2U(Q-q)-2\). For Cycle GI’s gap \(r_*-\chi\), this is
\(m=2U-2+\mathrm{gap}/2\). Residue \(m\equiv 2U-2\pmod{2U}\), so
Cycle FW gives \(G(m,2U-2)=G(2U-2,2U-2)=1\). The clock is **not**
\(2U-2\) on pre-cone hits and is **not** independent of \(q\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: a formula for the Green clock at the \(Q\) hits
does not prove covering never-fail.

Helper: `python3 research/cycle_gj.py --certify` (~0.01s). Dump:
`research/cycle_gj.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FW/GG/GI (algebraic \(k\le 11\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (\(m=2U(Q-q)-2=2U-2+\mathrm{gap}/2\); \(G=1\))

Certified \(k\le 11\), \(W\in\{4U,8U,16U\}\). Last hit \(q=Q-1\)
recovers Cycle GE’s \(m=2U-2\) at \(s=W+1\). For \(W=8U\), the two
clocks are \(4U-2\) then \(2U-2\).

## Killed

\(m=2U-2\) on pre-cone: at \(k=2\), \(W=8U\), \(q=0\), \(m=4U-2\).
\(m\) independent of \(q\): \(4U-2\) vs \(2U-2\). Last-hit
\(m=W/2-2\) when \(Q>1\): \(2U-2\neq 4U-2\).

## Verdict

`LEMMA` (\(m=2U(Q-q)-2\); \(m=2U-2+\mathrm{gap}/2\); \(G(m,2U-2)=1\)).
`KILLED` (\(m=2U-2\) on pre-cone; \(m\) independent of \(q\); last
\(m=W/2-2\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_gj.md` (this note)
- `research/cycle_gj.py`
- `research/cycle_gj.json`
