# Cycle TJ: residue time APs 2-fold as interleaved 16-APs

At \(k\ge 1\), even children of parent \(n\equiv r\pmod{4}\) have
times the 16-AP \(2\mathrm{lo}+1,\ldots,2\mathrm{hi}+1\) and land
on child residue \(2r\bmod 4\). Odd children have times
\(2\mathrm{lo}-1,\ldots,2\mathrm{hi}-1\) on residue
\(2r+1\bmod 4\). Each child residue AP is the interleaving of those
two parent 16-APs. Pal-center tot does **not** 2-fold by residue
(dies at \(k=3\)). Do **not** claim residue pal-center tot
2-folds. Do **not** claim cellwise spat 2-fold. Do **not** claim
pal-center tot equals \(S\oplus T\). This is **not** rest
\(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
catalogue leftover \(p\) one-by-one. Do **not** catalogue leftover
\(d\). Do **not** catalogue further \(S\)/\(T\) subregions unless
the experiment answers why \(E_k=0\). Do **not** claim pal-left
leftover xor vanishes for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_tj.py --certify` (~0.14s).
Dump: `research/cycle_tj.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/OJ/PB/QV/SO/SV/SX/SY/SZ/TD/TH/TI (residue time APs
2-fold as interleaved 16-APs; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (even/odd child times of a residue AP are a 16-AP)

Parent times \(t=\mathrm{lo}+8j\). Even-child times are
\(2t+1=2\mathrm{lo}+1+16j\); odd-child times are
\(2t-1=2\mathrm{lo}-1+16j\). Even children land on
\(n\equiv 2r\pmod{4}\); odd children on \(n\equiv 2r+1\pmod{4}\).
Status: **lemma**. Algebra through \(k\le 64\); census through
\(k\le 12\).

## Lemma (each child residue AP interleaves two parent 16-APs)

Child residue \(0\) is even children of parent residues \(0,2\);
residue \(1\) is odd children of \(0,2\); residue \(2\) is even
children of \(1,3\); residue \(3\) is odd children of \(1,3\).
Each source contributes \(2^{k-1}\) times, filling the \(2^k\)
points of the child 8-AP. This is Cycle TH's odd-child origin of
\(n\equiv 1\pmod{4}\) in time language (odd children of all even
covering clocks). Status: **lemma**. Algebra through \(k\le 64\);
set equality through \(k\le 12\). **Killed:** pal-center tot on a
child residue equals the xor of pal-center tots on the parent
sources (dies at \(k=3\)).

## Verdict

`LEMMA` (even/odd child times of a residue AP are a 16-AP; each
child residue AP interleaves two parent 16-APs).
`CERTIFIED` (census through \(k\le 12\); pal-tot counterexample at
\(k=3\); \(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (residue pal-center tot 2-folds; pal-center tot on a
residue identically \(0\); cellwise spat 2-fold; pal-center tot
equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_tj.md` (this note)
- `research/cycle_tj.py`
- `research/cycle_tj.json`
