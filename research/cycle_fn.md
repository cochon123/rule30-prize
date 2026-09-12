# Cycle FN: \(4U\) right-band of width \(2U-1\) until \(5U\); \([2U,4U)\) misses \(10U\)

Dual of Cycle FL for the \(4U\)-shift on \([4U,6U)\). Green support is
\(2(s-4U+1)\le r\le 4U\) with \(r=p-6U\); the light cone restricts
\(r\le 2s-6U\). On \(s\in[4U,5U]\) that intersection has length
\(2U-1\); after \(5U\) the \(r\le 4U\) cap shrinks it to \(12U-2s-1\).
\(\Delta^{(4)}_R\) equals the band XOR. The earlier window \([2U,4U)\)
still matches targets \(6U\) and \(18U\) (Cycle FH) but **not** \(10U\).
Do **not** claim the width is \(2U-1\) on all of \([4U,6U)\). Do **not**
claim the last AND at packed \(p=10U\) is always live. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push the
even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\) past
414990. Do **not** increment consecutive `11` to \(n_8\).

Not a prize claim: a \(4U\)-band plus a failed \(10U\) match on
\([2U,4U)\) does not prove covering never-fail.

Helper: `python3 research/cycle_fn.py --certify`. Dump:
`research/cycle_fn.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FF/FH/FL/FM (packed check on \(k=2..6\);
no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (width \(2U-1\) on \([4U,5U]\); clip after \(5U\))

Certified \(k\le 12\). Freshman on \(p>6U\) leaves \(G(m,d+4U)\).

## Lemma (\(\Delta^{(4)}_R\) is the band XOR; \([2U,4U)\) matches \(18U\))

Packed AND XOR on \(2\le k\le 6\). Pointwise \(6U\) vs \(18U\) on
\([2U,4U)\) (subset of Cycle FH).

## Killed

\(J_{[2U,4U)\to 6U}=J_{[2U,4U)\to 10U}\) fails at \(k=4,6\). Width
\(2U-1\) on all of \([4U,6U)\): at \(k=2\), \(s=5U+1\) the width is
\(5\ne 7\). Last AND at \(p=10U\) is dead at \(k=2,3,5\).

## Verdict

`LEMMA` (width \(2U-1\) on \([4U,5U]\); clip after \(5U\);
\(\Delta^{(4)}_R\) is the band XOR; \([2U,4U)\) matches \(18U\)).
`KILLED` (\([2U,4U)\) remainders to \(10U\); flat width; last \(p=10U\)
always live).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_fn.md` (this note)
- `research/cycle_fn.py`
- `research/cycle_fn.json`
