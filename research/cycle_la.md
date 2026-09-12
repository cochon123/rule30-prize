# Cycle LA: tri three specials are the Mersenne unique, palindrome dual, and centre

For \(U=2^a\), the three isolated ones of \(G(3U-1)\) when \(a\) is
even are \(U-1\) (Cycle KY's unique Mersenne isolated one, on the
Cycle KP prefix), \(3U-1\) (the tri centre), and \(5U-1\) (palindrome
dual). When \(a\) is odd, the three run-3 starts are \(U-2\),
\(3U-2\), \(5U-2\) by the same split. This is **not** prefix-only,
**not** missing the centre, **not** a Mersenne special off the
prefix, and **not** a different odd-\(a\) geometry. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: this is the KY/KZ/KP run-shape mechanism, not
packed AND XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_la.py --certify`.
Dump: `research/cycle_la.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/IP/IR/KH/KP/KZ (\(a\le 8\) Green-only; covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (tri specials from Mersenne unique)

Certified \(a\le 8\). Mersenne centre is self-dual; the KP prefix
places it off-centre on \(3U-1\), so palindrome produces a second
copy and the middle band produces the new centre. Covering
\(J_6,J_{10}\) still have \(G=1\) columns \(22659\); odd-\(s\) \(J\)
XOR matches Cycles HF/HG.

## Lemma (tri three isolated ones iff \(a\) even)

Cycle KZ. Isolated ones at \(U-1,3U-1,5U-1\) when \(a\) is even;
run-3 starts \(U-2,3U-2,5U-2\) when \(a\) is odd.

## Killed

Prefix-only: \(a=2\) has three (\(3,11,19\)). Missing the centre:
includes \(n=11\). Mersenne special off the prefix: \(U-1=3\le 6\).
Odd \(a\) different: \(a=1\) is \(0,4,8\).

## Verdict

`LEMMA` (tri specials from Mersenne unique; tri three isolated ones
iff \(a\) even; Mersenne centre isolated iff \(L\) even).
`KILLED` (prefix-only; no centre; mer off-prefix; odd-a different).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_la.md` (this note)
- `research/cycle_la.py`
- `research/cycle_la.json`
