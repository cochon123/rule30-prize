# Cycle FI: on \([6U,10U)\) FF matches in-support; remainders to \(10U\) and \(18U\) need not agree

Let \(U=2^k\). For \(s\in[6U,10U)\) a light-cone AND at packed \(p\) has
\(m=10U-s-1\) and \(d=10U-p\). Then \(m<4U=2^{(k+3)-1}\), so Cycle FF’s
\(q=1\), \(a=k+3\) translation gives \(G(m+8U,d+8U)=G(m,d)\) whenever
\(0\le d\le 2m\). Freshman of the \(8U\)-shift is three terms
\(G(m,d+8U)\oplus G(m,d)\oplus G(m,d-8U)\); on-support those extras
leave \([0,2m]\) because \(2m<8U\). Off-support ANDs (\(d\notin[0,2m]\))
can still have \(G(m+8U,d+8U)=1\), so the remainders
\(J_{[6U,10U)\to 10U}\) and \(J_{[6U,10U)\to 18U}\) need not agree.

Packed bit \(0\) stays \(1\), and bit \(1=\mathrm{bit}_0\lor\mathrm{bit}_1\)
is \(1\) for every \(t\ge 1\), so the AND at \(p=1\) is live at \(s=6U\).
It contributes \(G(12U-1,18U-1)=1\) (peels to \(G(5,8)=1\)) to the
\(18U\) remainder and \(G(4U-1,10U-1)=0\) (off support) to the \(10U\)
remainder. That single mismatch does **not** force the window XOR to
\(1\) (\(k=5\) cancels). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push the
even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\) past
414990. Do **not** increment consecutive `11` to \(n_8\).

Not a prize claim: an on-support translation plus a live left AND does
not prove covering never-fail.

Helper: `python3 research/cycle_fi.py --certify`. Dump:
`research/cycle_fi.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FF/FG/FH (packed check on \(k=2..6\);
no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (\(m<4U\) on \([6U,10U)\))

\(s\in[6U,10U)\) forces \(m=10U-s-1\in[0,4U)\). Certified \(k\le 20\).

## Lemma (FF on-support for the \(8U\)-shift)

Whenever \(0\le d\le 2m\), the extras \(d\pm 8U\) leave \([0,2m]\).
Certified on endpoint samples \(k\le 12\).

## Lemma (\(G(12U-1,18U-1)=1\); AND \(p=1\) live)

Odd peeling: \(G(12U-1,18U-1)=G(6U-1,9U-1)=G(3U-1,9\cdot 2^{k-1}-1)
=\cdots=G(5,8)=1\) for \(k\ge 1\), and \(G(11,17)=1\). Bit \(0\) is
identically \(1\); bit \(1=1\) for \(t\ge 1\). Certified \(k\le 16\)
and \(t=1..64\).

## Killed

\(J_{[6U,10U)\to 10U}=J_{[6U,10U)\to 18U}\) fails at \(k=2,3,4,6\).
The off-support XOR \(\Delta\equiv 1\) fails at \(k=5\) (\(\Delta=0\)).

## Verdict

`LEMMA` (\(m<4U\); FF on-support \(8U\)-shift; \(G(12U-1,18U-1)=1\);
AND \(p=1\) live for \(t\ge 1\)).
`KILLED` (remainders to \(10U\) and \(18U\) equal; \(\Delta_{\mathrm{off}}=1\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_fi.md` (this note)
- `research/cycle_fi.py`
- `research/cycle_fi.json`
