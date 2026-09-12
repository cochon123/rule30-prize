# Cycle FQ: \(G(n+2^a,d)=G(n,d)\) for \(d<2^a\); unified \(T=2U+W\) band

Freshman \((1+x+x^2)^{2^a}=1+x^{2^a}+x^{2^{a+1}}\) yields
\(G(n+2^a,d)=G(n,d)\oplus G(n,d-2^a)\oplus G(n,d-2^{a+1})\). Both
extras vanish for \(0\le d<2^a\), with **no** bound on \(n\). This is
the dual of Cycle FF (which shifts both arguments and needs
\(n<2^{a-1}\)). On the left reduced strip, \(d=2U-p\) with \(p\ge 1\)
so \(d<2U\), and Green weights repeat in every \(2U\)-block. For a
\(W\)-shift comparing targets \(T\) and \(T+W\) with \(T=2U+W\), the
right \(r\)-band has width \(2U-1\) until \(s=U+W\) and then clips,
unifying Cycles FL (\(W=8U\)) and FN (\(W=4U\)) and predicting the
\(W=16U\) band on \([10U,18U)\). Do **not** claim the identity for
\(d=2^a\). Do **not** claim the width-\(2U\) word at \(2U\) equals
the word at \(4U\). Do **not** claim period from \(t=0\). Do **not**
claim flat width on the whole window. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: a low-degree \(n\)-shift plus a unified band does
not prove covering never-fail.

Helper: `python3 research/cycle_fq.py --certify` (~0.43s). Dump:
`research/cycle_fq.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FF/FL/FN/FP (algebraic band \(k\le 10\);
no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (\(G(n+2^a,d)=G(n,d)\) for \(d<2^a\))

Certified \(0\le a\le 8\), \(0\le n<40\). The left-strip instance
\(G(m+2U,2U-p)=G(m,2U-p)\) for \(p\ge 1\) holds on \(0\le k\le 8\).

## Lemma (unified \(T=2U+W\) right band)

For \(W\in\{4U,8U,16U\}\) and \(T=2U+W\), on \(s\in[T-W/2,T)\):
Green \(2(s-T+W/2+1)\le r\le W\), cone \(r\le 2s-T\). Width
\(2U-1\) on \([T-W/2,U+W]\); thereafter \(W-2(s-T+W/2+1)+1\ge 1\).
Certified \(k\le 10\).

## Killed

\(d=2^a\): \(G(2^a,2^a)=1\neq G(0,2^a)=0\). Width-\(2U\) word at
\(2U\) equals the word at \(4U\) fails for \(k=4\). Period from
\(t=0\) fails. Flat width on the whole window: at \(k=2\), \(W=8U\),
\(s=9U+1\) the width is not \(2U-1\).

## Verdict

`LEMMA` (\(G(n+2^a,d)=G(n,d)\) for \(d<2^a\); left-strip Green is
\(2U\)-periodic in \(m\); unified \(T=2U+W\) band).
`KILLED` (\(d=2^a\); period from \(t=0\); \(2U=4U\) on width \(2U\);
flat width).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_fq.md` (this note)
- `research/cycle_fq.py`
- `research/cycle_fq.json`
