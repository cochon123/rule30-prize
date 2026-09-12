# Cycle HL: odd-\(s\) Green 4-slot is \((0,G(n,j+1),0,G(n,j))\)

On covering \((n,j)\), odd-\(s\) Green at packed bits
\(p-3,\ldots,p\) (\(\rho=2j+3,\ldots,2j\)) is
\(\mathrm{odd\_green4}(n,j)=(0,\,G(n,j+1),\,0,\,G(n,j))\). Copy
slots vanish; coboundary slots copy \(G(n,j+1)\) and \(G(n,j)\).
Dual of Cycle HJ `green4`. The odd-\(s\) 4-tuple is **not** that
Green 4-tuple. `odd_green4` is **not** even-\(s\) `green4`. Odd-\(s\)
Green does **not** vanish on coboundary slots. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: the odd-\(s\) Green 4-slot is not a closed form
for the row along Green ones, so covering never-fail stays open.

Helper: `odd_green4`. Certify: `python3 research/cycle_hl.py --certify` (~0.09s).
Dump: `research/cycle_hl.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles AL/CA/GU/HF/HG/HJ/HK
(algebra \(n<64\); covering \(k\le 6\); no Fermat table, no extra
window, no \(n_0=16\) window).

## Lemma (odd-\(s\) Green 4-slot \(=\) `odd_green4`)

\(G(2n,2j+r)\) for \(r=0,1,2,3\): even \(m=2n\) kills odd \(\rho\),
and even \(\rho\) copies \(G(n,j)\) / \(G(n,j+1)\). Certified
algebraically \(n<64\), and on \(J_6,J_{10}\) for \(k\le 6\). Copy
slots vanish. Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Odd-\(s\) 4-tuple \(=\) `odd_green4`: at \(k=0\), \(s=3\), \(n=1\),
\(j=0\), \(p=6\), tuple \(1111\) vs Green \(0101\). `odd_green4` \(=\)
even-\(s\) `green4`: same \((n,j)\), \(0101\neq 1011\). Odd-\(s\) Green
vanishes on coboundary slots: those slots are \(1\) at the same
point.

## Verdict

`LEMMA` (odd-\(s\) Green 4-slot; copy slots vanish).
`KILLED` (odd-\(s\) 4-tuple \(=\) `odd_green4`; `odd_green4` \(=\)
`green4`; odd-\(s\) Green vanishes on coboundary slots).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_hl.md` (this note)
- `research/cycle_hl.py`
- `research/cycle_hl.json`
