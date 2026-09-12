# Cycle IV: \(G=1\) Green neighbors are the core-slot `IMAGE_ONES` offset

On odd \(n\), \((G(j+1),G(j-1))\) is `SLOT_NEIGH[r,d]` from
`half_run_image`. Even \(n\) and the seed **vanish** to \((0,0)\).
`g1_green4` is that pair as \((g_+,1-g_+,1,1-g_-)\). Even \(G=1\) is
**not** the odd-core \(\mathrm{green4}\). The run-3 middle is **not**
neighbors \(11\). Same \((r,d)\) is **not** parity-independent. Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: slot \(\mathrm{green4}\) still leaves packed AND
on every shape (all four fire), so covering never-fail stays open.

Helper: `SLOT_NEIGH`, `slot_neigh`, `slot_green4`. Certify:
`python3 research/cycle_iv.py --certify` (~0.76s).
Dump: `research/cycle_iv.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IG/IH/IP/IS/IT (\(n<64\); covering \(k\le 6\);
no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (\(G=1\) neighbors are `slot_neigh`)

For \(0\le n<64\), every \(G=1\) has `g_neigh==slot_neigh`. Census
\(n_{G=1}=1344\): odd \(928\), even \(415\), seed \(1\).
`SLOT_NEIGH` matches `half_run_image` on every `IMAGE_ONES` offset.

## Lemma (`g1_green4` is `slot_green4`)

`slot_green4=(g_+,1-g_+,1,1-g_-)`. Algebra shapes: \(1011\) \(371\),
\(1010\) \(141\), \(0110\) \(371\), \(0111\) \(461\) (even, seed, and
odd run-3 middles).

## Lemma (covering slot neighbors)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): \(G=1\) \(22659\),
seed \(14\), shapes \(1011/1010/0110/0111\) =
\(6297/2380/6197/7785\). Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Even \(G=1\) has the odd-core \(\mathrm{green4}\): at \(k=1\),
\(s=7\), \(n=2\), \(j=0\), packed \(0111\) vs core \(1011\),
\(p=12\). Run-3 middle has neighbors \(11\): at \(k=1\), \(s=5\),
\(n=3\), \(j=3\), slot \((0,3,3)\), neighbors \((0,0)\), \(p=6\).
Same \((r,d)\) is parity-independent: at \(k=1\), \(s=7\), \(n=2\),
\(j=2\), slot \((0,1,1)\), even \(0111\) vs odd-slot neighbors
\((1,1)\), \(p=8\).

## Verdict

`LEMMA` (\(G=1\) neighbors are `slot_neigh`; `g1_green4` is
`slot_green4`; covering slot neighbors).
`KILLED` (even \(G=1\) has the odd-core \(\mathrm{green4}\); run-3
middle has neighbors \(11\); same \((r,d)\) is parity-independent).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_iv.md` (this note)
- `research/cycle_iv.py`
- `research/cycle_iv.json`
