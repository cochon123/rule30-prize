# Cycle BC: eleven octuples; ten even nonuple seeds

Cycle BB classified sextuples and septuples. The even-count identity
for \(|S|=8\) has no solutions for \(c\ge 9\), so there are no even
octuples for \(a\ge 10\). The eleven octuples are the odd-lift orbit
of \(a=9\)’s packed bits
\(\{258,259,263,269,329,369,393,401,433,465,481\}\). For \(|S|=9\)
the even seeds stabilize: ten targets for \(a\ge 11\). Octuple XOR
and nonuple XOR are not \(I_k\). Nested left is still not a formula
for \(I_k\). Not a prize claim: \(I_k=1\) infinitely often remains
open.

Helper: `python3 research/cycle_bc.py --certify` (~7s). Dump:
`research/cycle_bc.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (no even octuples for \(a\ge 10\))

Cycle AV’s even count: \(|S(b,2e)|=8\) iff \(|B|+2|A\setminus B|=8\).
These fire at \(c=4,\ldots,8\) (even \(q\in\{24,26,28,30\}\) then
\(\{42,50\}\), \(\{68\}\), \(\{130,132\}\), \(\{258\}\)) and not for
\(c\ge 9\). Certified \(a\le 12\), mechanisms \(c\le 11\).

## Lemma (exactly eleven octuples)

Odd doubling sends octuples to octuples. At \(a=9\) the packed bits
with \(|S|=8\) are the eleven seeds above. With no even octuples for
\(a\ge 10\), for every \(a\ge 9\) there are exactly eleven, namely
\(p=2^{a-9}(s-1)+1\). Certified \(a\le 12\), and on the annulus for
\(5\le k\le 9\).

## Lemma (nonuple \(s\)-sets)

For \(n<2^{a-1}\) write \(s=2^{a-1}-1-n\). Then \(G(n,2^a-q)=1\) iff
\(s\) lies in a fixed 9-set, for \(a\) at least the seed level of \(q\):

| \(q\) | \(a\ge\) | \(s\) |
|------:|:--------:|:------|
| 38 | 7 | \(\{0,5,6,8,9,10,16,17,18\}\) |
| 54 | 7 | \(\{0,1,2,16,21,22,24,25,26\}\) |
| 132 | 9 | \(\{0,1,2,3,5,9,17,33,65\}\) |
| 196 | 9 | \(\{1,64,65,66,67,69,73,81,97\}\) |
| 258 | 10 | \(\{0,1,2,4,8,16,32,64,128\}\) |
| 260 | 10 | \(\{0,2,3,5,9,17,33,65,129\}\) |
| 386 | 10 | \(\{0,128,129,130,132,136,144,160,192\}\) |
| 388 | 10 | \(\{1,128,130,131,133,137,145,161,193\}\) |
| 514 | 11 | \(\{1,2,4,8,16,32,64,128,256\}\) |
| 770 | 11 | \(\{0,257,258,260,264,272,288,320,384\}\) |

Certified \(a\le 12\).

## Lemma (even nonuples are ten seeds)

\(|S(b,2e)|=9\) iff \(|B|+2|A\setminus B|=9\). The mechanisms produce,
and then preserve, the ten even targets
\(2^a-\{38,54,132,196,258,260,386,388,514,770\}\) for \(a\ge 11\)
(two at \(a=7,8\), four at \(a=9\), eight at \(a=10\)). Certified
\(a\le 12\), mechanisms \(c\le 11\).

## Lemma (nonuples are the ten families)

Odd doubling sends nonuples to nonuples. Packed bit
\(p=r\cdot 2^{j}+1\) with
\(r=q-1\in\{37,53,131,195,257,259,385,387,513,769\}\). Times are
\(t=T+s\cdot 2^{j}\) with the \(s\)-sets above. Certified on the
annulus for \(7\le k\le 9\).

## Octuple XOR and nonuple XOR — killed as formulas for \(I_k\)

On \(5\le k\le 9\) the XOR of octuple-Green firings disagrees with
\(I_k\). On \(7\le k\le 9\) the XOR of nonuple-Green firings disagrees
with \(I_k\). **Killed.**

## Nested left — still killed as a formula for \(I_k\)

\(I_k=B_{k}^{\ge 20}\) still has a bulk of multiplicity \(\ge 10\)
together with scaling unique families. On \(6\le k\le 9\), \(I_k\)
takes both values. **Killed.** Do not hunt another finite nested-left
family.

## Verdict

`LEMMA` (no even octuples for \(a\ge 10\); exactly eleven octuples;
even nonuples ten seeds for \(a\ge 11\); ten nonuple families).
`KILLED` (octuple XOR as \(I_k\); nonuple XOR as \(I_k\); nested left
as a formula for \(I_k\)).
`OPEN` (\(I_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_bc.md` (this note)
- `research/cycle_bc.py`
- `research/cycle_bc.json`
