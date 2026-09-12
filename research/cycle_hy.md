# Cycle HY: mixed cob/non-cob pairs contribute one-sided non-cob AND

If exactly one dual 4-tuple is coboundary-shaped, Cycle HT forces the
cob AND \(=0\), so the pair XOR equals the non-cob AND. Covering
odd-\(s\) \(J\) is then center AND XOR that mixed slice XOR
both-non-cob AND disagreements. Mixed cob is **not** always the left
column. Mixed non-cob is **not** always AND. Both-non-cob XOR is
**not** 4-tuple inequality. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: mixed one-sided AND still leaves both-non-cob
disagreements and the center AND, so covering never-fail stays open.

Helper: `mixed_oneside`. Certify: `python3 research/cycle_hy.py --certify`.
Dump: `research/cycle_hy.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HT/HU/HX (16-row table; covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (mixed cob/non-cob AND xor equals non-cob AND)

16\(\times\)16: if exactly one of two 4-tuples is cob-shaped, cob AND
is 0 and `mixed_oneside` equals the non-cob `and_clause`. Certified on
packed covering \(J_6,J_{10}\) for \(k\le 6\). Census:
\(n_{\mathrm{pair}}=8944\), mixed \(4383\) of which XOR \(2216\).

## Lemma (covering \(J\) equals center XOR mixed XOR both-non-cob)

Odd-\(s\) \(J\) is AND at \(j=n\) XOR mixed one-sided AND XOR
both-non-cob AND disagreements. Census: centers \(762\) of which
\(232\) AND; both-cob \(2438\) (xor \(0\), Cycle HX); both-non-cob
\(2123\) of which XOR \(1030\). Odd-\(s\) \(J\) XOR matches Cycles
HF/HG.

## Killed

Mixed cob always the left column: at \(k=1\), \(s=13\), \(n=3\),
\(j=1\) vs \(5\), fours \(0011\) vs \(0111\), \(p=18,10\). Mixed
non-cob always AND: at \(k=2\), \(s=17\), \(n=11\), \(j=6\) vs
\(16\), fours \(1000\) vs \(0001\), \(p=28,8\). Both-non-cob AND xor
equals 4-tuple inequality: at \(k=0\), \(s=7\), \(n=1\), \(j=0\) vs
\(2\), fours \(0010\) vs \(0100\), both AND \(=1\).

## Verdict

`LEMMA` (mixed oneside AND xor; covering \(J\) equals center XOR mixed
XOR both-non-cob; mixed cob AND \(0\)).
`KILLED` (mixed cob always left; mixed non-cob always AND;
both-non-cob xor equals 4-tuple inequality).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_hy.md` (this note)
- `research/cycle_hy.py`
- `research/cycle_hy.json`
