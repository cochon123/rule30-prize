# Cycle FM: \(4U\)-shift on \([4U,6U)\); left \(\Delta\) is \(1\) from the \((4U,1)\) AND

Dual of Cycles FI–FJ for the \(4U\)-shift comparing targets \(6U\) and
\(10U\). On \(s\in[4U,6U)\) one has \(m=6U-s-1<2U\), so Cycle FF matches
in-support. The left off-support strip \(p<2s-6U+2\) contains
\(p\le 2U\); Freshman reduces it to \(G(6U-s-1,2U-p)\). The AND at
\((s,p)=(4U,1)\) is live and contributes \(G(2U-1,2U-1)=1\); the rest
of the left strip XOR-cancels, so \(\Delta^{(4)}_L=1\). This is **not**
the naive dual of Cycle FJ’s \(\Delta_L=0\). Do **not** claim
\(\Delta^{(4)}_R=0\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push the
even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\) past
414990. Do **not** increment consecutive `11` to \(n_8\).

Not a prize claim: a definite left bit on \([4U,6U)\) does not prove
covering never-fail.

Helper: `python3 research/cycle_fm.py --certify` (~0.03s). Dump:
`research/cycle_fm.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FF/FI/FJ/FL (packed check on \(k=2..6\);
no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (\(m<2U\) on \([4U,6U)\); FF on-support)

Certified \(k\le 20\). In-support \(6U\) matches \(10U\) on \(2\le k\le 6\).

## Lemma (\(\Delta^{(4)}_L=1\) from \((4U,1)\))

Packed width \(p\le 2U\) is off-support. Freshman leaves
\(G(6U-s-1,2U-p)\). The live AND at packed \(p=1\), time \(4U\),
contributes \(G(2U-1,2U-1)=1\); the remaining left XOR is \(0\).
Certified \(2\le k\le 6\), with \(G(2U-1,2U-1)=G(4U-1,2U-1)=1\) for
\(k\le 16\).

## Killed

\(\Delta^{(4)}_L=0\) (the naive dual of Cycle FJ). \(\Delta^{(4)}_R=0\)
fails at \(k=5,6\). Hence \(\Delta^{(4)}=\Delta^{(4)}_R\) fails.

## Verdict

`LEMMA` (\(m<2U\); FF on-support \(4U\)-shift; \(\Delta^{(4)}_L=1\) from
the start AND).
`KILLED` (\(\Delta^{(4)}_L=0\); \(\Delta^{(4)}_R=0\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_fm.md` (this note)
- `research/cycle_fm.py`
- `research/cycle_fm.json`
