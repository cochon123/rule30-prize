# Cycle EW: scar \(n_3..n_6\) are \(\operatorname{rot}^{n_0-1}\) of \(T\)-functions; even-\(n_0\) \(n_6\) type N

Gap-parity is rotation-equivariant. Cycle DV’s \((n_3,n_4)\) is exactly
\((\operatorname{gap}(T),\operatorname{reconstruct}(T,\operatorname{gap}(T)))\).
Combined with Cycle EU’s \(n_3=\operatorname{rot}^{n_0-1}(T)\) and Cycle
ES reconstruct-rotation, the scar after \((0,T,1)\) is
\[
\begin{aligned}
n_3&=\operatorname{rot}^{n_0-1}(T),\\
n_4&=\operatorname{rot}^{n_0-1}(\operatorname{gap}(T)),\\
n_5&=\operatorname{rot}^{n_0-1}(\operatorname{reconstruct}(T,\operatorname{gap}(T))),\\
n_6&=\operatorname{rot}^{n_0-1}(\operatorname{reconstruct}(\operatorname{gap}(T),\operatorname{reconstruct}(T,\operatorname{gap}(T)))).
\end{aligned}
\]
For even \(n_0\), \(n_6\) is type N and is not \(0\) or \(n_5\).
\(\operatorname{ham}(n_5,n_6)\) is not \(n_0\) (\(n_0=4\) has Hamming 3).
Kills: gap not rotation-equivariant; DV pair is not
\((\operatorname{gap},\operatorname{reconstruct}(T,\operatorname{gap}))\);
\(\operatorname{ham}(n_5,n_6)=n_0\); \(n_6\) not type N for even \(n_0\).
Do **not** claim \(n_6\) type N for odd \(n_0\). Do **not** claim an
11-bit gap. Do **not** claim a formula for extra 414990. Do **not** bump
all \(n_0=16\) past 414990. Do **not** compute \(\varphi^{(3,5,9)}\) at
\(k=16\). Do **not** push the \(n_0=2\) seed past \(k=21\).

Not a prize claim: writing the scar as rotates of \(T\)-functions does
not give covering never-fail or at-most-one-odd for all \(k\).

Helper: `python3 research/cycle_ew.py --certify` (~0.03s). Dump:
`research/cycle_ew.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles CA/CB/CH/DV/DX/ER/ES/EU/EV (no new packed run,
no Fermat table, no ones/gap/run-form rerun, no \(n_0=16\) window).

## Lemma (gap is rotation-equivariant)

Backward distance to the previous 1 is cyclic-shift invariant, so
\(\operatorname{gap}(\operatorname{rot}^k S)=\operatorname{rot}^k\operatorname{gap}(S)\).
Exhaustive on every nonzero word of length \(2..8\), trials on length
\(12,16,32\).

## Lemma (DV pair is \((\operatorname{gap}(T),\operatorname{reconstruct}(T,\operatorname{gap}(T)))\))

Cycle DV defines \(n_3=\operatorname{reconstruct}(1,s)\) and
\(n_4=\operatorname{reconstruct}(s,n_3)\) for O-type \(s\). Cycle EU:
that \(n_3\) is gap-parity. So the DV pair is
\((\operatorname{gap}(T),\operatorname{reconstruct}(T,\operatorname{gap}(T)))\).
Exhaustive \(1\le n_0\le 8\).

## Lemma (scar \(n_3..n_6\) are \(\operatorname{rot}^{n_0-1}\) of those \(T\)-functions)

Cycle EU: \(\operatorname{reconstruct}(T,1)=\operatorname{rot}^{n_0-1}(T)\).
Cycle ES: reconstruct commutes with rotation. Therefore
\(n_4=\operatorname{rot}^{n_0-1}(\operatorname{gap}(T))\) and
\(n_5=\operatorname{rot}^{n_0-1}(\operatorname{reconstruct}(T,\operatorname{gap}(T)))\),
and for even \(n_0\) the next bit is
\(n_6=\operatorname{rot}^{n_0-1}(\operatorname{reconstruct}(\operatorname{gap}(T),\operatorname{reconstruct}(T,\operatorname{gap}(T))))\).
Exhaustive \(1\le n_0\le 8\).

## Lemma (even \(n_0\): \(n_6\) is type N)

Certified on every even-\(n_0\) O-type \(2\le n_0\le 10\). \(n_6\) is
never \(0\) or \(n_5\). \(\operatorname{ham}(n_5,n_6)=n_0\) fails: the
length-4 O-type with \(T_0=0100\) has Hamming 3.

## Killed

Gap-parity is rotation-equivariant. The DV pair is the gap/reconstruct
pair of \(T\). \(\operatorname{ham}(n_5,n_6)=n_0\) is false. Even
\(n_0\) \(n_6\) is type N.

## Verdict

`LEMMA` (gap rotation-equivariant; DV pair is gap/reconstruct; scar
\(n_3..n_6\) are \(\operatorname{rot}^{n_0-1}\) of \(T\)-functions; even
\(n_0\) \(n_6\) type N).
`KILLED` (\(\operatorname{ham}(n_5,n_6)=n_0\); gap not
rotation-equivariant).
`PREFIX` (\(n_6\) type N for odd \(n_0\); 11-bit gap; formula for extra
414990; at-most-one-odd for all \(k\); seed for all \(k\); \(\pi\)
formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ew.md` (this note)
- `research/cycle_ew.py`
- `research/cycle_ew.json`
