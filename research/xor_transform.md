# XOR / difference transforms of the Rule 30 centre

Cycle I screen of the unused Astra prompt: an exact closed form for a transformed sequence (first difference of `c`, or `c_t XOR (t mod 2)`) that is easier than `c`. This is not linear complexity of raw `c` (already `L(N)≈N/2` in `experiment.py` / `REPORT.md`), not dual-particle pairing, and not block energy `D(N)` of the untransformed centre as a standalone attack. Finite evidence only. **Not a prize claim.**

Certifier: `research/xor_transform.py`. Dump: `research/xor_transform.json`.
Does not modify `experiment.py`, `strip_graph.py`, or `strip_extend.py`.

## Transforms

Packed centre as in `experiment.center_bits`: `row=1`, bit `t` is `(row>>t)&1`,
`row=(row<<2)^((row<<1)|row)`. Prefix of length 256 matches that function.

\[
\begin{aligned}
a_t &= c_t \oplus (t \bmod 2),\\
d_t &= c_t \oplus c_{t+1},\\
e_t &= c_t \oplus c_{t//2},\\
s_t &= c_{t+1} \oplus c_t \oplus c_{t-1}\quad(t\ge 1),\\
m_t &= c_t \oplus (\mathrm{popcount}(t)\bmod 2).
\end{aligned}
\]

The Laplacian `s` is stored with index `0` equal to time `t=1`.
Raw `c` is included as a baseline, not as a new attack.

## Linear complexity

Binary Berlekamp–Massey copied from `experiment.py`. `L(N)` is the length after the length-`N` prefix of each transform.

| transform | formula | L(256) | L(1024) | L(4096) | L(16384) | L(4096)/4096 | L(16384)/16384 |
|---|---|---:|---:|---:|---:|---:|---:|
| `c` | c_t (raw baseline) | 128 | 513 | 2049 | 8192 | 0.5002 | 0.5000 |
| `a` | c_t XOR (t mod 2) | 128 | 512 | 2048 | 8193 | 0.5000 | 0.5001 |
| `d` | c_t XOR c_{t+1} | 128 | 512 | 2049 | 8192 | 0.5002 | 0.5000 |
| `e` | c_t XOR c_{t//2} | 127 | 513 | 2048 | 8192 | 0.5000 | 0.5000 |
| `s` | c_{t+1} XOR c_t XOR c_{t-1} (t>=1) | 129 | 512 | 2049 | 8190 | 0.5002 | 0.4999 |
| `m` | c_t XOR (popcount(t) mod 2) | 129 | 512 | 2049 | 8193 | 0.5002 | 0.5001 |

Kill on linear recurrences: every transform still has `L(N) ≥ N/4` at `N=4096` and `N=16384` (so none is a simpler linear recurrence than the known `L(c)≈N/2` profile).

## Period witnesses

Last mismatch of `f_t != f_(t+p)` on a 100000-bit prefix, `p=1..4096`, same packing as `experiment.period_witnesses`.

| transform | min last-mismatch | at period | # p with last-mismatch < N/2 | best p≤256 | last-mismatch for that p | last 00 | last 11 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `c` | 95902 | 4095 | 0 | 254 | 99739 | 99997 | 99982 |
| `a` | 95903 | 4096 | 0 | 254 | 99739 | 99998 | 99988 |
| `d` | 95899 | 4096 | 0 | 254 | 99739 | 99996 | 99994 |
| `e` | 95903 | 4096 | 0 | 255 | 99742 | 99996 | 99989 |
| `s` | 95901 | 4096 | 0 | 254 | 99739 | 99973 | 99994 |
| `m` | 95903 | 4095 | 0 | 256 | 99743 | 99995 | 99998 |

No transform is eventually periodic on the scanned prefix with a tiny last-mismatch (below `N/2`) for a small period. For an aperiodic-through-the-end prefix, last-mismatch for period `p` sits near `N-p`; the raw-`c` minimum `95902` matches `REPORT.md` / `results.json`. Digrams `00` and `11` both persist past the halfway mark on every sequence, so none is eventually `01^q` or `0^q1` on this prefix.

Run lengths on the full generated prefix:

| transform | max 0-run | max 1-run | suffix `01^q`? | suffix `0^q1`? | unique q after last `00` |
|---|---:|---:|---|---|---|
| `c` | 19 | 21 | None | None | None |
| `a` | 16 | 17 | None | None | None |
| `d` | 20 | 16 | None | None | None |
| `e` | 13 | 15 | None | None | None |
| `s` | 17 | 19 | None | None | None |
| `m` | 14 | 15 | None | None | None |

## Dyadic discrepancy versus raw `D(N)`

Signed sums \(D_f(N)=\sum_{t<N}(2f_t-1)\) and the annulus maximum \(A_m\) (max absolute partial imbalance on `[2^m,2^{m+1})`), against the same quantities for raw `c`.

| transform | D(4096) | D(16384) | D(32768) | D(65536) | D(end) | max A_m/2^m (m≥8) | same order as D(c) |
|---|---:|---:|---:|---:|---:|---:|---|
| `c` | -40 | 170 | 282 | 218 | 196 | 0.1016 | yes |
| `a` | 0 | -74 | -234 | 90 | 528 | 0.0508 | yes |
| `d` | -76 | 130 | 56 | 256 | 65 | 0.0859 | yes |
| `e` | 96 | 142 | 258 | 562 | 436 | 0.0898 | yes |
| `s` | -70 | -40 | -140 | -154 | 60 | 0.0938 | yes |
| `m` | 8 | 142 | 34 | 298 | -40 | 0.0742 | yes |

Signed sums stay the same order as raw `D(N)`: none is visibly `o(N)` better on these prefixes, so there is no Problem 2 shortcut.

## Why it died

Preregistered kill: every transform still has `L(N) ≥ N/4` at `N=4096` and `N=16384`; none is eventually periodic on the scanned prefix with a tiny last-mismatch; signed sums are the same order as raw `D(N)`. Overall kill if no transform is simpler in all three. All three clauses fire, so the overall clause fires. XOR with a period-2 or Thue–Morse sequence changes `L` by `O(1)`, as expected. First difference and the discrete Laplacian stay on the `L≈N/2` line. Paperfolding-style `e` has a *larger* `|D|` than raw `c` at `N=65536`. No bounded `L(N)` and no eventual period, so there is nothing to prove from Rule 30. Not a prize claim.

## Kill verdict

Killed. No transform is simpler than raw c in all three of linear complexity, periodicity witnesses, and discrepancy. Every screened transform still has L(N) ≥ N/4 at N=4096 and N=16384; none has a tiny last-mismatch for a small period on the scanned prefix; signed sums stay the same order as D(N). A single nicer statistic is not a prize claim. Not a prize claim.

A single nicer statistic would not have been a prize claim. Overall kill requires failure to be simpler in **all three** of `L(N)`, periodicity witnesses, and discrepancy; that overall clause fires.

No transform has bounded `L(N)` or a clear eventual period on the scanned prefixes, so there is nothing to prove from Rule 30 along this route.

Wall time: `1.043` seconds.

Self-check: packed centre agrees with `experiment.center_bits` on 256 bits;
copied BM agrees on `c[:100]` (`L=48`) and on the three toy words;
copied period witnesses agree with `experiment.period_witnesses` on 100 bits.

