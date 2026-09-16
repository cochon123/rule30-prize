# Period-2 \(L_0\): extra \(\ge 7\) lives on 18 length-6 prefixes

Checked lemma: every ugap onset with extra \(\ge 7\) and
\(T\in[8,48]\) has prefix \(u_0\ldots u_5\) in the disjoint union
\(P_{35}\cup P_{43}\) of the six \(T=35\) \(10\)-tail prefixes and
the twelve \(T=43\) period-8-tail prefixes — eighteen ugap cylinders
in all. High extra is confined to those cones. This is a census
reduction, not a \(T\)-independent bound. Not a prize claim.

Helper: `python3 research/period2_e7pref.py --certify`. Dump:
`research/period2_e7pref.json`. Families as in
`research/period2_t35ten.md` and `research/period2_e8fam.md`; extra
census as in `research/period2_e8cap.md`.

## Lemma (extra \(\ge 7\) support)

Let
\[
P_{35}=\{000100,001000,010000,010100,100100,101000\},
\]
\[
P_{43}=\{000010,000101,001001,001010,010001,010010,010101,
100001,100010,100101,101001,101010\}.
\]
These are disjoint, each word is ugap-legal, and
\(|P_{35}\cup P_{43}|=18\).

A complete ugap scan of onsets with extra \(\ge 7\) for every
\(T\in[8,48]\) finds no counterexample: every such prefix of length
6 lies in the union. Both families occur (first \(P_{35}\) extra
\(\ge 7\) at \(T=20\); first \(P_{43}\) at \(T=37\)). Max extra on
the scan is still \(8\).

A uniform extra \(\le 6\) would follow from extra \(\le 6\) on these
eighteen cylinders. A uniform extra \(\le 8\) would follow from extra
\(\le 8\) on the same cylinders. Neither cylinder bound is proved.

## What this does not do

The support can grow at larger \(T\). Extra \(\le 8\) on the cylinders
is still a census. \(S\)-minimal extra \(=8\) exists inside the
support. Infinite \(L_0\) is untouched. Other periods of \(c_t\) are
untouched.

## Verdict

`LEMMA`, wall time ~60s.

- Kill of period 2: no.
- Extra \(\ge 7\) through \(T=48\) confined to 18 prefixes: yes.
- Uniform extra \(\le 8\): no.
- Cylinder bound for all \(T\): no.

## Files

- `research/period2_e7pref.md` (this note)
- `research/period2_e7pref.py` (`--certify`)
- `research/period2_e7pref.json` (dump)
- `research/period2_e8fam.md` (extra \(=8\) families)
- `research/period2_t35ten.md` (\(P_{35}\) and \(P_{43}\) sources)
