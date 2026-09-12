# Cycle FJ: left off-support XOR on \([6U,10U)\) vanishes; \(\Delta=\Delta_R\)

Cycle FI’s mismatch
\(\Delta=J_{[6U,10U)\to 10U}\oplus J_{[6U,10U)\to 18U}\) is the XOR of
\(18U\)-Green on those ANDs with \(d=10U-p\notin[0,2m]\). Split them
into the left strip \(p<2s-10U+2\) (\(d>2m\)) and the right strip
\(p>10U\) (\(d<0\)). On the left, Freshman of the \(8U\)-shift leaves
only \(G(m,d-8U)=G(10U-s-1,2U-p)\), which vanishes for \(p>2U\). The
whole packed width \(p\le 2U\) sits in the left region
(\(2s-10U+2\ge 2U+2\)). Packed XOR of that strip is \(0\), so
\(\Delta_L=0\) and \(\Delta=\Delta_R\). Thus
\(J_{[6U,10U)\to 18U}=J_{[6U,10U)\to 10U}\oplus\Delta_R\). Do **not**
claim \(\Delta_R=1\) for all \(k\) (\(k=5\) has \(0\)). Do **not**
claim \(J_{[10U,18U)\to 18U}=1\) (\(k=3\) has \(0\)). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push the
even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\) past
414990. Do **not** increment consecutive `11` to \(n_8\).

Not a prize claim: pinning the mismatch to the right strip \(p>10U\)
does not prove covering never-fail.

Helper: `python3 research/cycle_fj.py --certify` (~0.12s). Dump:
`research/cycle_fj.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FF/FH/FI (packed check on \(k=2..6\);
tail kill only at \(k=3\); no Fermat table, no extra window, no
\(n_0=16\) window).

## Lemma (left \(2U\)-strip is off-support)

For \(s\in[6U,10U)\), \(2s-10U+2\ge 2U+2\), so every packed \(p\le 2U\)
has \(d>2m\). Certified \(k\le 20\).

## Lemma (Freshman reduces the left extra)

On that strip \(G(m+8U,d+8U)=G(m,d-8U)\) and \(G(m,d)=G(m,d+8U)=0\).
For \(p>2U\) the remaining argument \(2U-p\) is negative. Certified
on endpoint samples \(k\le 12\).

## Lemma (\(\Delta_L=0\), hence \(\Delta=\Delta_R\))

Packed AND XOR on \(2\le k\le 6\): left \(18U\)-Green sums to \(0\),
in-support \(10U\) matches \(18U\), and \(\Delta=\Delta_R\).

## Killed

\(\Delta_R\equiv 1\) fails at \(k=5\) (\(\Delta_R=0\)).
\(J_{[10U,18U)\to 18U}\equiv 1\) fails at \(k=3\) (value \(0\); AND
\(p=1\) is live on all \(8U\) steps of the window but off-support
for target \(18U\)).

## Verdict

`LEMMA` (left \(2U\) off-support; Freshman reduction; \(\Delta_L=0\);
\(\Delta=\Delta_R\)).
`KILLED` (\(\Delta_R\equiv 1\); tail remainder \(\equiv 1\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_fj.md` (this note)
- `research/cycle_fj.py`
- `research/cycle_fj.json`
