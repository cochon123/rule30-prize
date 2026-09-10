# Period-2 L_0: inductive polynomial certificates

This note records an attack on “no last 1 in \(F_k\)”. It does **not**
exclude eventual period 2, and it does not claim a prize result.

Helper: `research/period2_certificate.py --certify`.
Notation as in `research/period2_left_edge.md` and
`research/period2_vacuum.md`. Work in the Boolean Fibonacci ring

\[
\mathcal B=\mathbb F_2[u_0,u_1,\ldots]/\langle u_i^2+u_i,\ u_i u_{i+1}\rangle,
\]

with shift \(S(u_i)=u_{i+1}\) and

\[
F_k=G_{k-1}+(F_{k-1}\lor F_{k-2}),\qquad
G_k=SF_{k-1}+(G_{k-1}\lor G_{k-2}).
\]

A certificate of length \(R\) for onset \(T\) is an identity in \(\mathcal B\)

\[
F_T=\sum_{j=1}^{R} A_{T,j}F_{T+j}.
\]

On Fibonacci strings this is equivalent to: no \(u\) has \(F_T=1\) and
\(R\) further zeros. Such an identity for **every** \(T\), with some
constructive \(R(T)\), would kill every \(L_0\) onset and hence period 2
for every finite seed. Compactness says that if the infinite tail
\(F_k=0\) (\(k>T\)) is already unsatisfiable, some finite \(R\) exists;
the missing step is a construction covering all \(T\).

**Outcome.** No \(T\)-uniform (and no all-\(T\)) constructive certificate.
Linear multipliers exist through \(T=12\) (with \(T=4\) identically zero)
and fail at \(T=16\) and \(T=20\). Shift and \(T\mapsto T+2\) do not close.
Residual fold windows grow with the \(u\)-prefix; last-1 / Hamming ranks
are not well-founded. The zero-run/shift identity is real, but shortens
the zero tail by two columns per step, too fast to push an onset of width
\(T\) onto vacuum.

## Proved (ANF in \(\mathcal B\))

All identities below are reduced modulo \(u_i u_{i+1}=0\) and checked by
`check_anf_cert` against `compute_columns`.

- \(F_4=0\). \(F_8=u_1 u_3\). \(F_3=S F_1\), \(F_6=S^2 F_2\), \(F_7=S F_5\).
  These three shift equalities are the **only** coincidences
  \(F_k=S^s F_t\) with \(k\le 16\), \(s\in\{1,2,3,4\}\), \(F_k\neq 0\).
- \(F_1=F_2+(u_2+u_3)F_3+F_7+F_8\).
- \(F_2=u_0 F_3\).
- \(F_3=F_5+F_6\).
- \(F_5=u_4 F_6+(u_4+u_1)F_7+F_9\).
- \(F_6=u_4 F_7+F_{10}\).
- \(F_7=(1+u_3)F_9+u_4 F_{10}\).
- \(F_8=(u_6+u_4)(F_9+F_{10})+u_6 F_{11}+(u_7+u_6)F_{12}
  +u_7(F_{13}+F_{14})+(1+u_4)F_{15}+u_8 F_{16}
  +(1+u_6+u_5+u_4)F_{17}+(1+u_6)F_{18}\).
- \(F_9=(1+u_4)F_{10}+(u_6+u_5)F_{11}+u_7(F_{12}+F_{13})
  +(1+u_7+u_4)F_{15}+F_{16}\).
- \(F_{10}=(1+u_6+u_2)F_{11}+u_7 F_{12}+(1+u_6)F_{13}+u_7 F_{14}+u_4 F_{16}\).
- \(F_{11}=(u_6+u_3)F_{12}+(1+u_4)F_{13}+F_{14}\).
- \(F_{12}=(u_5+u_3+u_1 u_3)F_{13}+u_3 F_{14}\) (quadratic).

So every \(T\le 12\) has an explicit identity in \(\mathcal B\), with
\(R(T)\) equal to the killing distance from the onset table
(\(R(4)=0\) via \(F_4=0\)). The multipliers are linear in the \(u_i\)
except at \(T=12\).

There is **no** linear-multiplier identity for \(T=16\) with \(R=10\)
nor for \(T=20\) with \(R=17\), on the full Fibonacci tables of length
`nvars(T+R)`. Degree 0 (constant \(A_j\)) works only for \(T=3\) among
the cases tested. A uniform linear template is dead.

## Proved (value identity on a 1 followed by two zeros)

Spatial: \(G_k=F_{k+1}+(F_k\lor F_{k-1})\) for \(k\ge 1\)
(`certify_spatial_identity` in `period2_vacuum.py`). Fold:
\(G_k=F_{k-1}(Su)+(G_{k-1}\lor G_{k-2})\).

**Lemma.** If \(F_T(u)=1\) and \(F_{T+1}(u)=F_{T+2}(u)=0\), then
\(G_T(u)=G_{T+1}(u)=1\) and

\[
F_{T+3}(u)=1+F_{T+1}(Su).
\]

Proof: \(G_T=0+(1\lor F_{T-1})=1\), \(G_{T+1}=0+(0\lor 1)=1\),
\(G_{T+2}=F_{T+1}(Su)+(1\lor 1)=1+F_{T+1}(Su)\), and
\(F_{T+3}=G_{T+2}+(0\lor 0)\). Checked on the variety for \(T=1..12\)
(\(T\neq 4\)).

**Corollary.** An \(L_0\) tail with \(R\ge 3\) forces \(F_{T+1}(Su)=1\).
The same expansion gives \(F_{T+4}=1+F_{T+2}(Su)\) after one more zero,
then \(F_{T+5}=F_{T+3}(Su)\), \(F_{T+6}=F_{T+4}(Su)\) (pattern break:
the “\(1+\)” lasts two steps). On every last-sat model of
\(T\in\{8,16,20,22\}\), the window of \(F_\bullet(Su)\) at indices
\(T..T+7\) is exactly \(01100000\): two consecutive 1s at \(T+1,T+2\),
then zeros. So \(S\) sends a long \(L_0\) germ to a **different** germ
(a length-2 bump), not to \(L_0\) at a smaller \(T\).

If a zero run of length \(R\) transferred to \(Su\) with only a
constant loss of columns, \(R/2\) shifts would kill the run, while
vacuum is \(nvars(T+R)\approx(T+R)/2\) shifts away. The inequality
\(R/2\ge(T+R)/2\) forces \(T\le 0\). Zero-run propagation therefore
**cannot** reduce \(L_0\) to the already-proved eventual-vacuum lemma.
That is the precise obstruction to a shift-induction.

## Computational: onset certificates \(T=1..32\)

Sound scan, exactly `nvars(T+R)` Fibonacci strings
(`onset_table`). Every \(T\le 32\) dies at finite extra \(R\). Worst
remains \(T=20\), \(R=16\), killed by \(F_{37}\). Through \(T=32\),
\(\max R=16\); this is **not** a proof that \(R\le 16\) for all \(T\).

Boolean Nullstellensatz particular solution, checked by evaluation:
\(F_T\prod_{j=1}^{R}(1+F_{T+j})=0\) at the killing \(R\), hence
\(F_T\) lies in the ideal. Verified for \(T=1,2,8,16,20,22\). This is
compactness made explicit, not a uniform construction: the multipliers
are the tautological cofactors of the product, of degree growing with
\(R(T)\).

### \(T=8\) (unique last-sat word)

Forced prefix `010101001`, support \(\{1,3,5,8\}\). This is
\(F_8=u_1 u_3=1\) plus the extra bits that delay the next 1 until
\(F_{18}\). Among all \(u\) with \(F_8=1\), the first later 1 already
occurs at 11, 15, 17, or 18; the unique length-9 survivor is the last
of those. The linear identity above is the compact certificate.
\(S^2\) of this word is the unique last-sat word of \(T=12\)
(`0101001`). That \(T\mapsto T+4\) coincidence does **not** continue
to \(T=16\).

### \(T=16\)

`maxR=9`, four models, forced `.0...0..00001`, killed by \(F_{26}\).
Supports \(\{3,7,12\}\), \(\{2,4,6,12\}\), \(\{0,3,7,12\}\),
\(\{0,2,4,6,12\}\). Linear multipliers fail. Tautological \(R=10\)
holds on 610 strings.

### \(T=20\) (longest; six last-sat words)

Forced `....00010010010001`. All six length-18 survivors share the
period-3 tail `00010010010001` from index 4, and differ only by a
Fibonacci prefix of length 4, excluding `0001` and `1001`:

```
0000 00010010010001
0010 00010010010001
0100 00010010010001
0101 00010010010001
1000 00010010010001
1010 00010010010001
```

Each has \(u_{17}=1\), so the next bit \(u_{18}\) is illegal. The unique
legal extension is a trailing 0, and \(F_{37}=1\) on all six
(`certify_t20_explicit`). That is a complete finite certificate for this
\(T\), not a template for \(T+2\): \(T=22\) is a similar but not shifted
`10010010001` tail, with seven models and \(R=12\).

Two families appear repeatedly and do **not** exhaust the table:

- isolated odd 1s (`01` repeating): \(T=1,8,12,15,21,27\);
- period-3 `100` runs: \(T=20,22,26,29\).

Mixed forced masks (\(T=16,19,24,28,31,32\)) proliferate. There is no
finite list of monomial templates covering all \(T\).

## Shift and \(T\mapsto T+2\) do not close

On last-sat models:

- Prepending two zeros never lands in the last-sat variety of \(T+2\).
- Dropping \(u_0,u_1\) almost never does (exception: the single
  \(T=8\to T=12\) word above).
- \(S\) (drop \(u_0\)) lands in the \(T+2\) last-sat set for some \(T\)
  (1, 8, 9, 10, 16, 20) and not others (3, 5, 6, 7, 11–15, 17–19).
- \(F_\bullet(Su)\) is **not** an \(L_0\) of smaller width:
  `n_Su_L0_smaller=0` except the two \(T=3\) models. The last 1 of
  \(Su\) moves **right** (\(T=20\): last 1 at 44, past \(T+R=36\)).

So neither \(S\) nor \(T\mapsto T+2\) is a rank, and a certificate at
\(T\) does not transport.

## Automata / residual fold constraints

Folding is causal from the right. After a Fibonacci suffix of length
\(p\), the window \(W=(F_T,\ldots,F_{T+R})\) takes

- \(T=8\), \(R=10\): 1, 1, 1, 2, 4, 6, 10, 16, 25, 40 distinct windows
  for \(p=0..9\) (89 suffixes at \(p=9\));
- \(T=20\), \(R=16\): 1, …, 96 windows at \(p=12\) (377 suffixes).

The set is finite for each fixed \((T,R)\) (at most \(2^{R+1}\)), which
is compactness again. It does not stabilize at a \(T\)-independent
quotient: the number of live windows tracks a positive fraction of
Fibonacci suffixes as \(p\) grows, up to the window cap which itself
grows with the (non-uniform) \(R(T)\).

Candidate ranks on that window: index of the last 1, and Hamming
weight. Both **increase** under a legal extra fold (73 / 230 folds
raise last-1 for \(T=8\); 52 / 230 for \(T=20\)). No well-founded rank
of that form.

The 16-state vacuum FSM of `period2_vacuum.py` remains available only
when the \(u\)-suffix is already all zeros. That is the eventually-zero
case, already excluded.

## What is not proved

- Any \(R(T)\) given by a closed form, even \(R(T)=O(T)\). Empirically
  \(R(T)\le 16\) for \(T\le 32\), which would finish period 2 if it
  continued, and is not a theorem.
- Ideal membership of \(F_T\) in \(\langle F_{T+1},\ldots,F_{T+R}\rangle\)
  for a single constructive \(R\) that works for all \(T\ge 13\).
- A finite quotient of residual fold constraints compatible with every
  continuation of \(u\).
- Eventual period 2 of the prize seed.

## Strongest honest lemma

**Lemma (certificates through width 12; linear template dies later).**
In \(\mathcal B\), \(F_T\) lies in the ideal generated by
\(F_{T+1},\ldots,F_{T+R(T)}\) for every \(1\le T\le 12\), with explicit
multipliers as above and \(R(4)=0\). The same linear ansatz
(\(A_j\in\mathrm{span}\{1,u_i\}\)) fails for \(T=16\) and \(T=20\).
For every \(T\le 32\) some finite \(R(T)\) still exists by exhaustive
Fibonacci enumeration of the exact variable bound; the worst is
\(T=20\), \(R=16\).

Together with the eventual-vacuum lemma, every \(L_0\) onset that is
either of width \(\le 12\) or driven by an eventually-zero \(u\) is
impossible. Infinitely supported \(u\) at large \(T\) remains open.

## Why the attack dies as a uniform construction

Three independent obstructions, any one of which blocks a
\(T\)-independent certificate of the form sought:

1. **Residual memory scales with \(T\).** \(F_T\) depends on
   \(\lfloor(T-1)/2\rfloor+1\) bits. After a legal prefix those bits
   remain as a free Fibonacci germ; later zeros constrain a
   *different* set of variables. The surviving germs are not a finite
   list of monomials (01-family, 100-family, and mixed masks).
2. **Shift loses two columns per step.** The only exact coupling
   between \(F_\bullet(u)\) and \(F_\bullet(Su)\) on an \(L_0\) germ
   turns a 1-then-zeros into a 11-then-zeros of strictly smaller
   tail. It cannot reach vacuum while an onset of width \(T>0\) is
   still present, so it does not reduce to the 16-state machine.
3. **No well-founded rank on fold windows.** Last-1 position and
   Hamming weight increase; \(S\) sends last-sat models to strings
   whose last 1 is *farther* left.

A prize-relevant next lemma would need a new coupling — seed-finite
right support, ancestry depth, or a rank that uses both edges — not
another onset table.

## Files

- `research/period2_certificate.md` (this note)
- `research/period2_certificate.py` (`--certify` checks the ANF
  identities, the \(T+3\) value lemma, linear failure at \(T=16,20\),
  and the six-word \(T=20\) certificate)
- `research/period2_vacuum.py` / `period2_vacuum.md` (variable bound,
  vacuum FSM, sound onset idea)
- `research/period2_left_edge.py` / `period2_left_edge.md` (ANF engine,
  \(F_4=0\), \(F_8=u_1 u_3\))
