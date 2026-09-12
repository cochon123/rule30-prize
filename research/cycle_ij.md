# Cycle IJ: Green has no 4-run of ones; consecutive \(G=1\) \(\mathrm{green4}\) is 3-shaped

\(G(n,\cdot)\) ones-runs have length \(1\), \(2\), or \(3\) only
(\(n<64\)). Consecutive \(G=1\) never has both outer neighbors \(1\),
so \(\mathrm{green4}(n,j)=(1,0,1,1-G(j-1))\) and
\(\mathrm{green4}(n,j+1)=(G(j+2),1-G(j+2),1,0)\) with
\((G(j-1),G(j+2))\in\{(0,0),(0,1),(1,0)\}\). Green **does** have
run-3. Consecutive \(G=1\) is **not** always an isolated pair.
Consecutive \(G=1\) \(\mathrm{green4}\) is **not** always the
isolated-pair shape \((1011,0110)\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: no Green 4-run still leaves packed AND on Green
pairs and triples, so covering never-fail stays open.

Helper: `g11_green4`. Certify:
`python3 research/cycle_ij.py --certify`.
Dump: `research/cycle_ij.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HJ/HU/II (\(n<64\); covering \(k\le 6\); no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (Green has no 4-run of ones)

For \(n<64\), ones-runs of \(G(n,\cdot)\) are length \(1,2,3\) only.
Census: run-1 \(461\), run-2 \(230\), run-3 \(141\), run-\(\ge 4\)
\(0\). Consecutive \(G=1\) pairs \(512\), never
\((G(j-1),G(j+2))=(1,1)\).

## Lemma (consecutive \(G=1\) \(\mathrm{green4}\) is 3-shaped)

On \(G(n,j)=G(n,j+1)=1\),
`g11_green4` equals \(((1,0,1,1-g_-),(g_{+2},1-g_{+2},1,0))\).
The three neighbor classes are isolated pair \((0,0)\), left of a
triple \((0,1)\), and right of a triple \((1,0)\).

## Lemma (covering consecutive \(G=1\) \(\mathrm{green4}\))

Packed covering \(J_6,J_{10}\) for \(k\le 6\): consecutive \(G=1\)
\(8577\) (isolated \(3817\), left \(2380\), right \(2380\)), both-AND
\(463\). Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Green has no run of \(3\): at \(k=0\), \(s=3\), \(n=1\),
\(G(1)=(1,1,1)\). Consecutive \(G=1\) always isolated: same witness,
\((g_-,g_{+2})=(0,1)\). Consecutive \(G=1\) \(\mathrm{green4}\) always
\((1011,0110)\): same witness, \(1011\) vs \(1010\).

## Verdict

`LEMMA` (Green has no 4-run of ones; consecutive \(G=1\)
\(\mathrm{green4}\) is 3-shaped; covering consecutive \(G=1\)
\(\mathrm{green4}\)).
`KILLED` (Green has no run of \(3\); consecutive \(G=1\) always
isolated; consecutive \(G=1\) \(\mathrm{green4}\) always
\((1011,0110)\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ij.md` (this note)
- `research/cycle_ij.py`
- `research/cycle_ij.json`
