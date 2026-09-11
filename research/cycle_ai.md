# Cycle AI: dyadic step from arbitrary time

Cycle Z (and Cycle AH’s \(q=1\) case) starts at a dyadic time so the
light-cone edges cancel. The same Freshman factor
\((1+x+x^2)^{2^k}=1+x^{2^k}+x^{2^{k+1}}\) works from every time \(t\).
The AND remainder is a Boolean of the causal window of width
\(2^{k+1}+1\). The palindrome-constraint graph that recovers Cycle AB
at distance 1 has a mixing recurrent SCC at distances 2 and 4, so it
does not prove that the distance-\(2^k\) defect is not eventually 0.
Not a prize claim: \(I_k\) and infinitely many `00`s remain open.

Helper: `python3 research/cycle_ai.py --certify`. Dump:
`research/cycle_ai.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (dyadic step from arbitrary time)

Let \(U=2^k\). Packed Rule 150 for \(U\) steps multiplies by
\(1+x^{U}+x^{2U}\). Reading the centre at time \(t+U\) (packed bit
\(t+U\)) therefore gives

\[
[x^{t+U}]P_t\,(1+x^{U}+x^{2U})
=P_t[t+U]\oplus P_t[t]\oplus P_t[t-U],
\]

which are \(x(t,U)\), \(c_t\), and \(x(t,-U)\) respectively, with the
convention \(x(t,j)=0\) for \(|j|>t\). Packed Rule 30 is Rule 150 XOR
adjacent ANDs (Cycle Y), so

\[
c_{t+2^k}
=c_t\oplus x(t,-2^k)\oplus x(t,2^k)\oplus J_{t,k},
\]

where \(J_{t,k}\) is the Green parity of AND injections on the time
interval \([t,t+2^k)\) that hit packed bit \(t+2^k\).

Special cases:

- \(k=0\): \(J_{t,0}=c_t\land r_t\) and the identity is the Rule 30
  update \(c'=c\oplus d\oplus(c\land r)\).
- \(t=2^k\): both edges are 1 and cancel, recovering Cycle Z
  (\(J_{2^k,k}=I_{k+1}\)).
- \(k=1\): \(c_{t+2}=c_t\oplus a\oplus e\oplus J_{t,1}\) with a
  5-window remainder, a complementary time-split to Cycle AF’s
  older \(O_s\) (AF sums times \(<t\); \(J_{t,1}\) sums
  \([t,t+2)\)).

Certified: Green remainder matches the packed centre for
\(k\le 6\) and \(t<120\) (840 identities, zero failures); Cycle Z
edges and remainder for \(k\le 6\); \(J_{t,0}=c\land r\) on that
prefix.

## Lemma (\(J_{t,k}\) is causal)

The origin at time \(t+2^k\) has past light cone exactly
\([-2^k,2^k]\) at time \(t\). An AND at time \(t\) outside that
interval has Green degree \(t+2^k-p\) off the support of
\(G(2^k-1,\cdot)\), and later times in the cone are determined by
the same window. Hence \(J_{t,k}\) is a Boolean of those
\(2^{k+1}+1\) bits, for every initial condition, not only the prize
orbit. At a dyadic time \(t=2^k\) the window is the whole row, so
this does not shrink \(I_{k+1}\). Certified: on the prize orbit the
same window never yields two values of
\(c_{t+2^k}\oplus c_t\oplus x(t,\pm 2^k)\) for \(k=1,2,3\).

## Lemma (distance-1 palindrome graph)

Force \(\ell=r\) in every 5-window, and allow free exterior bits
\(x(\pm 3)\). The resulting 16-node graph has three recurrent SCCs,
all with constant centre:

- `00000` (vacuum, \(c=0\));
- `10101` (spatial checkerboard, \(c=1\));
- \(\{`01010`,`01011`\}\) (absorbing \(c=0\)).

An eventual palindrome at distance 1 therefore forces \(c\)
eventually constant, contradicting infinitely many 0s and 1s. This
is Cycle AB’s lemma as a 16-node check. Certified by enumerating
the graph.

## Distance \(2^k\) palindrome graphs — killed

The same construction at distance \(d=2^k\), extra cell of padding,
is sound as an implication: an eventual palindrome at distance \(d\)
would live in a recurrent SCC of that graph. For \(k=1\) (\(d=2\),
7-cell windows) one recurrent SCC has 21 states, both colours of
\(c\), and all four pairs \((c,\ell)\). For \(k=2\) (\(d=4\)) a
recurrent SCC of 355 states likewise takes both colours. Eventual
palindrome at distance 2 or 4 does **not** force a constant centre
or a width-2 obstruction, so this method does not prove that
\(\delta^{(k)}_t:=x(t,-2^k)\oplus x(t,2^k)\) fails to vanish.
**Killed** as a proof that \(\delta^{(k)}\) is not eventually 0 for
\(k\ge 1\). (On a prefix \(t<400\) those defects still fire about
half the time, with max 0-run \(\le 10\); finite evidence only.)

A centre `00` at time \(t\) does not force a `00` at \(t+2^k\) (on
\(t<250\) there are 61 such `00`s, of which
\(32,15,12,12,11,18\) remain `00` at lag \(2^k\) for
\(k=0,\ldots,5\)). **Killed** as a `00` production.

## Verdict

`LEMMA` (dyadic step from every \(t\); causality of \(J_{t,k}\);
distance-1 palindrome graph). `KILLED` (distance \(2,4\) palindrome
graphs as a defect-vanishing proof; `00` at lag \(2^k\)). `OPEN`
(eventual vanishing of \(I_k\); infinitely many `00`s). Prize
unsolved.

## Files

- `research/cycle_ai.md` (this note)
- `research/cycle_ai.py`
- `research/cycle_ai.json`
