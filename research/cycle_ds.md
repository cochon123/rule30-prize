# Cycle DS: even-spine covering-failure prefix past \(k=12\)

Cycle BO: the Fermat covering fails at \(k+1\) iff
\(\varphi^{(6)}_k=\varphi^{(10)}_k=\varphi^{(18)}_k=I_{k+1}\), and
that dangerous set is empty for \(2\le k\le 12\). This cycle samples
only the even spines \(\varphi^{(2,6,10)}\) through \(k=18\) and
\(\varphi^{(18)}\) through \(k=17\) (and \(k=18\) only if \(6\) and
\(10\) already match \(I\)). Covering at \(k\ge 14\) is inferred from
that criterion. It does **not** compute \(\varphi^{(3)},\varphi^{(5)},
\varphi^{(9)}\) at \(k=16\).

Not a prize claim: emptiness remains a prefix. The period-\(H\) seed
through \(k=19\) is still a prefix.

Helper: `python3 research/cycle_ds.py --certify`. Dump:
`research/cycle_ds.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (failure criterion)

Unchanged from Cycle BO (doubling, Cycle AL/AH): covering at \(k+1\)
vanishes iff the three even spines equal \(I_{k+1}=\varphi^{(2)}_k\).
This cycle does not re-prove doubling and does not dump a Fermat table.

## Prefix (dangerous set)

The BO empty set on \(2\le k\le 12\) is reproduced. The same packed
run extends the even-spine test through \(k=17\) (covering through
\(k=18\)) and through \(k=18\) unless \(\varphi^{(6)}_{18}=\varphi^{(10)}_{18}=I_{19}\),
in which case \(\varphi^{(18)}_{18}\) is sampled by continuing the run.
**PREFIX**, not a theorem that the dangerous set is empty for all \(k\).

## Fermat \(\varphi^{(3,5,9)}\) table at \(k=16\)

Not computed. Inferred covering bits are a boolean from the even-spine
criterion, not the triple \((\varphi^{(3)},\varphi^{(5)},\varphi^{(9)})\).

## Verdict

`LEMMA` (covering fails at \(k+1\) iff the even spines equal \(I\)).
`PREFIX` (dangerous set empty on the certified range; Fermat covering
for all \(k\); period-\(H\) seed for all \(k\)).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ds.md` (this note)
- `research/cycle_ds.py`
- `research/cycle_ds.json`
