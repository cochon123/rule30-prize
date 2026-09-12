# Cycle GD: in-cone hi/\(r_*\) is 1 iff \(s=W+2^j\)

Cycle GC’s in-cone residues \([1,U]\) are the offsets \(2^j\) from
\(W\): \(s=W+2^j\) for \(0\le j<a=k+1\) lies in \([W+1,\mathrm{clip}]\)
and is exactly the \(G=1\) set. In particular \(s=W+1\) (\(j=0\))
always has \(G=1\): \(m=2U-2\) and \(G(m,m)=1\) (Cycle FF diagonal /
Cycle FU center). The range is **not** \(j\le a\) (\(s=W+2U\) is after
clip), and the base is **not** \(t_0\). The AND at those times is
**not** always live. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push the
even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\) past
414990. Do **not** increment consecutive `11` to \(n_8\). Do **not**
walk \(32U\).

Not a prize claim: an explicit list \(s=W+2^j\) does not prove covering
never-fail (Cycle GC already killed AND on all \(k+1\) times).

Helper: `python3 research/cycle_gd.py --certify` (~0.01s). Dump:
`research/cycle_gd.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FZ/GB/GC (times \(k\le 11\); Green
\(k\le 7\); packed AND at \(k=2\), \(W=8U\); no Fermat table, no extra
window, no \(n_0=16\) window).

## Lemma (\(s=W+2^j\))

Certified \(k\le 11\), \(W\in\{4U,8U,16U\}\). Green \(G(m,2U-2)=1\) at
those times, \(k\le 7\).

## Lemma (\(s=W+1\) has \(G(m,m)=1\))

At \(s=W+1\), \(m=2U-2\). Same \(k\le 11\).

## Killed

\(j\) up to \(a\): at \(k=2\), \(W=8U\), \(s=W+2U\) is after clip.
In-cone ones from \(t_0\): \(t_0+1\neq W+1\). AND at all \(W+2^j\): 1
live and 2 dead.

## Verdict

`LEMMA` (\(s=W+2^j\); \(s=W+1\) has \(G(m,m)=1\)).
`KILLED` (\(j\le a\); base \(t_0\); AND all live).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_gd.md` (this note)
- `research/cycle_gd.py`
- `research/cycle_gd.json`
