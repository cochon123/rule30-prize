# Cycle KJ: child ones-run count equals parent Green weight

\(n_{\mathrm{runs}}(2m)=n_{\mathrm{runs}}(2m+1)=g_{\mathrm{wt}}(m)\),
and \(g_{\mathrm{wt}}(2m)=g_{\mathrm{wt}}(m)\). Odd child run count
is **not** \(n_{\mathrm{runs}}(m)\). It is **not** \(g_{\mathrm{wt}}\)
of itself. Even double is **not** twice parent runs or twice parent
weight. Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for
all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: this is Green-only freshman arithmetic, not the
packed AND XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_kj.py --certify`.
Dump: `research/cycle_kj.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/IP/KH/KI (\(m<128\); covering \(k\le 6\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (child runs equal parent weight)

For \(m<128\), \(n_{\mathrm{runs}}(2m)=n_{\mathrm{runs}}(2m+1)=g_{\mathrm{wt}}(m)\).
Even stretch copies weight: \(g_{\mathrm{wt}}(2m)=g_{\mathrm{wt}}(m)\).
Odd stretch adds two ones per parent run:
\(g_{\mathrm{wt}}(2m+1)=g_{\mathrm{wt}}(m)+2\cdot n_{\mathrm{runs}}(m)\).

## Lemma (image two pairs, covering clip)

Cycle KI: `half_run_image` contributes exactly 2 consecutive pairs.
Covering \(J_6,J_{10}\) for \(k\le 6\) still has \(G=1\) columns
\(22659\); odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

\(n_{\mathrm{runs}}(2m+1)\) equals \(n_{\mathrm{runs}}(m)\): \(n=3\)
has 3 runs, parent \(n=1\) has 1. Odd \(n_{\mathrm{runs}}\) equals
\(g_{\mathrm{wt}}(n)\): \(n=1\) has 1 run and weight 3.
\(n_{\mathrm{runs}}(2m)\) is twice \(n_{\mathrm{runs}}(m)\): \(n=2\)
has 3 runs, parent has 1. \(g_{\mathrm{wt}}(2m)\) is twice
\(g_{\mathrm{wt}}(m)\): \(n=2\) has weight 3, parent has 3.

## Verdict

`LEMMA` (child runs equal parent weight; even weight copies;
image two pairs; \(n_{\mathrm{pairs}}(2m+1)=2\cdot n_{\mathrm{runs}}(m)\)).
`KILLED` (child runs equal parent runs; odd runs equal own weight;
even runs twice parent; even weight twice parent).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_kj.md` (this note)
- `research/cycle_kj.py`
- `research/cycle_kj.json`
