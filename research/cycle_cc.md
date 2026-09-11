# Cycle CC: \(A=DB\) iff the next-right packed bit is the spatial AND

Packed update at bit \(p-1\) is
\(\lambda_{p-1}(t+1)=\lambda_{p-3}(t)\oplus(\lambda_{p-2}(t)\lor\lambda_{p-1}(t))\).
Writing \(c=\lambda_{p-3}\), \(a=\lambda_{p-2}\), \(b=\lambda_{p-1}\) and
\(b'=c\oplus(a\lor b)\), the eight-row identity \(a=b\oplus b'\) iff
\(c=a\land b\) holds for every triple. So the time series of
\((p-2,p-1)\) is a derivative pair iff \(\lambda_{p-3}(t)=\lambda_{p-2}(t)\land\lambda_{p-1}(t)\)
for every \(t\). Later ident-\(0\) at \(q+1\) is exactly that AND-triple
on bits \(q-3,q-2,q-1\). The pattern \(011\) is not always present.
No AND-triple after the scar on the \(k=4\) and \(k=8\) odd lifts
(prefix). Not a prize claim: the Fermat covering remains a prefix.

Helper: `python3 research/cycle_cc.py --certify` (~0.02s). Dump:
`research/cycle_cc.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (\(A=DB\) iff spatial AND)

On any Rule 30 orbit, \(b'=c\oplus(a\lor b)\). Expanding
\(a\lor b=a\oplus b\oplus(a\land b)\) gives
\(a=b\oplus b'\) if and only if \(c=a\land b\). The two predicates
agree on all eight triples. The AND-closed set is
\(\{000,001,010,111\}\); a single time in
\(\{011,100,101,110\}\) already kills \(A=DB\). Certified by truth
table.

## Lemma (later ident-\(0\) iff AND-triple)

Ident-\(0\) at packed bit \(q+1\) iff \(\lambda_{q-1}=\lambda_q\)
(Cycle BZ) iff \(U=B\) at bit \(q\) iff \(A=DB\) for
\((\lambda_{q-2},\lambda_{q-1})\) (Cycle CA) iff
\(\lambda_{q-3}=\lambda_{q-2}\land\lambda_{q-1}\). Certified: the two
lists agree, and both are empty, on the \(k=4\) and \(k=8\) odd
lifts.

## Always-\(011\) witness — killed

The forbidden slice \(011\) is missing at the toggle and the
ident-\(1\) bit, and at \(14\) later bits of the \(k=8\) lift.
**Killed** as a single-pattern witness for every later triple.

## Prefix (no AND-triple after the scar)

Every later triple on the \(k=4\) and \(k=8\) odd lifts leaves the
AND-closed set at least twice (\(k=4\)) or three times (\(k=8\)).
**PREFIX**, not a theorem for every odd lift. Combined with Cycles
BY–CB this keeps \(r\le 1\), the period-\(H\) seed, and
\(J_B^{\to 2U}=0\) as prefixes.

## Verdict

`LEMMA` (\(A=DB\) iff spatial AND; later ident-\(0\) iff AND-triple).
`PREFIX` (no AND-triple after the scar; at most one odd toggle for
all \(k\); seed for all \(k\); Fermat covering).
`KILLED` (always-\(011\) as a witness).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_cc.md` (this note)
- `research/cycle_cc.py`
- `research/cycle_cc.json`
