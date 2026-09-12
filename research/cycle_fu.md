# Cycle FU: palindrome center \(r=s-2U+1\) has \(G(m,m)=1\); in cone iff \(s\ge W+1\)

Cycle FT’s involution \(r\mapsto 2\mu-r\) has unique fixed point
\(\mu=s-2U+1\). The reduced degree there is \(W-\mu=m\), so
\(G(m,m)=1\) (Cycle FF diagonal). Together with Cycle FR’s endpoints
\(G(m,2m)=1\) at \(lo\) and \(G(m,0)=1\) at \(r=W\), the three
palindrome-special indices are the three Green corners. The center
lies in the cone-band iff \(s\ge W+1\). Live ANDs on \([lo,W]\) are
**not** palindrome-symmetric, and the center AND is **not** always
live. Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all
\(k\). Do **not** push the even-spine scan past \(k=18\). Do **not**
bump all \(n_0=16\) past 414990. Do **not** increment consecutive
`11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: locating the palindrome center does not prove
covering never-fail.

Helper: `python3 research/cycle_fu.py --certify` (~0.01s). Dump:
`research/cycle_fu.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FF/FR/FS/FT (packed AND checks on
\(k=2\), \(W=8U\); no Fermat table, no extra window, no \(n_0=16\)
window).

## Lemma (center degree \(m\); \(G(m,m)=1\))

Certified on endpoint samples \(k\le 10\), \(W\in\{4U,8U,16U\}\).

## Lemma (in cone iff \(s\ge W+1\))

\(\mu\le lo\) never fails on the window; \(\mu\le W\) holds;
\(\mu\le 2s-T\) iff \(s\ge W+1\). Same samples.

## Killed

AND palindrome-symmetry on \([lo,W]\): \(k=2\), \(W=8U\) has 24
mismatched pairs. Center AND always live: in the cone at \(k=2\),
\(W=8U\), 3 live and 4 dead.

## Verdict

`LEMMA` (center degree \(m\), \(G(m,m)=1\); in cone iff \(s\ge W+1\)).
`KILLED` (AND palindrome-symmetry; center AND always live).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_fu.md` (this note)
- `research/cycle_fu.py`
- `research/cycle_fu.json`
