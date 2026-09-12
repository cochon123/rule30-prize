# Cycle GT: at \(k=4\), AND at lo is dead on every covering hit

Extras XOR therefore misses lo, and in fact extras XOR vanishes on
all covering \(W\), so hit-cone XOR \(=Q\bmod 2\) (Cycle GS). AND at
lo is **not** dead on all odd \(s\) (live at \(\delta=17\) on
\(W=8U\)). Extras are **not** empty (\(W=8U\) has \(\{6,7\}\) and
\(\{1,4\}\)). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: a \(k=4\) lo-dead / extras-XOR-0 slice does not
prove covering never-fail (extras XOR is live at other \(k\); other
times still contribute).

Helper: `python3 research/cycle_gt.py --certify` (~0.01s). Dump:
`research/cycle_gt.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles CA/GG/GN/GQ/GS (packed \(k=4\), all covering
\(W\), 7 hits; kill at \(k=2\) extras XOR; no Fermat table, no extra
window, no \(n_0=16\) window).

## Lemma (\(k=4\) AND at lo dead on covering hits)

Certified on all 7 Cycle GG hits.

## Lemma (\(k=4\) extras XOR \(=0\); hit-cone XOR \(=Q\bmod 2\))

Interior extras exist (\(W=8U\): \(\{6,7\}\), \(\{1,4\}\); \(W=16U\):
\(\{1,3\}\)) but XOR to 0.

## Killed

AND at lo dead on all odd \(s\): at \(k=4\), \(W=8U\), \(\delta=17\)
(not a hit). Extras empty at \(k=4\): \(W=8U\), \(q=0\), \(\{6,7\}\).
Extras XOR \(=0\) for all \(k\): at \(k=2\), \(W=8U\), xor \(=1\).

## Verdict

`LEMMA` (\(k=4\) AND at lo dead on hits; extras XOR \(0\); hit-cone
XOR \(=Q\bmod 2\)).
`KILLED` (lo dead on all odd \(s\); extras empty; extras XOR \(0\)
for all \(k\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_gt.md` (this note)
- `research/cycle_gt.py`
- `research/cycle_gt.json`
