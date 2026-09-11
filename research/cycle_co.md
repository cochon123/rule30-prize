# Cycle CO: a `10` two pairs back forces inequality; seed `10`s at \((1,S)\) and \((S,U)\)

If \(A=1\) and \(B=0\) at any time, the split \(B=0\Rightarrow DC=A\) gives
\(DC=1\ne 0=B\), so \(D=\operatorname{reconstruct}(B,C)\) differs from
\(C\). A `10` in \((A,B)\) therefore makes the pair two steps later
unequal. \((1,S)\) always has a `10` (\(T\) has a \(1\)) and \((S,U)\)
always has a `10` (\(T\) has a `00`), so \(U\ne V\) and \(V\ne W\) for
every even \(|T_0|\ge 2\). Ident-\(0\) and ident-\(1\) never form a
`10` with their neighbours. `10` does not persist at every later pair
(\((U,V)\) misses it). Not a prize claim.

Helper: `python3 research/cycle_co.py --certify` (~1.3s). Dump:
`research/cycle_co.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (skip-\(2\) from `10`)

Packed update of \(C=\operatorname{reconstruct}(A,B)\) has
\(B=0\Rightarrow DC=A\). A `10` is a time with \(A=1,B=0\), hence
\(DC=1\ne B\), so \(D=\operatorname{reconstruct}(B,C)\) satisfies
\(D\ne C\). Pointwise on the two values of \(C\), and on every `10`
along the scar chain through even length \(16\) (\(212196\) events).

## Lemma (seed `10`s)

Nonconstant \(T=T_0\|\lnot T_0\) has a \(1\), so \(S=\lnot T\) shifted
has a \(0\), and \((1,S)\) has a `10`. It also has a `00` (not
alternating), which forces \(S=1,U=0\), so \((S,U)\) has a `10`.
The pairs \((0,T)\) and \((T,1)\) never have a `10`.

## Lemma (\(U\ne V\) and \(V\ne W\) from seeds)

Skip-\(2\) from \((1,S)\) gives \(U\ne V\). Skip-\(2\) from \((S,U)\)
gives \(V\ne W\). This is the qualitative form of Cycles CK and CL,
for every even \(|T_0|\ge 2\), without run-length Hamming.

## Every pair has a `10` — killed

\((U,V)\) lacks a `10` on some blocks (including both length-\(2\)
blocks). **Killed.** Skip-\(2\) therefore does not by itself protect
every later pair.

## Prefix (every \(2\)-power \(|T_0|\))

A `10` at every later pair is not proved. No later ident-\(0\) on a
window as long as the next high half remains a prefix. **PREFIX**.

## Verdict

`LEMMA` (skip-\(2\) from `10`; seed `10`s at \((1,S)\) and \((S,U)\);
\(U\ne V\) and \(V\ne W\) from those seeds; ident-\(0\)/ident-\(1\)
never a `10`).
`KILLED` (every pair has a `10`).
`PREFIX` (every \(2\)-power \(|T_0|\); at most one odd toggle for
all \(k\); seed for all \(k\); Fermat covering).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_co.md` (this note)
- `research/cycle_co.py`
- `research/cycle_co.json`
