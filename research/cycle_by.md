# Cycle BY: ident-0 twin; 2-power period; one odd toggle implies the seed

An identically-\(0\) packed bit \(p\) whose left neighbour is not
identically \(0\) forces identically-\(1\) at \(p+2\): the in-between
bit toggles, the first \(1\) resets bit \(p+2\) to \(1\), and
\(u'=b\lor u\) absorbs. The left-word period is a \(2\)-power: a
reset preserves the driver period, a toggle at most doubles it.
Nested low bits (Cycle BW) make \(\pi_{k+1}\) a multiple of
\(\pi_k\), so \(\pi_{k+1}=\pi_k\cdot 2^{r}\) with \(r\) the number of
odd-weight high toggles. If \(r\le 1\) at every scale then
\(\pi_k\mid 2^{k-1}\) for every \(k\), which is the Cycle BW seed.
Through \(k=16\) every ratio \(\pi_{k+1}/\pi_k\) is \(1\) or \(2\).
Two new ident-\(0\) bits can appear without doubling (\(k=16\)).
Not a prize claim: the Fermat covering remains a prefix.

Helper: `python3 research/cycle_by.py --certify` (~1.2s). Dump:
`research/cycle_by.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (ident-\(0\) twin)

If \(\lambda_p\equiv 0\) and \(\lambda_{p-1}\not\equiv 0\), then bit
\(p+1\) is a toggle (\(b\equiv 0\), \(a\not\equiv 0\)), hence not
identically \(0\). Bit \(p+2\) has \(a\equiv 0\) and a \(1\)-reset
from the toggle, so it is forced to \(1\) and stays \(1\) under
\(u'=b\lor u\). Thus \(\lambda_{p+2}\equiv 1\). Moreover ident-\(0\)
at \(p\) requires \(\lambda_{p-2}\equiv\lambda_{p-1}\) (the update
\(0=a\oplus b\)). Certified on prize cycles for \(3\le k\le 12\).

## Lemma (period is a \(2\)-power; nested multiple)

Resets give a unique continuation of the same period. Toggles give
period \(\pi\) or \(2\pi\). Starting from \(\pi_1=1\), every later
period is a \(2\)-power. Bits \(0,\ldots,2^{k-1}\) of scale \(k\) are
the scale-\((k-1)\) machine, so \(\pi_k\) is a multiple of
\(\pi_{k-1}\). Hence \(\pi_k=\pi_{k-1}\cdot 2^{r}\) with \(r\) the
odd-toggle count on that lift. Certified: periods through \(k=16\)
are \(1,2,4,4,8^4,16^8\); each divides the next; each divides
\(H=2^{k-1}\). At \(k=4\), \(\pi=4=H/2\).

## Lemma (two copies XOR to \(0\))

For any GF(\(2\)) block \(s\), \(\bigoplus(s\|s)=0\). After an odd
doubling, any driver that still has period \(\pi\) has even weight
over \(2\pi\), so it cannot odd-toggle again.

## Lemma (seed if ratios in \(\{1,2\}\))

If \(\pi_{k+1}\in\{\pi_k,2\pi_k\}\) for every \(k\), then by induction
\(\pi_k\mid 2^{k-1}\) for every \(k\). Autonomy (Cycle BW) then gives
\(F^H(L_k(2W))=L_k(2W)\). This is a theorem relating those two
statements, not a proof that the ratios stay in \(\{1,2\}\).

## Prefix (at most one odd toggle)

Every ratio through \(k=16\) is \(1\) or \(2\), and every lift
\(4\le k\le 12\) has at most one odd high toggle. **PREFIX**, not a
theorem for all \(k\). A ratio \(4\) (two odd toggles) while already
at period \(H\) would break the seed induction.

## At most one ident-\(0\) per lift — killed

At \(k=16\) two new ident-\(0\) bits appear and the period ratio is
\(1\) (even driver-XORs). **Killed.**

## Verdict

`LEMMA` (ident-\(0\) twin; period is a \(2\)-power; nested multiple;
two-copy XOR; \(k=4\) has \(\pi=H/2\); seed if ratios in
\(\{1,2\}\)).
`PREFIX` (at most one odd toggle for all \(k\); seed for all \(k\);
Fermat covering for all \(k\ge 2\)).
`KILLED` (at most one ident-\(0\) per lift).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_by.md` (this note)
- `research/cycle_by.py`
- `research/cycle_by.json`
