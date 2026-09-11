# Cycle U: de Bruijn factors of the centre

Every binary word of length \(\le 14\) occurs in the prize centre.
That is a finite theorem, not disjunctivity, and not a prize claim.
Predicted disagreement indices for square 2-kernel columns all fail.

Helper: `python3 research/cycle_u.py --certify`. Dump:
`research/cycle_u.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## De Bruijn prefix

On \(N=2^{18}\) centre bits, the number of missing length-\(n\) words is

| \(n\) | missing | \(2^n\) |
| ---: | ---: | ---: |
| \(\le 14\) | 0 | \(2^n\) |
| 15 | 12 | 32768 |
| 16 | 1253 | 65536 |

**Lemma (finite).** Every word in \(\{0,1\}^{\le 14}\) is a factor of
\((c_t)_{t\ge 0}\). Witness: the prefix of length \(2^{18}\).

If \(c\) were eventually periodic with preperiod \(T\) and period \(p\),
there are at most \(T+p\) distinct factors of each length, so
\(T+p\ge 2^{14}=16384\). This improves the kernel lower bound
\(|K|\ge 4096\) from `research/two_kernel.md` as a *period* bound; it
does not prove \(T+p=\infty\).

Length-10 words are not all present in a \(2^{12}\) prefix (7 missing,
including `1111111111`) but all appear by \(2^{13}\). Long 1-runs occur;
that does not give infinitely many \(11\)s (the run may lie before an
onset).

Disjunctivity (every finite word occurs) would solve Problem 1. It is
not proved: twelve length-15 words are missing from this prefix, and
an infinite family cannot be certified by one prefix.

Square columns at \(k=10\) cannot collide: `two_kernel.md` already has
\(2^{10}\) distinct length-128 prefixes at depth 10, which implies the
infinite sequences are distinct. A length-\(2^{10}\) collision would
contradict that table. The missing step remains a proof for every \(k\),
not a larger square.

## Predicted kernel index

On depths \(k=1,\ldots,6\), none of the formulas
\(i\in\{0,1,v_2(s-r),\mathrm{popcount}(r\oplus s),k-1\}\)
disagrees on every residue pair. The \(v_2\) template of Cycle T is
not rescued by a closed index. **Killed.**

## Verdict

Finite de Bruijn theorem through length 14. Kernel-index formulas
killed. Prize unsolved. Wall time 4.0s.

## Files

- `research/cycle_u.md` (this note)
- `research/cycle_u.py`
- `research/cycle_u.json`
