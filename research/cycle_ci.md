# Cycle CI: first continuation is reset-toggle; \(\operatorname{ham}(U,V)=|T_0|\)

After ident-\(1\), \(S=\lambda_{I+1}\) is shifted-not \(T\) (Cycle CH) and
the unique continuation \(U=\operatorname{reconstruct}(1,S)\) obeys
\(u_{t+1}=T_{t-1}\land\lnot u_t\). The next bit
\(V=\operatorname{reconstruct}(S,U)\) equals \(U\) iff \(S=DU\) iff
\(U=S\). The last is already killed for even \(|T_0|\ge 2\), so the
second tail pair is never equal. Exhaustively through even
\(|T_0|\le 16\), \(\operatorname{ham}(U,V)=|T_0|\) and
\(\operatorname{ham}(S,U)\) is a positive multiple of \(3\). Every
nonconstant length-\(16\) block has consecutive Hamming at least \(3\)
on \(24\) extra bits. Not a prize claim: later pairs and the Fermat
covering remain prefixes.

Helper: `python3 research/cycle_ci.py --certify` (~6s). Dump:
`research/cycle_ci.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (reset-toggle)

Packed update of \(U\) against driver \(S=\lnot T\) shifted and bit
\(I\equiv 1\) is
\(u_{t+1}=1\oplus(S_t\lor u_t)=\lnot S_t\land\lnot u_t\).
Substitute \(S_t=\lnot T_{t-1}\) to get \(u_{t+1}=T_{t-1}\land\lnot u_t\):
a \(0\) in \(T\) resets the next \(U\) bit to \(0\); a \(1\) toggles.
Checked on every nonconstant even \(|T_0|\in\{2,4,\ldots,16\}\).

## Lemma (\(S=DU\) iff \(U=S\))

From the reset-toggle, \(DU_t=u_t\oplus(T_{t-1}\land\lnot u_t)\). Then
\(S=DU\) forces \(u_t=\lnot T_{t-1}=S_t\) at every \(t\), and conversely
\(U=S\) makes \(S\) alternating iff \(T\) is, already killed. Exhaustive
on the same range.

## Lemma (second tail pair never equal)

\(V=U\) iff \(S=DU\) iff \(U=S\). Cycle CH kills \(U=S\) for every even
\(|T_0|\ge 2\). Combined with the first-pair lemma, the two packed bits
after ident-\(1\) are never a consecutive equal pair.

## Lemma (\(\operatorname{ham}(U,V)=|T_0|\))

On the same range, the Hamming distance of that second pair is exactly
\(n_0=|T_0|\), never \(0\). Exhaustive (\(70982\) nonconstant blocks).

## Lemma (\(\operatorname{ham}(S,U)\) is a positive multiple of \(3\))

Values through \(n_0=16\) are \(\{3,6,\ldots,3n_0/2\}\). In particular
the first tail pair has Hamming at least \(3\) for every even
\(|T_0|\ge 2\) in this range, strengthening Cycle CH's \(n_0\in\{4,8\}\)
count.

## Lemma (\(|T_0|=16\): tail Hamming \(\ge 3\))

All \(65534\) nonconstant blocks of length \(16\), \(24\) extra bits:
zero Hamming \(0\) or \(1\), minimum \(3\). Exhaustive. Not a window as
long as a later high half; still a prefix for \(r\le 1\) at every scale.

## Prefix (every \(2\)-power \(|T_0|\))

No later ident-\(0\) is not proved for \(|T_0|\ge 32\), nor for
\(|T_0|=16\) on a window as long as the next high half. **PREFIX**.

## Verdict

`LEMMA` (reset-toggle; \(S=DU\) iff \(U=S\); second pair never equal;
\(\operatorname{ham}(U,V)=n_0\) through \(16\); \(\operatorname{ham}(S,U)\)
a positive multiple of \(3\) through \(16\); length-\(16\) Hamming
\(\ge 3\) on \(24\) extra bits).
`PREFIX` (every \(2\)-power \(|T_0|\); at most one odd toggle for
all \(k\); seed for all \(k\); Fermat covering).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_ci.md` (this note)
- `research/cycle_ci.py`
- `research/cycle_ci.json`
