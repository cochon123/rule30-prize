# Cycle FY: unclipped hi-ones count \((W/4U)(a+a\bmod 2)\); residue walks backward

On the unified \(T=2U+W\) band the unclipped window is \(s\in[t_0,\mathrm{clip}]\)
with \(t_0=T-W/2\) and \(\mathrm{clip}=U+W\). Cycle FX’s residue
\(r(s)=(-s-1)\bmod 2U\) starts at \(2U-1\), steps \(-1\), and ends at
\(U-1\); the length is \(W/2-U+1\). Cycle FW’s one-zero residues all
lie in \([U-1,2U-1]\) and there are \(N=a+(a\bmod 2)\) of them (\(N\)
even, \(a=k+1\)). The walk is \((W/(4U)-1)\) full periods plus that high
half, so the unclipped hi-ones count is \((W/4U)\,N\) and the unclipped
hi Green XOR-vanishes. At clip, \(m=U-1\) and
\(G(m,2U-2)=G(m,0)=G(m,2m)=1\). The unclipped formula fails after clip,
the count depends on \(W\), and the whole-window hi XOR does **not**
vanish (clipped tail length \(U-1\)). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push the
even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\) past
414990. Do **not** increment consecutive `11` to \(n_8\). Do **not**
walk \(32U\).

Not a prize claim: an even ones-count on the hi edge does not prove
covering never-fail (Cycle FX already killed hi AND whenever \(G=1\)).

Helper: `python3 research/cycle_fy.py --certify` (~0.01s). Dump:
`research/cycle_fy.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FS/FW/FX (walk \(k\le 11\); full-window
Green \(k\le 7\); no Fermat table, no extra window, no \(n_0=16\)
window).

## Lemma (residue walk)

Certified \(k\le 11\), \(W\in\{4U,8U,16U\}\). Start \(2U-1\), step
\(-1\), end \(U-1\), length \(W/2-U+1\).

## Lemma (ones-count; unclipped hi XOR vanishes)

One-zero support lies in \([U-1,2U-1]\), size \(N=a+(a\bmod 2)\) even
(\(a\le 15\)). Count \((W/4U)\,N\) on the walk; XOR \(0\). Full-window
\(G(m,2U-2)\) matches \(k\le 7\).

## Lemma (clip corner)

At \(s=U+W\), \(m=U-1\) and \(G(m,2U-2)=G(m,0)=G(m,2m)=1\). Certified
\(k\le 11\).

## Killed

Unclipped formula after clip: at \(k=2\), \(W=8U\), \(s=\mathrm{clip}+1\),
\(G(m,2U-2)=0\neq G(m,0)=1\). Ones-count independent of \(W\): at
\(k=2\) the counts are \(4,8,16\). Whole-window hi XOR vanishes: the
clipped tail has length \(U-1\) (odd for \(k\ge 1\)), so the total is
\(1\).

## Verdict

`LEMMA` (residue walk; ones-count \((W/4U)N\); unclipped hi XOR \(0\);
clip corner).
`KILLED` (formula after clip; count independent of \(W\); whole-window
XOR \(0\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_fy.md` (this note)
- `research/cycle_fy.py`
- `research/cycle_fy.json`
