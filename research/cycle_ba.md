# Cycle BA: even pentuples are \(2^a-\{12,16,18,20,26,28,34,50\}\)

Cycles AV–AZ classified unique through quadruple half-window supports
of \(G\). The even-count identity for \(|S|=5\) has three mechanisms.
They produce eight even seeds, stable for \(a\ge 7\). Packed bits are
\(p=r\cdot 2^{j}+1\) for \(r\in\{11,15,17,19,25,27,33,49\}\). The
tails \(e_{20},\ldots,e_{27}\) are period 4 and \(e_{30}\equiv 1\) for
\(t\ge 33\), so bits 20, 24, and 25 never fire. Pentuple XOR is not
\(I_k\). Nested left is still not a formula for \(I_k\). Not a prize
claim: \(I_k=1\) infinitely often remains open.

Helper: `python3 research/cycle_ba.py --certify` (~5s). Dump:
`research/cycle_ba.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (half-window \(s\)-sets)

For \(n<2^{a-1}\) write \(s=2^{a-1}-1-n\). Then \(G(n,2^a-q)=1\) iff
\(s\) lies in a fixed 5-set, for \(a\) at least the seed level of \(q\):

| \(q\) | \(a\ge\) | \(s\) |
|------:|:--------:|:------|
| 12 | 5 | \(\{0,1,2,3,5\}\) |
| 16 | 5 | \(\{1,4,5,6,7\}=S_4\) |
| 18 | 6 | \(\{0,1,2,4,8\}\) |
| 20 | 6 | \(\{0,2,3,5,9\}\) |
| 26 | 6 | \(\{0,8,9,10,12\}\) |
| 28 | 6 | \(\{1,8,10,11,13\}\) |
| 34 | 7 | \(\{1,2,4,8,16\}\) |
| 50 | 7 | \(\{0,17,18,20,24\}\) |

The case \(q=16\) is Cycle AT’s Jacobsthal law at \(b=4\). Certified
\(a\le 12\).

## Lemma (even pentuples)

Cycle AV’s even count: \(|S(b,2e)|=5\) iff
\(|B|=1\) and \(|A\setminus B|=2\), or \(|B|=3\) and
\(|A\setminus B|=1\), or \(|B|=5\) and \(A\subseteq B\).

- (i) Unique predecessor with \(|A\setminus B|=2\): the only such \(D\)
  are \(2^{c}-9\) and \(2^{c}-7\) (unique packed bits 9 and 7 adjacent
  to the even triple seeds 8 and 6). These produce \(2^{a}-16\) and
  \(2^{a}-12\).
- (ii) Triple predecessor with \(|A\setminus B|=1\): the only such
  \(D\) are \(2^{c}-\{15,14,11,10\}\), producing
  \(2^{a}-\{28,26,20,18\}\).
- (iii) Pentuple predecessor with \(A\subseteq B\): none at \(c=5\);
  for \(c\ge 6\) the only such \(D\) are \(2^{c}-26\) and
  \(2^{c}-18\), producing \(2^{a}-50\) and \(2^{a}-34\).

Thus even \(D\) with \(|S(a,D)|=5\) are \(\{2^{a}-12,2^{a}-16\}\) at
\(a=5\), six targets at \(a=6\), and exactly the eight seeds for
\(a\ge 7\). Certified \(a\le 12\), mechanisms \(c\le 11\).

## Lemma (pentuples are the 11, 15, 17, 19, 25, 27, 33, 49 families)

Odd doubling sends pentuples to pentuples. Combined with the eight
even seeds, every pentuple \(D\) is an odd lift of \(2^{b}-q\) for
some \(q\in\{12,16,18,20,26,28,34,50\}\) and \(b\le a\). Packed bit
\(p=2^{a}-D=r\cdot 2^{j}+1\) with \(r=q-1\). On the dyadic annulus
the families cut at the seed levels:

- \(11\cdot 2^{j}+1\) and \(15\cdot 2^{j}+1\) for \(j\le k-5\);
- \(17\cdot 2^{j}+1\), \(19\cdot 2^{j}+1\), \(25\cdot 2^{j}+1\),
  \(27\cdot 2^{j}+1\) for \(j\le k-6\);
- \(33\cdot 2^{j}+1\) and \(49\cdot 2^{j}+1\) for \(j\le k-7\).

There are \(8(k-5)\) such bits (\(k\ge 6\)), and two at \(k=5\).
Times are \(t=T+s\cdot 2^{j}\) with the \(s\)-sets above. Certified
on the annulus for \(5\le k\le 8\).

## Lemma (\(e_{20},\ldots,e_{27}\) are period 4)

The recurrence is \(e_{j}(t+1)=e_{j-2}(t)\oplus(e_{j-1}(t)\lor e_{j}(t))\).
Cycles AV–AZ supply \(e_{17}\) through \(e_{19}\). The tails

| \(j\) | \(e_{j}=1\) iff | holds from |
|------:|:----------------|:------------|
| 20 | \(t\equiv 0,1\pmod{4}\) | \(t=23\) |
| 21 | \(t\not\equiv 3\pmod{4}\) | \(t=23\) |
| 22 | \(t\equiv 0,3\pmod{4}\) | \(t=25\) |
| 23 | \(t\) even | \(t=24\) |
| 24 | \(t\equiv 3\pmod{4}\) | \(t=27\) |
| 25 | \(t\equiv 0,3\pmod{4}\) | \(t=28\) |
| 26 | \(t\not\equiv 0\pmod{4}\) | \(t=29\) |
| 27 | \(t\not\equiv 0\pmod{4}\) | \(t=30\) |

are invariant, and hold from the listed onsets. Certified on
\(t<256\), including the recurrence from \(t=20\).

## Lemma (\(e_{30}\equiv 1\) for \(t\ge 33\))

Cycle AD: \(e_{28}\equiv 0\) for \(t\ge 31\). The recurrence then
collapses to \(e_{30}(t+1)=e_{29}(t)\lor e_{30}(t)\). Directly
\(e_{30}(32)=0\) and \(e_{30}(33)=1\), after which the tail is
identically 1. Certified on \(t<256\).

## Lemma (bits 20, 24, 25 never fire)

The AND at packed bit \(p\) is \(e_{p}\land e_{p-1}\). For \(t\ge 32\):

- Bit 20: \(e_{20}=1\) iff \(t\equiv 0,1\) and \(e_{19}=1\) iff
  \(t\equiv 2,3\), so the AND is empty.
- Bit 24: \(e_{24}=1\) only for \(t\equiv 3\) (odd) and \(e_{23}=1\)
  only for even \(t\), so the AND is empty.
- Bit 25 is the \(j=3\) unique 3-family member, Green only at
  \(t=T+8\equiv 0\pmod{4}\). The AND \(e_{25}\land e_{24}\) fires
  only for \(t\equiv 3\pmod{4}\).

Certified on \(t<256\) and on the annulus for \(6\le k\le 8\). These
are not a nested-left formula for \(I_k\).

## Packed bit 33 fires at \(T\) — prefix

Bit \(p=33=2^{5}+1\) is the \(j=5\) unique \(2\)-family member, Green
only at \(t=T\). It fires for \(7\le k\le 12\). **Prefix**, not a
theorem: \(e_{32}\) and \(e_{33}\) are period 8, not a closed form.

## Pentuple XOR — killed as a formula for \(I_k\)

On \(5\le k\le 8\) the XOR of pentuple-Green firings disagrees with
\(I_k\). **Killed.**

## Nested left — still killed as a formula for \(I_k\)

\(I_k=B_{k}^{\ge 20}\) (Cycle AZ) still has a bulk of packed bits
\(\ge 20\) after removing the three bits that never fire. On
\(6\le k\le 8\), \(I_k\) takes both values. **Killed.** Do not hunt
another finite nested-left family.

## Verdict

`LEMMA` (eight even \(s\)-sets; even pentuples for \(a\ge 7\);
11, 15, 17, 19, 25, 27, 33, 49 families; \(e_{20},\ldots,e_{27}\)
period 4; \(e_{30}\equiv 1\) for \(t\ge 33\); bits 20, 24, 25 never
fire).
`PREFIX` (bit 33 fires at every \(T\)).
`KILLED` (pentuple XOR as \(I_k\); nested left as a formula for
\(I_k\)).
`OPEN` (\(I_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_ba.md` (this note)
- `research/cycle_ba.py`
- `research/cycle_ba.json`
