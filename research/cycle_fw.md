# Cycle FW: \(G(2^n-1,2^n)=n\bmod 2\); \(G(r,2^a-2)=1\) on \(\{2^a-1-2^j\}\) (and all-ones iff \(a\) odd)

Palindrome sends \(G(2^n-1,2^n-2)\) to \(G(2^n-1,2^n)\). The odd-\(m\)
recursion gives \(G(2^n-1,2^n)=1\oplus G(2^{n-1}-1,2^{n-1})\) with
\(G(1,2)=1\), hence \(n\bmod 2\). Cycle FQ reduces \(G(m,2^a-2)\) to
\(r=m\bmod 2^a\). On \(0\le r<2^a\) the value is 1 iff
\(r=2^a-1-2^j\) for some \(0\le j<a\), or \(r=2^a-1\) with \(a\) odd.
That is a closed form for Cycle FS’s unclipped cone-hi
\(G(m,2U-2)\). Do **not** claim \(G(2^n-1,2^n)=1\) for all \(n\). Do
**not** claim every \(r\) of Hamming weight \(\ge a-1\). Do **not**
claim remainder \(J\) equals the center-AND XOR. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: a bit-pattern for \(G(\cdot,2^a-2)\) does not prove
covering never-fail.

Helper: `python3 research/cycle_fw.py --certify` (~0.01s). Dump:
`research/cycle_fw.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FQ/FS/FV (pattern \(a\le 10\); no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (\(G(2^n-1,2^n)=n\bmod 2\))

Certified \(1\le n\le 16\). Palindrome matches \(G(2^n-1,2^n-2)\).

## Lemma (bit-pattern on \(r<2^a\); FQ reduction)

Certified \(1\le a\le 10\) for the pattern; \(a\le 8\), \(m<5\cdot 2^a\)
for the reduction.

## Killed

\(G(2^n-1,2^n)=1\) for all \(n\): \(G(3,4)=0\). All weight
\(\ge a-1\): \(a=4\), \(r=15\), \(G(15,14)=0\). Remainder \(J\) equals
the center-AND XOR: \(J_6=1\neq 0\) at \(k=4\).

## Verdict

`LEMMA` (\(G(2^n-1,2^n)=n\bmod 2\); bit-pattern; FQ reduction).
`KILLED` (all \(n\); all high weight; \(J=\) center XOR).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_fw.md` (this note)
- `research/cycle_fw.py`
- `research/cycle_fw.json`
