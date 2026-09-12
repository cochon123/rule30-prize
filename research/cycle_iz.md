# Cycle IZ: consecutive \(G=1\) \(\mathrm{green4}\) pair is `slot_kind`

`KIND_GREEN4` sends left to \((1011,1010)\), right to \((1010,0110)\),
iso to \((1011,0110)\). That equals `g11_green4` and the
`slot_green4` pair. Iso is **not** the left shape. Left second is
**not** \(0110\). Right first is **not** \(1011\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: kind \(\mathrm{green4}\) still leaves packed AND
on every pair (all three kinds fire all four AND patterns), so
covering never-fail stays open.

Helper: `KIND_GREEN4`, `kind_green4`. Certify:
`python3 research/cycle_iz.py --certify`.
Dump: `research/cycle_iz.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IJ/IN/IV/IX (\(n<64\); covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (pair \(\mathrm{green4}\) is `kind_green4`)

For \(n<64\), every consecutive \(G=1\) pair has
`g11_green4==kind_green4==KIND_GREEN4[slot_kind]`. Census
\(n_{11}=512\): left \(141\), right \(141\), iso \(230\).

## Lemma (the three `KIND_GREEN4` shapes)

Left \((1011,1010)\), right \((1010,0110)\), iso \((1011,0110)\).
These are the Cycle IJ neighbor shapes with
\((g_-,g_{+2})=(0,1),(1,0),(0,0)\).

## Lemma (covering kind \(\mathrm{green4}\))

Packed covering \(J_6,J_{10}\) for \(k\le 6\): in-support pairs
\(8577\) (left \(2380\), right \(2380\), iso \(3817\)). Odd-\(s\)
\(J\) XOR matches Cycles HF/HG.

## Killed

Iso has the left \(\mathrm{green4}\): at \(k=1\), \(s=5\), \(n=3\),
\(j=0\), shape \((1011,0110)\), \(p=12\). Left second is \(0110\):
at \(k=0\), \(s=3\), \(n=1\), \(j=0\), second \(1010\), \(p=6\).
Right first is \(1011\): at \(k=1\), \(s=9\), \(n=1\), \(j=1\),
first \(1010\), \(p=10\).

## Verdict

`LEMMA` (pair \(\mathrm{green4}\) is `kind_green4`; the three
`KIND_GREEN4` shapes; covering kind \(\mathrm{green4}\)).
`KILLED` (iso has the left \(\mathrm{green4}\); left second is
\(0110\); right first is \(1011\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_iz.md` (this note)
- `research/cycle_iz.py`
- `research/cycle_iz.json`
