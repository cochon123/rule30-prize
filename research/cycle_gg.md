# Cycle GG: unclipped cone-hi contributes iff \(s=t_0+1+q\cdot 2U\); XOR is 1 iff \(W=4U\)

Unclipped cone-hi \(G\cdot\mathrm{AND}\) is 1 iff \(s\) is odd and dyadic
(Cycles FZ+GF). \(t_0\) is even, so that is \(\delta\equiv 1\pmod{2U}\):
\(s=t_0+1+q\cdot 2U\) for \(0\le q<Q=W/(4U)\), ending at \(W+1\). Those
\(Q\) times XOR to \(Q\bmod 2\), which is 1 iff \(W=4U\) (and 0 for
\(W=8U,16U\)). The XOR is **not** always 1 or always 0, and **not**
every \(W+2^j\) contributes. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push the
even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\) past
414990. Do **not** increment consecutive `11` to \(n_8\). Do **not**
walk \(32U\).

Not a prize claim: the cone-hi edge XOR is not \(J\) (other band indices
still contribute), so this does not prove covering never-fail.

Helper: `python3 research/cycle_gg.py --certify` (~0.01s). Dump:
`research/cycle_gg.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FZ/GD/GE/GF (times \(k\le 11\); packed
\(k\le 6\); no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (contrib times \(t_0+1+q\cdot 2U\))

Certified \(k\le 11\), \(W\in\{4U,8U,16U\}\). Last time is \(W+1\).

## Lemma (XOR is 1 iff \(W=4U\))

Packed \(G\cdot\mathrm{AND}\) matches; XOR \(=Q\bmod 2\). Certified
\(k\le 6\).

## Killed

XOR always 1: \(W=8U\) has \(Q=2\). XOR always 0: \(W=4U\) has \(Q=1\).
All \(W+2^j\) contribute: \(s=W+2\) is even, AND dead.

## Verdict

`LEMMA` (contrib times \(t_0+1+q\cdot 2U\); XOR 1 iff \(W=4U\)).
`KILLED` (XOR always 1; XOR always 0; all \(W+2^j\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_gg.md` (this note)
- `research/cycle_gg.py`
- `research/cycle_gg.json`
