# Cycle IR: isolated ones on odd \(n\) are the middle \(1\) of a parent run-3

A length-3 half-run image is \(011010110\); the center \(1\) is
isolated. Every isolated \(G=1\) on odd \(n<64\) (all
\(n\equiv 3\pmod{4}\)) is that middle bit. Even \(n\) isolated ones
are **not** parent run-3. \(n\equiv 1\pmod{4}\) has **no** isolated
ones. Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all
\(k\). Do **not** push the even-spine scan past \(k=18\). Do **not**
bump all \(n_0=16\) past 414990. Do **not** increment consecutive
`11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: isolated-one placement still leaves packed AND on
those columns (and on pairs/triples), so covering never-fail stays
open.

Helper: `isolated_one`, `r3_middle`. Certify:
`python3 research/cycle_ir.py --certify`.
Dump: `research/cycle_ir.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IP/IQ (\(n<64\); covering \(k\le 6\); no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (odd-\(n\) isolated ones are parent run-3 middle)

For odd \(n<64\), every isolated \(G=1\) has `r3_middle`. Census
\(n_{\mathrm{odd}}=45\), all \(n\equiv 3\pmod{4}\). Even \(n\)
isolated ones \(416\) are not parent run-3.

## Lemma (\(n\equiv 1\pmod{4}\) has no isolated ones)

Residue \(1\) isolated-one count \(0\) (only triples).

## Lemma (covering odd-\(n\) isolated ones)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): in-support isolated
ones on odd \(n\) \(741\), all parent run-3 middle, of which AND
\(159\). Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Odd-\(n\) isolated \(1\) is not r3 middle: at \(k=0\), \(s=3\),
\(n=3\), \(j=3\), \(G(3,3)=1\) is the middle of \(G(1)=111\),
\(p=4\). Even-\(n\) isolated \(1\) is r3 middle: at \(k=0\),
\(s=5\), \(n=2\), \(j=0\), \(G(2,0)=1\), \(p=10\).
\(n\equiv 1\pmod{4}\) has an isolated one: at \(k=0\), \(s=3\),
\(n=1\), \(G(1)=111\), \(p=6\).

## Verdict

`LEMMA` (odd-\(n\) isolated ones are parent run-3 middle;
\(n\equiv 1\pmod{4}\) has no isolated ones; covering odd-\(n\)
isolated ones).
`KILLED` (odd-\(n\) isolated \(1\) is not r3 middle; even-\(n\)
isolated \(1\) is r3 middle; \(n\equiv 1\) has an isolated one).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ir.md` (this note)
- `research/cycle_ir.py`
- `research/cycle_ir.json`
