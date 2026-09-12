# Cycle GN: \(G(2^k-1,f)=1\) iff \(f\not\equiv 2\pmod{3}\) on \(0\le f<2^k\)

Mersenne Green on the low interval \([0,U)\) is the period-3 bit
\(f\not\equiv 2\pmod{3}\). The ones-count is
\((2U+1+(k\bmod 2))/3\), matching Cycle GK. The rule **fails** at
\(f=U\) (Cycle FW: \(G(U-1,U)=k\bmod 2\)). It is **not** “\(f\) even”
and **not** “\(f\not\equiv 1\pmod{3}\)”. Last-hit even-\(r\) Green
palindromes onto this interval. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: a mod-3 rule for low Mersenne Green does not prove
covering never-fail (AND still selects a proper subset; pre-cone hits
are not the Mersenne clock).

Helper: `python3 research/cycle_gn.py --certify` (~0.01s). Dump:
`research/cycle_gn.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FW/GK/GM (Mersenne \(k\le 12\); last
hit \(k\le 11\); no Fermat table, no extra window, no \(n_0=16\)
window).

## Lemma (\(G(2^k-1,f)=1\) iff \(f\not\equiv 2\pmod{3}\) on \([0,2^k)\))

Certified \(0\le k\le 12\). Ones-count matches Cycle GK.

## Lemma (last-hit palindromes onto the low interval)

At \(q=Q-1\), even-\(r\) Green equals \(G(U-1,f)\) for
\(f=2U-2-(W/2-r/2)\in[0,U)\), hence the mod-3 bit. Certified
\(k\le 11\).

## Killed

Rule at \(f=U\): \(k=1\), \(G(1,2)=1\) but \(2\equiv 2\pmod{3}\).
Iff \(f\) even: \(k=1\), \(f=1\), \(G=1\). Iff \(f\not\equiv 1\pmod{3}\):
same \(f=1\).

## Verdict

`LEMMA` (mod-3 bit on \([0,U)\); last-hit palindrome).
`KILLED` (rule at \(f=U\); iff even; iff \(\not\equiv 1\pmod{3}\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_gn.md` (this note)
- `research/cycle_gn.py`
- `research/cycle_gn.json`
