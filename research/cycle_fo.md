# Cycle FO: \(G(2^n-1,2^m-1)=1\) for \(n\ge m\); \(16U\) left \(\Delta\) on \([10U,18U)\) is \(0\)

Odd peeling gives \(G(2^n-1,2^m-1)=G(2^{n-1}-1,2^{m-1}-1)\) down to
\(G(2^{n-m}-1,0)=1\) whenever \(n\ge m\ge 0\). That is the start-bit
Green on every \(2^a\)-shift left strip (packed \(p=1\) at window
start). On \([10U,18U)\) the \(16U\)-shift comparing \(18U\) to \(34U\)
has \(m<8U\), so Cycle FF matches in-support; the left strip start
contributes \(1\) and the rest cancels, so \(\Delta^{(16)}_L=0\)
(Cycle FJ-like, **not** the \(4U\) Cycle FM pattern \(\Delta_L=1\)).
Do **not** claim \(G(2^n-1,2^m-1)=1\) for \(n<m\). Do **not** claim
\(\Delta^{(16)}_L=1\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push the
even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\) past
414990. Do **not** increment consecutive `11` to \(n_8\).

Not a prize claim: a Mersenne Green identity plus left cancellation
on a non-covering target \(34U\) does not prove covering never-fail.

Helper: `python3 research/cycle_fo.py --certify`. Dump:
`research/cycle_fo.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FF/FJ/FK/FM/FN (packed check on
\(k=2..5\); no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (\(G(2^n-1,2^m-1)=1\) for \(n\ge m\))

Certified \(0\le m\le n\le 12\). Corners \(G(\cdot,0)=1\) from Cycle FK.

## Lemma (\(m<8U\) on \([10U,18U)\); \(\Delta^{(16)}_L=0\))

FF on-support. Packed: start AND at \((10U,1)\) contributes \(1\), rest
XOR is \(1\), so left \(\Delta=0\) on \(2\le k\le 5\).

## Killed

\(G(2^n-1,2^m-1)=1\) for \(n<m\): \(G(1,3)=0\). \(\Delta^{(16)}_L=1\)
(the \(4U\) pattern does not continue).

## Verdict

`LEMMA` (Mersenne Green; \(m<8U\); \(\Delta^{(16)}_L=0\) from start
\(1\) plus rest \(1\)).
`KILLED` (\(n<m\); \(\Delta^{(16)}_L=1\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_fo.md` (this note)
- `research/cycle_fo.py`
- `research/cycle_fo.json`
