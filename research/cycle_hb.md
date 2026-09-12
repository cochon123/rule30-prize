# Cycle HB: \(W=16U\) unified-band XOR is \(\Delta^{(16)}_R\), not \(J_{\mathrm{tail}}\)

Cycles GZ/HA put that band in the \(j\)-index. Remainder Green to
\(18U\) vanishes on \(p>18U\), so \(J_{\mathrm{tail}}\) is in-support;
the right strip is the \(16U\)-shift \(\Delta\) toward \(34U\) (dual of
FL/FN). \(\Delta^{(16)}_R\) is **not** \(J_{\mathrm{tail}}\) (\(k=2\):
\(0\) vs \(1\)) and is **not** \(\Delta_R\) (\(k=2\): \(0\) vs \(1\)).
Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: identifying the \(W=16U\) band with
\(\Delta^{(16)}_R\) does not prove covering never-fail
(\(J_{\mathrm{tail}}\) is a different XOR; AND still has no closed
form). The GZ/HA \(j\)-index on \(W=16U\) is therefore a formula for
\(\Delta^{(16)}_R\), not for \(J_{\mathrm{tail}}\).

Helper: `_walk16` in this file. Certify:
`python3 research/cycle_hb.py --certify` (~0.2s). Dump:
`research/cycle_hb.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FL/FO/FR/HA (packed \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (\(\Delta^{(16)}_R=\) \(W=16U\) band XOR)

Certified \(k\le 6\). Outside the cone/Green band those \(34U\)-Greens
vanish. Unified \(G(m,W-r)\) matches. \(J_{\mathrm{tail}}\) agrees
with Cycle FR on \(k=2..5\).

## Killed

Equals \(J_{\mathrm{tail}}\): at \(k=2\), \(0\neq 1\). Identically 0:
at \(k=3\), xor \(=1\). Equals \(\Delta_R\): at \(k=2\), \(0\neq 1\).

## Verdict

`LEMMA` (\(W=16U\) band XOR \(=\Delta^{(16)}_R\)).
`KILLED` (\(\Delta^{(16)}_R=J_{\mathrm{tail}}\); \(\Delta^{(16)}_R=0\);
\(\Delta^{(16)}_R=\Delta_R\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_hb.md` (this note)
- `research/cycle_hb.py`
- `research/cycle_hb.json`
