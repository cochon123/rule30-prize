# Cycle KY: Mersenne \(G(2^L-1)\) has a unique centre isolated one iff \(L\) even

For \(L\) even, Green row \(2^L-1\) has a unique run-1 at the centre,
no run-3, and \(n_{\mathrm{run2}}=(\operatorname{jacobsthal}(L+2)-1)/2\).
For \(L\) odd, it has no isolated ones, a unique run-3 at the centre
(start \(n-1\)), and \(n_{\mathrm{run2}}=(\operatorname{jacobsthal}(L+2)-3)/2\).
This is **not** isolated ones on odd \(L\), **not** two isolated ones,
**not** off-centre, and **not** a run-3 on even \(L\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: this is the run shape of Cycle KL's Mersenne
weight, not packed AND XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_ky.py --certify`.
Dump: `research/cycle_ky.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AT/CA/IP/IR/KH/KJ/KX (\(L\le 10\) Green-only; covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (Mersenne centre isolated iff \(L\) even)

Certified \(L\le 10\). Matches Cycle IW centre type
(\(v_2(n+1)=L\)) and Cycle KI run recurrences. Covering \(J_6,J_{10}\)
still have \(G=1\) columns \(22659\); odd-\(s\) \(J\) XOR matches
Cycles HF/HG.

## Lemma (mer10 extra is \(j=5U+1\))

Cycle KX. \(q=10\) max-Mersenne extra right is the first clipped
column.

## Killed

Odd \(L\) has isolated ones: \(L=1\), \(n=1\) has none. Two isolated
ones: \(L=2\), \(n=3\) is only the centre. Off-centre: that one is
\(j=n\). Even \(L\) has a run-3: \(L=2\) has none.

## Verdict

`LEMMA` (Mersenne centre isolated iff \(L\) even; mer10 extra
\(j=5U+1\); family clip left/right).
`KILLED` (odd isolated; two isolated; off-centre; even run-3).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ky.md` (this note)
- `research/cycle_ky.py`
- `research/cycle_ky.json`
