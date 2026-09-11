# Cycle BE: Fermat covering prefix through \(k=15\)

Cycle AK recorded that on \(2\le k\le 10\) at least one of
\(\varphi^{(3)}_k\), \(\varphi^{(5)}_k\), \(\varphi^{(9)}_k\) is 1.
Any infinite subsequence of that covering would kill every eventual
period \(2^m\) (Cycle AL: period \(2^m\) forces every integer
\(\varphi^{(q)}=0\)). The same packed-centre check holds through
\(k=15\). Still a prefix: there is no closed form that forces a 1,
and a later \(k\) could vanish. Not a prize claim: some
\(\varphi^{(q)}_k=1\) infinitely often remains open.

Helper: `python3 research/cycle_be.py --certify`. Dump:
`research/cycle_be.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Prefix (Fermat covering)

Let \(U=2^k\) and \(\varphi^{(q)}_k=c_{qU}\oplus c_U\). For Fermat-odd
\(q=2^a+1\), Cycle AK/AL give \(\varphi^{(q)}_k=1\oplus S^{(q)}_k\)
with leftmost-11 hit parity 1. On \(2\le k\le 12\) (certified) and
\(13\le k\le 15\) (same evolution, longer window) one has

| \(k\) | \(I_k\) | \(\varphi^{(3)}\) | \(\varphi^{(5)}\) | \(\varphi^{(9)}\) | \(\varphi^{(17)}\) |
|------:|:-------:|:-----------------:|:-----------------:|:-----------------:|:------------------:|
| 2 | 1 | 1 | 1 | 1 | 1 |
| 3 | 0 | 0 | 1 | 0 | 0 |
| 4 | 0 | 0 | 1 | 1 | 0 |
| 5 | 1 | 1 | 0 | 0 | 0 |
| 6 | 1 | 0 | 0 | 1 | 1 |
| 7 | 0 | 1 | 1 | 0 | 1 |
| 8 | 0 | 1 | 1 | 0 | 1 |
| 9 | 1 | 0 | 0 | 1 | 1 |
| 10 | 1 | 0 | 1 | 1 | 1 |
| 11 | 1 | 0 | 1 | 1 | 1 |
| 12 | 1 | 0 | 0 | 1 | 0 |
| 13 | 0 | 1 | 0 | 1 | 0 |
| 14 | 1 | 1 | 1 | 0 | 0 |
| 15 | 1 | 1 | 1 | 1 | 0 |

No row has \(\varphi^{(3)}=\varphi^{(5)}=\varphi^{(9)}=0\). No single
\(q\) is identically 1 (\(\varphi^{(17)}\) vanishes for \(k=12,\ldots,15\);
\(\varphi^{(3)}\) vanishes on several earlier \(k\)). **Prefix**, not a
theorem.

A proof that the covering continues for all \(k\ge 2\) would already
kill every eventual period \(2^m\), including period 2, without
controlling \(I_k\). Periods 3, 5, 6, 7 and isolated-zero \(q=8\)
would remain.

## Verdict

`PREFIX` (Fermat covering \(\varphi^{(3)},\varphi^{(5)},\varphi^{(9)}\)
has a 1 for \(2\le k\le 15\)).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often; \(I_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_be.md` (this note)
- `research/cycle_be.py`
- `research/cycle_be.json`
