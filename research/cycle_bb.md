# Cycle BB: five sextuples; ten even septuple seeds; bit 22 contributes 1

Cycle BA classified pentuples. The even-count identity for \(|S|=6\)
has no solutions for \(c\ge 7\), so there are no even sextuples for
\(a\ge 8\). The five sextuples are the odd-lift orbit of \(a=7\)’s
packed bits \(\{66,67,71,77,85\}\). For \(|S|=7\) the even seeds
stabilize: ten targets for \(a\ge 9\). Packed bit 22 is the \(j=0\)
member of the 21-family and contributes 1. Sextuple XOR and septuple
XOR are not \(I_k\). Nested left is still not a formula for \(I_k\).
Not a prize claim: \(I_k=1\) infinitely often remains open.

Helper: `python3 research/cycle_bb.py --certify` (~7s). Dump:
`research/cycle_bb.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (no even sextuples for \(a\ge 8\))

Cycle AV’s even count: \(|S(b,2e)|=6\) iff \(|B|=0\) and
\(|A\setminus B|=3\), or \(|B|=2\) and \(|A\setminus B|=2\), or
\(|B|=4\) and \(|A\setminus B|=1\), or \(|B|=6\) and \(A\subseteq B\).

These fire only at \(c=4\) (\(q=22,20\)), \(c=5\) (\(q=36,34\)), and
\(c=6\) (\(q=66\), the pentuple-predecessor case \(A\subseteq B\)).
For \(c\ge 7\) none of the four mechanisms occur. Certified \(a\le 12\),
mechanisms \(c\le 11\).

## Lemma (exactly five sextuples)

Odd doubling sends sextuples to sextuples. At \(a=7\) the packed bits
with \(|S|=6\) are \(66,67,71,77,85\). With no even sextuples for
\(a\ge 8\), for every \(a\ge 7\) there are exactly five, namely
\(p=2^{a-7}(s-1)+1\) for \(s\in\{66,67,71,77,85\}\). Certified
\(a\le 12\), and on the annulus for \(5\le k\le 8\).

## Lemma (septuple \(s\)-sets)

For \(n<2^{a-1}\) write \(s=2^{a-1}-1-n\). Then \(G(n,2^a-q)=1\) iff
\(s\) lies in a fixed 7-set, for \(a\) at least the seed level of \(q\):

| \(q\) | \(a\ge\) | \(s\) |
|------:|:--------:|:------|
| 22 | 6 | \(\{1,2,5,6,8,9,10\}\) |
| 30 | 6 | \(\{0,1,2,9,10,13,14\}\) |
| 36 | 7 | \(\{0,1,2,3,5,9,17\}\) |
| 52 | 7 | \(\{1,16,17,18,19,21,25\}\) |
| 66 | 8 | \(\{0,1,2,4,8,16,32\}\) |
| 68 | 8 | \(\{0,2,3,5,9,17,33\}\) |
| 98 | 8 | \(\{0,32,33,34,36,40,48\}\) |
| 100 | 8 | \(\{1,32,34,35,37,41,49\}\) |
| 130 | 9 | \(\{1,2,4,8,16,32,64\}\) |
| 194 | 9 | \(\{0,65,66,68,72,80,96\}\) |

Certified \(a\le 12\).

## Lemma (even septuples are ten seeds)

\(|S(b,2e)|=7\) iff \(|B|=1\) and \(|A\setminus B|=3\), or \(|B|=3\)
and \(|A\setminus B|=2\), or \(|B|=5\) and \(|A\setminus B|=1\), or
\(|B|=7\) and \(A\subseteq B\). The unique-predecessor case does not
occur. The other three produce, and then preserve, the ten even
targets \(2^a-\{22,30,36,52,66,68,98,100,130,194\}\) for \(a\ge 9\)
(two at \(a=6\), four at \(a=7\), eight at \(a=8\)). Certified
\(a\le 12\), mechanisms \(c\le 11\).

## Lemma (septuples are the ten families)

Odd doubling sends septuples to septuples. Packed bit
\(p=r\cdot 2^{j}+1\) with \(r=q-1\in\{21,29,35,51,65,67,97,99,129,193\}\).
On the dyadic annulus the families cut at the seed levels, giving
\(10k-66\) such bits for \(k\ge 8\). Times are
\(t=T+s\cdot 2^{j}\) with the \(s\)-sets above. Certified on the
annulus for \(6\le k\le 8\).

## Lemma (bit 22 contributes 1)

For \(k\ge 6\), packed bit \(22=21+1\) is the \(j=0\) member of the
21-family, a septuple, times \(T+s\) for
\(s\in\{1,2,5,6,8,9,10\}\). Cycle BA: \(e_{22}=1\) iff
\(t\equiv 0,3\pmod{4}\) and \(e_{21}=1\) iff \(t\not\equiv 3\pmod{4}\),
so the AND fires iff \(t\equiv 0\pmod{4}\). Residues of the seven
times (using \(T\equiv 0\pmod{4}\)) are \(1,2,1,2,0,1,2\), hence
fires \(0,0,0,0,1,0,0\) and XOR \(1\). Certified \(6\le k\le 8\).
This is not a nested-left formula for \(I_k\).

## Sextuple XOR and septuple XOR — killed as formulas for \(I_k\)

On \(5\le k\le 8\) the XOR of sextuple-Green firings disagrees with
\(I_k\). On \(6\le k\le 8\) the XOR of septuple-Green firings
disagrees with \(I_k\). **Killed.**

## Nested left — still killed as a formula for \(I_k\)

\(I_k=B_{k}^{\ge 20}\) (Cycle AZ) still has a bulk after removing
bit 22’s contribution 1. On \(6\le k\le 8\), \(I_k\) takes both
values. **Killed.** Do not hunt another finite nested-left family.

## Verdict

`LEMMA` (no even sextuples for \(a\ge 8\); exactly five sextuples;
even septuples ten seeds for \(a\ge 9\); ten septuple families;
bit 22 contributes 1).
`KILLED` (sextuple XOR as \(I_k\); septuple XOR as \(I_k\); nested
left as a formula for \(I_k\)).
`OPEN` (\(I_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_bb.md` (this note)
- `research/cycle_bb.py`
- `research/cycle_bb.json`
