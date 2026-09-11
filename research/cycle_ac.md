# Cycle AC: 00-preimages and eventually periodic left-diagonals

Cycle AB identified centre `00` with the triple `000`. The update
makes `00` exactly the triples `000` and `101`. Each has four
5-window preimages, a 32-case local check. Every left-diagonal
\(e_j(t)=x(t,-t+j)\) (packed bit \(j\)) is eventually periodic, but
the centre is the onset \(c_t=e_t(t)\), which leaves the periodic
tail at \(j=18\). Not a prize claim: infinitely many `00`s remain
unproved.

Helper: `python3 research/cycle_ac.py --certify`. Dump:
`research/cycle_ac.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (`00` is `000` or `101`)

\(c'= \ell\oplus(c\lor r)\). Among the eight centred triples, \(c=c'=0\)
holds exactly for `000` and `101`. Likewise \(c=c'=1\) holds exactly
for `010` and `011` (Cycle X). Certified by enumerating all eight
neighbourhoods. In particular infinitely many centre `00`s — which
would kill every eventual isolated-zero period \(01^q\), including
period 2 and \(q=8\) — is infinitely many `000` **or** `101`, not
`000` alone. On \(t<2^{12}\) the two mechanisms split 534 / 529.

## Lemma (5-window preimages)

A centred `000` at time \(t+1\) iff the centred 5-window at time \(t\)
is one of

\[
00000,\quad 11101,\quad 11110,\quad 11111.
\]

Proof: writing \((a,b,c,d,e)\) for \(x(t,-2),\ldots,x(t,2)\), the three
outputs are 0 iff \(a=b\lor c\), \(b=c\lor d\), \(c=d\lor e\), which
forces \(a=b=c\) and \(c=d\lor e\). The solutions are the four words
above. Certified on all 32 windows, and on the prize orbit those four
are the only `000`-predecessors (\(t<2^{12}\), zero illegal).

A centred `101` at time \(t+1\) iff the 5-window is one of
`01100`, `10001`, `01010`, `01011`. Same 32-case check.

## Lemma (left-diagonals are eventually periodic)

Write \(e_j(t)\) for packed bit \(j\) at time \(t\), i.e.
\(x(t,-t+j)\). The packed step gives, whenever the bits exist,

\[
e_j(t+1)=e_{j-2}(t)\oplus\bigl(e_{j-1}(t)\lor e_j(t)\bigr)
\]

(\(e_m=0\) for \(m<0\)). Certified on \(t<256\). Base:
\(e_0\equiv 1\); \(e_1\equiv 1\) for \(t\ge 1\) (Cycle AA);
\(e_2\equiv 0\) for \(t\ge 2\) (because
\(e_2(t+1)=e_0(t)\oplus(e_1(t)\lor e_2(t))=1\oplus 1=0\)).

Induction: if \(e_{j-2}\) and \(e_{j-1}\) are eventually periodic of
period dividing \(p\), the bit \(x_t=e_j(t)\) obeys
\(x_{t+1}=a_t\oplus(b_t\lor x_t)\) with periodic \((a,b)\). The state
\((t\bmod p,\,x_t)\) has \(2p\) values, so \(e_j\) is eventually
periodic. Thus every left-diagonal is eventually periodic. This is
the nested left of the prize triangle, as rays parallel to the left
light cone.

## Onsets are not the tails — killed as a formula for \(c\)

The centre is the diagonal sample \(c_t=e_t(t)\). For \(j\le 17\) the
periodic tail of \(e_j\) already holds at time \(t=j\). At \(j=18\)
the onset is still in the transient (\(T=2\), period 4). The eventual
period of diagonal \(t\) does not compute \(c_t\). Certified
\(j\le 23\).

## Verdict

`LEMMA` (`00` triples; 5-window preimages; left-diagonal recurrence;
every \(e_j\) eventually periodic). `KILLED` (`00` is only `000`;
\(c_t\) from the tail of \(e_t\)). `OPEN` (infinitely many `00`s).
Wall time 0.04s. Prize unsolved.

## Files

- `research/cycle_ac.md` (this note)
- `research/cycle_ac.py`
- `research/cycle_ac.json`
