# Cycle BV: left \(2^k+1\) machine; freeze implies \(J_B^{\to 2U}=0\)

Packed bits \(0,\ldots,2^k\) evolve autonomously. Freshman of length
\(W=2^k\) targeting packed bit \(W\) picks up the left edge, so

\[
Q_k(r)
:=J_{[rW,\,(r+1)W)\to W}
=1\oplus\alpha_k(r)\oplus\alpha_k(r+1),
\]

where \(\alpha_k(r)\) is packed bit \(W\) at time \(rW\). For \(k=1\),
packed bit 2 is \(0\) for every \(t\ge 2\); for \(k=2\), packed bit 4
is \(1\) for every \(t\ge 2\). If the left word at time \(2W\) equals
that at time \(3W\), autonomy freezes it at every later sample
\(rW\) (\(r\ge 2\)), hence \(Q_k(r)=1\) and
\(\alpha_k(3)=\alpha_k(5)\). That last equality is
\(J_B^{\to 2U}=0\) at covering scale \(k-1\). The word equality
holds through \(k=12\) (prefix). Not a prize claim: the Fermat
covering remains a prefix.

Helper: `python3 research/cycle_bv.py --certify` (~0.04s). Dump:
`research/cycle_bv.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (left machine)

The update of packed bit \(p\) reads only packed bits \(p-2,p-1,p\)
(with the convention that negative indices are \(0\)). Hence bits
\(0,\ldots,W\) form a closed \(W+1\)-bit automaton, for every initial
condition, not only the prize orbit. Packed bit 0 stays 1: the
outside cell to its left is \(0\), and \(0\oplus(0\lor 1)=1\).
Certified against the prize orbit for \(1\le k\le 6\) and
\(W\le t<6W\).

## Lemma (packed bits 2 and 4)

For \(t\ge 1\), packed bits 0 and 1 are 1 (Cycle AA). The bit-2
update is then \(1\oplus(1\lor\lambda_2)=0\), so \(\lambda_2(t)=0\)
for every \(t\ge 2\). For \(t\ge 2\) the bit-4 update collapses to
\(\lambda_3\lor\lambda_4\). At \(t=2\), packed bit 4 is the right
edge, hence 1, and 1 is absorbing under \(\lor\). Thus
\(\lambda_4(t)=1\) for every \(t\ge 2\). Certified \(t\le 128\).

In particular \(\alpha_1(r)=0\) and \(\alpha_2(r)=1\) for all
\(r\ge 1\), so \(Q_1(r)=Q_2(r)=1\).

## Lemma (\(Q_k(r)=1\oplus\alpha_k(r)\oplus\alpha_k(r+1)\))

A freshman step of length \(W\) targeting packed bit \(W\) (the
cell \(W\) from the left edge) has linear image
\(a_W\oplus a_0\oplus a_{-W}\). Packed bit \(0\) is the left edge
(\(=1\)) and \(a_{-W}\) is outside the seed cone, so the linear
image is \(\alpha\oplus 1\). The AND remainder is \(Q_k(r)\).
Certified \(1\le k\le 5\) and \(1\le r\le 4\).

## Lemma (one equality freezes all later samples)

If \(L_k(2)=L_k(3)\), the left word is a fixed point of the
\(W\)-step map, so \(L_k(r)=L_k(2)\) for every \(r\ge 2\) by
autonomy. Then \(\alpha_k\) is constant on \(r\ge 2\), hence
\(Q_k(r)=1\) and \(\alpha_k(3)=\alpha_k(5)\).

Covering block \(B\) at scale \(U=2^{n}\) has left extra packed
bit \(2U=2^{n+1}\) at times \(6U=3\cdot 2^{n+1}\) and
\(10U=5\cdot 2^{n+1}\), i.e. \(\alpha_{n+1}(3)\) and
\(\alpha_{n+1}(5)\). Freshman of length \(4U\) targeting that bit
has vanishing extras (Cycle BU), so
\(J_B^{\to 2U}=\alpha_{n+1}(3)\oplus\alpha_{n+1}(5)\). Freeze at
level \(n+1\) forces this to \(0\). Certified as an identity of
cells for \(1\le n\le 11\).

## Prefix (\(L_k(2)=L_k(3)\))

The left words at times \(2^{k+1}\) and \(3\cdot 2^k\) agree for
\(1\le k\le 12\), and then also at \(4\cdot 2^k\). **PREFIX**, not
a theorem for all \(k\). On that prefix \(Q_k(r)=1\) for \(r\ge 2\)
and \(J_B^{\to 2U}=0\) for covering scales \(n\le 11\).

## Packed bit \(2^k\) identically constant — killed

For \(k\ge 3\) the bit \(2^k\) takes both values on
\([2^k,4\cdot 2^k]\). Sample-time freeze is not a freeze of the
bit at every time. **Killed.**

## Verdict

`LEMMA` (left machine; packed bits 2 and 4; \(Q=1\oplus\alpha\oplus\alpha\);
one equality freezes later samples; \(J_B^{\to 2U}=\alpha(3)\oplus\alpha(5)\)).
`PREFIX` (\(L_k(2)=L_k(3)\) for all \(k\); Fermat covering for all
\(k\ge 2\)).
`KILLED` (packed bit \(2^k\) identically constant for \(k\ge 3\)).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_bv.md` (this note)
- `research/cycle_bv.py`
- `research/cycle_bv.json`
