# Cycle KR: covering family clip is only the largest Mersenne (and \(3\cdot 2^k-1\) on \(q=10\))

For covering \(k\le 6\), no-\(00\) family clocks with clipped \(G=1\)
are: \(q=6\) none if \(k<2\) else \(n=2^{k+1}-1\); \(q=10\) always
\(n=2^{k+2}-1\), and also \(n=3\cdot 2^k-1\) when \(k\ge 2\). This is
**not** \(2^k-1\) on \(q=6\), **not** only the max Mersenne on
\(q=10\), **not** \(q=6\) at \(k=0\), and **not** \(3U-1\) on
\(q=6\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for
all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: this is covering geometry of Cycle KQ's family
parity, not packed AND XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_kr.py --certify` (~0.13s).
Dump: `research/cycle_kr.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HG/KH/KJ/KM/KQ (covering \(k\le 6\); no Fermat table, no extra
window, no \(n_0=16\) window).

## Lemma (family clippers)

Certified \(k\le 6\). Clip counts: \(q=6\) \(k\ge 2\) drops
\(2,4,10,20,42\) ones on the max Mersenne; \(q=10\) drops ones on
the max Mersenne and, for \(k\ge 2\), on \(3\cdot 2^k-1\).

## Lemma (family weight odd; covering parity is \(q\))

Cycle KQ. Covering \(J_6,J_{10}\) for \(k\le 6\) still have \(G=1\)
columns \(22659\); odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

\(q=6\) clips \(2^k-1\): \(k=2\), \(n=3\) is fully in support.
\(q=10\) clips only the max Mersenne: \(k=2\) also clips \(n=11\).
\(q=6\) \(k=0\) clips: \(n=1\) is fully in support. \(q=6\) clips
\(3\cdot 2^k-1\): \(k=2\), \(n=11\) is not a covering clock.

## Verdict

`LEMMA` (family clippers; family weight odd; covering family parity
is \(q\)).
`KILLED` (\(q=6\) clips \(2^k-1\); \(q=10\) only max; \(q=6\) \(k=0\);
\(q=6\) clips \(3U-1\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_kr.md` (this note)
- `research/cycle_kr.py`
- `research/cycle_kr.json`
