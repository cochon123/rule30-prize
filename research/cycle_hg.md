# Cycle HG: \(J_{10}\) and \(J_{18}\) are the in-support \(j\)-index from time \(2U\)

Cycle HF put \(J_6\) on \([2U,6U)\) with \(Q=2\). The other covering
remainders are the same clock: \(J_{10}\) on \([2U,10U)\) with \(Q=4\),
\(J_{18}\) on \([2U,18U)\) with \(Q=8\), left-clipped for
\(s<T/2-1\). Splits recover FR: \(J_{\mathrm{pre10}}\oplus J_{\mathrm{mid10}}=J_{10}\),
and \(J_{18}\) parts are \(J_6\), \(J_{\mathrm{mid10}}\oplus\Delta_R\),
\(J_{\mathrm{tail}}\). The mid10 XOR is **not** \(J_{10}\) (\(k=2\):
\(0\) vs \(1\)). The tail XOR is **not** \(J_{18}\) (\(k=2\): \(1\) vs
\(0\)). The \(J_{10}\) window is **not** unclipped full Green. Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: writing all three covering \(J_q\) as
\(G\cdot\mathrm{AND}\) forms does not give a closed form for packed
AND, so covering never-fail stays open.

Helper: `J10_WINDOW` / `J18_WINDOW` / `covering_Q`. Certify:
`python3 research/cycle_hg.py --certify` (~0.77s). Dump:
`research/cycle_hg.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FR/FH/GU/HC/HF (packed \(k\le 6\);
algebra \(k\le 12\); no Fermat table, no extra window, no \(n_0=16\)
window).

## Lemma (\(J_{10}=\) in-support \(j\)-index \(Q=4\); \(J_{18}\) with \(Q=8\))

Certified \(k\le 6\). Odd \(s\) enumerates \(n\in[0,UQ)\). Clip length
\(U(q/2-2)-1\).

## Lemma (left clip \(s<qU/2-1\); first unclipped has \(\mathrm{lo}=0\))

Certified \(k\le 12\), \(q=10,18\). After clip, \(T-\mathrm{lo}=2m\).

## Killed

mid10 XOR \(=J_{10}\): at \(k=2\), \(0\neq 1\). Tail XOR \(=J_{18}\):
at \(k=2\), \(1\neq 0\). Unclipped full Green on the \(J_{10}\)
window: at \(k=2\), \(s=t_0\), width \(41\neq 63\).

## Verdict

`LEMMA` (\(J_{10}=\) \(j\)-index \(Q=4\); \(J_{18}=\) \(j\)-index
\(Q=8\); left clip \(s<5U-1\) / \(s<9U-1\)).
`KILLED` (mid10 \(=J_{10}\); tail \(=J_{18}\); unclipped full Green).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_hg.md` (this note)
- `research/cycle_hg.py`
- `research/cycle_hg.json`
