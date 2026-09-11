# Cycle BM: leftmost 11 hits \(\Theta(T)\) on the odd part of \(T\)

Packed bit 1 at time \(T\) Green-hits the 3-fold remainder
\(\Theta(T):=c_{3T}\oplus c_T\) iff \(\chi(T):=G(2T-1,3T-1)=1\).
Even doubling gives \(\chi(2S)=\chi(S)\), so the value depends only
on the odd part \(r\) of \(T\). The odd cases reduce to
\(\chi(1)=1\), \(\chi(4p+1)=0\) for \(p\ge 1\), and
\(\chi(4p+3)=\chi(p+1)\), which match the predicate “\(r=1\), or
\(r\equiv 3\pmod{4}\) with no adjacent \(0\)-bits”. In particular
the hit is identically 1 for \(T=2^k\) (Cycle AJ) and for
\(T=3\cdot 2^k\), so \(\varphi^{(9)}_k\oplus\theta_k\) always has a
forced leftmost-11. That remainder is not identically 1, and
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

So the leftmost 11 contributes to \(\Theta(T)\) precisely for those
\(T\). Families: identically 1 on \(T=2^k\), \(3\cdot 2^k\),
\(7\cdot 2^k\), \(11\cdot 2^k\); identically 0 on \(T=5\cdot 2^k\)
and \(T=9\cdot 2^k\). Certified \(k\le 12\).

## \(\Theta(3\cdot 2^k)\) identically 1 — killed

For \(T=3U\) with \(U=2^k\) one has \(\chi(T)=1\), hence
\(\varphi^{(9)}_k\oplus\theta_k=\Theta(3U)=1\oplus S'_k\) with a
forced packed-bit-1 hit at time \(3U\). On \(2\le k\le 12\) the
value takes both \(0\) and \(1\) (zero at \(k=2\)). **Killed.**

## \(\{\theta,\varphi^{(9)}\}\) covering — killed

Both vanish at \(k=3\) (\(c_8=c_{24}=c_{72}\)). **Killed** as a
covering of every \(k\ge 2\). Through \(k=12\) they do not both
vanish for \(k\ge 4\); that is still a prefix, not a theorem, and
Cycle BE already needs \(\varphi^{(5)}\) at \(k=3\). Do not rerun
the Fermat covering through \(k=15\).

## Verdict

`LEMMA` (\(\chi(2S)=\chi(S)\); \(G(2p,3p)=0\); odd reduction;
\(\chi=\mathrm{pred}\); leftmost 11 hits \(\Theta(2^k)\) and
\(\Theta(3\cdot 2^k)\)).
`KILLED` (\(\Theta(3\cdot 2^k)\equiv 1\);
\(\theta_k\lor\varphi^{(9)}_k\) for all \(k\ge 2\)).
`PREFIX` (Fermat covering for all \(k\ge 2\)).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_bm.md` (this note)
- `research/cycle_bm.py`
- `research/cycle_bm.json`
