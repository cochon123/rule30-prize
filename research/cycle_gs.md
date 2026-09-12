# Cycle GS: all covering \(W\), hit-cone XOR = extras XOR \(\oplus(Q\bmod 2)\)

Cycle GR was the even-\(Q\) (\(W=8U\)) case. Cone-hi AND is live on
every hit (GQ), so hi XOR \(=Q\bmod 2\) (GG) and the \(\mathrm{mer\_one}\)
AND XOR over hits is extras XOR \(\oplus(Q\bmod 2)\). Equals extras
XOR iff \(Q\) is even. On \(W=4U\) extras are still only lo through
\(k=4\), **not** at \(k=5\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: reducing the hit-time cone XOR to extras XOR
plus \(Q\bmod 2\) does not prove covering never-fail (other times
and columns still contribute; extras still mix at \(k\ge 5\)).

Helper: `python3 research/cycle_gs.py --certify` (~0.01s). Dump:
`research/cycle_gs.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles CA/GG/GN/GQ/GR (packed \(k\le 6\), all
covering \(W\); no Fermat table, no extra window, no \(n_0=16\)
window).

## Lemma (hit-cone XOR = extras XOR \(\oplus(Q\bmod 2)\))

Certified \(k\le 6\), \(W\in\{4U,8U,16U\}\). So \(W=4U\) has
XOR \(=\) extras XOR \(\oplus 1\); \(W=8U,16U\) recover Cycle GR.

## Lemma (\(W=4U\) extras \(\subseteq\{0\}\) through \(k=4\))

One \(k\) past Cycle GQ’s all-\(W\) bound. At \(k=5\), extras
\(\{9,12\}\).

## Killed

Equals extras XOR on \(W=4U\): at \(k=0\), \(1\neq 0\). Equals lo
XOR \(\oplus(Q\bmod 2)\) for all \(k\): at \(k=5\), \(W=8U\), lo XOR
\(=1\) but hit XOR \(=0\). \(W=4U\) extras only lo at \(k=5\):
\(\{9,12\}\).

## Verdict

`LEMMA` (all-\(W\) hit-cone XOR = extras XOR \(\oplus(Q\bmod 2)\);
\(W=4U\) extras only lo through \(k=4\)).
`KILLED` (equals extras XOR on \(W=4U\); equals lo XOR
\(\oplus(Q\bmod 2)\) for all \(k\); \(W=4U\) extras only lo at
\(k=5\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_gs.md` (this note)
- `research/cycle_gs.py`
- `research/cycle_gs.json`
