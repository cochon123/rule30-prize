# Cycle GB: palindrome dual of cone-hi is the stationary column \(r=W-2U+2\)

Cycle FT’s involution \(r\mapsto 2\mu-r\) with \(\mu=s-2U+1\) sends the
moving cone-hi \(2s-T\) to the fixed index \(r_*=W-2U+2\), whose degree
is constantly \(2U-2\) (Cycle FS). That column lies in Green support
\([lo,W]\) iff \(s\le\mathrm{clip}\), equals the lo-edge at clip, lies
in the cone-band iff \(W+1\le s\le\mathrm{clip}\), and equals the
palindrome center at \(s=W+1\). It is **not** in-support after clip,
**not** equal to lo except at clip, and **not** in-cone from \(t_0\).
The AND there does **not** fire whenever \(G=1\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push the
even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\) past
414990. Do **not** increment consecutive `11` to \(n_8\). Do **not**
walk \(32U\).

Not a prize claim: locating the dual column does not prove covering
never-fail (Cycle FX already killed hi AND whenever \(G=1\)).

Helper: `python3 research/cycle_gb.py --certify` (~0.01s). Dump:
`research/cycle_gb.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FS/FT/FU/GA (geometry \(k\le 10\); packed
AND at \(k=2\), \(W=8U\); no Fermat table, no extra window, no
\(n_0=16\) window).

## Lemma (dual of cone-hi is \(r_*=W-2U+2\))

\(2\mu-(2s-T)=W-2U+2\) and \(W-r_*=2U-2\). Certified on the full
window \(k\le 10\), \(W\in\{4U,8U,16U\}\).

## Lemma (in-support iff \(s\le\mathrm{clip}\); equals lo at clip)

Same samples. At clip, \(lo=r_*\).

## Lemma (in-cone iff \(W+1\le s\le\mathrm{clip}\); equals center at \(s=W+1\))

Same samples. At \(s=W+1\), \(\mu=r_*\) and cone-hi \(=r_*\).

## Killed

In-support after clip: at \(k=2\), \(W=8U\), \(s=\mathrm{clip}+1\),
\(lo>r_*\). Equal to lo always: at \(t_0\), \(lo=2\neq r_*\). In-cone
from \(t_0\): cone-hi \(=2U<r_*\). AND whenever \(G=1\): 1 live and 7
dead.

## Verdict

`LEMMA` (stationary dual column; in-support iff unclipped; in-cone on
\([W+1,\mathrm{clip}]\)).
`KILLED` (in-support after clip; \(r_*=lo\) always; in-cone from
\(t_0\); AND whenever \(G=1\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_gb.md` (this note)
- `research/cycle_gb.py`
- `research/cycle_gb.json`
