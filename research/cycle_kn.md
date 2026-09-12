# Cycle KN: \(G(3\cdot 2^a-1,d)\) is the AN cube divided by \(1+x+x^2\)

For \(U=2^a\) and \(n=3U-1\),
\(G(n,d)=f(d)\oplus f(d-U)\oplus f(d-3U)\oplus f(d-5U)\oplus f(d-6U)\)
with \(f(t)=1\) iff \(t\ge 0\) and \(t\not\equiv 2\pmod{3}\). The
\(6U\) term vanishes on the row \(d\le 6U-2\). This is **not**
\(f(d)\) alone, **not** the cancelled \(x^{2U}\) freshman term,
**not** Mersenne \(G(2^a-1,d)\), and **not** zeros at
\(\min(j,2n-j)\equiv 2\pmod{3}\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: this is Green-row shape for Cycle KM's
\(3\cdot 2^a-1\) family, not the packed AND XOR \(J\), so covering
never-fail stays open.

Certify: `python3 research/cycle_kn.py --certify`.
Dump: `research/cycle_kn.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/AN/CA/KH/KJ/KM (\(a\le 8\); covering \(k\le 6\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (\(G(3U-1,d)\) from the cube)

Certified \(a\le 8\) (\(n=2,5,11,23,47,95,191,383,767\)). Those rows
have no consecutive zeros. In range the \(6U\) term is identically
\(0\), so \(r\in\{0,1,3,5\}\) matches \(r\in\{0,1,3,5,6\}\).

## Lemma (odd no-\(00\) family)

Cycle KM: odd no-\(00\) iff Mersenne or \(3\cdot 2^k-1\). Covering
\(J_6,J_{10}\) for \(k\le 6\) still has \(G=1\) columns \(22659\);
odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Equals \(f(d)\): \(n=5\), \(d=2\) is \(1\), \(f(2)=0\). Includes
\(x^{2U}\): \(n=5\), \(d=4\) is \(1\) vs \(0\). Equals Mersenne
\(G(2^a-1,d)\): same cell is \(1\) vs \(G_{\mathrm{mersenne}}(1,4)=0\).
Zeros iff \(\min(j,2n-j)\equiv 2\pmod{3}\): \(n=5\), \(d=2\) has
\(G=1\).

## Verdict

`LEMMA` (\(G(3U-1)\) closed form; in-range no \(6U\); odd no-\(00\)
characterization; odd no-\(00\) family).
`KILLED` (equals \(f\); includes \(2U\); equals Mersenne; Mersenne
mod-3 zeros).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_kn.md` (this note)
- `research/cycle_kn.py`
- `research/cycle_kn.json`
