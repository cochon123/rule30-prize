# Cycle HS: even-\(s\) Green never fires odd-\(s\) AND

`and_from_tuple(*green4)` is identically 0: even-\(s\) Green is
never in `AND_ONES`. Same-row \(11\) on `green4` (DIE \(0111/1011\))
iff \(G(n,j)=1\) and \(G(n,j-1)=0\). Dual of Cycle HR's AND of
`odd_green4`. Packed odd-\(s\) AND is **not** identically 0. Packed
even-\(s\) AND is **not** that Green formula. `green4` is **not**
DIE-free. Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for
all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: if AND followed Green then odd-\(s\) AND would
vanish on \(G=1\), so every covering \(J_q\) would be 0 and covering
would always fail. The packed row is not Green, so covering
never-fail stays open.

Helper: `GREEN_DIE`. Certify: `python3 research/cycle_hs.py --certify`.
Dump: `research/cycle_hs.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HJ/HK/HR (8-row table and algebra \(n<64\);
covering \(k\le 6\); no Fermat table, no extra window, no \(n_0=16\)
window).

## Lemma (AND of `green4` identically 0)

8-row over \(G(n,j+1),G(n,j),G(n,j-1)\). `green4` is coboundary-shaped
(\(a=z\oplus b\)) and never lies in `AND_ONES`. Certified
algebraically \(n<64\), and on \(J_6,J_{10}\) for \(k\le 6\).
Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Lemma (even Green \(11\) iff \(G(j)=1\) and \(G(j-1)=0\))

That is DIE \(\{0111,1011\}\). Dual of Cycle HR:
AND of `odd_green4` iff \(G(j+1)=1\) and \(G(j)=0\).

## Killed

Odd-\(s\) AND identically 0: at \(k=0\), \(s=3\), \(n=1\), \(j=0\),
\(p=6\), packed AND \(=1\). Even-\(s\) AND \(=\) \(G(j)\land\lnot G(j-1)\):
at \(k=0\), \(s=2\), \(n=1\), \(j=0\), \(p=6\), four \(0100\), packed
\(0\) vs Green formula \(1\). `green4` DIE-free: at \(k=0\), \(s=8\),
\(n=0\), \(j=0\), \(p=10\), four \(=\) Green \(0111\).

## Verdict

`LEMMA` (AND of `green4` identically 0; even Green \(11\) iff
\(G(j)=1\) and \(G(j-1)=0\); that is DIE \(0111/1011\)).
`KILLED` (odd-s AND identically 0; even-s AND \(=\)
\(G(j)\land\lnot G(j-1)\); `green4` DIE-free).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_hs.md` (this note)
- `research/cycle_hs.py`
- `research/cycle_hs.json`
