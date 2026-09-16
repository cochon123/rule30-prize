# Period-2 \(L_0\): extra \(=8\) through \(T=48\) is two prefix families

Checked lemma: every extra-\(8\) ugap onset with \(T\in[44,48]\) lies
in an explicit prefix family already seen at \(T=35\) or \(T=43\).
The six \(T=35\) \(10\)-tail prefixes reappear as all of \(T=46\)
extra \(=8\) and as five of five \(T=47\) extra-\(8\) words; those
five are not \(R=3\) images. The twelve \(T=43\)
\((00010010)^2\) prefixes reappear as twelve of fifteen \(T=48\)
extra-\(8\) words. This classifies the extra-\(8\) census; it does
not bound extra independently of \(T\). Not a prize claim.

Helper: `python3 research/period2_e8fam.py --certify`. Dump:
`research/period2_e8fam.json`. Census as in
`research/period2_e8cap.md`; \(T=35\) prefixes as in
`research/period2_t35ten.md`; \(R=3\) as in
`research/period2_r3pull.md`.

## Lemma (two prefix families)

Write \(P_{35}\) for the six length-\(6\) prefixes of the \(T=35\)
isolated extra-\(7\) \(10\)-tail family, and \(P_{43}\) for the twelve
length-\(6\) prefixes of the \(T=43\) isolated extra-\(8\)
period-8-tail family.

- \(T=44\): three isolated `11` extra-\(8\) words, tail
  `001000010001000101`, prefixes \(\{0001,0101,1001\}\). They
  descend to bump `11` extra \(=6\) at \(T=46\).
- \(T=46\): extra \(=8\) is exactly \(P_{35}\) followed by
  `10100101010001010` (bump even \(F\), extra bits `00101010`,
  \(R=15\)). Descent: bump even \(F\) extra \(=6\) at \(T=48\).
- \(T=47\): extra \(=8\) is exactly five words of \(P_{35}\)
  (missing `010000`) followed by `010010101000010000`. Isolated
  even \(F\), \(R=16\). No even-\(F\) extra-\(2\) preimage at
  \(T=46\).
- \(T=48\): extra \(=8\) is \(P_{43}\) followed by
  `000101001000100001` (twelve bump even \(F\)) together with
  prefixes \(\{0001,0101,1001\}\) followed by
  `00100100100010100100` (three bump even \(F\)).

Certified by forcing every listed word and matching the extra-\(8\)
lists of `research/period2_e8cap.json`. \(T=20\) bump `11` extra
\(=8\) uses three of \(P_{35}\) (already in
`research/period2_alldesc.md`); \(T=37\) bump `11` extra \(=8\) is a
separate \(10\)-run family.

## What this does not do

The families are \(S\)-minimal at these \(T\) (no extra-\(10\) parent,
and \(T=47\) is not \(R=3\)). Uniform extra \(\le 8\) is false:
\(S\)-minimal extra \(=10\) exists at \(T=51\)
(`research/period2_e10t51.md`). Infinite \(L_0\) is untouched. Other
periods of \(c_t\) are untouched.

## Verdict

`LEMMA`, wall time ~0.1s.

- Kill of period 2: no.
- Extra \(=8\) through \(T=48\) classified: yes.
- Uniform extra \(\le 8\): no (fails at \(T=51\)).
- \(T=47\) extra \(=8\) is \(R=3\): no.

## Files

- `research/period2_e8fam.md` (this note)
- `research/period2_e8fam.py` (`--certify`)
- `research/period2_e8fam.json` (dump)
- `research/period2_e8cap.md` (extra \(\le 8\) through \(T=48\))
- `research/period2_t35ten.md` (\(P_{35}\) and \(P_{43}\))
- `research/period2_e7pref.md` (extra \(\ge 7\) through \(T=48\) lives on these 18 prefixes)
- `research/period2_e10t51.md` (\(S\)-minimal extra \(=10\) at \(T=51\))
