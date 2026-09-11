# Cycle CD: AND-triples stay iff a forced fifth bit; \(d=Da\)

If a packed triple \((c,a,b)\) is AND-closed, the update collapses to
\(a'=d\oplus a\) and \(b'=a\oplus b\), and the next triple stays
AND-closed iff \(e=a\oplus(d\land\lnot(a\lor b))\). An identically
AND triple therefore forces \(d=Da\), hence
\(d_t=b_t\oplus b_{t+2}\). A forbidden triple cannot enter the
AND-closed set when \((e,d)=(0,1)\). The AND-closed set is not
absorbing (\(8\) entries and \(8\) exits among the \(32\) five-bit
states). No identically-AND triple after the scar on the \(k=4\)
and \(k=8\) odd lifts (prefix). Not a prize claim: the Fermat
covering remains a prefix.

Helper: `python3 research/cycle_cd.py --certify` (~0.03s). Dump:
`research/cycle_cd.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (stay iff forced \(e\))

Write \(S=\{000,001,010,111\}\). Packed update on five consecutive
bits is \(b'=c\oplus(a\lor b)\), \(a'=d\oplus(c\lor a)\),
\(c'=e\oplus(d\lor c)\). If \((c,a,b)\in S\) then \(c=a\land b\), so
\(b'=a\oplus b\) and \(a'=d\oplus a\). The next triple lies in \(S\)
iff \(e=a\oplus(d\land\lnot(a\lor b))\). Certified on all \(16\)
AND-closed five-bit states.

## Lemma (identically AND implies \(d=Da\))

If \((c,a,b)\in S\) at every time then \(a'=d\oplus a\) at every
time, so \(d=Da\). Combined with \(b'=a\oplus b\) one has \(a=Db\)
and \(d=D^2b\), i.e. \(d_t=b_t\oplus b_{t+2}\). Certified on every
settled ident-\(0\) at \(r\ge 7\) for \(3\le k\le 12\) (bits \(7\),
\(28\), \(399\)): the AND-triple holds and \(d=Da=D^2b\).

## Lemma (no entry from \(F\) when \((e,d)=(0,1)\))

The four forbidden triples \(\{011,100,101,110\}\) with
\((e,d)=(0,1)\) all step to a forbidden triple. Certified by truth
table.

## AND-closed set absorbing — killed

Among the \(32\) five-bit states, \(8\) transitions enter \(S\) from
\(F\) and \(8\) leave \(S\). **Killed.** Visiting \(S\) does not
force an identically-AND time series.

## Prefix (no AND-triple after the scar)

The \(k=4\) and \(k=8\) odd lifts have no identically-AND triple
after the scar (minimum \(2\) and \(3\) forbidden slices). After the
scar, \(d=Da\) holds only on a few triples (\(3/4\) and \(4/113\))
and never with AND. **PREFIX**, not a theorem for every odd lift.

## Verdict

`LEMMA` (stay iff forced \(e\); collapse of \(a',b'\) on \(S\);
identically AND implies \(d=Da\); no entry from \(F\) when
\((e,d)=(0,1)\)).
`PREFIX` (no AND-triple after the scar; at most one odd toggle for
all \(k\); seed for all \(k\); Fermat covering).
`KILLED` (\(S\) absorbing).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_cd.md` (this note)
- `research/cycle_cd.py`
- `research/cycle_cd.json`
