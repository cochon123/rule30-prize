# Cycle AF: two-step Green support and annulus-parity kills for \(I_k\)

Every 1-run ending fires the centre-left AND, and that AND Green-hits
\(c_{s+2}\) because \(G(1,2)=1\). The only time-\(s\) ANDs that hit
\(c_{s+2}\) are three local pairs. The older remainder \(O_s\) is not
identically 0, so those three ANDs do not force a centre `00`. Annulus
parities of `10`/`00`/`11` are not \(I_k\). Not a prize claim:
infinitely many `00`s and non-vanishing of \(I_k\) remain unproved.

Helper: `python3 research/cycle_af.py --certify`. Dump:
`research/cycle_af.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (two-step Green support)

\(G(1,0)=G(1,1)=G(1,2)=1\) and \(G(1,d)=0\) otherwise, since
\(1+x+x^2\) is the \(m=1\) Green polynomial. An AND at packed bit
\(p\) at time \(s\) contributes to \(c_{s+2}\) iff
\(G(1,s+2-p)=1\), i.e. \(p\in\{s,s+1,s+2\}\). Those three bits are
the pairs \((\ell,c)\), \((c,r)\), and \((r,e)\). A time-\(s+1\) AND
hits \(c_{s+2}\) iff \(p=s+2\), i.e. the single pair \((c',r')\).

## Lemma (two-step identity)

Writing \(O_s\) for the Green parity of AND injections at times
strictly before \(s\) that hit packed bit \(s+2\) at time \(s+2\),

\[
c_{s+2}
=1
\oplus(\ell\land c)
\oplus(c\land r)
\oplus(r\land e)
\oplus(c'\land r')
\oplus O_s.
\]

The leading 1 is \(G(s+2,s+2)\) (Cycle AA). Certified for \(s<36\).
This is a bulk rewrite, not a local closed form: \(O_s\) sees the
whole past light cone.

## Lemma (1-run AND hits \(c_{s+2}\))

A 1-run ending has \((\ell,c)=(1,1)\), so \(\ell\land c=1\), and
\(c'=0\), so \(c'\land r'=0\). The identity collapses to

\[
c_{s+2}=(r\land\lnot e)\oplus O_s.
\]

The centre-left AND always Green-hits \(c_{s+2}\). Then `00` follows
iff \(O_s=r\land\lnot e\). On the scanned 1-run endings \(O_s\) takes
both values, so it is not identically 0: the three local ANDs do not
by themselves force `00`. Certified as a 4-row identity plus the
orbit check \(s<36\).

## Annulus parities — killed as formulas for \(I_k\)

On \([2^{k-1},2^k)\) none of the following equals \(I_k=c_{2^k}\oplus
c_{2^{k-1}}\) for every \(k\le 10\): parity of `10` transitions,
parity of `00`, parity of `11`, XOR of \(r\land\lnot e\) at `10`s,
XOR of the Cycle AE predicate \(a=r\lor e\) at `10`s. First failures
are at \(k=2,1,1,2,1\) respectively. Cycle Z/AA already killed other
local and unweighted-11 formulas; these are the remaining 1-run
annulus candidates.

## Verdict

`LEMMA` (\(G(1,\cdot)\) support; two-step identity; 1-run AND hits
\(c_{s+2}\); \(O_s\) not identically 0). `KILLED` (local three ANDs
force `00`; \(I_k\) equals an annulus `10`/`00`/`11` or 1-run
Boolean parity). `OPEN` (infinitely many `00`s; eventual vanishing of
\(I_k\)). Wall time 0.01s. Prize unsolved.

## Files

- `research/cycle_af.md` (this note)
- `research/cycle_af.py`
- `research/cycle_af.json`
