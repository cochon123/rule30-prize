# Cycle HT: coboundary-shaped 4-tuples never fire odd-\(s\) AND

A 4-tuple \((z,a,b,c)\) is coboundary-shaped iff \(a=z\oplus b\).
Those 8 tuples have AND \(=0\): if \(b=0\) then \(z\oplus(a\lor b)=0\);
if \(b=1\) then the two AND factors are \(z\) and \(\lnot z\).
`green4` is always cob-shaped, so this implies Cycle HS. It holds on
the packed row, not only Green. Cob-shaped is **not** `green4`.
Non-coboundary is **not** AND. Cob-shaped is **not** only on \(G=0\).
Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: cob-shaped columns contribute 0 to covering
\(J_q\), but non-cob AND still fires on \(G=1\), so covering
never-fail stays open.

Helper: `cob_shaped`. Certify: `python3 research/cycle_ht.py --certify` (~0.10s).
Dump: `research/cycle_ht.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HJ/HS (16-row table and algebra \(n<64\);
covering \(k\le 6\); no Fermat table, no extra window, no \(n_0=16\)
window).

## Lemma (cob-shaped AND identically 0)

16-row identity. `AND_ONES` is disjoint from the 8 cob-shaped
tuples. `green4` is always cob-shaped. Certified algebraically
\(n<64\), and on packed covering \(J_6,J_{10}\) for \(k\le 6\).
Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Cob-shaped \(=\) `green4`: at \(k=0\), \(s=2\), \(n=3\), \(j=0\),
\(p=10\), four \(0000\) vs Green \(1011\). Non-coboundary iff AND: at
\(k=1\), \(s=11\), \(n=4\), \(j=3\), \(p=14\), four \(1111\), packed
AND \(=0\). Cob-shaped only on \(G=0\): the \(k=0\) witness has
\(G(3,0)=1\).

## Verdict

`LEMMA` (cob-shaped AND identically 0; `green4` is cob-shaped;
`AND_ONES` not cob-shaped).
`KILLED` (cob-shaped \(=\) `green4`; non-cob iff AND; cob-shaped only
on \(G=0\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ht.md` (this note)
- `research/cycle_ht.py`
- `research/cycle_ht.json`
