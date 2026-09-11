# Rule 30 prize research

Sustained attempt at the [Rule 30 prizes](https://rule30prize.org/).
**No prize problem is solved.** Do not submit or contact the committee
from this repo.

## Continue on another machine

```sh
git clone git@github.com:cochon123/rule30-prize.git
cd rule30-prize
python3 experiment.py --bits 1000
```

Read in this order:

1. [REPORT.md](REPORT.md) — checked conclusions and cycle summaries
2. [research/LOG.md](research/LOG.md) — what was tried and what died
3. The notes those files cite under `research/`

Last completed cycle is **AC**. Centre `00` is the triple `000` or
`101`, each with four 5-window preimages. Every left-diagonal
\(e_j(t)=x(t,-t+j)\) is eventually periodic, but \(c_t=e_t(t)\) is an
onset, not a tail value. Infinitely many `00`s are unproved. The prize
is still open.

Do not overwrite `experiment.py`, `research/strip_graph.py`, or
`research/strip_extend.py`.

## Constraints that still hold

- Official site still open; width-1 center periodicity is the gap after
  Jen/Kopra (width-2 aperiodicity). Every iterate \(F^p\) has Kopra
  width \(2p\) (Cycle V), so the gap is not closed by passing to a
  power. An infinite 2-kernel would close it: \(v_k=v_{k+1}\) already
  forces \((c_{2^j})_{j\ge k}\) constant (Cycle Y). One doubling is
  \(c_{2^k}=c_{2^{k-1}}\oplus I_k\) with \(I_k\) the AND-Green remainder
  (Cycle Z). Every \(c_t\land r_t\) on that annulus hits \(I_k\)
  (Cycle AA); the off-centre remainder is the palindrome-defect
  parity \(\bigoplus(\ell\oplus r)\) and cannot be eventually the zero
  sequence (Cycle AB). Every left-diagonal \(x(t,-t+j)\) is eventually
  periodic; the centre is the onset \(e_t(t)\), not the tail
  (Cycle AC). Centre `00` is the triple `000` or `101`.
- Infinitely many 0s and 1s in the center are proved.
- Isolated-zero periods `01^q` are excluded except `q ∈ {1,2,3,4,5,6,8}`.
- Period 2 has no uniform-in-onset bound (`maxR=16` at `T=20` is still
  the worst through `T=34`). The even right neighbor of a period-2
  centre has no five consecutive zeros, in addition to no consecutive
  1s. Origin-in-hull rows of weight `≤10` and span `≤20` (weight `≤8`
  through span 24) have `L_run≤31`. Off-hull weight-8 reaches 35.
  Periods 3–7 and `q=8` remain.
- Density and linear-time computation are untouched by a proof.
  Problem 2 is exactly \(N_{11}-N_{00}=o(N)\) via
  \(D(N)=N_{11}-N_{00}+c_{N-1}\). There is no finite-window coboundary
  or small-range bond flux for \(2c_t-1\) (Cycle X).

Helper scripts live in `research/`. Dumps are the matching `.json` files.
Astra briefs and idea lists are `research/_astra_brief*.md` and
`research/_astra_ideas*.md`.
