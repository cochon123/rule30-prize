# Periodically driven invasion fronts

Attack on prize problem 1 for the residual drivers `001` and `0111`, as
specified in [_astra_ideas6.md](_astra_ideas6.md) item 5. Finite-support
translations exist in the frozen widths. They are not infinite periodic
wakes, and the proposed drift certificate is infeasible. This is not a
prize claim.

Certifier: `research/invasion_front.py`. Dump:
`research/invasion_front.json`. Does not modify `experiment.py`,
`strip_graph.py`, or `strip_extend.py`.

## Target

On the right half-line, drive \(x(t,0)\) by a periodic word \(w\in\{001,0111\}\)
and take a finite initial word followed by zeros — the actual right-hand
data at any onset. An exact travelling solution with a periodic wake on
its left and vacuum on its right, together with a stability theorem that
every finite perturbation is swept away from each fixed site behind the
front, would make column \(1\) eventually periodic. With a periodic
centre that would be a periodic width-2 trace, contradicting Jen/Kopra
independently of the onset.

## Family

Interface width at most 12, wake spatial period at most 8, temporal
period at most 12 and a multiple of \(|w|\), positive displacement per
period. Full enumeration when wake plus interface is at most 14 cells;
beyond that, a periodic wake plus an optional leading 1 in the
interface. Verified against the local rule with vacuum on the right.

Hits: 5 for `001` (all the single block `011101` at \(T=12\), \(d=2\),
partitioned as different \((q,\mathrm{iw})\)), and 102 for `0111`
(mostly \(q=0\) compact pulses at \(T=4\), \(d=4\)).

## Not an infinite wake

Repeating the putative `001` wake (`011101` eight times, or `01` eight
times plus the interface) destroys the travelling match: after 12 steps
the shifted copy fails in several sites and the right support is not a
translate. The `0111` \(q=0\) hits remain matched as finite pulses: they
are the light-cone edge of a compact blob, leaving vacuum immediately
behind, not a periodic field filling the half-line. The empty `0111`
drive itself fills the first columns with a period-8 pattern, so vacuum
is not the driven background.

## Drift is infeasible

Astra’s certificate is \(B_t=\min(\ell_t,R_t)+\phi(s_t)\) with \(s_t\)
the phase and an eight-cell interface window, \(|\phi|\le 16\), and
\(B_{t+1}\ge B_t+\varepsilon\) for \(\varepsilon>0\) on every local
case.

Witness, driver `0111`, phase 0: the eight-cell window `00000000` with a
single 1 at site 11 (0-based). The next window is still `00000000` and
the leftmost 1 moves to site 10. Then \(\Delta\phi=0\) and
\(\Delta\ell=-1\), so \(B\) decreases. Finite defects to the right of
the driver move left. No choice of \(\phi\) on that window produces
positive drift. A certificate that ignored those defects would need a
bound on the initial perturbation’s length, which the assignment forbids.

The empty `001` drive has aperiodic column 1 through time 512, so there
is not even an attracting periodic wake to drift toward in that case.

## Why it died

Finite-support translations exist, but they are not the travelling
periodic-wake solutions that were required. The drift constraints are
infeasible on a left-moving defect outside a vacuum window. A travelling
front without attraction does not pass. Not a prize claim.
