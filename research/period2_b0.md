# Period-2 \(L_0\): the 11-bump \(B_0\) and a descent of finite \(R\)

Checked lemma: a long \(L_0\) onset becomes, under the Fibonacci shift
\(S\), a length-2 bump \(B_0\) (\(F_S=F_{S+1}=1\), then zeros) whose
zero-run is four shorter than the original. On \(B_0\) one has
\(G_S=0\), \(G_{S+1}=G_{S+2}=1\), and \(S\) sends \(B_0(S,R)\) to
\(B_0(S+2,R-4)\). Finite \(R\) therefore descends once the onset is a
bump. Infinite \(L_0\) still maps to infinite \(B_0\) at larger \(S\),
so this is not a uniform bound. Isolated onsets (\(F_{T-1}=0\)) have
\(\max R\le 9\) through \(T=22\); every last-sat with \(R\ge 12\) is a
bump. Not a prize claim.

Helper: `python3 research/period2_b0.py --certify`. Dump:
`research/period2_b0.json`. Notation as in
`research/period2_germ.md`. The three-zero skip of
`research/period2_qshift.md` is not used in the proofs below.

## Lemma (\(L_0\) to \(B_0\) tail)

Suppose \(F_T=1\) and \(F_{T+1}=\cdots=F_{T+R}=0\) with \(R\ge 4\),
\(T\neq 4\). Spatial reconstruction gives \(G_k=0\) for every
\(T+2\le k\le T+R-1\). The germ identities of
`research/period2_germ.md` already yield
\[
F_T(Su)=0,\qquad F_{T+1}(Su)=F_{T+2}(Su)=1.
\]
Fold at \(k\in[T+4,T+R-1]\) then gives \(F_{k-1}(Su)=0\), i.e.
\(F_j(Su)=0\) for \(T+3\le j\le T+R-2\). So \(Su\) is a \(B_0\) onset
at \(S=T+1\) with at least \(R-4\) further zeros.

## Lemma (\(B_0\) \(G\)-pattern)

If \(F_S=F_{S+1}=1\) and \(F_{S+2}=0\), then \(G_S=0\). If also
\(F_{S+3}=0\), then \(G_{S+1}=G_{S+2}=1\). Proof is spatial:
\(G_S=1\oplus(1\lor F_{S-1})=0\), independent of \(F_{S-1}\);
\(G_{S+1}=0\oplus 1=1\); \(G_{S+2}=0\oplus 1=1\).

## Lemma (\(B_0\) to \(B_0\) under \(S\))

Suppose \(F_S=F_{S+1}=1\) and \(F_k=0\) for \(S+2\le k\le S+1+R\) with
\(R\ge 4\). Then \(G_S=0\), \(G_{S+1}=G_{S+2}=1\), and \(G_k=0\) for
\(S+3\le k\le S+R\). Fold reconstruction
\(F_{k-1}(Su)=G_k\oplus(G_{k-1}\lor G_{k-2})\) yields
\[
F_{S+1}(Su)=0,\qquad
F_{S+2}(Su)=F_{S+3}(Su)=1,\qquad
F_j(Su)=0\text{ for }S+4\le j\le S+R-1.
\]
So \(Su\) is \(B_0\) at \(S+2\) with at least \(R-4\) further zeros.

## Corollary (finite bump rank)

A finite \(B_0\) of run \(R\) becomes, after \(\lfloor R/4\rfloor\)
shifts, a bump of run \(<4\). This is a rank on *finite* extra zeros,
not on an infinite \(L_0\) tail: \(R=\infty\) is fixed by \(R\mapsto
R-4\), and \(S\) increases.

## Checks

- Every Fibonacci word of length 12: \(G\)-pattern at every 11-bump
  with a following 0.
- Last-sat \(L_0\) of
  \((T,R)\in\{(8,9),(15,6),(16,9),(20,16),(22,12),(26,5)\}\): \(Su\) is
  \(B_0\) at \(T+1\) with \(\ge R-4\) zeros. \(T=20\) and \(T=22\) have
  \(F_{T-1}=1\) (already \(B_0\)); the others are isolated.
- The six \(T=20\) words are \(B_0\) at \(S=19\), \(R=16\), \(G=(0,1,1)\);
  \(S\) sends them to \(B_0\) at \(S=21\), \(R=12\).
- Sound split through \(T=22\): isolated \(\max R\le 9\); bump
  \(\max R=16\) uniquely at \(T=20\); every \(R\ge 12\) last-sat is a
  bump.

## What this does not do

An infinite \(L_0\) produces an infinite \(B_0\) chain at
\(S,S+2,S+4,\ldots\), all with infinite run. The descent does not
hit the empty bump-table at \(S\in\{1,3,\ldots,8\}\), which lies at
*smaller* \(S\). Isolated onsets are empirically short, but
\(\max R\le 9\) through \(T=22\) is not a bound. A uniform \(R(T)\)
still needs a \(T\)-independent 11-clip, `00000`-clip, or even-column
fire of the forced tail (`research/period2_qshift.md`).

Periodic \(u\) is already infinite on the left
(`research/period2_periodic.md`). Aperiodic \(u\) remains the
obstruction to period 2.

## Verdict

`LEMMA`, wall time a few seconds.

- Kill of period 2: no.
- Finite bump rank under \(S\): yes.
- Uniform \(R\): no.

## Files

- `research/period2_b0.md` (this note)
- `research/period2_b0.py` (`--certify`)
- `research/period2_b0.json` (dump)
