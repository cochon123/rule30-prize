# Cycle OK: palindrome-right \(S\)-xor vanishes on every even \(n\)

Cycle NA’s \(S\) contributes \(G(n,j+1)\) on palindrome-right cells
with \(d\bmod 3=1\), \(G(n,j)=1\), and \(G(n,j-1)=0\). If \(n\) is
even and \(G(n,j)=1\), then \(j\) is even (Green even-\(n\) /
odd-\(d\)), so \(j+1\) is odd and \(G(n,j+1)=0\). Palindrome-right
\(S\)-xor and \(S\)-fire therefore vanish on every even \(n\). This
is the same clause that kills palindrome-right \(T\)-fire on even
\(n\) (Cycle OI), applied to the right neighbour. Covering \(S\) is
an odd-\(n\) xor. Clip \(p\ge 0\) cannot restore a fire.

This is **not** \(S=0\) on odd \(n\) (\(n=9\): xor \(=1\)), **not**
\(S=T\) (\(n=1\): \(S=0\), \(T=1\)), **not** a closed evaluation of
odd-\(n\) \(S\), and **not** even-\(n\) packed rest vanishing
(\(q=10\), \(k=0\): \(R_{\mathrm{even}}=1\)). Do **not** claim
\(E_k=0\) for all \(k\). Do **not** claim \(S\) equals rest or
\(J_{\mathrm{full}}\). Do **not** catalogue further \(S\)/\(T\)
subregions unless the experiment answers why \(E_k=0\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).

Certify: `python3 research/cycle_ok.py --certify` (~0.14s).
Dump: `research/cycle_ok.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OI/OJ/OG (Green even-\(n\) \(S\)-vanish; odd \(n=2m+1\)
doubling reduction; prefix OJ covering \(T_k\) and OG \(E_k\); no
Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (even \(n\): pal-right \(S\) vanishes)

Let \(n\) be even and \(G(n,j)=1\). Then \(j\) is even, \(j+1\) is
odd, and \(G(n,j+1)=0\). Every palindrome-right \(S\)-cell on even
\(n\) is silent. Status: **lemma** for all even \(n\). Checked on
\(n<256\) (\(n_S=611\) silent cells on \(111\) nonempty even rows).

## Lemma (odd \(n=2m+1\): doubling reduction)

Pal-right even \(j=2k\) with \(k=m+r\) contributes \(1\) iff
\(r\bmod 3=1\) and \((G(m,k-1),G(m,k))=(0,1)\). Pal-right odd
\(j=2k+1\) contributes \(1\oplus G(m,k+1)\) iff \(r\bmod 3=2\) and
\((G(m,k-1),G(m,k))=(1,1)\). Status: **lemma** (reduction, not a
closed value). Checked on \(m<128\). Odd-\(n\) \(S\) has no claimed
closed form.

## Killed

Odd-\(n\) \(S\) vanishes: \(n=9\) has xor \(=1\). Equals \(T\):
\(n=1\) has \(S=0\) and \(T=1\). Even-\(n\) packed rest vanishes:
\(q=10\), \(k=0\) has \(R_{\mathrm{even}}=1\). Closed odd-\(n\)
\(S\). \(E_k=0\) for all \(k\).

## Verdict

`LEMMA` (even-\(n\) pal-right \(S\)-xor vanishes for all even \(n\);
odd-\(n\) doubling reduction; covering \(T_k=1\) iff \(k=2\)).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (odd-\(n\) \(S=0\); \(S=T\); even-\(n\) \(R=0\)).
`PREFIX` (closed odd-\(n\) \(S\); \(E_k=0\) for all \(k\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ok.md` (this note)
- `research/cycle_ok.py`
- `research/cycle_ok.json`
