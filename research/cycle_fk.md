# Cycle FK: right-strip Freshman; \(\Delta_R=G(m,8U-r)\) on \(p=10U+r\)

Dual of Cycle FJ. On the right off-support strip \(p>10U\) one has
\(d=10U-p<0\) and therefore \(d-8U<0\), so Freshman of the \(8U\)-shift
leaves only \(G(m,d+8U)=G(10U-s-1,8U-r)\) with \(r=p-10U\). In
particular \(r=1\) is always off the reduced support
(\(8U-1>2m\) for \(s\ge 6U\)) even though the AND at \(p=10U+1\) does
fire. The Green corners \(G(n,0)=G(n,2n)=1\) hold with Cycle FF’s
\(G(n,n)=1\). Do **not** claim \(\Delta_R\) equals the \(r=2\) XOR
(that XOR vanishes while \(\Delta_R\) need not). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push the
even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\) past
414990. Do **not** increment consecutive `11` to \(n_8\).

Not a prize claim: reducing \(\Delta_R\) to a right-strip Green XOR
does not prove covering never-fail.

Helper: `python3 research/cycle_fk.py --certify`. Dump:
`research/cycle_fk.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FF/FI/FJ (packed check on \(k=2..6\);
no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (corners \(G(n,0)=G(n,2n)=1\))

Coefficient of \(x^0\) (resp. \(x^{2n}\)) in \((1+x+x^2)^n\) is \(1\).
Certified \(n<256\), with Cycle FF’s \(G(n,n)=1\).

## Lemma (Freshman on \(p>10U\))

\(G(m+8U,d+8U)=G(m,d+8U)\) and \(G(m,d)=G(m,d-8U)=0\). Certified on
endpoint samples \(k\le 12\).

## Lemma (\(r=1\) off reduced support)

For \(s\in[6U,10U)\), \(8U-1>2m\). Certified \(k\le 20\). Packed AND
at \(p=10U+1\) is live on \(2\le k\le 6\) but contributes \(0\).

## Killed

\(\Delta_R\) equals the \(r=2\) XOR: that XOR is \(0\) on \(2\le k\le 6\)
while \(\Delta_R=1\) except at \(k=5\). The AND at \(p=10U+1\) is not
identically dead.

## Verdict

`LEMMA` (corners; right Freshman; \(r=1\) off reduced support).
`KILLED` (\(\Delta_R=\) \(r=2\) XOR; \(r=1\) AND never live).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_fk.md` (this note)
- `research/cycle_fk.py`
- `research/cycle_fk.json`
