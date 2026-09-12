# Cycle KX: \(q=10\) max-Mersenne extra right is the first clipped column \(j=5U+1\)

Certified \(k\le 10\): on \(n=2^{k+2}-1\) the Cycle KW extra right is
\(\min(\mathrm{clip\_js})=5\cdot 2^k+1\), with \(\mathrm{green4}=0110\).
The clip threshold \(j>5U\) starts at a \(d\equiv 0\pmod{3}\) one.
This is **not** the last clipped column, **not** \(j=5U\) (in support,
\(p=0\)), **not** a left, and **not** \(q=6\) first-clipped as an extra.
Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: this locates Cycle KW's extra right, not packed
AND XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_kx.py --certify` (~0.14s).
Dump: `research/cycle_kx.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/HG/KH/KT/KV/KW (\(k\le 10\) Green-only; covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (mer10 extra is \(j=5U+1\))

Certified \(k\le 10\) (11 max-Mersenne clippers). Removing that
column leaves left/right balanced. Covering \(J_6,J_{10}\) still have
\(G=1\) columns \(22659\); odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Lemma (family clip left/right)

Cycle KW. Equal left/right except \(q=10\) max Mersenne one extra
right.

## Killed

Extra is last clipped: \(k=2\), \(n=15\) last is \(30\), extra is
\(21\). Extra is \(j=5U\): \(j=20\) has packed index \(0\). Extra is
a left: \(j=21\) is right \(0110\). \(q=6\) first clipped is an extra:
\(k=2\), \(n=7\) is balanced \(1,1\).

## Verdict

`LEMMA` (mer10 extra \(j=5U+1\); family clip left/right; family clip
isolated-pair).
`KILLED` (last clipped; \(j=5U\); extra left; \(q=6\) first is extra).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_kx.md` (this note)
- `research/cycle_kx.py`
- `research/cycle_kx.json`
