# Cycle KO: piecewise residues for \(G(3\cdot 2^a-1,d)\)

For \(U=2^a\) and \(n=3U-1\) Cycle KN's XOR splits by bands:
\(d<U\) is \(1\) iff \(d\not\equiv 2\pmod{3}\); \(U\le d<3U\) is \(1\)
iff \(d\not\equiv (1\text{ if }a\text{ even else }0)\pmod{3}\);
\(3U\le d<5U\) is \(f(d-U)\); \(d\ge 5U\) is the middle-band rule at
\(d-U\). This is **not** the low-band rule on the whole row, **not**
forbid \(2\) on the middle band, **not** \(f(d)\) on \([3U,5U)\),
and **not** \(d\bmod 3\) on the high band. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: this is a residue rewrite of Cycle KN, not the
packed AND XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_ko.py --certify`.
Dump: `research/cycle_ko.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/AN/CA/KH/KN (\(a\le 8\); covering \(k\le 6\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (piecewise residues)

Certified \(a\le 8\). Matches \(G\), `g_tri`, and `g_tri_row`.

## Lemma (\(G(3U-1)\) closed form)

Cycle KN: XOR of \(f(d-rU)\) over \(r\in\{0,1,3,5,6\}\). Covering
\(J_6,J_{10}\) for \(k\le 6\) still has \(G=1\) columns \(22659\);
odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Whole row \(\not\equiv 2\pmod{3}\): \(n=5\), \(d=2\) is \(1\). Middle
band zeros at \(\equiv 2\): same cell. Band \([3U,5U)\) equals
\(f(d)\): \(n=5\), \(d=7\) is \(0\) vs \(f(7)=1\). High band uses
\(d\bmod 3\): \(n=11\), \(d=20\) is \(0\) vs \(1\).

## Verdict

`LEMMA` (piecewise residues; \(G(3U-1)\) closed form; in-range no
\(6U\)).
`KILLED` (whole row \(\not\equiv 2\); middle forbid \(2\); band
\(f(d)\); high \(d\bmod 3\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ko.md` (this note)
- `research/cycle_ko.py`
- `research/cycle_ko.json`
