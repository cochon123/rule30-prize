# Cycle KV: family clip \(G=1\) is an isolated-pair column; \(\mathrm{green4}\) by \(d\bmod 3\)

Clipped \(G=1\) on covering family clippers are never isolated ones
and never run-3. Each is a run-2 column: \(\mathrm{green4}\) is
\(1011\) (left) iff \((2n-j)\equiv 1\pmod{3}\), and \(0110\) (right)
iff \((2n-j)\equiv 0\pmod{3}\). This is **not** a single
\(\mathrm{green4}\), **not** isolated-one \(0111\), **not** run-3
middle \(1010\), and **not** \(d\equiv 0\) giving left \(1011\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: this is the shape of Cycle KT's columns (low-band
\(f\bmod 3\) has runs of length 2 only), not packed AND XOR \(J\), so
covering never-fail stays open.

Certify: `python3 research/cycle_kv.py --certify` (~0.15s).
Dump: `research/cycle_kv.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HJ/IG/IN/IR/KH/KR/KT (\(k\le 10\) Green-only; covering \(k\le 6\);
no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (family clip is isolated-pair)

Certified \(k\le 10\) (6791 clipped ones; 3390 left, 3401 right).
Covering \(J_6,J_{10}\) still have \(G=1\) columns \(22659\);
odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Lemma (family clip green4 XOR)

Cycle KU. \(q=6\) max Mersenne and \(q=10\) \(3U-1\) give \(1101\) if
\(k\ge 2\) is even and \(0000\) if odd; \(q=10\) max Mersenne is
\(0110\) at \(k=0\) and \(1011\) for \(k\ge 1\).

## Killed

Clipped are isolated ones: \(k=2\), \(q=6\), \(n=7\), \(j=13,14\) are
run-2. All the same \(\mathrm{green4}\): those two are \(1011\) and
\(0110\). Run-3 middle \(1010\): none. \(d\equiv 0\) is left:
\(k=0\), \(q=10\), \(n=3\), \(j=6\) is right \(0110\).

## Verdict

`LEMMA` (family clip isolated-pair; family clip green4 XOR; family
clip columns).
`KILLED` (isolated ones; all same green4; run-3; \(d\equiv 0\) left).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_kv.md` (this note)
- `research/cycle_kv.py`
- `research/cycle_kv.json`
