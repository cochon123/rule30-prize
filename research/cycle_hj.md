# Cycle HJ: fresh AND occupies even-\(s\) Green copy/cob slots

On covering \((n,j)\), even-\(s\) Green at packed bits
\(p-3,\ldots,p\) (\(\rho=2j+3,\ldots,2j\)) is
\((G(n,j+1),\,G(n,j+1)\oplus G(n,j),\,G(n,j),\,G(n,j)\oplus G(n,j-1))\).
Fresh \(0010\) occupies only the copy(\(j\)) slot; \(0100\) occupies
only cob(\(j+1\)); \(1001\) occupies copy(\(j+1\)) and cob(\(j\)).
The even-\(s\) 4-tuple is **not** that Green 4-tuple. Fresh \(0010\)
is **not** only on \(G(n,j)=1\). Fresh \(0100\) is **not** only on
cob(\(j+1\))=1. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: naming the Green slots the three fresh patterns
occupy does not give a closed form for the row 4-tuple along Green
ones, so covering never-fail stays open.

Helper: `green4` / `FRESH_SLOT` / `SLOT_NAMES`. Certify:
`python3 research/cycle_hj.py --certify`. Dump:
`research/cycle_hj.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/GU/HF/HG/HH/HI (algebra \(n<64\);
covering \(k\le 6\); no Fermat table, no extra window, no \(n_0=16\)
window).

## Lemma (even-\(s\) Green 4-slot \(=\) `green4`)

\(G(2n+1,2j+r)\) for \(r=0,1,2,3\) is the coboundary/copy pair from
Cycle GY. Certified algebraically \(n<64\), and on \(J_6,J_{10}\)
for \(k\le 6\). Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Lemma (fresh occupation)

\(0010\) occupies only copy(\(j\)); \(0100\) occupies only
cob(\(j+1\)); \(1001\) occupies copy(\(j+1\)) and cob(\(j\)).
Continuation \(0011\) occupies copy(\(j\)) and cob(\(j\)).

## Killed

4-tuple \(=\) Green 4-tuple: at \(k=0\), \(s=2\), \(n=1\), \(j=0\),
\(p=6\), tuple \(0100\) vs Green \(1011\). Fresh \(0010\) only on
\(G=1\): at \(k=1\), \(s=7\), \(n=2\), \(j=1\), \(p=10\), \(G=0\).
Fresh \(0100\) only on cob(\(j+1\))=1: at \(k=0\), \(s=3\), \(n=1\),
\(j=0\), \(p=6\), cob=0 and \(G=1\).

## Verdict

`LEMMA` (even-\(s\) Green 4-slot; fresh \(0010\) occupies copy(\(j\));
\(0100\) occupies cob(\(j+1\)); \(1001\) occupies copy(\(j+1\))+cob(\(j\))).
`KILLED` (4-tuple \(=\) Green 4-tuple; \(0010\) only on \(G=1\);
\(0100\) only on cob(\(j+1\))=1).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_hj.md` (this note)
- `research/cycle_hj.py`
- `research/cycle_hj.json`
