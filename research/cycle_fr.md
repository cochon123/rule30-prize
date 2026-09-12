# Cycle FR: band lower edge is \(G(m,2m)=1\); \(J_{\mathrm{post}}=J_{\mathrm{mid10}}\oplus\Delta_R\oplus J_{\mathrm{tail}}\)

On Cycle FQ’s unified \(T=2U+W\) right band, the lower index
\(r_{\mathrm{lo}}=2(s-T+W/2+1)\) is the Green corner:
\(W-r_{\mathrm{lo}}=2m\), so \(G(m,W-r_{\mathrm{lo}})=G(m,2m)=1\).
After the clip \(s=U+W\) the upper index is \(r=W\) and
\(G(m,0)=1\). The AND at the lower edge is **not** always live. Splitting
\([6U,18U)\) and using Cycle FJ’s \(\Delta=\Delta_R\) gives

\[
J_{\mathrm{post}}=J_{[6U,10U)\to 10U}\oplus\Delta_R\oplus J_{[10U,18U)\to 18U}.
\]

Do **not** claim the lower-edge AND always fires. Do **not** claim
\(J_{\mathrm{post}}=\Delta_R\). Do **not** claim \(J_{\mathrm{mid10}}=0\).
Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: locating the band corners and splitting
\(J_{\mathrm{post}}\) does not prove covering never-fail.

Helper: `python3 research/cycle_fr.py --certify` (~0.08s). Dump:
`research/cycle_fr.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FF/FH/FJ/FK/FQ (packed split on
\(k=2..5\); no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (lower edge is \(G(m,2m)=1\))

Certified on endpoint samples \(k\le 10\), \(W\in\{4U,8U,16U\}\).
Corners \(G(n,0)=G(n,2n)=1\) from Cycle FK.

## Lemma (after clip, upper edge is \(G(m,0)=1\))

Certified \(k\le 10\).

## Lemma (\(J_{\mathrm{post}}=J_{\mathrm{mid10}}\oplus\Delta_R\oplus J_{\mathrm{tail}}\))

Packed AND XOR on \(2\le k\le 5\). Also \(J_{10}=J_{\mathrm{pre10}}\oplus J_{\mathrm{mid10}}\).

## Killed

Lower-edge AND always live: at \(k=2\), \(W=4U\), 7 of 8 times are
dead. \(J_{\mathrm{post}}=\Delta_R\) fails at the candidate \(k=5\)
(\(J_{\mathrm{post}}=1\), \(\Delta_R=0\)). \(J_{\mathrm{mid10}}=0\)
fails at \(k=4\).

## Verdict

`LEMMA` (lo-edge corner; hi-edge after clip; \(J_{\mathrm{post}}\)
split).
`KILLED` (lo-edge AND always live; \(J_{\mathrm{post}}=\Delta_R\);
\(J_{\mathrm{mid10}}=0\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_fr.md` (this note)
- `research/cycle_fr.py`
- `research/cycle_fr.json`
