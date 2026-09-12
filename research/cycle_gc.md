# Cycle GC: \(r_*\) is in-cone for \(U\) times; ones-count is \(k+1\) independent of \(W\)

Cycle GB puts \(r_*=W-2U+2\) in the cone-band iff
\(W+1\le s\le\mathrm{clip}\). That interval has length \(U\),
independent of covering \(W\). On it, \((s-t_0)\bmod 2U\) runs through
\([1,U]\) (never 0), so Cycle FZ’s hi/\(r_*\) Green is 1 iff the residue
is a positive power of 2; the ones-count is \(a=k+1\), independent of
\(W\). The length does **not** scale with \(W\), offset 0 is **not**
in-cone, the count is **not** \(N=a+(a\bmod 2)\), and the AND does
**not** fire on all \(k+1\) times. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push the
even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\) past
414990. Do **not** increment consecutive `11` to \(n_8\). Do **not**
walk \(32U\).

Not a prize claim: a \(W\)-independent in-cone ones-count does not prove
covering never-fail (Cycle GB already killed AND whenever \(G=1\) at
\(r_*\)).

Helper: `python3 research/cycle_gc.py --certify` (~0.01s). Dump:
`research/cycle_gc.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FZ/GA/GB (window \(k\le 11\); Green
\(k\le 7\); packed AND at \(k=2\), \(W=8U\); no Fermat table, no extra
window, no \(n_0=16\) window).

## Lemma (in-cone length \(U\))

\([W+1,\mathrm{clip}]\) has length \(U\) for every covering \(W\).
Certified \(k\le 11\).

## Lemma (ones-count \(k+1\), independent of \(W\))

Residues run through \([1,U]\); \(G=1\) on \(\{2^j:0\le j<a\}\). Count
\(a=k+1\). Full-window Green matches \(k\le 7\).

## Killed

Length depends on \(W\): all three \(W\) give length \(U\). Offset 0
in-cone: \(t_0<W+1\). Count equals \(N=a+(a\bmod 2)\): at \(k=2\), ones
\(=3\neq 4\). AND on all \(k+1\) times: 1 live and 2 dead.

## Verdict

`LEMMA` (in-cone length \(U\); ones-count \(k+1\) independent of \(W\)).
`KILLED` (length depends on \(W\); offset 0 in-cone; count \(=N\); AND
all live).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_gc.md` (this note)
- `research/cycle_gc.py`
- `research/cycle_gc.json`
