# Cycle II: consecutive 4-tuples overlap stride-2; the discrepancy is a bit-string

Packed, \(\mathrm{green4}\), and packed-XOR-\(\mathrm{green4}\) 4-tuples
at \(j\) and \(j+1\) share \((z,a)_j=(b,c)_{j+1}\) with
\(p_{j+1}=p_j-2\). Error is cob-shaped iff the packed 4-tuple is
(because \(\mathrm{green4}\) is cob, Cycle HT). Consecutive packed
4-tuples are **not** independent. Consecutive \(\mathrm{green4}\)
are **not** equal. Consecutive \(G=1\) AND **does** fire. Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: the discrepancy bit-string still reads the packed
row, so a Green-only error formula stays open.

Helper: `xor4`, `stride2_overlap`, `error4`. Certify:
`python3 research/cycle_ii.py --certify`.
Dump: `research/cycle_ii.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HJ/HT/HU/IH (\(n<64\) plus 16\(\times\)8-row;
covering \(k\le 6\); no Fermat table, no extra window, no \(n_0=16\)
window).

## Lemma (stride-2 overlap of packed, \(\mathrm{green4}\), and error)

For \(n<64\) and \(0\le j<2n\),
`stride2_overlap(green4(n,j), green4(n,j+1))`. Census
\(n_{\mathrm{g4}}=4032\). Covering \(k\le 6\): consecutive in-support
columns \(95059\), all three overlaps. Odd-\(s\) \(J\) XOR matches
Cycles HF/HG.

## Lemma (error cob-shaped iff packed cob-shaped)

On the \(8\) cob \(\mathrm{green4}\) 4-tuples, all \(16\) packed
4-tuples have `cob_shaped(error4(four,g4))==cob_shaped(four)`
(\(128\) rows). Covering: \(n_{\mathrm{ok}}=95821\).

## Lemma (covering consecutive \(G=1\) AND)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): consecutive \(G=1\)
pairs \(8577\), both-AND \(463\).

## Killed

Consecutive packed 4-tuples independent: at \(k=0\), \(s=3\),
\(n=1\), \(j=0\) vs \(1\), fours \(0100\) vs \(1001\), overlap
\((z,a)=(b,c)=(0,1)\). Consecutive \(\mathrm{green4}\) equal: same
witness, \(1011\) vs \(1010\). Consecutive \(G=1\) AND never both
fire: same witness, both AND.

## Verdict

`LEMMA` (stride-2 overlap of packed, \(\mathrm{green4}\), and error;
error cob-shaped iff packed cob-shaped; covering consecutive \(G=1\)
AND).
`KILLED` (consecutive packed independent; consecutive
\(\mathrm{green4}\) equal; no consecutive \(G=1\) AND).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ii.md` (this note)
- `research/cycle_ii.py`
- `research/cycle_ii.json`
