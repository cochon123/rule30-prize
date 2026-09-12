# Cycle FG: \(J_{[4U,6U)\to 6U}=J_{[4U,6U)\to 18U}\)

Let \(U=2^k\) and let an AND injection at time \(s\in[4U,6U)\) sit at
packed bit \(p\) with \(0\le p\le 2s\). Write \(m=6U-s-1\) and
\(d=6U-p\). Cycle FF’s Freshman expansion of the \(q=3\), \(a=k+2\)
shift is

\[
G(m+12U,\,d+12U)
=G(m,d+12U)\oplus G(m,d+8U)\oplus G(m,d)
\oplus G(m,d-8U)\oplus G(m,d-12U).
\]

The light cone and the window \(s\ge 4U\) force the four extra
arguments off the support \([0,2m]\): \(d+8U>2m\), \(d+12U>2m\),
\(d-8U<0\), and \(d-12U<0\). Hence \(G(m+12U,d+12U)=G(m,d)\) for every
such AND, and the remainder of \([4U,6U)\) targeting \(6U\) equals the
remainder targeting \(18U\). The same equality to target \(10U\) is
false (the \(4U\)-shift extras need not leave the support). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\).

Not a prize claim: one matching pair of covering remainders on a
length-\(2U\) window does not force the three off-cone \(J\) never to
vanish.

Helper: `python3 research/cycle_fg.py --certify`. Dump:
`research/cycle_fg.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FE/FF (packed check on \(k=2..7\) only;
no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (cone kills the Freshman extras)

For every \(k\ge 0\), \(s\in[4U,6U)\), and \(0\le p\le 2s\),
\(d+8U-2m=2(U+s+1)-p\ge 2U+2>0\) and \(d-8U\le 6U-8U=-2U<0\).
Certified on endpoint samples \(k\le 12\).

## Lemma (\(J_{[4U,6U)\to 6U}=J_{[4U,6U)\to 18U}\))

Every light-cone AND contributes equally to the two targets. Packed
AND XOR on \(2\le k\le 7\) matches.

## Killed

\(J_{[4U,6U)\to 6U}=J_{[4U,6U)\to 10U}\) fails at \(k=2,3,4,7\).

## Verdict

`LEMMA` (cone kills extras; remainders to \(6U\) and \(18U\) agree).
`KILLED` (same remainder to \(10U\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_fg.md` (this note)
- `research/cycle_fg.py`
- `research/cycle_fg.json`
