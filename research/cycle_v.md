# Cycle V: Kopra width of \(F^p\), prize \(u\) vs \(X\), even-decimation chain

Four attacks. One is a lemma that kills a Problem 1 route for every iterate.
The others hit their kill criteria. Not a prize claim.

Helper: `python3 research/cycle_v.py --certify`. Dump:
`research/cycle_v.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## 1. Lemma: \(F^p\) has Kopra width \(2p\)

Rule 30 is \((1,1)\) left permutive, so \(F^p\) is \((p,p)\) left permutive
and left expansive of width \(w=m+n\). The \(p\)-step centre at the origin
has causal neighbourhood \(\subseteq[-p,p]\). Both edges are attained:

- Vacuum stays vacuum, so the \(p\)-step centre is \(0\).
- A single \(1\) at \(+p\) is the prize seed shifted by \(p\). After \(p\)
  steps the origin is the left edge of that triangle, \(x(p,-p)=1\).
- A single \(1\) at \(-p\) is the prize seed shifted by \(-p\). After \(p\)
  steps the origin is the right edge, \(x(p,p)=1\).

Hence \(m=n=p\) and \(w=2p\ge 2\) for every \(p\ge 1\). In particular
**no iterate \(F^p\) is rapidly left-expansive of width 1**, so Kopra’s
Theorem 3.5 applied to \(F^p\) never yields aperiodicity of the width-1
trace \((c_{np})_{n\ge 0}\). Exhaustive neighbourhood census through
\(p=6\) matches \(m=n=p\); the two-configuration witness is checked
through \(p=32\).

This is the same light-cone sharpness that makes both prize edges
identically 1. It closes the “maybe \(F^3\) is width 1” gap left by
Cycle P/S killing only \(F^2\).

## 2. Prize even-right vs the period-2 SFT \(X\)

Phase `01` requires a suffix of \(u_n=x(2n,1)\) in the SFT forbidding
\(\{11,00000\}\) (`period2_ugap.md`). On \(N=2^{18}\) centre bits
(\(2^{17}\) even samples):

| window | legal in \(X\) | fraction |
| ---: | ---: | ---: |
| 8 | 21948 | 0.167 |
| 16 | 2650 | 0.020 |
| 32 | 20 | \(1.5\cdot 10^{-4}\) |
| 64 | 0 | 0 |

A length-8 factor of \(u\) in \(X\) exists, so there is no lemma that
prize \(u\) avoids \(X\). Length 64 is empty in this prefix only; that is
not a uniform obstruction. Consecutive \(11\) in \(u\) occurs 32738
times, last at index 131067 of 131072, with max gap 46. Infinitely many
such \(11\)s would exclude period-2 phase `01` for this seed; the table
does not prove that. Both global period-2 phases break on the last two
centre bits. **Killed** as a never-in-\(X\) lemma.

## 3. Even-decimation chain

Let \(v_k[n]=c_{n 2^k}\). Sibling splitting does not give an infinite
kernel (Thue–Morse). Pairwise distinctness of \(\{v_k\}_{k\ge 0}\)
would. On this prefix the first disagreement \(n_*(k)\) between \(v_k\)
and \(v_{k+1}\) lies in \(\{1,2,3\}\) for every \(k=0,\ldots,15\),
matching `two_kernel.md`. No collision \(v_k=v_{k+1}\) appears. A
closed witness in \(\{1,2,3\}\) for every \(k\) is not proved: the
three-bit system
\(c_{2^k}=c_{2^{k+1}}=c_{2^{k+2}}\) together with
\(c_{3\cdot 2^k}=c_{3\cdot 2^{k+1}}\) is exactly the \(n_*=3\) case,
which occurs (at \(k=2,6\)) and is saved by the third index, not
forbidden. **Killed** as a proof; the chain remains distinct on the
prefix.

## 4. Right-special factors and lag disagreements

Longest right-special factor in the \(2^{18}\) prefix has length 33
(\(\approx 2\log_2 N\)). That certifies \(p(34)>p(33)\) and is weaker
than Cycle U’s \(T+p\ge 2^{14}\). Every lag \(p=1,\ldots,2^{17}\) has a
disagreement within 32 of the end of the comparable range, so any
eventual period \(p\le 2^{17}\) would need onset after this prefix.
Periods \(p>2^{17}\) still satisfy only \(T+p\ge p\), and the uniform
complexity bound remains Cycle U’s \(16384\). Finite, not a proof.

## Verdict

`LEMMA` (Kopra width of every \(F^p\) is \(2p\)); `KILLED` (never-in-\(X\),
closed even-decimation witness, right-special as a prize argument).
Wall time 5.7s. Prize unsolved.

## Files

- `research/cycle_v.md` (this note)
- `research/cycle_v.py`
- `research/cycle_v.json`
