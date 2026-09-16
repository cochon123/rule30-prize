# Period-2 \(L_0\): \(T=33\) isolated extra \(=7\) pulls back under \(R=3\)

Checked lemma: the three \(T=33\) isolated even-\(F\) extra-\(7\)
ugap onsets of `research/period2_alldesc.md` (shared tail
`00010100100100`, \(R=14\)) are exactly the isolated images under
\(S\) of bump even-\(F\) extra-\(2\) onsets at \(T=32\). They are
therefore not \(S\)-minimal: they are the extra-raising instances of
the \(R=3\) germ. The map does **not** absorb later isolated extra
\(=7\). Not a prize claim.

Helper: `python3 research/period2_r3pull.py --certify`. Dump:
`research/period2_r3pull.json`. Germ as in
`research/period2_r3iso.md`; family as in
`research/period2_alldesc.md`.

## Lemma (\(T=33\) isolated extra \(=7\) is an \(R=3\) image)

Write \(T=32\). A ugap onset even-\(F\)-clipping with extra \(=2\) has
\(n_0=16\), \(n_{\mathrm{clip}}=18\), \(R=3\), and clip at \(F_{36}=1\).
The germ sends \(Su\) to an isolated onset at \(T+1=33\). On this
family the image extra is \(7\) (clip at \(n=24\), even \(F_{48}=1\),
\(R=14\)). Explicitly the five bump sources

```
0001000101001001  ↦  00100010100100100
1001000101001001  ↦  00100010100100100
0010000101001001  ↦  01000010100100100
1010000101001001  ↦  01000010100100100
0101000101001001  ↦  10100010100100100
```

are all of the \(T=32\) bump even-\(F\) extra-\(2\) onsets whose
image extra is \(7\), and their three images are all of the \(T=33\)
isolated extra-\(7\) ugap onsets. The missing sixth prepend
`1101000101001001` is illegal ugap (`11`). Silent \(u_0\) identifies
the paired sources.

Certified on the three alldesc words, on every ugap string of length
\(\mathrm{nvars}(33)=17\), and on every bump even-\(F\) extra-\(2\)
onset at \(T=32\).

## What this does not do

Isolated extra \(=7\) still occurs \(S\)-minimally. The six \(T=35\)
isolated even-\(F\) extra-\(7\) words with \(10\)-periodic tail
`101010101010` have no even-\(F\) extra-\(2\) preimage at \(T=34\).
\(T=37\) bump `11` extra \(=8\) is likewise not an \(R=3\) image
(\(R=3\) lands on isolated onsets at odd \(T\)). Uniform extra
\(\le 8\) remains a census. Infinite \(L_0\) is untouched. Other
periods of \(c_t\) are untouched.

## Verdict

`LEMMA`, wall time ~1s.

- Kill of period 2: no.
- \(T=33\) isolated extra \(=7\) \(S\)-minimal: no (it is an \(R=3\) image).
- Isolated extra \(=7\) killed: no (\(T=35\) survives).
- Uniform extra \(\le 8\): no.

## Files

- `research/period2_r3pull.md` (this note)
- `research/period2_r3pull.py` (`--certify`)
- `research/period2_r3pull.json` (dump)
- `research/period2_r3iso.md` (\(R=3\) even fire \(\mapsto\) isolated at \(T+1\))
- `research/period2_alldesc.md` (the three \(T=33\) words as isolated extra max)
