# Cycle GE: at \(s=W+2^j\), \(m=2U-1-2^j\); right-edge AND live iff \(t\) odd

On Cycle GD’s times \(s=W+2^j\) the Green clock is \(m=2U-1-2^j\),
from the diagonal \(m=2U-2\) at \(j=0\) to the clip corner \(m=U-1\) at
\(j=a-1\). Cone-hi equals \(r_*\) iff \(j=0\) (the palindrome pair
collapses to one cell). Packed bit \(2t\) is the right edge
\(x(t,t)=1\); the right-edge AND (bits \(2t\) and \(2t-1\)) is live iff
\(t\) is odd. Covering \(W\) is even, so \(s=W+1\) is odd and the
collapsed cell has \(G=1\) **and** live AND. Right-edge AND is **not**
always live, collapse is **not** for all \(j\), and the palindrome-pair
AND XOR is **not** identically 0. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push the
even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\) past
414990. Do **not** increment consecutive `11` to \(n_8\). Do **not**
walk \(32U\).

Not a prize claim: one live \(G=1\) cell at \(s=W+1\) does not prove
covering never-fail (the rest of the band still contributes).

Helper: `python3 research/cycle_ge.py --certify` (~0.01s). Dump:
`research/cycle_ge.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles CA/GB/GD (geometry \(k\le 11\); right-edge
\(t\le 256\); collapsed AND \(k\le 6\); no Fermat table, no extra
window, no \(n_0=16\) window).

## Lemma (\(m=2U-1-2^j\); collapse iff \(j=0\))

Certified \(k\le 11\), \(W\in\{4U,8U,16U\}\).

## Lemma (right-edge AND live iff \(t\) odd)

Bit \(2t=1\) for \(t\ge 0\); bit \(2t-1=t\bmod 2\) for \(t\ge 1\).
Certified \(1\le t\le 256\).

## Lemma (collapsed cell AND live)

At \(s=W+1\), packed index \(T+r_*=2s\). AND live. Certified \(k\le 6\).

## Killed

Right-edge AND always live: \(t=2\). Collapse for all \(j\): at
\(k=2\), \(W=8U\), \(j=1\), cone-hi \(\neq r_*\). Pair AND XOR \(=0\):
at \(k=4\), \(W=4U\), \(j=4\) gives XOR \(1\).

## Verdict

`LEMMA` (\(m=2U-1-2^j\); collapse iff \(j=0\); right-edge AND iff
\(t\) odd; collapsed AND live).
`KILLED` (AND always live; collapse all \(j\); pair XOR \(0\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ge.md` (this note)
- `research/cycle_ge.py`
- `research/cycle_ge.json`
