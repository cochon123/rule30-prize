# Cycle GM: at a cone-hi hit, even-\(r\) Green is \(G(U(Q-q)-1,W/2-r/2)\)

Cycle GL’s even \(r\) have even degree \(W-r\). Cycle GJ’s clock
\(m=2U(Q-q)-2\) is even, so freshman gives
\(G(m,W-r)=G(U(Q-q)-1,W/2-r/2)\). The half-index \(\rho=r/2\) runs
through an interval of length \(U\). The reduced clock is **not**
\(U-1\) on pre-cone hits; a naive half-index on odd \(r\) can be 1
while \(G=0\); reduced \(G\) is **not** identically 1. Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: a freshman half-step on even \(r\) does not prove
covering never-fail.

Helper: `python3 research/cycle_gm.py --certify` (~0.01s). Dump:
`research/cycle_gm.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/GJ/GK/GL (algebraic \(k\le 11\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (\(G(m,W-r)=G(U(Q-q)-1,W/2-r/2)\); \(\rho\)-interval length \(U\))

Certified \(k\le 11\), \(W\in\{4U,8U,16U\}\). Last hit \(q=Q-1\)
reduces to the Mersenne clock \(U-1\).

## Killed

Naive half on odd \(r\): at \(k=2\), \(W=8U\), \(r=5\), \(G=0\) but
\(G(m/2,(W-r)//2)=1\). Reduced clock \(U-1\) on pre-cone: at
\(k=2\), \(W=8U\), \(q=0\), degree \(7\neq 3\). Reduced \(G\)
identically 1: at \(k=2\), \(W=4U\), \(r=8\), \(G_{\mathrm{red}}=0\).

## Verdict

`LEMMA` (even-\(r\) freshman half-step; \(\rho\)-interval length \(U\)).
`KILLED` (odd-\(r\) naive half; reduced clock \(U-1\) on pre-cone;
reduced \(G\) identically 1).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_gm.md` (this note)
- `research/cycle_gm.py`
- `research/cycle_gm.json`
