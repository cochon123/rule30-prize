# Vanishing-noise susceptibility

Attack on prize problem 2, as specified in [_astra_ideas7.md](_astra_ideas7.md)
item 1. The first derivative \(B_N'(0)\) stays below the frozen envelope
\(8N^{3/2}\). Noisy relaxation does not statistically contradict the
declared exponential. Higher-order fault clusters remain uncontrolled,
which was the required next lemma. This is not a prize claim.

Certifier: `research/noise_susceptibility.py`. Dump:
`research/noise_susceptibility.json`. Does not modify `experiment.py`,
`strip_graph.py`, or `strip_extend.py`.

## First derivative

A single flipped update at each cone site \(v\) produces a new
discrepancy \(D_N^{[v]}\). Then
\(B_N'(0)=\frac1N\sum_v(D_N^{[v]}-D_N)\). Centres match
`experiment.center_bits` on a prefix of length 257.

| \(N\) | \(D_N\) | sites | \(B_N'(0)\) | \(8N^{3/2}\) |
| ---: | ---: | ---: | ---: | ---: |
| 64 | 6 | 4095 | −64.28 | 4096 |
| 128 | −2 | 16383 | 337.11 | 11585 |
| 256 | 14 | 65535 | −661.41 | 32768 |

\(|B_N'(0)|\) is \(O(N)\), not \(O(N^{3/2})\) and not \(O(N^2)\). The
preregistered derivative kill does not fire. Max single-site change of
\(D_N\) is 22, 34, 56.

## Noisy relaxation

Independent update noise at \(\varepsilon=2^{-6},2^{-8},2^{-10}\), 8192
trajectories through time 512. Late-time mean absolute magnetisation is
about 0.009, at Monte-Carlo scale \(1/\sqrt{8192}\approx 0.011\). With
that slack the means do not contradict \(2e^{-t\sqrt\varepsilon/4}\).
Without slack the envelope at large \(t\) is far below the sampling
error, so the exponential is not resolved.

## Pair interactions

Four hundred random pairs of update sites at \(N=64\) and \(N=128\):

\[
I(v,w)=D^{[v,w]}-D^{[v]}-D^{[w]}+D.
\]

Mean \(|I|\) is 2.19 and 3.22; maxima 38 and 58; about 30% of pairs
interact. There is no proved uniform bound on \(k\)-fault clusters.

## Why it died

The first-experiment numerical kills on \(B_N'(0)\) and on a resolved
envelope violation do not fire. Astra required, next, a uniform lemma
on higher-order fault interactions. That lemma was not obtained; pair
terms are already order-one to tens and grow with \(N\). The route is
abandoned. An \(O(N)\) first derivative is not a proof that
\(|D(N)|=o(N)\). Not a prize claim.
