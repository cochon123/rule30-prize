# Cycle BM: leftmost 11 hits \(\Theta(T)\) on the odd part of \(T\)

Packed bit 1 at time \(T\) Green-hits the 3-fold remainder
\(\Theta(T):=c_{3T}\oplus c_T\) iff \(\chi(T):=G(2T-1,3T-1)=1\).
Even doubling gives \(\chi(2S)=\chi(S)\), so the value depends only
on the odd part \(r\) of \(T\). The odd cases reduce to
\(\chi(1)=1\), \(\chi(4p+1)=0\) for \(p\ge 1\), and
\(\chi(4p+3)=\chi(p+1)\), which match the predicate “\(r=1\), or
\(r\equiv 3\pmod{4}\) with no adjacent \(0\)-bits”. Time \(T\) itself
is therefore a hit for every \(T=2^k\) (Cycle AJ, unique on
\([U,3U)\)) and every \(T=3\cdot 2^k\). On \([3U,9U)\) there is a
second packed-bit-1 hit at \(t=4U\), so the two always-firing hits
cancel and \(\varphi^{(9)}_k\oplus\theta_k\) has net bit-1 parity 0.
That remainder is not identically 1, and
\(\{\theta,\varphi^{(9)}\}\) is not a covering (both vanish at
\(k=3\)). Not a prize claim: the Fermat covering remains a prefix.

Helper: `python3 research/cycle_bm.py --certify` (~0.1s). Dump:
`research/cycle_bm.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (even doubling)

For \(S\ge 1\), both \(2\cdot(2S)-1\) and \(3\cdot(2S)-1\) are odd, so

\[
\chi(2S)=G(4S-1,6S-1)=G(2S-1,3S-1)=\chi(S).
\]

Certified \(S\le 1024\). Thus \(\chi(T)=\chi(r)\) with \(r\) the odd
part of \(T\).

## Lemma (\(G(2p,3p)=0\))

Let \(p=2^a r\) with \(r\) odd and \(p\ge 1\). Then
\(G(2p,3p)=G(2^{a+1}r,\,3\cdot 2^a r)\). The two arguments share
exactly \(a\) factors of \(2\), so this equals \(G(2r,3r)\). Now
\(2r\) is even and \(3r\) is odd, hence \(G(2r,3r)=0\). Certified
\(p\le 256\).

## Lemma (odd reduction)

\(\chi(1)=G(1,2)=1\). For \(p\ge 1\), the odd doubling rules give
\(\chi(4p+1)=G(2p,3p)=0\) and
\(\chi(4p+3)=G(2p+1,3p+2)=\chi(p+1)\). Certified \(p\le 256\).

## Lemma (closed form)

Write \(\mathrm{pred}(T)=1\) iff the odd part \(r\) of \(T\) is \(1\),
or \(r\equiv 3\pmod{4}\) and the binary of \(r\) has no substring
`00`. Then \(\mathrm{pred}\) obeys the same recurrences:
\(\mathrm{pred}(2S)=\mathrm{pred}(S)\), \(\mathrm{pred}(1)=1\),
\(\mathrm{pred}(4p+1)=0\) for \(p\ge 1\), and
\(\mathrm{pred}(4p+3)=\mathrm{pred}(p+1)\). Therefore
\(\chi(T)=\mathrm{pred}(T)\). Certified \(1\le T\le 4096\).

So the leftmost 11 contributes at time \(T\) precisely for those
\(T\). That is a single-time statement, not a net-parity statement
on \([T,3T)\). Families for \(\chi(T)\): identically 1 on
\(T=2^k\), \(3\cdot 2^k\), \(7\cdot 2^k\), \(11\cdot 2^k\);
identically 0 on \(T=5\cdot 2^k\) and \(T=9\cdot 2^k\). Certified
\(k\le 12\).

## Lemma (two bit-1 hits on \([3U,9U)\))

Let \(U=2^k\) and \(T=3U\). Cycle AR/BF: \(G(m,9U-1)=1\) iff
\(2^k\mid(m+1)\) and \(G((m+1)/U-1,8)=1\). On \(t\in[3U,9U)\) one
has \(m+1=\lambda U\) with \(\lambda\in\{1,\ldots,6\}\), and
\(G(\lambda-1,8)=1\) only for \(\lambda\in\{5,6\}\). The times are
\(t=(9-\lambda)U\), i.e. \(t=4U\) and \(t=3U\). Packed bit 1 always
fires (Cycle AA), so the two hits cancel and the bit-1 parity on
this annulus is 0. Hence \(\Theta(3U)=\varphi^{(9)}_k\oplus\theta_k\)
has **no** forced net 1 from packed bit 1. Certified \(2\le k\le 8\).

## \(\Theta(3\cdot 2^k)\) identically 1 — killed

\(\chi(3U)=1\) only says time \(3U\) is a hit. The second hit at
\(4U\) cancels it. On \(2\le k\le 12\) the value \(\Theta(3U)\) takes
both \(0\) and \(1\) (zero at \(k=2\)). **Killed** as a 1-production,
and as \(1\oplus S'\) with a net forced 1.

## \(\{\theta,\varphi^{(9)}\}\) covering — killed

Both vanish at \(k=3\) (\(c_8=c_{24}=c_{72}\)). **Killed** as a
covering of every \(k\ge 2\). Through \(k=12\) they do not both
vanish for \(k\ge 4\); that is still a prefix, not a theorem, and
Cycle BE already needs \(\varphi^{(5)}\) at \(k=3\). Do not rerun
the Fermat covering through \(k=15\).

## Verdict

`LEMMA` (\(\chi(2S)=\chi(S)\); \(G(2p,3p)=0\); odd reduction;
\(\chi=\mathrm{pred}\); leftmost 11 hits at \(T=2^k\) (unique) and
at \(T=3\cdot 2^k\); exactly two bit-1 hits on \([3U,9U)\), net 0).
`KILLED` (\(\Theta(3\cdot 2^k)\equiv 1\), including the net-forced-1
reading; \(\theta_k\lor\varphi^{(9)}_k\) for all \(k\ge 2\)).
`PREFIX` (Fermat covering for all \(k\ge 2\)).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_bm.md` (this note)
- `research/cycle_bm.py`
- `research/cycle_bm.json`
