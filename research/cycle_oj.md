# Cycle OJ: palindrome-right \(T\)-xor is \(1\) for every odd \(n\)

Let \(n=2m+1\). Palindrome-right cells are \(j\in[n+1,2n]\). Green
doubling gives
\[
G(n,2k)=G(m,k)\oplus G(m,k-1),\qquad G(n,2k+1)=G(m,k).
\]
The palindrome-right xor of \(G(n,j-1)\) on \(G(n,j)=1\) then splits
by the parity of \(j\):

- even \(j=2k\) with \(k=m+1,\ldots,2m+1\) contributes \(1\) iff
  \(G(m,k-1)=1\) and \(G(m,k)=0\);
- odd \(j=2k+1\) with \(k=m+1,\ldots,2m\) contributes \(1\) iff
  \(G(m,k)=1\) and \(G(m,k-1)=0\).

Those are exactly the bit-flips of \(G(m,i)\) for
\(i=m,\ldots,2m-1\), plus the right corner \(k=2m+1\) where
\(G(m,2m)=1\) and \(G(m,2m+1)=0\) always. Hence
\[
T(n)=1\oplus\bigoplus_{i=m}^{2m-1}\bigl(G(m,i)\oplus G(m,i+1)\bigr)
=1\oplus G(m,m)\oplus G(m,2m)=1\oplus 1\oplus 1=1.
\]
The telescope is the Boolean identity that the xor of consecutive
differences of a bit-string equals its endpoints. Combined with
Cycle OI’s even-\(n\) vanish, palindrome-right \(T\)-xor equals
\(n\bmod 2\) for every \(n\). Covering \(T_k\) uses \(n<2^{k-1}\), so
it is the number of odd integers in that range, mod \(2\): \(0\) for
\(k\le 1\), \(1\) at \(k=2\), and \(2^{k-2}\) (even) for \(k\ge 3\).
Thus covering \(T_k=1\) iff \(k=2\), for all \(k\). Dyadic bands
\(B_k=0\) for \(k=0\) and \(k\ge 3\), and \(B_1=B_2=1\).

This is **not** pal-right \(T\)-xor vanishing on odd \(n\), **not**
\(T_2=0\), **not** \(T=E\) (\(T_2=1\), \(E_2=0\) on \(q=10\)), and
**not** \(E_k=0\) for all \(k\). Do **not** claim \(T\) equals rest
or \(S\) or \(J_{\mathrm{full}}\). Do **not** catalogue further
\(S\)/\(T\) subregions unless the experiment answers why \(E_k=0\).
Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Even-time \(J_{\mathrm{even}}\) is still required
for \(J_{\mathrm{full}}\). Do **not** claim Green-only rest for all
\(k\). Do **not** record unique-slot XOR vs \(J\).

Certify: `python3 research/cycle_oj.py --certify` (~0.14s).
Dump: `research/cycle_oj.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OI/OG (Green doubling on odd \(n=2m+1\); prefix OI even-\(n\)
vanish and odd \(n<2048\); prefix OG \(E_k\); no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\), no
\(k=12\) \(T\)-band walk).

## Lemma (odd \(n\): pal-right \(T\)-xor \(=1\))

Green doubling plus the endpoint telescope, using \(G(m,m)=1\) and
\(G(m,2m)=1\). Status: **lemma** for every odd \(n\). Checked on
\(m<128\) (the doubling slots \(n_{\mathrm{ok}}=16512\), the even/odd
contributions, and the telescope). \(n=1\) has \(n_T=1\).

## Lemma (covering \(T_k=1\) iff \(k=2\))

Pal-right \(T\)-xor equals \(n\bmod 2\). Covering \(n<2^{k-1}\)
therefore has xor equal to the number of odd \(n\) in that range,
mod \(2\). Status: **lemma** for all \(k\). Checked on covering
windows \(k\le 6\) (not a \(k=12\) band walk).

## Killed

Pal-right \(T\)-xor vanishes on odd \(n\): \(n=1\) has xor \(=1\).
Covering \(T_2=0\): \(T_2=1\). Equals \(E_k\): \(T_2=1\) and
\(E_2=0\) on \(q=10\). \(E_k=0\) for all \(k\).

## Verdict

`LEMMA` (odd-\(n\) pal-right \(T\)-xor is \(1\) for every odd \(n\);
even-\(n\) vanish; covering \(T_k=1\) iff \(k=2\); dyadic \(T\)-band
vanishes for all \(k\ge 3\)).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (odd-\(n\) xor \(=0\); covering \(T_2=0\); \(T=E\)).
`PREFIX` (\(E_k=0\) for all \(k\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_oj.md` (this note)
- `research/cycle_oj.py`
- `research/cycle_oj.json`
