# Cycle BO: Fermat covering fails iff the even spines match \(I\)

Doubling gives \(\varphi^{(q)}_{k+1}=\varphi^{(2q)}_k\oplus I_{k+1}\)
for \(q=3,5,9\), with \(I_{k+1}=\varphi^{(2)}_k\). Therefore the Fermat
covering fails at \(k+1\) if and only if

\[
\varphi^{(6)}_k=\varphi^{(10)}_k=\varphi^{(18)}_k=I_{k+1}.
\]

Equivalently: \(\varphi^{(6)}_k=\varphi^{(10)}_k=I_{k+1}\) and
\(\Theta(6\cdot 2^k)=0\). That dangerous set is empty for
\(2\le k\le 12\) (covering through \(k=13\) stays a prefix).
\(\varphi^{(6)}_k\) is not identically 1 for \(k\ge 5\) (it vanishes
at \(k=13\)), and \(\{\varphi^{(5)},\varphi^{(6)}\}\) is not a
covering. Not a prize claim: the Fermat covering remains a prefix.

Helper: `python3 research/cycle_bo.py --certify` (~2s). Dump:
`research/cycle_bo.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (doubling for the covering spines)

Cycle AL/AH: \(\varphi^{(q)}_{k+1}=\varphi^{(2q)}_k\oplus I_{k+1}\)
with \(I_{k+1}=\varphi^{(2)}_k=c_{2^{k+1}}\oplus c_{2^k}\). Certified
for \(q=3,5,9\) and \(2\le k\le 12\).

## Lemma (failure criterion)

Covering at \(k+1\) is \(\varphi^{(3)}_{k+1}\lor\varphi^{(5)}_{k+1}\lor\varphi^{(9)}_{k+1}\).
Substituting doubling, this vanishes iff each even spine equals
\(I_{k+1}\). Since \(\Theta(6\cdot 2^k)=\varphi^{(18)}_k\oplus\varphi^{(6)}_k\),
the same vanishing is \(\varphi^{(6)}_k=\varphi^{(10)}_k=I_{k+1}\) and
\(\Theta(6\cdot 2^k)=0\). Certified equivalent on \(2\le k\le 12\).

In particular \(\Theta(3\cdot 2^m)\equiv 1\) is still false (Cycle BM)
and is *not* required: covering only needs \(\Theta(6\cdot 2^k)=1\)
on the dangerous alignment \(\varphi^{(6)}=\varphi^{(10)}=I\), which
did not occur for \(2\le k\le 12\).

## Prefix (dangerous set empty)

For \(2\le k\le 12\) the three even spines are never all equal to
\(I_{k+1}\). The Fermat covering through \(k=13\) is the Cycle BE
prefix, not a new table and not a push to \(k=16\). **PREFIX**, not
a theorem that the dangerous set is empty for all \(k\).

## \(\varphi^{(6)}_k\equiv 1\) for \(k\ge 5\) — killed

On \(k=2,\ldots,13\) the spine is
`000111111110`. The run of 1s from \(k=5\) dies at \(k=13\).
**Killed** as a 1-production. The pair
\(\varphi^{(5)}_k\lor\varphi^{(6)}_k\) also vanishes at \(k=13\).
**Killed** as a covering of every \(k\ge 2\).

## Verdict

`LEMMA` (doubling for \(q=3,5,9\); covering fails at \(k+1\) iff
\(\varphi^{(6)}_k=\varphi^{(10)}_k=\varphi^{(18)}_k=I_{k+1}\)).
`PREFIX` (dangerous set empty for \(2\le k\le 12\); Fermat covering
for all \(k\ge 2\)).
`KILLED` (\(\varphi^{(6)}_k\equiv 1\) for \(k\ge 5\);
\(\varphi^{(5)}\lor\varphi^{(6)}\) for all \(k\ge 2\)).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_bo.md` (this note)
- `research/cycle_bo.py`
- `research/cycle_bo.json`
