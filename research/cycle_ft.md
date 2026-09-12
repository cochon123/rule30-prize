# Cycle FT: Green support \([lo,W]\) is palindrome-symmetric about \(s-2U+1\)

Cycle FS palindrome \(G(m,d)=G(m,2m-d)\) acts on the right-band index
by \(r\mapsto 2\mu-r\) with \(\mu=s-2U+1\). On the unified
\(T=2U+W\) band this swaps the Green endpoints:
\(2\mu-W=lo=2(s-T+W/2+1)\) and \(2\mu-lo=W\). So the Green interval
\([lo,W]\) is palindrome-symmetric. The light-cone cut
\([lo,\min(2s-T,W)]\) is **not**: before clip, \(2\mu-lo=W\neq hi\).
Do **not** claim the cone-restricted band is palindrome-symmetric.
Do **not** claim the midpoint is \(s-U\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: Green-interval palindrome symmetry does not prove
covering never-fail.

Helper: `python3 research/cycle_ft.py --certify` (~0.01s). Dump:
`research/cycle_ft.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles CA/FQ/FR/FS (algebraic \(k\le 10\); no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (\([lo,W]\) palindrome-symmetric about \(s-2U+1\))

Certified on endpoint samples \(k\le 10\), \(W\in\{4U,8U,16U\}\).

## Killed

Cone-band palindrome-symmetric: at \(k=2\), \(W=8U\), \(s=6U\),
\(lo=2\), \(hi=8\), while \(2\mu-lo=W=32\). Midpoint \(s-U\): it is
\(s-2U+1\).

## Verdict

`LEMMA` (Green interval palindrome-symmetric about \(s-2U+1\)).
`KILLED` (cone-band palindrome-symmetric; midpoint \(s-U\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ft.md` (this note)
- `research/cycle_ft.py`
- `research/cycle_ft.json`
