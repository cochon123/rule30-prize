# Cycle KI: \(\mathrm{half\_run\_image}\) contributes exactly 2 pairs

Every parent ones-run lifts to two consecutive \(G=1\) pairs, so
\(n_{\mathrm{pairs}}(2m+1)=2\cdot n_{\mathrm{runs}}(m)\). Run
counts lift as \(n_{\mathrm{run3}}(2m+1)=n_{\mathrm{run1}}(m)\),
\(n_{\mathrm{run1}}(2m+1)=n_{\mathrm{run3}}(m)\),
\(n_{\mathrm{run2}}(2m+1)=2(n_{\mathrm{run2}}(m)+n_{\mathrm{run3}}(m))\).
Even \(n\) has \(n_{\mathrm{pairs}}=0\). The image does **not** have
0 pairs. Odd \(n_{\mathrm{pairs}}\) is **not** \(n_{\mathrm{runs}}(m)\).
Odd run-3 is **not** from parent run-2. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: this is the freshman mechanism for Cycle KH's
even pair count, not the packed AND XOR \(J\), so covering
never-fail stays open.

Certify: `python3 research/cycle_ki.py --certify` (~0.17s).
Dump: `research/cycle_ki.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/IP/KH (\(m<128\); covering \(k\le 6\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (image contributes exactly 2 pairs)

`half_run_image(r)` for \(r\in\{1,2,3\}\) has exactly two consecutive
ones-pairs: \(01110\), \(0110110\), \(011010110\). For \(m<128\),
every parent run lifts by that dictionary, and
\(n_{\mathrm{pairs}}(2m+1)=2\cdot n_{\mathrm{runs}}(m)\). Even
\(n<256\) has \(n_{\mathrm{pairs}}=0\).

## Lemma (run counts lift)

For \(m<128\), \(n=2m+1\):
\(n_{\mathrm{run3}}(n)=n_{\mathrm{run1}}(m)\),
\(n_{\mathrm{run1}}(n)=n_{\mathrm{run3}}(m)\),
\(n_{\mathrm{run2}}(n)=2(n_{\mathrm{run2}}(m)+n_{\mathrm{run3}}(m))\).
Covering \(J_6,J_{10}\) for \(k\le 6\) still has \(G=1\) columns
\(22659\); odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Image has 0 consecutive pairs: \(r=1\) is \(01110\) with 2 pairs.
\(n_{\mathrm{pairs}}(2m+1)\) equals \(n_{\mathrm{runs}}(m)\): \(n=1\)
has 2 pairs from 1 parent run. Even \(n\) has consecutive pairs:
\(n=2\) has three isolated ones and \(n_{\mathrm{pairs}}=0\). Odd
run-3 comes from parent run-2: \(n=5\) has 3 triples from 3 parent
run-1s (\(n_{\mathrm{run2}}(2)=0\)).

## Verdict

`LEMMA` (image contributes exactly 2 pairs;
\(n_{\mathrm{pairs}}(2m+1)=2\cdot n_{\mathrm{runs}}(m)\); row-XOR of
\(\mathrm{green4}\) is \(0111\); covering clip XOR of
\(\mathrm{green4}\)).
`KILLED` (image has 0 pairs; \(n_{\mathrm{pairs}}=n_{\mathrm{runs}}\);
even \(n\) has pairs; run-3 from run-2).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ki.md` (this note)
- `research/cycle_ki.py`
- `research/cycle_ki.json`
