# Cycle FP: \(G(q\cdot 2^a-1,2^a-1)=1\); each \(2U\) left-block XOR is \(1\)

Peeling \(a\) times gives \(G(q\cdot 2^a-1,2^a-1)=G(q-1,0)=1\) for every
integer \(q\ge 1\). Cycle FO is the 2-power-\(q\) case. On the
\(4U/8U/16U\) windows, each aligned \(2U\) time block of the left
off-support strip has a live packed-\(p=1\) start contributing \(1\)
and the rest of the block XOR-cancels, so the block XOR is \(1\).
Hence \(\Delta_L=(\#\mathrm{blocks})\bmod 2\), recovering Cycle FM
(one block), Cycle FJ (two), and Cycle FO (four). Do **not** claim
the rest of a block is \(1\). Do **not** claim the identity for
\(q=0\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all
\(k\). Do **not** push the even-spine scan past \(k=18\). Do **not**
bump all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\).

Not a prize claim: a blockwise left XOR of \(1\) does not prove
covering never-fail.

Helper: `python3 research/cycle_fp.py --certify` (~0.02s). Dump:
`research/cycle_fp.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FF/FJ/FK/FM/FO (packed \(4U/8U\) on
\(k=2..5\), \(16U\) on \(k=2..4\); no Fermat table, no extra window,
no \(n_0=16\) window).

## Lemma (\(G(q\cdot 2^a-1,2^a-1)=1\))

Certified \(0\le a\le 8\), \(1\le q\le 16\).

## Lemma (each \(2U\) left-block XOR is \(1\))

Start AND \(p=1\) live, Green \(1\), rest \(0\). Packed as above.
Then \(\Delta_L=(\#\mathrm{blocks})\bmod 2\).

## Killed

Block rest \(\equiv 1\) (it is \(0\)). The identity for \(q=0\)
(\(0\cdot 2^a-1=-1\) is off the Green domain).

## Verdict

`LEMMA` (\(G(q\cdot 2^a-1,2^a-1)=1\); each \(2U\) left-block XOR is
\(1\); block rest \(0\); \(\Delta_L=(\#\mathrm{blocks})\bmod 2\)).
`KILLED` (block rest \(1\); \(q=0\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_fp.md` (this note)
- `research/cycle_fp.py`
- `research/cycle_fp.json`
