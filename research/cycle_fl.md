# Cycle FL: \(\Delta_R\) lives on a sliding \(r\)-band of width \(2U-1\) until \(9U\)

Cycle FK reduced \(\Delta_R\) to \(G(10U-s-1,8U-r)\) on AND \(p=10U+r\).
Green support is \(2(s-6U+1)\le r\le 8U\); the light cone further
restricts \(r\le 2s-10U\). On \(s\in[6U,9U]\) that intersection
has length \(2U-1\); after \(9U\) the \(r\le 8U\) cap shrinks it to
\(20U-2s-1\), ending at width \(1\). For \(r<2(s-6U+1)\) the reduced
Green vanishes, even when the AND fires (\(r=2\) after \(s=6U\)). Do
**not** claim the width is \(2U-1\) on all of \([6U,10U)\) (it clips
at \(s=9U+1\)). Do **not** claim the last AND at packed \(p=18U\) is
always live. Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for
all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\).

Not a prize claim: locating \(\Delta_R\) on a sliding band does not
prove covering never-fail.

Helper: `python3 research/cycle_fl.py --certify` (~0.05s). Dump:
`research/cycle_fl.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FF/FJ/FK (packed check on \(k=2..6\);
no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (width \(2U-1\) on \([6U,9U]\))

For \(s\in[6U,9U]\),
\(\min(2s-10U,8U)-(2(s-6U+1))+1=2U-1\). Certified \(k\le 12\).

## Lemma (clip after \(9U\))

For \(s\in(9U,10U)\), the \(r\le 8U\) cap gives width \(20U-2s-1\ge 1\).
Certified \(k\le 12\).

## Lemma (\(\Delta_R\) is the band XOR)

Packed AND XOR on \(2\le k\le 6\): outside-band right ANDs contribute
\(0\) to \(\Delta_R\).

## Killed

Width \(2U-1\) on all of \([6U,10U)\): at \(k=2\), \(s=9U+1\) the
width is \(5\ne 7\). Last AND at \(p=18U\) is dead at \(k=2,3,4\).

## Verdict

`LEMMA` (width \(2U-1\) on \([6U,9U]\); clip after \(9U\); \(\Delta_R\)
is the band XOR).
`KILLED` (flat width on the whole window; last \(p=18U\) always live).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_fl.md` (this note)
- `research/cycle_fl.py`
- `research/cycle_fl.json`
