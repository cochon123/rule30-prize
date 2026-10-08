# Coalescence of nearby seeds does not fire inside the light cone

Attack on prize problems 1 and 3, from the unused ideas7 prompt
“coupling from the past / coalescence of two seeds that agree on \([-T,T]\)”.
Left-permutivity of Rule 30 forbids coalescence of a left disagreement before
it reaches the centre. This is not a prize claim.

Certifier: `research/coalescence.py`. Dump: `research/coalescence.json`.
Does not modify `experiment.py`, `strip_graph.py`, or `strip_extend.py`.

## Theorem

Let \(F\) be Rule 30, \(x'_{j}=x_{j-1}\oplus(x_j\lor x_{j+1})\). Write
\(c_t(x)\) for site \(0\) of \(F^t(x)\). Suppose two configurations \(x,y\)
satisfy \(x_j=y_j\) for all \(|j|\le W\) and \(x_{-W-1}\ne y_{-W-1}\). Then

\[
c_t(x)=c_t(y)\qquad\text{for all }0\le t\le W,
\]
and
\[
c_{W+1}(x)\ne c_{W+1}(y).
\]

Proof. The value \(c_t\) is a function of the initial interval \([-t,t]\)
only, so the centres agree through time \(W\). At time \(W+1\) the extreme
left input of the cone is \(x_{-W-1}\). Rule 30 is left-permutive: for any
fixed centre and right bits,
\[
0\oplus(b\lor r)=b\lor r,\qquad 1\oplus(b\lor r)=\lnot(b\lor r),
\]
so flipping the left neighbour flips the output. Inductively, flipping the
extreme left ancestor of a space-time triangle flips the apex. Hence
\(c_{W+1}\) flips.

## Machine check

For the prize seed \(\delta_0\) versus \(\delta_0+\delta_{-W-1}\), the first
centre disagreement is exactly time \(W+1\), for every \(W=0,\ldots,48\).
Right-side perturbations at \(+W+1\) never affect the centre before time
\(W+1\) (the right cone bound); they need not flip it, because the rule is
not right-permutive.

## Why it died

Preregistered kill: coalescence inside the cone. Seeds that agree on a
centred window remain coupled exactly until the window’s left edge arrives,
then a left disagreement is copied to the centre. There is no earlier
identification of distinct exteriors, and no \(o(W)\) dependence of \(c_W\)
on a proper subwindow. Coupling-from-the-past therefore does not compress
the prize orbit. Not a prize claim.
