# Cycle BJ: exactly two / two quad-Green bits on the covering annuli

Cycle BI closed the triple-Green remainder on the 5-fold and 9-fold
Fermat annuli. The even-target interval count \(H(m)\) equals 4 only
for \(m\in\{4,7,14\}\). For every \(m\ge 8\) except \(m=14\), a hit
strictly before the complementary pair \(\{2m-2,2m-1\}\) forces
\(H(m)\ge 5\). Truncated covering windows then have \(C_{\le}\ge 5\)
except the 9-fold \(M=0\), \(r=1\) slot. Full power-of-two windows
have no even quads for level \(a\ge 6\) by Cycle AZ; the \(a=4,5\)
seeds give only three annulus residues. The surviving quads are
exactly two packed bits on each covering annulus, for every
\(k\ge 3\), with closed times. Their firing XOR takes both values,
so they are not identically-1 productions. Not a prize claim: the
Fermat covering remains a prefix.

Helper: `python3 research/cycle_bj.py --certify` (~0.4s). Dump:
`research/cycle_bj.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (\(H(m)=4\) only at \(4,7,14\))

Cycle BI: \(H(1)=H(2)=2\), \(H(3)=H(6)=3\), and \(H(m)\ge 4\) for
every other \(m\ge 4\). Directly \(H(4)=4\) with hits
\(\{4,5,7,8\}\), \(H(7)=4\) with \(\{7,11,13,14\}\), and
\(H(14)=4\) with \(\{14,22,26,28\}\) (the even lift of \(m=7\), with
no odd hits). \(H(5)=5\) and \(H(8)=6\).

## Lemma (third hit before the complementary pair)

Cycle BI: for \(m\ge 8\) exactly one of \(G(2m-2,2m)\),
\(G(2m-1,2m)\) is 1. Write \(\mathrm{comp}\) for that hit. The next
hit \(n_3\) after \(n_2\) equals \(\mathrm{comp}\) if and only if
\(m=14\) (where \(n_2=22\) and \(\mathrm{comp}=26\)). For every
other \(m\in[8,64]\) one has \(n_3<\mathrm{comp}\), hence five
distinct hits \(m,n_2,n_3,\mathrm{comp},2m\) and \(H(m)\ge 5\).
Certified \(8\le m\le 64\). Even doubling
\(H(m)\ge H(m/2)\) then keeps \(H\ge 5\) along even towers once a
level with \(H\ge 5\) is reached; \(m=28=2\cdot 14\) already has
odd hits (\(H(28)=10\)).

## Lemma (truncated windows)

Cycle BH: for \(M\ge 1\), \(d\le n_{\mathrm{cone}}\), so
\(N\ge 2m\) and \(C_{\le}\ge H(m)\). The only \(m\) with
\(H(m)\le 4\) are \(\{1,2,3,4,6,7,14\}\). Checking those residues
on both covering annuli: either \(C_{\le}\) is 2 or 3 (Cycles
BH–BI), or \(N\) is a full power-of-two window treated below, or
\(N\) overshoots the \(C_{\le}=4\) range (e.g. \(m=7\) has
\(C_{\le}=4\) only for \(N\le 22\), while 5-fold \(M\ge 3\) has
\(N\ge 26\)). The remaining truncated quad is 9-fold \(M=0\),
\(r=1\): \(d=0\) and \(N=3\), so \(C_{\le}=N+1=4\). Certified:
\(C_{\le}=4\) scan for \(q=5\), \(0\le M\le 8\) and \(q=9\),
\(0\le M\le 7\).

## Lemma (full-window even quads)

If \(N=W\), the count is Cycle AZ’s half-window \(S(a,d)\) with
\(a=M+3\) (5-fold) or \(a=M+4\) (9-fold). Cycle AZ: no even
\(|S|=4\) for \(a\ge 6\). Thus 5-fold \(M\ge 3\) and 9-fold
\(M\ge 2\) have no even full-window quads.

- \(a=4\): even \(|S|=4\) iff \(d\in\{2,4,6\}\). On 5-fold \(M=1\),
  \(N=W\) requires \(r\ge 7\), so only \(r=7\) (\(d=6\)).
- \(a=5\): even \(|S|=4\) iff \(d=14\), i.e. \(r=15\). This is
  5-fold \(M=2\) and 9-fold \(M=1\).

Certified \(a=4,5,6,7\).

## Lemma (\(M<0\))

For \(j>k\), \(r=1\) is unique or double (Cycles BG–BH), never a
quad, and \(r=7,15\) are off-range. Certified \(3\le k\le 7\).
The 9-fold \(M=0\), \(r=1\) quad is already in the \(M\ge 0\) list
(packed bit \(p=8U+1\)).

## Lemma (exactly two / two quad-Green bits)

Let \(k\ge 3\). The quad-Green packed bits are exactly

- 5-fold: \(\{5\cdot 2^{k-2}+1,\,3\cdot 2^{k-1}+1\}\), times
  \(\{5U/4,3U/2,2U,3U\}\) and \(\{U,3U/2,2U,3U\}\);
- 9-fold: \(\{3\cdot 2^{k-1}+1,\,8U+1\}\), times
  \(\{3U/2,2U,3U,5U\}\) and \(\{5U,6U,7U,8U\}\).

Certified against a full Green census for \(3\le k\le 7\).

## Extra quad bits — killed as forced 1s

On \(3\le k\le 8\) the XOR of the two 5-fold quad firings takes
both values, as does the XOR of the two 9-fold quad firings.
Neither XOR equals \(\varphi^{(5)}\) or \(\varphi^{(9)}\). **Killed**
as identically-1 productions for the covering. The remainder after
unique through quadruple bits is pentuples and higher
even-multiplicity terms. The covering
\(\varphi^{(3)},\varphi^{(5)},\varphi^{(9)}\) is still a prefix
through \(k=15\).

## Verdict

`LEMMA` (\(H(m)=4\) only at \(4,7,14\); \(n_3\) before complementary
except \(m=14\); exactly two quad-Green bits on each covering
annulus, for every \(k\ge 3\)).
`KILLED` (those bits as identically-1 productions).
`PREFIX` (Fermat covering for all \(k\ge 2\)).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_bj.md` (this note)
- `research/cycle_bj.py`
- `research/cycle_bj.json`
