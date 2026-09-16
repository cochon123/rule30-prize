# Period-2 \(L_0\): \(T=35\) isolated extra \(=7\) is the \(10\)-tail family

Checked lemma: every \(T=35\) isolated extra-\(7\) ugap onset is one
of six words with prefix in
\(\{000100,001000,010000,010100,100100,101000\}\) and
\(10\)-periodic tail `101010101010`. They share extra bits `0101000`,
\(R=14\), and \(F\)-pattern \(1\) then fourteen zeros then \(1\). None
is an \(R=3\) image. They are \(S\)-minimal births of bump even-\(F\)
extra \(=5\) at \(T=37\). Isolated extra \(=8\) still lives
\(S\)-minimally at \(T=43\). Not a prize claim.

Helper: `python3 research/period2_t35ten.py --certify`. Dump:
`research/period2_t35ten.json`. \(R=3\) pullback as in
`research/period2_r3pull.md`; extra descent as in
`research/period2_alldesc.md`; alternating \(u\) as in
`research/period2_mod7.md`.

## Lemma (\(T=35\) isolated extra \(=7\) is a \(10\)-tail)

\(\mathrm{nvars}(35)=18\). A ugap scan finds exactly six isolated
extra-\(7\) onsets, namely

```
000100101010101010
001000101010101010
010000101010101010
010100101010101010
100100101010101010
101000101010101010
```

Silent \(u_0\) pairs the first with the fifth and the second with the
sixth; the third and fourth have illegal \(u_0\)-flips (`11`). Each
word even-\(F\)-clips at \(n=25\) with extra bits `0101000`, so
\(R=14\). Direct \(F\) gives \(F_{35}=1\), \(F_{36}=\cdots=F_{49}=0\),
\(F_{50}=1\). Prepending \(0\) or \(1\) never yields an even-\(F\)
extra-\(2\) onset at \(T=34\) whose \(R=3\) image is the word. The
\(T+2\) descent sends each to a bump even-\(F\) extra-\(5\) onset.

The same six prefixes with a \(10\)-tail at every other odd
\(T\in[15,47]\) are not extra-\(7\) (probe, not in this certificate).
A strictly alternating \(u\) has period-\(7\) left
(`research/period2_mod7.md`); these words are alternating only after
a length-\(6\) defect, and the Q-forced extra does not continue \(10\).

## What this does not do

Isolated extra \(=8\) still occurs. At \(T=43\) there are twelve
isolated even-\(F\) extra-\(8\) onsets, all with tail
`0001001000010010` and \(R=16\). Three are \(R=3\) images of bump
even-\(F\) extra \(=2\) at \(T=42\); **nine are \(S\)-minimal**.
Uniform extra \(\le 8\) remains a census. Infinite \(L_0\) is
untouched. Other periods of \(c_t\) are untouched.

## Verdict

`LEMMA`, wall time ~5s.

- Kill of period 2: no.
- \(T=35\) isolated extra \(=7\) classified: yes (\(10\)-tail, \(S\)-minimal).
- Isolated extra \(=8\) killed: no (nine \(S\)-minimal at \(T=43\)).
- Uniform extra \(\le 8\): no.

## Files

- `research/period2_t35ten.md` (this note)
- `research/period2_t35ten.py` (`--certify`)
- `research/period2_t35ten.json` (dump)
- `research/period2_r3pull.md` (\(T=33\) isolated extra \(=7\) is an \(R=3\) image)
- `research/period2_mod7.md` (strictly alternating \(u\) has period-\(7\) left)
- `research/period2_e8cap.md` (extra \(\le 8\) through \(T=48\); \(T=43\) period-8 tail)
