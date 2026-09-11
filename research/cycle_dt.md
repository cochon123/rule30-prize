# Cycle DT: even spines never all equal through \(k=18\)

Cycle BO: covering at \(k+1\) fails iff
\(\varphi^{(6)}_k=\varphi^{(10)}_k=\varphi^{(18)}_k=I_{k+1}\). Cycle DS
found that dangerous set empty through \(k=18\). Doubling identifies
all-equal even spines with an all-equal Fermat triple at \(k+1\), so
covering failure is the all-zero case and Fermat all-ones is the
all-equal-to-\(\neg I\) case. On \(2\le k\le 18\) the three even spines
are never all equal. That is strictly stronger than dangerous-empty:
it also forbids Fermat all-ones at \(k=3,\ldots,19\) (\(k=2\) is the
unique all-ones row in that range). Equivalently,
\(\varphi^{(6)}=\varphi^{(10)}\) forces
\(\varphi^{(18)}=\varphi^{(6)}\oplus 1\), i.e. \(\Theta(6\cdot 2^k)=1\)
on that slice. Do **not** compute \(\varphi^{(3,5,9)}\) at \(k=16\).

Not a prize claim: never-equal for all \(k\) remains a prefix.

Helper: `python3 research/cycle_dt.py --certify`. Dump:
`research/cycle_dt.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycle DS (no new packed run).

## Lemma (even all-equal iff Fermat all-equal)

Write \(I=I_{k+1}=\varphi^{(2)}_k\). Doubling gives
\(\varphi^{(3)}_{k+1}=\varphi^{(6)}_k\oplus I\), and likewise for
\(5,10\) and \(9,18\). For every bits \(a,b,g,I\in\{0,1\}\),

\[
a=b=g \iff (a\oplus I)=(b\oplus I)=(g\oplus I).
\]

Covering fails iff the Fermat triple is \((0,0,0)\), iff
\(a=b=g=I\). The Fermat triple is \((1,1,1)\) iff \(a=b=g=\neg I\).
The slice implication \(a=b\Rightarrow g=a\oplus 1\) is exactly
\(\neg(a=b=g)\). Certified on all eight triples.

## Prefix (never all equal, \(2\le k\le 18\))

Cycle DS even spines: no \(k\in[2,18]\) has
\(\varphi^{(6)}=\varphi^{(10)}=\varphi^{(18)}\). Matches
\(\varphi^{(6)}=\varphi^{(10)}\) at
\(k=5,6,7,8,11,13,14,15,17,18\), and on each of those
\(\varphi^{(18)}=\neg\varphi^{(6)}\). Inferred covering bits at
\(k=3,\ldots,19\) are all 1, matching BO through \(k=13\). Fermat
all-ones occurs only at \(k=2\) on \(2\le k\le 19\). **PREFIX**, not
a theorem that the even spines are never equal for all \(k\).

## \(\Theta(6\cdot 2^k)\equiv 1\) — killed

\(\varphi^{(18)}\oplus\varphi^{(6)}\) vanishes at \(k=2\) and
\(k=12\). **Killed** as a 1-production. The same XOR is 1 on every
\(\varphi^{(6)}=\varphi^{(10)}\) row in the prefix, which is the
slice implication above, not an identity for all \(k\).
\(\varphi^{(6)}\equiv\varphi^{(10)}\) and
\(\varphi^{(18)}\equiv\neg\varphi^{(6)}\) likewise fail off that
slice. **Killed.**

## \(I_k\equiv 1\) for \(k\ge 13\) — killed

\[
(I_k)_{k=1}^{21}=110011001111011011101.
\]

Zeros at \(k=13,16,20\). Both values still occur after \(k=12\).
\(I_k=1\) infinitely often remains **OPEN**.

## Verdict

`LEMMA` (even all-equal iff Fermat all-equal; slice implication iff
never all-equal).
`PREFIX` (never all-equal on \(2\le k\le 18\); Fermat all-ones only
at \(k=2\) through \(k=19\); covering through \(k=19\); covering and
never-equal for all \(k\); period-\(H\) seed).
`KILLED` (\(\Theta(6\cdot 2^k)\equiv 1\);
\(\varphi^{(6)}\equiv\varphi^{(10)}\);
\(\varphi^{(18)}\equiv\neg\varphi^{(6)}\);
\(I_k\equiv 1\) for \(k\ge 13\)).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_dt.md` (this note)
- `research/cycle_dt.py`
- `research/cycle_dt.json`
