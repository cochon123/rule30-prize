# Cycle KZ: \(G(3\cdot 2^a-1)\) has three isolated ones iff \(a\) even

For \(a\) even, Green row \(3\cdot 2^a-1\) has isolated ones at
\(U-1\), \(3U-1\), \(5U-1\) with \(U=2^a\), no run-3, and
\(n_{\mathrm{run2}}=2^{a+1}-2\). For \(a\) odd, it has no isolated
ones, run-3 starts at \(U-2\), \(3U-2\), \(5U-2\), and
\(n_{\mathrm{run2}}=2^{a+1}-4\). This is **not** a unique isolated
one, **not** a unique run-3, **not** a run-3 on even \(a\), and
**not** isolated ones on odd \(a\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: this is the run shape of Cycle KN's \(3U-1\)
row, not packed AND XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_kz.py --certify`.
Dump: `research/cycle_kz.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AT/CA/IP/IR/KH/KJ/KP/KY (\(a\le 8\) Green-only; covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (tri three isolated ones iff \(a\) even)

Certified \(a\le 8\). Matches Cycle IW centre type
(\(v_2(n+1)=a\)) with two palindrome copies at \(\pm 2U\). Covering
\(J_6,J_{10}\) still have \(G=1\) columns \(22659\); odd-\(s\) \(J\)
XOR matches Cycles HF/HG.

## Lemma (Mersenne centre isolated iff \(L\) even)

Cycle KY. Unique centre isolated one when \(L\) is even; unique
centre run-3 when \(L\) is odd.

## Killed

Unique isolated one: \(a=2\), \(n=11\) has three
(\(3,11,19\)). Unique run-3: \(a=1\), \(n=5\) has three. Odd \(a\)
has isolated ones: \(a=1\) has none. Even \(a\) has a run-3:
\(a=2\) has none.

## Verdict

`LEMMA` (tri three isolated ones iff \(a\) even; Mersenne centre
isolated iff \(L\) even; mer10 extra \(j=5U+1\)).
`KILLED` (unique iso; unique run-3; odd isolated; even run-3).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_kz.md` (this note)
- `research/cycle_kz.py`
- `research/cycle_kz.json`
