# Cycle DS: even-spine covering-failure empty through \(k=18\)

Cycle BO: the Fermat covering fails at \(k+1\) iff
\(\varphi^{(6)}_k=\varphi^{(10)}_k=\varphi^{(18)}_k=I_{k+1}\), and
that dangerous set is empty for \(2\le k\le 12\). This cycle samples
only the even spines. Covering at \(k\ge 14\) is inferred from that
criterion. It does **not** compute \(\varphi^{(3)},\varphi^{(5)},
\varphi^{(9)}\) at \(k=16\).

The dangerous set is empty for \(2\le k\le 18\), so the covering does
not fail through \(k=19\), matching the period-\(H\) seed through
\(k=19\). Not a prize claim: both remain prefixes.

Helper: `python3 research/cycle_ds.py --certify` (~1867s). Dump:
`research/cycle_ds.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (failure criterion)

Unchanged from Cycle BO (doubling, Cycle AL/AH): covering at \(k+1\)
vanishes iff the three even spines equal \(I_{k+1}=\varphi^{(2)}_k\).
This cycle does not re-prove doubling and does not dump a Fermat table.

## Prefix (dangerous set empty through \(k=18\))

The BO empty set on \(2\le k\le 12\) is reproduced. Candidates where
\(\varphi^{(6)}=\varphi^{(10)}=I\) but \(\varphi^{(18)}\ne I\) sit at
\(k=5,8,11,15,18\). None of them is dangerous. In particular \(k=18\)
needed the continuation to time \(18\cdot 2^{18}\) because \(6\) and
\(10\) already matched \(I_{19}\); \(\varphi^{(18)}_{18}=0\ne 1=I_{19}\).

**PREFIX**, not a theorem that the dangerous set is empty for all \(k\).
Do not claim \(\varphi^{(18)}=\neg I\) on every later candidate.

## \(I_k\) through \(k=21\)

\[
(I_k)_{k=1}^{21}=110011001111011011101.
\]

Both values still occur after \(k=12\) (\(I_{16}=I_{20}=0\),
\(I_{21}=1\)). \(I_k=1\) infinitely often remains **OPEN**. Nested left
is still not a formula.

## Fermat \(\varphi^{(3,5,9)}\) table at \(k=16\)

Not computed. Inferred covering bits are a boolean from the even-spine
criterion, not the triple \((\varphi^{(3)},\varphi^{(5)},\varphi^{(9)})\).
\(\varphi^{(6)}_k\) is \(0\) on \(k=13,\ldots,17\) and returns to \(1\)
at \(k=18\); do not claim it stays \(0\).

## Verdict

`LEMMA` (covering fails at \(k+1\) iff the even spines equal \(I\)).
`PREFIX` (dangerous set empty for \(2\le k\le 18\); Fermat covering
for all \(k\); period-\(H\) seed for all \(k\)).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ds.md` (this note)
- `research/cycle_ds.py`
- `research/cycle_ds.json`
