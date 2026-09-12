# Cycle KL: Mersenne Green weight is Jacobsthal \(|S_{L+2}|\)

\(a_L=g_{\mathrm{wt}}(2^L-1)\) equals
\(\operatorname{jacobsthal}(L+2)=|S_{L+2}|\) from Cycle AT, so
\(g_{\mathrm{wt}}(n)\) is the product of \(|S_{L+2}|\) over binary
1-runs. \(a_L\) is **not** \(|S_L|\) or \(|S_{L+1}|\).
\(g_{\mathrm{wt}}(n)\) is **not** \(\operatorname{jacobsthal}(n)\)
or \(\operatorname{jacobsthal}(\mathrm{popcount}+2)\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: this identifies Cycle KK's Mersenne weights with
Cycle AT's Jacobsthal sets, not the packed AND XOR \(J\), so covering
never-fail stays open.

Certify: `python3 research/cycle_kl.py --certify`.
Dump: `research/cycle_kl.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AT/CA/KH/KJ/KK (\(n<256\), \(L\le 10\); covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (\(a_L=|S_{L+2}|\))

For \(0\le L\le 10\), \(a_L=\operatorname{jacobsthal}(L+2)=|S_{L+2}|\),
and for \(L\le 8\) this equals \(g_{\mathrm{wt}}(2^L-1)\). Cycle AT's
cardinality \(|S_b|=(2^b-(-1)^b)/3\) is the Mersenne Green weight
shifted by two.

## Lemma (weight is a Jacobsthal product)

For \(n<256\), \(g_{\mathrm{wt}}(n)=\prod\operatorname{jacobsthal}(L+2)\)
over binary ones-runs of \(n\), matching Cycle KK's product.
Covering \(J_6,J_{10}\) for \(k\le 6\) still has \(G=1\) columns
\(22659\); odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

\(a_L=|S_L|\): \(L=3\) has \(a=11\), \(|S_3|=3\).
\(a_L=|S_{L+1}|\): \(L=3\) has \(a=11\), \(|S_4|=5\).
\(g_{\mathrm{wt}}(n)=\operatorname{jacobsthal}(n)\): \(n=7\) has
weight \(11\), \(J_7=43\).
\(g_{\mathrm{wt}}(n)=\operatorname{jacobsthal}(\mathrm{popcount}+2)\):
\(n=5\) has weight \(9\), \(J_4=5\).

## Verdict

`LEMMA` (\(a_L=|S_{L+2}|\); weight is a Jacobsthal product; Cycle KK
run product; Mersenne \(a_L\) closed form).
`KILLED` (\(a_L=|S_L|\); \(a_L=|S_{L+1}|\); \(g_{\mathrm{wt}}(n)=J_n\);
\(g_{\mathrm{wt}}=J_{\mathrm{popcount}+2}\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_kl.md` (this note)
- `research/cycle_kl.py`
- `research/cycle_kl.json`
