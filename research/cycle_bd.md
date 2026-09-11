# Cycle BD: period-8 tails \(e_{29}\)–\(e_{33}\); bit 33 contributes 1

Cycle AW listed packed bit 33 firing at every dyadic \(T\) as a
prefix, because \(e_{32}\) and \(e_{33}\) were only period 8 on a
window. Cycle BA’s tails \(e_{27}\) period 4, \(e_{28}\equiv 0\), and
\(e_{30}\equiv 1\) for \(t\ge 33\) make the period-8 forms of
\(e_{29},e_{31},e_{32},e_{33}\) invariant under the left-diagonal
recurrence. The AND at bit 33 then fires iff \(t\equiv 0\pmod{8}\).
Since \(T=2^{k-1}\equiv 0\pmod{8}\) for \(k\ge 4\), bit 33 contributes
1 for every \(k\ge 7\). Nested left is still not a formula for
\(I_k\). Not a prize claim: \(I_k=1\) infinitely often remains open.

Helper: `python3 research/cycle_bd.py --certify`. Dump:
`research/cycle_bd.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (\(e_{29},e_{31},e_{32},e_{33}\) are period 8)

The recurrence is \(e_{j}(t+1)=e_{j-2}(t)\oplus(e_{j-1}(t)\lor e_{j}(t))\).
Cycle BA: \(e_{27}(t)=1\) iff \(t\not\equiv 0\pmod{4}\),
\(e_{28}\equiv 0\) for \(t\ge 31\), and \(e_{30}\equiv 1\) for
\(t\ge 33\). Substituting gives

\[
\begin{aligned}
e_{29}(t+1)&=e_{27}(t)\oplus e_{29}(t),\\
e_{31}(t+1)&=e_{29}(t)\oplus 1,\\
e_{32}(t+1)&=1\oplus(e_{31}(t)\lor e_{32}(t)),\\
e_{33}(t+1)&=e_{31}(t)\oplus(e_{32}(t)\lor e_{33}(t)).
\end{aligned}
\]

The tails

| \(j\) | \(e_{j}=1\) iff | holds from |
|------:|:----------------|:------------|
| 29 | \(t\equiv 0,1,3,6\pmod{8}\) | \(t=30\) |
| 31 | \(t\equiv 0,3,5,6\pmod{8}\) | \(t=34\) |
| 32 | \(t\equiv 0,2,5\pmod{8}\) | \(t=36\) |
| 33 | \(t\equiv 0,3,7\pmod{8}\) | \(t=36\) |

are invariant under those maps. Certified on \(t<512\), including the
recurrence from \(t=20\), and by checking all eight residues of the
maps.

## Lemma (bit 33 contributes 1)

Packed bit \(33=2^{5}+1\) is the \(j=5\) unique \(2\)-family member,
Green only at \(t=T\). The AND \(e_{33}\land e_{32}\) fires iff
\(t\equiv 0\pmod{8}\). For \(k\ge 4\), \(T=2^{k-1}\equiv 0\pmod{8}\).
The tails hold from \(t=36\), and \(T\ge 64\) for \(k\ge 7\). Hence
the bit fires at every such \(T\) and contributes 1. Certified
\(7\le k\le 12\), including uniqueness of the Green time. This
upgrades Cycle AW’s prefix. It is not a nested-left formula for
\(I_k\).

## Lemma (bit 29 never fires)

The AND at packed bit 29 is \(e_{29}\land e_{28}\). Cycle AD/BA:
\(e_{28}\equiv 0\) for \(t\ge 31\), so the AND is empty. Certified on
\(t<512\).

## Nested left — still killed as a formula for \(I_k\)

\(I_k=B_{k}^{\ge 20}\) still has a bulk after removing bit 33’s
contribution 1. On \(7\le k\le 12\), \(I_k\) takes both values.
**Killed.** Do not hunt another finite nested-left family.

## Verdict

`LEMMA` (\(e_{29},e_{31},e_{32},e_{33}\) period 8; bit 33 contributes
1 for \(k\ge 7\); bit 29 never fires).
`KILLED` (nested left as a formula for \(I_k\)).
`OPEN` (\(I_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_bd.md` (this note)
- `research/cycle_bd.py`
- `research/cycle_bd.json`
