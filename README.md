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

Last completed cycle is **J** (ideas9). Exhaustive radius 11 kills a
constant `L_run≤24`: a true radius-11 row has a period-2 centre burst
of length 29. Period 3 and isolated-zero `q=8` finite-row scans still
grow with radius. Short matrix-trace products are unsat. Cycle I’s
capped theorem for `w≤10` inside `tcap=8w+128` is unchanged.

Do not overwrite `experiment.py`, `research/strip_graph.py`, or
`research/strip_extend.py`.

## Constraints that still hold

- Official site still open; width-1 center periodicity is the gap after
  Jen/Kopra (width-2 aperiodicity).
- Infinitely many 0s and 1s in the center are proved.
- Isolated-zero periods `01^q` are excluded except `q ∈ {1,2,3,4,5,6,8}`.
- Period 2 has no uniform-in-onset bound. Every nonzero row of radius
  `w≤10` has period-2 centre runs of length at most 24 *inside*
  `tcap=8w+128`; at radius 11 the longest burst is 29. Periods 3–7
  and `q=8` remain.
- Density and linear-time computation are untouched by a proof.

Helper scripts live in `research/`. Dumps are the matching `.json` files.
Astra briefs and idea lists are `research/_astra_brief*.md` and
`research/_astra_ideas*.md`.
