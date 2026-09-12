# Cycle HX: dual packed indices palindrome; both-cob pairs drop out of \(J\)

In-support dual columns have \(p+p'=2(T-2n)\). Both-cob \(G=1\) pairs
have AND xor \(0\), so they drop out of the palindrome fold.
Bit-reverse sends CONT to cob \(1100\) and permutes the three FRESH.
Dual 4-tuple is **not** bit-reverse. Cob-shape is **not** palindromic
on \(G=1\). Center is **not** `green4`. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: both-cob pairs dropping out still leaves cob/non-cob
and both-non-cob disagreements, so covering never-fail stays open.

Helper: `reverse_four`. Certify: `python3 research/cycle_hx.py --certify`.
Dump: `research/cycle_hx.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HI/HJ/HT/HU/HW (16-row table; covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (dual packed-index palindrome)

For in-support dual \(j\) and \(2n-j\), packed indices satisfy
\(p+p'=2(T-2n)\). Certified on packed covering \(J_6,J_{10}\) for
\(k\le 6\).

## Lemma (both-cob pairs have AND xor \(0\))

If both dual 4-tuples are coboundary-shaped, Cycle HT forces both
AND \(=0\). Covering census: \(n_{\mathrm{pair}}=8944\), both-cob
\(2438\), of which AND xor \(=0\). Odd-\(s\) \(J\) XOR matches
Cycles HF/HG.

## Lemma (bit-reverse sends CONT to cob \(1100\))

16-row: reverse of CONT \(0011\) is cob \(1100\). Reverse permutes
the three FRESH 4-tuples. So bit-reverse does not preserve
`AND_ONES`.

## Killed

Dual 4-tuple equals bit-reverse: at \(k=1\), \(s=9\), \(n=1\),
\(j=0\) vs \(2\), fours \(1100\) vs \(0001\). Cob-shape palindromic
on \(G=1\): at \(k=1\), \(s=5\), \(n=7\), \(j=6\) vs \(8\), fours
\(0001\) vs \(1001\). Center equals `green4`: at \(k=0\), \(s=3\),
\(n=1\), \(j=1\), \(p=4\), four \(1001\) vs Green \(1010\).

## Verdict

`LEMMA` (dual packed-index palindrome; both-cob pairs AND xor \(0\);
reverse CONT to cob \(1100\)).
`KILLED` (dual equals bit-reverse; cob palindromic on \(G=1\); center
equals `green4`).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_hx.md` (this note)
- `research/cycle_hx.py`
- `research/cycle_hx.json`
