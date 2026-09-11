# Cycle DT: \(\varphi^{(6)}=\varphi^{(10)}=1\) forces \(\varphi^{(18)}=0\)

Cycle BO: covering at \(k+1\) fails iff
\(\varphi^{(6)}_k=\varphi^{(10)}_k=\varphi^{(18)}_k=I_{k+1}\). Doubling
identifies all-equal even spines with an all-equal Fermat triple at
\(k+1\). On \(2\le k\le 18\), \(\varphi^{(6)}=\varphi^{(10)}=1\) forces
\(\varphi^{(18)}=0\), so the even spines are never all \(1\). The only
all-equal row is \(k=14\) (all \(0\), \(I_{15}=1\)), which produces
Fermat all-ones at \(k=15\), not a covering failure. The two-sided
slice \(\varphi^{(6)}=\varphi^{(10)}\Rightarrow\varphi^{(18)}=\neg\varphi^{(6)}\)
fails at \(k=14\). Do **not** compute \(\varphi^{(3,5,9)}\) at \(k=16\).

Not a prize claim: the one-sided implication remains a prefix.

Helper: `python3 research/cycle_dt.py --certify`. Dump:
`research/cycle_dt.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycle DS (no new packed run).

## Lemma (even all-equal iff Fermat all-equal)

Write \(I=I_{k+1}=\varphi^{(2)}_k\). Doubling gives
\(\varphi^{(3)}_{k+1}=\varphi^{(6)}_k\oplus I\), and likewise for
\((5,10)\) and \((9,18)\). For every bits \(a,b,g,I\in\{0,1\}\),

\[
a=b=g \iff (a\oplus I)=(b\oplus I)=(g\oplus I).
\]

Covering fails iff the Fermat triple is \((0,0,0)\), iff
\(a=b=g=I\). The Fermat triple is \((1,1,1)\) iff \(a=b=g=\neg I\).
In particular the \(I=1\) dangerous pattern is the triple
\((1,1,1)\) of even spines, and the implication
\(a=b=1\Rightarrow g=0\) forbids that tuple. Certified on all
input bits.

## Prefix (one-sided \(11\Rightarrow 0\), \(2\le k\le 18\))

On Cycle DS spines, \(\varphi^{(6)}=\varphi^{(10)}=1\) at
\(k=5,6,7,8,11,18\), and \(\varphi^{(18)}=0\) on each. All-equal
rows: only \(k=14\), the triple \((0,0,0)\) with \(I_{15}=1\).
Inferred covering bits at \(k=3,\ldots,19\) are all 1, matching BO
through \(k=13\). Fermat all-ones at \(k=2\) (Cycle BE) and at
\(k=15\) (inferred from \(k=14\)). No \(I=0\) and no \(I=1\)
dangerous row. **PREFIX**, not a theorem that
\(\varphi^{(6)}=\varphi^{(10)}=1\Rightarrow\varphi^{(18)}=0\) for all
\(k\). If that held, covering failure could only be all-zero even
spines with \(I=0\).

## Two-sided complement, never-all-equal, all-ones-only-at-\(k=2\) — killed

\(\varphi^{(6)}=\varphi^{(10)}\Rightarrow\varphi^{(18)}=\neg\varphi^{(6)}\)
fails at \(k=14\) (\(0,0,0\)). Never-all-equal fails at the same
row. Fermat all-ones is not unique to \(k=2\). \(\Theta(6\cdot 2^k)
=\varphi^{(18)}\oplus\varphi^{(6)}\) vanishes at \(k=2,12,14\).
**Killed** as identities.

## \(I_k\equiv 1\) for \(k\ge 13\) — killed

\[
(I_k)_{k=1}^{21}=110011001111011011101.
\]

Zeros at \(k=13,16,20\). \(I_k=1\) infinitely often remains **OPEN**.

## Verdict

`LEMMA` (even all-equal iff Fermat all-equal; one-sided \(11\Rightarrow 0\)
kills \(I=1\) dangerous).
`PREFIX` (one-sided implication on \(2\le k\le 18\); all-zero only at
\(k=14\); Fermat all-ones at \(k=2,15\); covering through \(k=19\);
one-sided implication and Fermat covering for all \(k\); period-\(H\)
seed).
`KILLED` (two-sided complement; never-all-equal; Fermat all-ones only
at \(k=2\); \(\Theta(6\cdot 2^k)\equiv 1\); \(I_k\equiv 1\) for
\(k\ge 13\)).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_dt.md` (this note)
- `research/cycle_dt.py`
- `research/cycle_dt.json`
