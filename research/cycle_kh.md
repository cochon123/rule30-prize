# Cycle KH: every Green row XORs \(\mathrm{green4}\) to \(0111\)

Every \(n\) has XOR of \(\mathrm{green4}\) over \(G=1\) columns
equal to \(0111\). Covering clipped XOR of \(\mathrm{green4}\) is
\((1,1,0,(k+1)\bmod 2)\) for \(k\ge 2\), independent of
\(q\in\{6,10\}\). Packed XOR is **not** that value. Row-XOR is
**not** \(0000\). Covering XOR is **not** independent of \(k\).
Covering XOR is **not** independent of clip. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: this is a Green-only 4-bit walk identity, not
the packed AND XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_kh.py --certify`.
Dump: `research/cycle_kh.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HJ/HU/IG/KG (\(n<256\); covering \(k\le 6\);
no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (row-XOR of \(\mathrm{green4}\) is \(0111\))

For \(n<256\), XOR of \(\mathrm{green4}\) over \(G=1\) columns is
\(0111\). Ingredients: palindrome \(G(n,j)=G(n,2n-j)\), centre
\(G(n,n)=1\), odd length \(2n+1\), even consecutive-pair count
(equivalently even run-2 count). Unclipped XOR over \(n=0,\ldots,N-1\)
is \(0000\) if \(N\) is even and \(0111\) if \(N\) is odd.

## Lemma (covering clip XOR of \(\mathrm{green4}\))

Packed covering \(J_6,J_{10}\) for \(k\le 6\): \(G=1\) columns
\(22659\). Clipped XOR of \(\mathrm{green4}\) is \(0000\) (\(k=0\),
\(q=6\)), \(0110\) (\(k=0\), \(q=10\)), \(0000\) (\(k=1\), \(q=6\)),
\(1100\) (\(k=1\), \(q=10\)), and \((1,1,0,(k+1)\bmod 2)\) for
\(k\ge 2\) on both \(q\). Unclipped covering XOR is \(0000\)
(\(UQ\) even). Odd-\(s\) \(J\) XOR matches Cycles HF/HG. Packed
4-tuple XOR equals the green4 XOR on only 1 of 14 walks.

## Killed

Row-XOR of \(\mathrm{green4}\) is \(0000\): seed \(n=0\) is
\(0111\). Covering green4 XOR is independent of \(k\): \(k=2\) is
\(1101\), \(k=3\) is \(1100\). Covering green4 XOR equals packed
XOR: at \(k=0\), \(q=6\), green4 \(0000\) vs packed \(1111\).
Covering green4 XOR is independent of clip: at \(k=0\), \(q=10\),
clipped \(0110\) vs unclipped \(0000\).

## Verdict

`LEMMA` (row-XOR of \(\mathrm{green4}\) is \(0111\); covering clip
XOR of \(\mathrm{green4}\); packed vs \(\mathrm{green4}\) fills all
\(64\)).
`KILLED` (row-XOR is \(0000\); covering XOR independent of \(k\);
covering XOR equals packed XOR; covering XOR independent of clip).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_kh.md` (this note)
- `research/cycle_kh.py`
- `research/cycle_kh.json`
