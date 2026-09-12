# Cycle KU: family clip \(\mathrm{green4}\) XOR is \(1101\)/\(0000\) or \(0110\)/\(1011\)

On covering family clippers, the XOR of \(\mathrm{green4}\) over
clipped \(G=1\) is: \(q=6\) max Mersenne and \(q=10\) \(3U-1\) give
\(1101\) if \(k\ge 2\) is even and \(0000\) if odd; \(q=10\) max
Mersenne is \(0110\) at \(k=0\) and \(1011\) for \(k\ge 1\). This is
**not** covering \(\mathrm{clip\_want}\), **not** independent of
\(k\), **not** \(q=10\) max equal to \(q=6\) max, and **not**
row-XOR \(0111\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: this is Green-only XOR on Cycle KT's columns, not
packed AND XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_ku.py --certify`.
Dump: `research/cycle_ku.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HJ/KH/KR/KT (\(k\le 10\) Green-only; covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (family clip green4 XOR)

Certified \(k\le 10\) (29 clipper clocks). Palindrome sends clipped
\(\mathrm{green4}\) to low-band \(g_1\) shapes. Covering \(J_6,J_{10}\)
still have \(G=1\) columns \(22659\); odd-\(s\) \(J\) XOR matches
Cycles HF/HG.

## Lemma (family clip columns)

Cycle KT. Clipped \(G=1\) is \(j=2n-d\) for \(d\not\equiv 2\pmod{3}\)
in the low prefix.

## Killed

Equals covering \(\mathrm{clip\_want}\): \(k=1\), \(q=10\) is \(1011\)
vs \(1100\). Independent of \(k\): \(k=2\) is \(1101\), \(k=3\) is
\(0000\). \(q=10\) max equals \(q=6\) max: \(k=2\) is \(1011\) vs
\(1101\). Equals row-XOR \(0111\): \(k=2\), \(q=6\) is \(1101\).

## Verdict

`LEMMA` (family clip green4 XOR; family clip columns; family clip
counts).
`KILLED` (equals clip_want; independent of \(k\); mer10 equals mer6;
equals row-XOR).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ku.md` (this note)
- `research/cycle_ku.py`
- `research/cycle_ku.json`
