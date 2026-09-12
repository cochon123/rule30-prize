# Cycle IP: ones-runs on \(m\) lift to a closed dictionary on \(n=2m+1\)

Freshman sends a length-\(r\) ones-run to `half_run_image(r)`:
\(r=1\mapsto 01110\), \(r=2\mapsto 0110110\),
\(r=3\mapsto 011010110\) (flanking zeros included). Run-2 does **not**
lift to a triple. Run-3 on \(m\) does **not** lift to one run-3 on
\(n\). Run-1 is **not** an isolated pair. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: the run dictionary still leaves packed AND on
odd-\(n\) Green pairs and triples, so covering never-fail stays open.

Helper: `half_run_image`, `g_runs`. Certify:
`python3 research/cycle_ip.py --certify`.
Dump: `research/cycle_ip.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IN/IO (\(n<64\); covering \(k\le 6\); no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (half-run dictionary)

For \(m<32\), every ones-run of \(G(m)\) of length \(r\in\{1,2,3\}\)
lifts to `half_run_image(r)` on \(n=2m+1\). Census: run-1 \(141\),
run-2 \(70\), run-3 \(45\), total \(256\).

## Lemma (odd-\(n\) run-3 comes from run-1 on \(m\))

Every run-3 for odd \(n<64\) starts at even \(j=2k\) with a length-1
run of \(G(n//2)\) at \(k\). Census \(n_{\mathrm{run3}}=141\).

## Lemma (covering clocks obey the dictionary)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): unique-clock runs on
\(m=n//2\) lift as run-1 \(2818\), run-2 \(1402\), run-3 \(873\).
In-support consecutive \(G=1\) \(8577\). Odd-\(s\) \(J\) XOR matches
Cycles HF/HG.

## Killed

Run-2 lifts to a triple: at \(k=1\), \(s=5\), \(n=7\), \(m=3\),
image \(0110110\), `g_run_kind` iso, \(p=20\). Run-3 on \(m\) lifts
to one run-3 on \(n\): at \(k=0\), \(s=3\), \(n=3\), image
\(011010110\), \(G(3)=1101011\), \(p=10\). Run-1 image is an
isolated pair \(0110\): at \(k=0\), \(s=3\), \(n=1\), image
\(01110\), `g_run_kind` left, \(p=6\).

## Verdict

`LEMMA` (half-run dictionary; odd-\(n\) run-3 comes from run-1 on
\(m\); covering clocks obey the dictionary).
`KILLED` (run-2 lifts to a triple; run-3 on \(m\) lifts to one run-3
on \(n\); run-1 image is an isolated pair).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ip.md` (this note)
- `research/cycle_ip.py`
- `research/cycle_ip.json`
