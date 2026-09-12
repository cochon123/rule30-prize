# Cycle HH: covering \(s=T-2n-1\); packed AND steps on four bit tuples

On every covering remainder window of length \(2UQ\), the GU clock
rewrites as odd \(s=T-2n-1\) and even \(s=T-2n-2\), so odd-\(s\)
\(\mathrm{AND}(n,j)\) is packed AND at \((T-2n-1,\,T-2j)\). The AND
step is \(1\) iff the previous four row bits \(p-3,\ldots,p\) lie in
\(\{0010,0011,0100,1001\}\). That is **not** \(s=t_0+2n+1\). AND is
**not** \(G(n,j)\). AND\((n,j)\) still depends on \(T\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: a coordinate change plus a 4-bit AND production
does not give a closed form for \(\mathrm{AND}(n,j)\) along Green
ones, so covering never-fail stays open.

Helper: `AND_ONES` / `and_from_tuple` / `ALL_WINDOWS`. Certify:
`python3 research/cycle_hh.py --certify` (~0.03s). Dump:
`research/cycle_hh.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/GU/HC/HF/HG (algebra \(k\le 12\);
AND step \(t<64\); no Fermat table, no extra window, no \(n_0=16\)
window).

## Lemma (odd \(s=T-2n-1\); even \(s=T-2n-2\))

Certified \(k\le 12\) on the three HC windows and the three full
\(J_q\) windows. Odd-\(s\) \(J_q\) is
\(\bigoplus_n\bigoplus_{G(n,j)=1}A(T-2n-1,T-2j)\).

## Lemma (AND step \(=1\) iff 4-tuple in \(\{0010,0011,0100,1001\}\))

16-row identity with \(A'=(a\oplus(b\lor c))\land(z\oplus(a\lor b))\).
Packed check \(t<64\).

## Killed

\(s=t_0+2n+1\): at \(k=2\), \(J_6\), first odd \(s=9\neq 23\).
AND\((n,j)=G(n,j)\): at \(k=1\), \(q=6\), \(n=3\), \(j=0\), AND
\(=0\neq 1\). AND independent of \(T\): at \(k=0\), \(n=0\), \(j=0\),
\(J_6=1\) vs \(J_{10}=0\).

## Verdict

`LEMMA` (odd \(s=T-2n-1\); even \(s=T-2n-2\); AND 4-tuple production).
`KILLED` (\(s=t_0+2n+1\); AND \(=G(n,j)\); AND independent of \(T\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_hh.md` (this note)
- `research/cycle_hh.py`
- `research/cycle_hh.json`
