# Cycle BZ: ident-0 iff consecutive equal; no consecutive ident-0

If two consecutive packed-bit strings are equal and not identically
\(0\), the unique reset continuation is identically \(0\): the first
\(1\)-reset has \(a=b=1\), so it forces \(u=0\), and \(0\) is
invariant under \(u'=a\oplus(b\lor u)\) when \(a=b\). Hence ident-\(0\)
at \(p\) iff \(\lambda_{p-2}=\lambda_{p-1}\), on any orbit with packed
bit \(0\) equal to \(1\) (a leftward cascade of ident-\(0\) would
reach bit \(0\)). Consecutive ident-\(0\) is therefore impossible.
After an odd high toggle the Hamming distance between consecutive
high bits stays positive through the rest of the lift (prefix). Even
weight is not invariant under unique continuation. Not a prize claim:
the Fermat covering remains a prefix.

Helper: `python3 research/cycle_bz.py --certify` (~0.03s). Dump:
`research/cycle_bz.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (\(a=b\not\equiv 0\Rightarrow u\equiv 0\))

On a period-\(\pi\) drive with \(a_t=b_t\) and some \(b_{s_0}=1\),
the forced value is \(u_{s_0+1}=a_{s_0}\oplus 1=0\). If \(u\equiv 0\)
then \(u'=a\oplus b=0\). The unique continuation is the zero string.
Certified: \(300\) random equal drives at lengths \(4,8,16\).

## Lemma (ident-\(0\) iff consecutive equal)

The update at bit \(p\) is identically \(0\) iff
\(\lambda_{p-2}\equiv\lambda_{p-1}\). One direction is \(0=a\oplus b\).
The converse is the previous lemma unless \(b\equiv 0\), in which
case \(a\equiv 0\) too and bit \(p\) is constant; a constant \(1\)
would be ident-\(1\), but a leftward cascade of ident-\(0\) reaches
packed bit \(0\), which is \(1\). Certified: the two lists agree on
prize cycles for \(3\le k\le 12\), and no two ident-\(0\) indices
are adjacent.

## Lemma (no consecutive ident-\(0\))

If bits \(p\) and \(p+1\) were both ident-\(0\), the driver of
\(p+1\) would be ident-\(0\), so \(p+1\) would be a toggle of
\(\lambda_{p-1}\). The zero toggle requires \(\lambda_{p-1}\equiv 0\),
hence ident-\(0\) at \(p-1\). Iterating reaches bit \(0\),
contradicting \(\lambda_0\equiv 1\). This holds on the whole left
machine, not only the prize orbit.

## Prefix (positive Hamming distance after an odd toggle)

A second odd toggle in the same lift is exactly a later
consecutive-equal pair with odd driver XOR. After the first odd
high toggle, the Hamming distance between consecutive reconstructed
bits stays at least \(3\) on the \(k=4\) and \(k=8\) lifts (no zeros).
**PREFIX**, not a theorem for all \(k\).

## Even weight invariant — killed

Unique continuation after an odd doubling produces both even and
odd \(2\pi\)-weights (\(k=8\): \(56\) odd and \(56\) even among the
post-toggle bits). Settled prize cycles already have odd-weight bits
for \(k\ge 4\). **Killed** as a route to \(r\le 1\).

## Verdict

`LEMMA` (\(a=b\not\equiv 0\Rightarrow u\equiv 0\); ident-\(0\) iff
consecutive equal; no consecutive ident-\(0\)).
`PREFIX` (positive Hamming distance after an odd toggle; at most one
odd toggle for all \(k\); seed for all \(k\); Fermat covering).
`KILLED` (even-weight invariant; all bits even \(\pi\)-weight for
\(k\ge 3\)).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_bz.md` (this note)
- `research/cycle_bz.py`
- `research/cycle_bz.json`
