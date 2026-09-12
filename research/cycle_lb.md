# Cycle LB: covering FRESH \(1001\) AND xor is \(J\) xor \(1_{q=6,\,k\equiv 2\pmod{4}}\)

On covering \(J_6,J_{10}\) for \(k\le 6\), the XOR of packed AND
pattern \(1001\) on \(G=1\) equals \(J\) except when \(q=6\) and
\(k\equiv 2\pmod{4}\), where it flips. This is **not** equal to \(J\),
**not** a remainder on all even \(k\), **not** all \(q=6\), and
**not** only \(k=2\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: this is a two-walk correction to one FRESH
pattern, not a Green-only formula for packed AND XOR \(J\), so
covering never-fail stays open.

Certify: `python3 research/cycle_lb.py --certify` (~0.22s).
Dump: `research/cycle_lb.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HG/HH/HI/HU/KH/LA (covering \(k\le 6\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (\(1001\) AND xor remainder)

Certified \(k\le 6\). Flips at \((k,q)=(2,6)\) (\(n_{1001}=5\)) and
\((6,6)\). Covering \(J_6,J_{10}\) still have \(G=1\) columns
\(22659\); odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Lemma (tri specials from Mersenne unique)

Cycle LA. The three specials of \(G(3U-1)\) are the Mersenne unique
at \(U-1\), the centre, and the palindrome dual.

## Killed

Equal to \(J\): \(k=2\), \(q=6\) is \(1\) vs \(J=0\). All even \(k\):
\(k=4\), \(q=6\) rem \(0\). All \(q=6\): \(k=0\) rem \(0\). Only
\(k=2\): \(k=6\), \(q=6\) rem \(1\).

## Verdict

`LEMMA` (\(1001\) AND xor remainder; tri specials from Mersenne
unique; tri three isolated ones iff \(a\) even).
`KILLED` (equals \(J\); all even \(k\); all \(q=6\); only \(k=2\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_lb.md` (this note)
- `research/cycle_lb.py`
- `research/cycle_lb.json`
