# Period-2 \(L_0\): \(R=3\) even fire maps under \(S\) to an isolated 1 at \(T+1\)

Checked lemma: if \(F_T=1\), \(F_{T+1}=F_{T+2}=F_{T+3}=0\) and
\(F_{T+4}=1\), then \(Su\) is isolated at \(T+1\):
\(F_T(Su)=0\), \(F_{T+1}(Su)=1\), \(F_{T+2}(Su)=0\). Even-\(T\)
even-\(F\) extra \(=2\) is exactly this 5-tuple (\(R=3\), clip at
\(T+4\)). It is the \(R=3\) companion of the \(R\ge 4\) germ, which
produced a bump rather than an isolated 1. Extra of the image is
**not** a rank. Not a prize claim.

Helper: `python3 research/period2_r3iso.py --certify`. Dump:
`research/period2_r3iso.json`. \(R\ge 4\) germ as in
`research/period2_germ.md` and `research/period2_b0.md`; extra-2
even-\(F\) at even \(T\) as the excluded kernel of
`research/period2_alldesc.md`.

## Lemma (\(R=3\) even fire)

Work on any \(u\) for which the spatial identity
\(G_k=F_{k+1}\oplus(F_k\lor F_{k-1})\) (\(k\ge 1\)) and the fold
\(G_k(u)=F_{k-1}(Su)\oplus(G_{k-1}\lor G_{k-2})\) hold. Assume
\(F_T=1\), \(F_{T+1}=F_{T+2}=F_{T+3}=0\), \(F_{T+4}=1\). Spatial
reconstruction gives
\begin{align*}
G_T&=0\oplus(1\lor F_{T-1})=1,\\
G_{T+1}&=0\oplus(0\lor 1)=1,\\
G_{T+2}&=0\oplus(0\lor 0)=0,\\
G_{T+3}&=1\oplus(0\lor 0)=1.
\end{align*}
Fold at \(T+1,T+2,T+3\):
\begin{align*}
G_{T+1}&=F_T(Su)\oplus(G_T\lor G_{T-1})
\implies 1=F_T(Su)\oplus 1
\implies F_T(Su)=0,\\
G_{T+2}&=F_{T+1}(Su)\oplus(G_{T+1}\lor G_T)
\implies 0=F_{T+1}(Su)\oplus 1
\implies F_{T+1}(Su)=1,\\
G_{T+3}&=F_{T+2}(Su)\oplus(G_{T+2}\lor G_{T+1})
\implies 1=F_{T+2}(Su)\oplus 1
\implies F_{T+2}(Su)=0.
\end{align*}
So \(Su\) is isolated at \(T+1\).

The \(R\ge 4\) germ of `research/period2_germ.md` has the same first
three zeros but \(F_{T+4}=0\), which flips \(G_{T+3}\) to \(0\) and
\(F_{T+2}(Su)\) to \(1\), producing a bump instead.

## Corollary (even-\(T\) even-\(F\) extra \(=2\))

If \(T\) is even and a ugap onset even-\(F\)-clips with extra \(=2\),
then \(n_0=T/2\), \(n_{\mathrm{clip}}=n_0+2\), \(R=2n_{\mathrm{clip}}-1-T=3\),
and the clip is \(F_{T+4}=1\). The lemma applies: \(Su\) is isolated
at \(T+1\). Certified as arithmetic for every even \(T\in[8,80]\), on
every Fibonacci word of length 12 for every such 5-tuple with
\(T\in[5,16]\), and on every ugap even-\(F\) extra-\(2\) onset for
even \(T\in[8,32]\) (270/270).

## What this does not do

The image isolated onset at \(T+1\) can have extra larger or smaller
than 2; extra is not a rank on this class. The three \(T=33\) isolated
extra-\(7\) onsets are extra-raising instances
(`research/period2_r3pull.md`); later isolated extra \(=7\) need not
pull back. Infinite \(L_0\) is untouched. Uniform extra \(\le 8\) is
still a census. Other periods of \(c_t\) are untouched.

## Verdict

`LEMMA`, wall time ~0.6s.

- Kill of period 2: no.
- \(R=3\) even fire \(\mapsto\) isolated at \(T+1\): yes.
- Extra rank on this class: no.
- Uniform extra \(\le 8\): no.

## Files

- `research/period2_r3iso.md` (this note)
- `research/period2_r3iso.py` (`--certify`)
- `research/period2_r3iso.json` (dump)
- `research/period2_germ.md` (\(R\ge 4\) germ to a bump)
- `research/period2_alldesc.md` (even-\(F\) extra \(=2\) at even \(T\) excluded from extra-\(-2\))
- `research/period2_r3pull.md` (\(T=33\) isolated extra \(=7\) is an \(R=3\) image)
