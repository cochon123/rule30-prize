# Cycle CB: half-xor intertwines with the cyclic derivative

On a length-\(2\pi\) string write \(v(s)_t=s_t\oplus s_{t+\pi}\). The
cyclic derivative commutes with this half-xor: \(v(DB)=D(v(B))\).
Hence \(A=DB\) forces \(v(A)=D(v(B))\). In particular an odd
\(2\)-copy driver cannot be a derivative of an even \(2\)-copy bit.
Unique continuation does not preserve \(2\)-copy type, and
\(v(A)\ne D(v(B))\) is not absorbing under arbitrary unique
continuation. After the three-pair scar window on the \(k=8\) odd
lift, the half-xor obstruction fires on every remaining pair
(prefix). Not a prize claim: the Fermat covering remains a prefix.

Helper: `python3 research/cycle_cb.py --certify` (~0.02s). Dump:
`research/cycle_cb.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (\(v\circ D=D\circ v\))

Let \(B\) have even length \(L=2m\). Then
\[
v(DB)_t=(B_t\oplus B_{t+1})\oplus(B_{t+m}\oplus B_{t+m+1})
=v(B)_t\oplus v(B)_{t+1}
\]
for \(t<m-1\), and the wrap \(t=m-1\) is
\(v(B)_{m-1}\oplus v(B)_0\) because \(B_{2m}=B_0\). So
\(v(DB)=D(v(B))\) in \(\mathbb{F}_2^m\). Certified on \(600\) random
strings of lengths \(8,16,32\).

## Lemma (\(A=DB\Rightarrow v(A)=D(v(B))\); odd \(2\)-copy)

If \(A=DB\) then \(v(A)=D(v(B))\). An odd \(2\)-copy has \(v=\mathbf{1}\);
an even \(2\)-copy has \(v=\mathbf{0}\). The derivative of even
\(2\)-copy (and of odd \(2\)-copy) is even \(2\)-copy, so an odd
\(2\)-copy string is never a cyclic derivative of a \(2\)-copy bit.
Certified on random even/odd blocks of lengths \(2,4,8,16\).

## \(2\)-copy invariant — killed

Unique continuation of an odd/even \(2\)-copy drive is typically not
a \(2\)-copy. On the prize odd lifts the fourth reconstructed bit is
already type \(N\) (\(k=4\) bit \(32\); \(k=8\) bit \(403\)).
**Killed** as a route to \(A\not=DB\) on the whole high half.

## Half-xor obstruction absorbing — killed

On random length-\(16\) drives, \(v(A)\ne D(v(B))\) fails to pass to
the next pair \((B,U)\) in a positive fraction of trials. The
obstruction is not an invariant of unique continuation on the whole
affine space. **Killed** as an abstract (orbit-free) argument.

## Prefix (obstruction after the scar window)

On the \(k=8\) odd lift (toggle at packed bit \(400\)) the necessary
condition \(v(A)=D(v(B))\) holds only at bits \(400,401,403\). Those
three are the scar pairs already excluded by Cycle CA. On the
remaining \(109\) pairs the half-xor Hamming distance is at least
\(1\). The \(k=4\) lift is only four bits long, so it has no
post-window tail. **PREFIX**, not a theorem for every odd lift.

## Verdict

`LEMMA` (half-xor intertwines with \(D\); \(D\) kills odd \(2\)-copy).
`PREFIX` (half-xor obstruction after the scar window; at most one
odd toggle for all \(k\); seed for all \(k\); Fermat covering).
`KILLED` (\(2\)-copy invariant; half-xor obstruction absorbing).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_cb.md` (this note)
- `research/cycle_cb.py`
- `research/cycle_cb.json`
