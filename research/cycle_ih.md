# Cycle IH: dual \(j\mapsto 2n-j\) swaps the Green neighbors of a \(G=1\) column

\(G(n,j_2+1)=G(n,j-1)\) and \(G(n,j_2-1)=G(n,j+1)\) at \(j_2=2n-j\).
On \(G=1\), dual \(\mathrm{green4}\) is \((g_-,1-g_-,1,1-g_+)\). Cycle
IG's slot formula on that 4-tuple matches the dual packed AND.
Dual does **not** preserve neighbor order. Dual \(\mathrm{green4}\)
is **not** the primal 4-tuple (nor its bit-reverse). Dual \(G=1\)
AND xor is **not** identically 0. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: dual error slots are not a function of the primal
slots, so a Green-only discrepancy formula stays open.

Helper: `g_neigh`, `g1_green4_swap`. Certify:
`python3 research/cycle_ih.py --certify` (~0.13s).
Dump: `research/cycle_ih.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/HX/IG (\(n<64\); covering \(k\le 6\); no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (dual swaps Green neighbors)

For \(n<64\) and \(0\le j\le 2n\),
`g_neigh(n,j2)==(g_-,g_+)` with \((g_+,g_-)=\)`g_neigh(n,j)`.
At \(j=n\), \(G(n,n+1)=G(n,n-1)\). Census \(n_{\mathrm{ok}}=2016\).

## Lemma (dual \(G=1\) \(\mathrm{green4}\) is the swapped neighborhood)

On \(G=1\), `g1_green4(n,j2)==g1_green4_swap(n,j)`, equal to
\((g_-,1-g_-,1,1-g_+)\). This is not `reverse_four` of the primal
green4.

## Lemma (covering dual AND xor matches Cycle IG slots)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): in-support pairs
\(8944\), AND xor \(3246\). Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Dual preserves \((g_+,g_-)\): at \(k=0\), \(s=7\), \(n=1\), \(j=0\)
vs \(2\), fours \(0010\) vs \(0100\), \((g_+,g_-)=(1,0)\) vs
\((0,1)\). Dual \(\mathrm{green4}\) equals primal (or reverse): same
witness, primal \(1011\), dual \(0110\), reverse \(1101\). Dual
\(G=1\) AND xor identically \(0\): at \(k=1\), \(s=5\), \(n=7\),
\(j=6\) vs \(8\), fours \(0001\) vs \(1001\), xor \(1\).

## Verdict

`LEMMA` (dual swaps Green neighbors; dual \(G=1\) \(\mathrm{green4}\)
is the swapped neighborhood; covering dual AND xor matches Cycle IG
slots).
`KILLED` (dual preserves \((g_+,g_-)\); dual \(\mathrm{green4}\)
equals primal; dual \(G=1\) AND xor identically \(0\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ih.md` (this note)
- `research/cycle_ih.py`
- `research/cycle_ih.json`
