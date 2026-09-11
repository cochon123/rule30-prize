# Cycle BX: reset lift; frozen bits; period doubling

If packed bit \(p-1\) is not identically \(0\) on a period-\(\pi\)
orbit of the lower bits, bit \(p\) has a unique period-\(\pi\)
continuation: the first \(1\)-reset forces it, and wrap-around is
automatic (the full-period map contains a constant factor). If bit
\(p-1\) is identically \(0\), bit \(p\) toggles by bit \(p-2\) and the
period is \(\pi\) or \(2\pi\) according to the XOR of that driver.
Reconstructing high bits this way matches the prize word at time
\(2W\) on every unblocked lift \(k\to k+1\) through \(k=12\). Period
\(8\) for all \(k\ge 5\) is false (\(k=9\) has period \(16\)). Frozen
zeros \(2,7,28\) grow at \(k=9\). A high identically-\(0\) bit does
not force a period doubling (even driver-XOR at \(k=16\)). Not a
prize claim: the Fermat covering remains a prefix.

Helper: `python3 research/cycle_bx.py --certify` (~1.2s). Dump:
`research/cycle_bx.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (reset ⇒ unique continuation)

On a period-\(\pi\) drive \(a_t=\lambda_{p-2}(t)\),
\(b_t=\lambda_{p-1}(t)\), the bit-\(p\) update is
\(u_{t+1}=a_t\oplus(b_t\lor u_t)\). If some \(b_{s_0}=1\), then
\(u_{s_0+1}=a_{s_0}\oplus 1\) is independent of \(u_{s_0}\). The
full-period map therefore contains a constant factor, so wrap-around
to the forced value is automatic: every \(a,b\) with a \(1\) in \(b\)
has a unique period-\(\pi\) response. Certified: \(400\) random
drives at lengths \(4,8,16\) never wrap-inconsistently; every
\(b\not\equiv 0\) returns unique.

## Lemma (toggle when \(b\equiv 0\))

If \(\lambda_{p-1}\equiv 0\), then \(u_{t+1}=a_t\oplus u_t\), hence
\(u_{t+\pi}=u_t\oplus\bigoplus a\). The period is \(\pi\) or \(2\pi\)
according as that XOR vanishes. Certified on every ident-\(0\)-driven
bit of the prize cycles for \(3\le k\le 8\).

## Lemma (unblocked lift matches the prize)

Starting from the prize cycle at scale \(k\), the reset construction
produces bits \(W+1,\ldots,2W\) of scale \(k+1\). Whenever it does
not hit an identically-\(0\) driver, the result is the unique
period-\(\pi\) lift, and it equals the prize word at time
\(2^{k+2}\) up to phase. Certified unblocked for
\(k\in\{5,6,7,9,10,11\}\) (and the blocked hits are packed bits
\(29\) at \(k=4\) and \(400\) at \(k=8\)).

## Prefix (period divides \(H\))

The minimal period of \(L_k(2W)\) through \(k=16\) is
\(1,2,4,4,8,8,8,8,16,16,16,16,16,16,16,16\). Each divides
\(H=2^{k-1}\). **PREFIX**, not a theorem for all \(k\). On that
prefix the Cycle BW seed holds. One odd-weight toggle per scale
would keep the next period dividing \(H_{k+1}\); two odd-weight
toggles while already at period \(H\) would not. That bound is not
proved.

## Period \(8\) for all \(k\ge 5\) — killed

At \(k=9\) the period is \(16\). **Killed.**

## Frozen zeros \(\{2,7,28\}\) for all \(k\ge 5\) — killed

At \(k=9\) packed bit \(399\) is identically \(0\) and bit \(401\) is
identically \(1\) (the \(+2\) twin). At \(k=16\) two further zeros
appear at \(53207\) and \(58286\). **Killed.**

## High ident-\(0\) iff period doubles — killed

Necessary: a doubling requires an identically-\(0\) driver (toggle
lemma). Not sufficient: \(k=16\) has high zeros and keeps period
\(16\) (even driver-XOR). **Killed** as an iff.

## Verdict

`LEMMA` (reset unique continuation; automatic wrap; toggle when
\(b\equiv 0\); unblocked lift matches prize).
`PREFIX` (period divides \(H\) for all \(k\); seed for all \(k\);
Fermat covering for all \(k\ge 2\)).
`KILLED` (period \(8\) for all \(k\ge 5\); ident-\(0\) set frozen at
\(\{2,7,28\}\); high ident-\(0\) iff doubling).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_bx.md` (this note)
- `research/cycle_bx.py`
- `research/cycle_bx.json`
