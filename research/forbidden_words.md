# Attempt: forcing recurrent `00`/`11` center words

Assume the center trace (c_t=x(t,0)) is eventually free of `00`. Then every
zero is followed by one. The inverse center equation is
\[
l_t=c_{t+1}\oplus(c_t\lor r_t).
\]
Its phase consequences are:

* on a `11` transition, (l_t=0) is forced;
* on a `10` transition, (l_t=1) is forced;
* on a `01` transition, (l_t=1-r_t), retaining a free right-trace bit.

Thus if the center has infinitely many `11` transitions, column (-1) has
infinitely many forced zeros, but this does not make it periodic. If `11`
occurs only finitely often, the center is eventually the strictly alternating
word `0101...`; the alternating analysis in `research/alternating.md` shows
that the free even subsequence of the right trace survives all the way into
the left reconstruction.

The analogous assumption of eventual avoidance of `11` leaves arbitrary
zero-runs and does not force a periodic adjacent trace. In particular, the
already-proved facts “infinitely many zeros and infinitely many ones” do not
imply recurrence of either `00` or `11`: an eventually alternating binary
sequence has neither word.

Therefore no valid Jen-style contradiction has been obtained from forbidding
one length-2 center word. Any proof that claims `00` or `11` must recur needs
an additional global property of the finite-seed right trace; the local rule
alone leaves the phase-`01` degree of freedom above.
