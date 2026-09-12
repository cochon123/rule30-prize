# Cycle KW: family clip left/right counts are equal except \(q=10\) max Mersenne

Certified \(k\le 10\): clipped isolated-pair left and right counts
are equal on the \(q=6\) max Mersenne and \(q=10\) \(3U-1\). The
\(q=10\) max Mersenne has one extra right
(\(\frac{c-1}{2}\) left, \(\frac{c+1}{2}\) right with
\(c=2^{k+1}-1\)). The \(f\bmod 3\) prefix of length \(3U-2\) ends on
\(d\equiv 0\pmod{3}\). This is **not** mer10 balanced, **not** an
extra left, **not** \(q=6\) unbalanced, and **not** a tri extra
right. Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all
\(k\). Do **not** push the even-spine scan past \(k=18\). Do **not**
bump all \(n_0=16\) past 414990. Do **not** increment consecutive
`11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: this is the left/right split of Cycle KV, not
packed AND XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_kw.py --certify`.
Dump: `research/cycle_kw.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/KR/KS/KT/KV (\(k\le 10\) Green-only; covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (family clip left/right)

Certified \(k\le 10\) (29 clipper clocks). Covering \(J_6,J_{10}\)
still have \(G=1\) columns \(22659\); odd-\(s\) \(J\) XOR matches
Cycles HF/HG.

## Lemma (family clip is isolated-pair)

Cycle KV. \(\mathrm{green4}\) is \(1011\) (left) iff
\((2n-j)\equiv 1\pmod{3}\) and \(0110\) (right) iff
\((2n-j)\equiv 0\pmod{3}\).

## Killed

\(q=10\) max Mersenne is balanced: \(k=0\), \(n=3\) is \(0\) left,
\(1\) right. Extra is a left: that extra is a right. \(q=6\)
unbalanced: \(k=2\), \(n=7\) is \(1,1\). Tri extra right: \(k=2\),
\(n=11\) is \(1,1\).

## Verdict

`LEMMA` (family clip left/right; family clip isolated-pair; family
clip green4 XOR).
`KILLED` (mer10 balanced; extra left; \(q=6\) unbalanced; tri extra
right).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_kw.md` (this note)
- `research/cycle_kw.py`
- `research/cycle_kw.json`
