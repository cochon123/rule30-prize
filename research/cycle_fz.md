# Cycle FZ: unclipped hi is 1 iff \((s-t_0)\bmod 2U\) is 0 (\(a\) odd) or a power of 2

Cycle FY walks \(r(s)=(-s-1)\bmod 2U\) backward from \(2U-1\). That
residue is a one-zero bit iff the offset \(\delta=s-t_0\) satisfies
\((\delta\bmod 2U)=0\) with \(a=k+1\) odd, or \((\delta\bmod 2U)\) is a
positive power of 2. The whole-window hi Green XOR is then
\((U-1)\bmod 2\) (unclipped XOR vanishes; the clipped tail of length
\(U-1\) is all 1s). Offset 0 is **not** always 1 (\(a\) even), and
\(\delta\) itself being 0 or a power of 2 **misses the wrap**. Do
**not** claim the hi AND fires at those dyadic times (Cycle FX). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: a dyadic time-index for the hi Green does not prove
covering never-fail.

Helper: `python3 research/cycle_fz.py --certify` (~0.02s). Dump:
`research/cycle_fz.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FW/FX/FY (walk \(k\le 11\); full-window
Green \(k\le 7\); no Fermat table, no extra window, no \(n_0=16\)
window).

## Lemma (dyadic offset)

Certified \(k\le 11\), \(W\in\{4U,8U,16U\}\). Full-window \(G(m,2U-2)\)
matches \(k\le 7\). Helper `dyadic_offset` in `cycle_fz.py`.

## Lemma (whole-window hi XOR is \((U-1)\bmod 2\))

Certified \(k\le 11\). Equals 1 for \(k\ge 1\), and 0 at \(k=0\) (no
clipped tail).

## Killed

Offset 0 always 1: at \(k=1\) (\(a\) even), \(W=4U\), \(s=t_0\),
\(G=0\). \(\delta\) itself 0-or-pow2 without reducing mod \(2U\): at
\(k=2\), \(W=8U\), \(\delta=2U+1\) is a wrap hit (\(G=1\)) but not a
power of 2.

## Verdict

`LEMMA` (dyadic offset; whole-window hi XOR \((U-1)\bmod 2\)).
`KILLED` (offset 0 always; \(\delta\) pow2 without mod).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_fz.md` (this note)
- `research/cycle_fz.py`
- `research/cycle_fz.json`
