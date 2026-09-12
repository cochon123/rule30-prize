# Cycle GR: \(W=8U\) hit-cone AND XOR equals extras XOR, not \(J_{\mathrm{mid10}}\)

On the \(\Delta_R\) / mid10 band \(W=8U\), Cycle GG’s two cone-hi ANDs
cancel (\(Q\) even). The XOR of all \(\mathrm{mer\_one}\) AND over the
two hits is therefore the extras XOR. That is **not** identically 0
and is **not** \(J_{\mathrm{mid10}}\) (\(k=2\): \(1\) vs \(0\); \(k=4\):
\(0\) vs \(1\)). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\)
for all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: showing the hit-time cone XOR is not
\(J_{\mathrm{mid10}}\) does not prove covering never-fail (other
times and columns still contribute).

Helper: `python3 research/cycle_gr.py --certify` (~0.01s). Dump:
`research/cycle_gr.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles CA/FR/GG/GN/GQ (packed \(k\le 6\), \(W=8U\);
\(J_{\mathrm{mid10}}\) from Cycle FR for \(2\le k\le 5\); no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (\(W=8U\) hit-cone XOR = extras XOR)

Certified \(k\le 6\). Cone-hi XOR is \(0\) (\(Q=2\)).

## Killed

Hit-cone XOR identically 0: at \(k=2\), xor \(=1\). Equals
\(J_{\mathrm{mid10}}\): at \(k=2\), \(1\neq 0\); at \(k=4\),
\(0\neq 1\). Extras XOR identically 0: at \(k=2\), xor \(=1\).

## Verdict

`LEMMA` (\(W=8U\) hit-cone XOR = extras XOR; cone-hi XOR \(0\)).
`KILLED` (hit-cone XOR always 0; equals \(J_{\mathrm{mid10}}\);
extras XOR always 0).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_gr.md` (this note)
- `research/cycle_gr.py`
- `research/cycle_gr.json`
