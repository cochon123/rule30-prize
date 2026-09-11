# Cycle X: local coboundaries for \(D(N)\), and ideas21.1

Two leftover attacks. Both hit their kill criteria. The vacuum
obstruction is a lemma: it kills every finite-window current for
\(2c_t-1\) on **every** orbit, and the prize orbit itself visits a
vacuum 5-window for five consecutive times. Not a prize claim.

Helper: `python3 research/cycle_x.py --certify`. Dump:
`research/cycle_x.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## 1. Local coboundaries and bond fluxes (Problem 2)

Write \(s_t=2c_t-1\) and \(D(N)=\sum_{t<N}s_t\). A function \(\varphi\)
of a centred spatial window of width \(w\in\{3,5\}\) with

\[
s_t=\varphi(\text{next window})-\varphi(\text{current window})
\]

would give \(D(N)=O(1)\) on every orbit. A bond flux \(J\) of width
\(2,3,4\) would rewrite the same identity as
\(s_t=\Delta\varphi+J_{\mathrm{left}}-J_{\mathrm{right}}\), so that
\(D(N)\) becomes a flux sum. Both families are linear over \(\mathbb Q\)
on the \(2^{w+2}\) Rule 30 neighbourhoods (32 or 128 equations). The
same systems are also imposed on the pair current
\(e_t=c_t+c_{t+1}-1\) and on \(2c_t\) (vacuum-compatible), and on a
2-phase copy of \(\varphi\).

**Lemma (vacuum).** The zero configuration is a fixed point, and
\(s=e=-1\) there. Hence no function of a finite window, and no 2-phase
family, can satisfy \(\Delta\varphi=s\) or \(\Delta\varphi=e\) on all of
\(\{0,1\}^{\mathbb Z}\): already \(0=-1\), and two vacuum steps of a
2-phase family sum to \(0=-2\). Certified on the 5-tuple `00000`.

**Lemma (prize vacuum run).** The prize light cone visits the spatial
5-window `00000` about the origin (527 times on \(t<2^{14}\)), including
a run of length 5. On that run the next 5-window is again vacuum, so
the same \(0=-1\) equation holds **on this orbit**. First such run:
\(t=156,157,158\) (self-check on a length-200 prefix).

**Lemma (no small-range current).** Gaussian elimination over \(\mathbb Q\)
kills all 21 universal families (plain coboundary of width 3 or 5,
2-phase, and fluxes of width 2–4) for each of \(s\), \(e\), and \(2c\).
The \(2c\) target is compatible with vacuum and is still inconsistent:
Rule 30 has no local continuity equation
\(2x_0=\Delta\varphi+\Delta J\) in this range. Infinitely many 1s in
\(c\) (Jen) independently kill any *bounded* \(2c\) coboundary, because
\(\sum 2c_t\) diverges while a window function is bounded.

On \(t<2^{14}\) every spatial 3-, 5-, and 7-window about the origin
occurs (8/8, 32/32, 128/128). The orbit-restricted systems therefore
coincide with the universal ones at this range and die with them. In
particular \(D(t)\) is not a function of the 3-window: each of the eight
triples occurs with a \(D\)-range of 276 or 277.

This is not Cycle T’s packed-popcount correlation and not the
coarse-graining factor of `coarse_bias.md`. Those searched for a
specific current, or for a block factor first. Here every current of
the stated range is excluded.

## 2. ideas21.1 is not a reduction (Problem 1)

Eventual period 2 is exactly: only finitely many `00` and finitely many
`11` in the centre. A centre `11` is the spatial triple `010` or `011`,
i.e. \((c,\ell)=(1,0)\). Condrey’s infinitely many 0s in column \(-1\)
together with infinitely many 1s in \(c\) do **not** force that pair:

on phase `01` one has \(c=0\) at even times and \(\ell=1\) at odd times,
so \((c,\ell)=(1,0)\) is empty after onset, while column \(-1\) may still
be 0 at even times (\(u=1\)) and \(c\) is 1 at every odd time. The four
local assignments (`100`,`001` even; `110`,`111` odd) are listed in the
dump. Period 2 is a consistent hypothetical for those two infinitudes.
A CA production of `010`/`011` infinitely often remains equivalent to
infinitely many `11`s, not a weaker lemma. **Killed as a reduction.**

On the prize prefix the pair \((c,\ell)=(1,0)\) occurs 4148 times
(\(t<2^{14}\), last at 16370). That is finite evidence of `11`s, not a
production.

## Verdict

`KILLED` (all local currents in range, ideas21.1 as a reduction),
wall time 0.63s. Prize unsolved.

## Files

- `research/cycle_x.md` (this note)
- `research/cycle_x.py`
- `research/cycle_x.json`
