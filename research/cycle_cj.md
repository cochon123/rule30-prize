# Cycle CJ: \(U\) is the run-parity of \(T\); \(\operatorname{ham}(S,U)=\frac32(n_0-n_{\mathrm{odd}})\)

Reset-toggle unfolds to a closed form: \(U_t\) is the length of the
\(1\)-run of \(T\) ending at time \(t-2\), modulo \(2\). Counting
\(00/01/10/11\) windows against that formula gives
\(\operatorname{ham}(S,U)=\frac32(n_0-n_{\mathrm{odd}})\), where
\(n_{\mathrm{odd}}\) is the number of odd-length \(1\)-runs of \(T\).
For even \(|T_0|\ge 2\), \(T=T_0\|\lnot T_0\) has weight \(n_0\) on
length \(2n_0\) and is not alternating, so \(n_{\mathrm{odd}}\le n_0-2\)
and the Hamming distance is at least \(3\). This is the closed form of
Cycle CI's exhaustive multiple-of-\(3\) count. Not a prize claim:
later pairs and the Fermat covering remain prefixes.

Helper: `python3 research/cycle_cj.py --certify` (~1s). Dump:
`research/cycle_cj.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (\(U\) is run-parity)

Reset-toggle is \(U_t=T_{t-2}\land\lnot U_{t-1}\). If \(T_{t-2}=0\) then
\(U_t=0\). If \(T_{t-2}=1\) then \(U_t=\lnot U_{t-1}\) and the \(1\)-run
length ending at \(t-2\) is one more than the length ending at
\(t-3\). Every \(1\)-run is bounded by a \(0\) (\(T\) has \(n_0\)
zeros), so walking from that \(0\) toggles once per \(1\) and
\(U_t\equiv r_T(t-2)\pmod{2}\). Checked on every nonconstant even
\(|T_0|\in\{2,4,\ldots,16\}\).

## Lemma (\(T_{t-2}=0\Rightarrow U_t=0\))

Immediate from \(U_t=T_{t-2}\land\lnot U_{t-1}\). If \(U_t=0\) then
the next step is \(U_{t+1}=T_{t-1}\).

## Lemma (\(\operatorname{ham}(S,U)=\frac32(n_0-n_{\mathrm{odd}})\))

\(S_t=\lnot T_{t-1}\) and \(U_t=r_T(t-2)\bmod 2\). Summing
\(S_t\oplus U_t\) over the four windows of \((T_{t-2},T_{t-1})\):

- each \(1\)-run of length \(r\) contributes \(\lfloor r/2\rfloor\)
  plus \(1\) if \(r\) is even;
- each \(0\)-run of length \(z\) contributes \(z-1\).

The \(0\)-run total is \(n_0-n_{\mathrm{runs}}\). The \(1\)-run total
is \(\frac12(n_0-n_{\mathrm{odd}})+n_{\mathrm{even}}\). Adding and
cancelling \(n_{\mathrm{even}}\) leaves
\(\frac32(n_0-n_{\mathrm{odd}})\). Exhaustive on the same range.

## Lemma (\(\operatorname{ham}(S,U)\ge 3\) for every even \(|T_0|\ge 2\))

\(T=T_0\|\lnot T_0\) has weight \(n_0\) on length \(2n_0\). Then
\(n_{\mathrm{odd}}\equiv n_0\pmod{2}\), and no-\(11\) uses all \(n_0\)
zeros as separators, so the only balanced no-\(11\) string is
alternating. Cycle CH kills alternating. Any \(1\)-run of length
\(\ge 2\) drops \(n_{\mathrm{odd}}\) by at least \(2\), hence
\(n_{\mathrm{odd}}\le n_0-2\) and
\(\operatorname{ham}(S,U)\ge\frac32\cdot 2=3\). In particular the
first tail pair is never equal, with a uniform gap of \(3\), for every
even \(|T_0|\ge 2\).

## Prefix (every \(2\)-power \(|T_0|\))

No later ident-\(0\) is not proved past the first pair, nor for
\(|T_0|\ge 32\) on a long window. \(\operatorname{ham}(U,V)=|T_0|\)
remains exhaustive through \(16\). **PREFIX**.

## Verdict

`LEMMA` (\(U\) is run-parity; zeros of \(T\) reset \(U\);
\(\operatorname{ham}(S,U)=\frac32(n_0-n_{\mathrm{odd}})\);
\(\operatorname{ham}(S,U)\ge 3\) for every even \(|T_0|\ge 2\)).
`PREFIX` (every \(2\)-power \(|T_0|\); at most one odd toggle for
all \(k\); seed for all \(k\); Fermat covering).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_cj.md` (this note)
- `research/cycle_cj.py`
- `research/cycle_cj.json`
