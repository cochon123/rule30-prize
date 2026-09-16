# Period-2 \(L_0\): 11-clip extra of a bump descends by 2

Checked lemma: a ugap bump onset (\(F_T=F_{T-1}=1\)) whose Q-forced
tail 11-clips with extra \(e\ge 3\) has \(Su\) a bump 11-clip at
\(T+2\) with extra \(e-2\). Extra of a 11-clip bump family is
therefore a rank. Uniform extra \(\le 8\) on this class is equivalent
to extra \(\le 8\) at every \(S\)-minimal member, which is **not**
proved. Isolated onsets and even-\(F\) clips are outside the identity.
Not a prize claim.

Helper: `python3 research/period2_exdesc.py --certify`. Dump:
`research/period2_exdesc.json`. Skip identity from
`research/period2_qshift.md`; \(B_0\) pattern from
`research/period2_b0.md`; clip-to-\(R\) from
`research/period2_qextra.md`.

## Lemma (skip at a 11-clip of extra \(\ge 3\))

Write \(n_0=\mathrm{nvars}(T)\) and \(n_\ast=n_0+e\). A 11-clip has
\(R=2n_\ast-T\), so \(e\ge 3\) gives \(R\ge 6\) and
\(F_k=0\) for every \(T<k\le 2n_\ast\). The three-zero skip
\(Q_n(u)=Q_{n-1}(Su)\) needs \(2n-3>T\). This holds at
\(n=n_\ast\) and at \(n=n_\ast-1\):
\[
2(n_\ast-1)-3=2n_\ast-5=T+R-5\ge T+1.
\]
Certified as arithmetic for every \(T\in[5,80]\) and \(e\in[3,11]\).

## Lemma (11-clip extra descent)

Assume a bump, a 11-clip, and \(e\ge 3\). Then
\(Q_{n_\ast}(u)=1\) and \(u_{n_\ast-1}=1\). Skip at \(n_\ast\) and
\(n_\ast-1\) gives
\[
Q_{n_\ast}(u)=Q_{n_\ast-1}(Su),\qquad
u_{n_\ast-1}=Q_{n_\ast-1}(u)=Q_{n_\ast-2}(Su),
\]
so \(Su\) 11-clips at \(n_\ast-1\). Also \(\mathrm{nvars}(T+2)=n_0+1\),
hence the extra of \(Su\) at \(T+2\) is \(e-2\). The \(B_0\) identity
makes \(Su\) a bump at \(T+2\) once \(R\ge 4\).

Certified on every ugap bump 11-clip of extra \(\ge 3\) through
\(T=40\): 122 onsets, 122 descents, 0 failures. The same scan has
max extra \(8\), uniquely at \(T=20\) (three words) and \(T=37\)
(three words). Those two families descend to extra \(6\) at \(T=22\)
and \(T=39\).

## Corollary (rank, not a bound)

Iterating, a 11-clip bump of extra \(e\ge 3\) reaches extra
\(<3\) after \(\lfloor(e-1)/2\rfloor\) shifts of \(+2\) in \(T\).
Equivalently extra \(=e_{\mathrm{ker}}+2m\) with
\(e_{\mathrm{ker}}\in\{0,1,2\}\) at the large-\(T\) end of the family.
The *maximum* extra in a family is at its smallest \(T\). A uniform
extra \(\le 8\) for 11-clip bumps is therefore the statement that no
\(S\)-minimal member has extra \(\ge 9\). That statement is a census
through \(T=40\), not a theorem.

The \(T=20\) family of `research/period2_b0.md` (extra \(=28-T\)) is
one instance. The identity is not special to that family.

## What this does not do

Isolated 11-clips and even-\(F\) clips do not obey extra \(\mapsto\)
extra\(-2\) at \(T+2\). \(T=43\) isolated even-\(F\) extra \(=8\) is
untouched. Infinite \(B_0\) (infinite extra) is a fixed point of
\(e\mapsto e-2\) and is not killed. Other periods of \(c_t\) are
untouched.

## Verdict

`LEMMA`, wall time ~8s.

- Kill of period 2: no.
- Extra rank on 11-clip bumps: yes.
- Uniform extra \(\le 8\): no.

## Files

- `research/period2_exdesc.md` (this note)
- `research/period2_exdesc.py` (`--certify`)
- `research/period2_exdesc.json` (dump)
