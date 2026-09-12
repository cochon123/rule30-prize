# Cycle FE: covering fails iff three off-cone \(J\) from time \(2U\) vanish

Cycle AI gives
\(c_{t+2^m}=c_t\oplus x(t,\pm 2^m)\oplus J_{[t,t+2^m)\to t+2^m}\),
with the convention \(x(t,j)=0\) for \(|j|>t\). Let \(U=2^k\) and start
at time \(t=2U\). The covering steps \(4U,8U,16U\) satisfy
\(|j|\ge 2t>t\), so the spatial extras vanish and

\[
\varphi^{(q)}_k=I_{k+1}\oplus J_{[2U,\,qU)\to qU}
\qquad(q\in\{6,10,18\}).
\]

Covering fails at \(k+1\) iff those three remainders vanish, which is
exactly Cycle BO’s even-spine criterion \(\varphi^{(6)}=\varphi^{(10)}
=\varphi^{(18)}=I_{k+1}\). On Cycle DS spines through \(k=18\),
\(J_6=J_{10}=0\) occurs at the five candidates
\(k=5,8,11,15,18\) and forces \(J_{18}=1\), so the triple never
vanishes. Kills: \(J_6=J_{10}=1\Rightarrow J_{18}=0\) (counterexample
\(k=14\), where all three \(J\) are 1). Do **not** claim never-fail for
all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** compute \(\varphi^{(3,5,9)}\) at \(k=16\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\).

Not a prize claim: restating failure as three off-cone Green
remainders does not prove they never vanish for all \(k\).

Helper: `python3 research/cycle_fe.py --certify`. Dump:
`research/cycle_fe.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AI/BO/CA/DS/FD (no new packed run, no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (off-cone extras from time \(2U\))

For every \(k\ge 0\), \(t=2^{k+1}\) and \(W\in\{2^{k+2},2^{k+3},2^{k+4}\}\)
have \(W>t\). Certified \(0\le k\le 40\).

## Lemma (\(\varphi^{(q)}=I\oplus J_{[2U,qU)}\) for \(q=6,10,18\))

Cycle AI plus vanishing extras. Then covering fails iff
\(J_6=J_{10}=J_{18}=0\). Certified equivalent to even spines equal
\(I\) on Cycle DS through \(k=18\).

## Prefix (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) through \(k=18\))

The five DS candidates are exactly \(\{k:J_6=J_{10}=0\}\), and each
has \(J_{18}=1\). **PREFIX**, not a theorem for all \(k\).

## Killed

\(J_6=J_{10}=1\Rightarrow J_{18}=0\) fails at \(k=14\) (all three \(J\)
equal 1; Fermat all-ones at \(k+1=15\)).

## Verdict

`LEMMA` (off-cone extras from \(2U\); \(\varphi^{(q)}=I\oplus J\);
covering fails iff the three \(J\) vanish).
`KILLED` (\(J_6=J_{10}=1\Rightarrow J_{18}=0\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) through \(k=18\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_fe.md` (this note)
- `research/cycle_fe.py`
- `research/cycle_fe.json`
