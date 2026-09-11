# Cycle CQ: \(V\) always has consecutive \(1\)s; fifth tail pair closed

Every even \(T_0\|\lnot T_0\) has a `11` in \(V\): a \(1\)-run of \(T\) of
length at least \(3\), or a `0011`, or a `001`. Skip-\(2\) from a `10`
in \((V,W)\) gives \(Y\ne X\). If instead \(V\to W\), that `11` forces
\(W_t=W_{t+1}=1\) with \(X_{t+1}=0\ne 1=V_{t+1}\), which is Cycle CN's
witness \(B\). Hence \(Y\ne X\) for every even \(|T_0|\ge 2\). This
closes the length-\(16\) census of the fifth tail pair. Not a prize
claim.

Helper: `python3 research/cycle_cq.py --certify`. Dump:
`research/cycle_cq.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (\(V\) has a `11`)

Three exhaustive sources, using Cycle CK's split and Cycle CP's incoming
\(V=0\) at every \(0\)-run start.

1. A \(1\)-run of length \(\ge 3\). At the even offset of the run,
   \(U=0\) and the previous \(U=1\) sets \(V=T_{\mathrm{second}}=1\). The
   next bit is \(V\oplus\lnot T_{\mathrm{third}}=1\).
2. Else every run of \(T\) has length \(1\) or \(2\). Not alternating, so
   some run has length \(2\); the half-period bijection supplies a
   length-\(2\) \(0\)-run and a length-\(2\) \(1\)-run.
   - If some `00` is followed by `11`, the length-\(2\) \(1\)-run has
     even previous \(0\)-run, so \(V=1\) at its first odd offset and
     \(V_{\mathrm{next}}=T_{\mathrm{second}}=1\).
   - Otherwise every `00` is followed by an isolated \(1\). Incoming
     \(V=0\) then two \(U=0\) steps with \(T_{t-1}=01\) yield consecutive
     \(1\)s.

Checked on every nonconstant even \(|T_0|\in\{2,4,\ldots,16\}\)
(\(68256\) by (1), \(2098\) by `0011`, \(628\) by `001`).

## Lemma (skip-\(2\) or \(V\to W\) with witness \(B\))

If \((V,W)\) has a `10`, skip-\(2\) from Cycle CO gives \(Y\ne X\). If
\(V\to W\) and \(V_t=V_{t+1}=1\), then \(W_t=1\) (else a `10`) and
\(U_t=0\) (else \(W_{t+1}=0\) with \(V_{t+1}=1\)). Then
\(W_{t+1}=\lnot U_t=1\) and \(X_{t+1}=\lnot V_t=0\ne V_{t+1}\). That is
witness \(B\) of Cycle CN, so \(W\ne DX\) and \(Y\ne X\).

On the certified range, \(V\to W\) on \(20\) blocks (all length \(10\));
the rest have a `10` in \((V,W)\). The local argument does not use that
count.

## Lemma (fifth tail pair never equal)

Every even \(|T_0|\ge 2\) has a `11` in \(V\), hence either skip-\(2\) or
witness \(B\). Together \(Y\ne X\), including the \(20\) blocks where
skip-\(2\) from \((V,W)\) fails. Combined with Cycles CH–CP, the five
packed bits after ident-\(1\) are never a consecutive equal pair.

## Prefix (every \(2\)-power \(|T_0|\))

The sixth pair is not proved. No later ident-\(0\) on a window as long
as the next high half remains a prefix. Do not claim every pair has a
`10`. Do not classify a sixth pair unless a closed witness appears.
**PREFIX**.

## Verdict

`LEMMA` (\(V\) has a `11`; skip-\(2\) or \(V\to W\) with witness \(B\);
fifth pair never equal for every even \(|T_0|\ge 2\)).
`PREFIX` (every \(2\)-power \(|T_0|\); sixth pair; at most one odd
toggle for all \(k\); seed for all \(k\); Fermat covering).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_cq.md` (this note)
- `research/cycle_cq.py`
- `research/cycle_cq.json`
