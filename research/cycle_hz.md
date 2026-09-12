# Cycle HZ: bitwise complement swaps cob/non-cob; same-class never Hamming 4

`complement_four` flips all four bits. That swaps coboundary-shape with
non-cob, so `AND_ONES` maps to cob (AND \(=0\)). Complement of CONT
is cob \(1100\), the same as reverse. Covering same-class duals
(both-cob and both-non-cob) **never** have Hamming 4. Dual is **not**
complement. Complement is **not** reverse. Complement does **not**
preserve AND. Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\)
for all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: forbidding Hamming 4 on both-non-cob still leaves
Hamming \(0,1,2,3\) disagreements and the center AND, so covering
never-fail stays open.

Helper: `complement_four`. Certify: `python3 research/cycle_hz.py --certify`.
Dump: `research/cycle_hz.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HI/HT/HU/HX/HY (16-row table; covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (complement swaps cob and non-cob)

16-row: cob-shape of a 4-tuple is the negation of cob-shape of its
bitwise complement. Hamming with the complement is always 4.
Complement of every `AND_ONES` tuple is coboundary-shaped (AND \(=0\)).
Complement of CONT \(0011\) is cob \(1100\), equal to `reverse_four`.

## Lemma (same-class duals never Hamming 4)

On packed covering \(J_6,J_{10}\) for \(k\le 6\), both-cob (\(2438\))
and both-non-cob (\(2123\)) duals have Hamming \(\in\{0,1,2,3\}\).
Mixed pairs have Hamming 4 on \(524\) of \(4383\), and those are
exactly the complementary pairs. Odd-\(s\) \(J\) XOR matches Cycles
HF/HG.

## Killed

Dual 4-tuple equals complement: at \(k=1\), \(s=5\), \(n=7\), \(j=6\)
vs \(8\), fours \(0001\) vs \(1001\), Hamming \(1\). Complement equals
reverse: at \(k=0\), \(s=7\), \(n=1\), \(j=0\), \(p=10\), four \(0010\),
reverse \(0100\) vs complement \(1101\). Complement preserves AND: at
\(k=2\), \(s=17\), \(n=3\), \(j=0\) vs \(6\), fours \(0011\) vs \(1100\).

## Verdict

`LEMMA` (complement swaps cob/non-cob; AND complement is cob;
same-class duals never Hamming 4).
`KILLED` (dual equals complement; complement equals reverse;
complement preserves AND).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_hz.md` (this note)
- `research/cycle_hz.py`
- `research/cycle_hz.json`
