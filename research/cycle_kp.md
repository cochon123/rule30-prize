# Cycle KP: \(G(2^a-1)\) is a prefix of \(G(3\cdot 2^a-1)\)

For \(0\le d\le 2^{a+1}-2\),
\(G(2^a-1,d)=G(3\cdot 2^a-1,d)\). That is the full Mersenne row,
not only \(d<2^a\). The rows are **not** equal, the prefix is **not**
\(G(2^{a+1}-1)\) or Fermat \(G(2^a+1)\), and the middle of
\(3\cdot 2^a-1\) is **not** Mersenne. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: this embeds Cycle KM's two no-\(00\) families,
not the packed AND XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_kp.py --certify` (~0.13s).
Dump: `research/cycle_kp.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/KH/KO (\(a\le 8\); covering \(k\le 6\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (Mersenne prefix)

Certified \(a\le 8\). Matches \(G(2^a-1,d)\), \(G(3\cdot 2^a-1,d)\),
and Cycle KO's piecewise form on \(0\le d\le 2^{a+1}-2\). The suffix
of length \(2^{a+1}-1\) equals the same Mersenne row by palindrome.

## Lemma (piecewise residues)

Cycle KO: residue bands for \(G(3U-1)\). Covering \(J_6,J_{10}\) for
\(k\le 6\) still has \(G=1\) columns \(22659\); odd-\(s\) \(J\) XOR
matches Cycles HF/HG.

## Killed

The two rows are equal: \(n=5\), \(d=4\) is \(1\) vs \(G(1,4)=0\).
Prefix is next Mersenne \(G(2^{a+1}-1)\): \(G(5,2)=1\) vs
\(G(3,2)=0\). Prefix is Fermat \(G(2^a+1)\): \(G(11,2)=0\) vs
\(G(5,2)=1\). Middle of \(3\cdot 2^a-1\) is Mersenne: \(G(5,3)=0\)
vs \(G(1,0)=1\).

## Verdict

`LEMMA` (Mersenne prefix; piecewise residues; \(G(3U-1)\) closed
form).
`KILLED` (full rows equal; next Mersenne; Fermat; middle Mersenne).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_kp.md` (this note)
- `research/cycle_kp.py`
- `research/cycle_kp.json`
