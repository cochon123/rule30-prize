# Cycle FV: remainder palindrome \(p\mapsto 2s+2-p\); center \(p=s+1\) always in-support

For a Green remainder to target \(T\) at time \(s<T\), in-support is
\(p\in[2s-T+2,T]\). Cycle FS palindrome acts by \(p\mapsto 2s+2-p\)
and swaps the endpoints (\(G(m,2m)=1\) at \(p_{\mathrm{lo}}\),
\(G(m,0)=1\) at \(p=T\)). The unique fixed point is \(p=s+1\), with
degree \(m\), so \(G(m,m)=1\). Unlike Cycle FU’s comparison-band
center (in cone only for \(s\ge W+1\)), the remainder center is
in-support for every \(s\) in the window. Applies to \(J_6\),
\(J_{10}\), \(J_{\mathrm{tail}}\), and \(J_{18}\). Do **not** claim
remainder ANDs are palindrome-symmetric. Do **not** claim the
remainder-center AND always fires. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: a remainder palindrome dual of Cycles FT–FU does
not prove covering never-fail.

Helper: `python3 research/cycle_fv.py --certify` (~0.01s). Dump:
`research/cycle_fv.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FF/FS/FT/FU (packed AND checks on the
\(J_{\mathrm{tail}}\) window at \(k=2\); no Fermat table, no extra
window, no \(n_0=16\) window).

## Lemma (\(p\mapsto 2s+2-p\) swaps remainder endpoints)

Certified on endpoint samples \(k\le 10\) for targets \(6U,10U,18U\).

## Lemma (center \(p=s+1\) always in-support; \(G(m,m)=1\))

Same samples. Contrast Cycle FU: comparison center waits until
\(s\ge W+1\).

## Killed

Remainder AND palindrome-symmetry: \(J_{\mathrm{tail}}\) at \(k=2\)
has 166 mismatched pairs. Remainder-center AND always live: 5 live
and 27 dead on that window.

## Verdict

`LEMMA` (remainder palindrome; center \(s+1\) always in-support).
`KILLED` (remainder AND palindrome-symmetry; remainder-center AND
always live).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_fv.md` (this note)
- `research/cycle_fv.py`
- `research/cycle_fv.json`
