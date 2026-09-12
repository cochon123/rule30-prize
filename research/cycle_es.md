# Cycle ES: reconstruct is rotation-equivariant; 2-power \(n_0\) partitions into classes of size \(2n_0\)

Unique continuation \(u_{t+1}=a_t\oplus(b_t\lor u_t)\) is cyclic-shift
invariant, so
\(\operatorname{reconstruct}(\operatorname{rot}^k a,\operatorname{rot}^k b)=\operatorname{rot}^k\operatorname{reconstruct}(a,b)\)
when defined. Starting from \((0,T_0\|\neg T_0,1)\), the all-0 and
all-1 bits are shift-invariant, hence the first ident-0 extra and its
even/odd kind are constant on the rotation class of \(T=T_0\|\neg T_0\).
For 2-power \(n_0\), \(T\) has min period \(2n_0\) (any proper period
would divide \(n_0\) and force \(T_0[0]=\neg T_0[0]\)), so the classes
have size \(2n_0\) and partition all \(2^{n_0}\) words. Cycle DI already
had the \(n_0=4\) orbits; this cycle is the same fact for every 2-power
\(n_0\). Kills: extras attach to isolated \(T_0\)s; \(n_0=8\) families
of 16 are coincidental; \(T\) can have period \(<2n_0\) for 2-power
\(n_0\). Do **not** claim a formula for extra 414990. Do **not** claim
every class eventually hits ident-0. Do **not** bump all \(n_0=16\)
past 414990. Do **not** claim an 11-bit gap. Do **not** compute
\(\varphi^{(3,5,9)}\) at \(k=16\). Do **not** push the \(n_0=2\) seed
past \(k=21\).

Not a prize claim: rotation classes do not give covering never-fail or
at-most-one-odd for all \(k\).

Helper: `python3 research/cycle_es.py --certify`. Dump:
`research/cycle_es.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles DI, DM, DN, EP, ER. Exhaustive reconstruct
equivariance on rings of length 4 and 8; `census(8, 53000)` for the
sixteen \(n_0=8\) classes. No new packed run, no Fermat table, no
\(n_0=16\) window past 414990.

## Lemma (reconstruct is rotation-equivariant)

For every \(a,b\) of length \(L\in\{4,8\}\) and every shift \(k\),
\(\operatorname{reconstruct}(\operatorname{rot}^k a,\operatorname{rot}^k b)\)
equals \(\operatorname{rot}^k\operatorname{reconstruct}(a,b)\) when
either side is defined (and both are undefined when \(b\equiv 0\)).
Random trials on \(L=16,32\) agree.

## Lemma (2-power \(n_0\): min period of \(T\) is \(2n_0\))

If \(T=T_0\|\neg T_0\) had period \(d\mid 2n_0\) with \(d\le n_0\), then
\(T[n_0]=T[0]\), so \(T_0[0]=\neg T_0[0]\). For \(n_0=2^m\) every proper
divisor of \(2n_0\) divides \(n_0\). Certified for every \(T_0\) of
length \(2,4,8,16\): class counts \(1,2,16,2048\).

## Lemma (\(n_0=2,4,8,16\) classes)

- \(n_0=2\): one class of 4, extra 22 (odd).
- \(n_0=4\): FAM89 and FAM372 partition all 16 words (Cycle DI).
- \(n_0=8\): 16 classes of 16. Nine extras in 53000, all full 16-classes
  (Cycle DM counts); seven miss, representatives
  `00011000`, `00100100`, `00110100`, `01010100`, `01011000`,
  `01101000`, `01110000`. Prize \(T_0=00000110\) is the extra-52809
  class.
- \(n_0=16\): 2048 classes of 32. FAM414990 is the class of \(T^*\)
  (Cycle ER).

## Killed

Ident-0 extras are not properties of isolated \(T_0\) strings: they are
invariants of the rotation class of \(T_0\|\neg T_0\). The \(n_0=8\)
families of 16 are the forced class size \(2n_0\), not a coincidence.
For 2-power \(n_0\), \(T\) never has period \(<2n_0\).

## Verdict

`LEMMA` (reconstruct rotation-equivariant; extra constant on class;
2-power min period \(2n_0\); class counts at \(n_0=2,4,8,16\)).
`KILLED` (extras attach to isolated \(T_0\); \(n_0=8\) size-16
coincidental; period \(<2n_0\) for 2-power \(n_0\)).
`PREFIX` (formula for extra 414990; every class eventually hits;
at-most-one-odd for all \(k\); seed for all \(k\); \(\pi\) formula;
Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_es.md` (this note)
- `research/cycle_es.py`
- `research/cycle_es.json`
