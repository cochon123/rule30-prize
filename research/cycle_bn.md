# Cycle BN: net packed-bit-1 parity \(P(q,T)\) on \([T,qT)\)

Packed bit 1 always fires for \(t\ge 1\) (Cycle AA). Its Green hits
on the annulus \([T,qT)\) targeting \(qT\) therefore contribute the
net parity

\[
P(q,T):=\bigoplus_{m<(q-1)T}G(m,qT-1).
\]

Even doubling gives \(P(q,2S)=P(q,S)\) for every \(q,S\ge 1\), so
\(P(q,2^k)=P(q,1)=P(q)=1\oplus\mathrm{wt}(q)\), recovering Cycle AL
for every integer \(q\), not only Fermat-odd \(q\). For the 3-fold
remainder \(\Theta(T):=c_{3T}\oplus c_T\) the odd cases reduce to
\(P(3,1)=1\), \(P(3,3)=0\), \(P(3,4p+1)=P(3,p)\), and
\(P(3,4p+3)=P(3,p\lor 1)\) for \(p\ge 1\). Families:
\(P(3,2^k)=1\) (unique bit-1 on \(\theta_k\)); \(P(3,3\cdot 2^k)=0\)
(two hits on \([3U,9U)\) cancel, Cycle BM);
\(P(3,5\cdot 2^k)=P(3,7\cdot 2^k)=1\). Net parity 1 is not a covering
production: \(\Theta(T)=P(3,T)\oplus S_{\mathrm{other}}\) still lets
\(S_{\mathrm{other}}\) cancel on \(\theta_k\). Not a prize claim: the
Fermat covering remains a prefix.

Helper: `python3 research/cycle_bn.py --certify` (~0.2s). Dump:
`research/cycle_bn.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (even doubling)

Let \(q,S\ge 1\) and \(T=2S\). The target \(qT-1=2qS-1\) is odd, so
\(G(2k,qT-1)=0\). Odd doubling gives
\(G(2k+1,2qS-1)=G(k,qS-1)\). The range \(2k+1<(q-1)T=2(q-1)S\) is
exactly \(k<(q-1)S\), hence \(P(q,2S)=P(q,S)\). Certified
\(q\le 12\), \(S\le 24\). In particular \(P(q,2^k)=P(q,1)\). Cycle AL
identifies \(P(q,1)=1\oplus\mathrm{wt}(q)\). Certified \(q\le 16\),
\(k\le 6\).

## Lemma (\(P(3,4p+1)=P(3,p)\))

Write \(P(3,T)=\bigoplus_{m<2T}G(m,3T-1)\). For \(T=4p+1\) the target
\(12p+2\) is even. Even/odd doubling collapses the sum to
\(\bigoplus_{k=0}^{4p}G(k,6p)\). The bound \(6p>2k\) kills \(k<3p\),
so

\[
P(3,4p+1)=\bigoplus_{n=3p}^{4p}G(n,6p).
\]

If \(p=2q+1\) is odd, a further even/odd split leaves
\(\bigoplus_{k=3q+1}^{4q+1}G(k,6q+2)\), because the two extras
\(G(3q+1,6q+3)=G(m,2m+1)=0\) and \(G(4q+2,6q+3)=0\) (even \(m\), odd
\(d\)) vanish. That window is exactly \(P(3,2q+1)=P(3,p)\).

If \(p=2q\) is even, the same split leaves
\(G(4q,6q)\oplus\bigoplus_{k=3q}^{4q-1}G(k,6q-1)\). Cycle BM gives
\(G(4q,6q)=G(2q,3q)=0\). The remaining odd-\(k\) terms are
\(\bigoplus_{t}G(t,3q-1)\) over the cone \(2t\ge 3q-1\), which is
\(P(3,q)=P(3,p)\). Certified \(p\le 40\), including the window
identity. Also \(G(m,2m+1)=0\) for \(m\le 64\) and \(G(2p,3p)=0\)
for \(p\le 64\).

Directly \(P(3,1)=G(1,2)=1\). Directly
\(P(3)=\bigoplus_{m<6}G(m,8)=G(4,8)\oplus G(5,8)=1\oplus 1=0\).

## Lemma (\(P(3,4p+3)=P(3,p\lor 1)\))

For \(p\ge 1\), \(P(3,4p+3)=P(3,p)\) if \(p\) is odd and
\(P(3,p+1)\) if \(p\) is even, i.e. \(P(3,4p+3)=P(3,p\lor 1)\).
(The \(p=0\) slot is the base \(P(3,3)=0\), which is *not*
\(P(3,1)\).) Certified \(p\le 40\). Together with even doubling and
the \(4p+1\) case, every \(T\ge 1\) reduces to \(\{1,3\}\):

- strip factors of \(2\);
- if \(T\equiv 1\pmod{4}\) and \(T>1\), replace \(T\) by \(T/4\);
- if \(T\equiv 3\pmod{4}\) and \(T>3\), replace \(T\) by
  \(((T-3)/4)\lor 1\).

Certified \(1\le T\le 128\) against the Green sum. In particular
\(P(3,T)\) depends only on the odd part of \(T\) after those
foldings. There is no simpler XOR identity
\(P(3,4p+3)=P(3,p)\oplus P(3,p+1)\) (or that XOR 1) that holds for
all \(p\).

## Families

The reduction gives, for every \(k\ge 0\):

| family | value | reason |
|---|---|---|
| \(T=2^k\) | 1 | odd part 1 |
| \(T=3\cdot 2^k\) | 0 | odd part 3 |
| \(T=5\cdot 2^k\) | 1 | \(5=4\cdot 1+1\mapsto 1\) |
| \(T=7\cdot 2^k\) | 1 | \(7=4\cdot 1+3\mapsto 1\) |
| \(T=9\cdot 2^k\) | 1 | \(9=4\cdot 2+1\mapsto 2\mapsto 1\) |
| \(T=11\cdot 2^k\) | 0 | \(11=4\cdot 2+3\mapsto 3\) |
| \(T=13\cdot 2^k\) | 0 | \(13=4\cdot 3+1\mapsto 3\) |
| \(T=15\cdot 2^k\) | 0 | \(15=4\cdot 3+3\mapsto 3\) |

Certified by the reduction through \(k\le 16\). The first two lines
are Cycle BM’s unique bit-1 on \(\theta_k\) and the two cancelling
hits on \([3U,9U)\), now as net parities rather than single-time
hits.

## \(P=1\) is not a covering production — killed

\(\Theta(T)=P(3,T)\oplus S_{\mathrm{other}}(T)\). On \(T=2^k\) one
has \(P=1\), so \(\theta_k=1\oplus S_k\), which is Cycle AJ/AK: the
leftmost 11 forces a 1 that the rest of the annulus may cancel.
Through \(k=12\), \(\theta_k\) takes both values, so \(S_k\) is not
identically 0. On \(T=3\cdot 2^k\) one has \(P=0\), recovering
Cycle BM’s cancelled pair, with no forced net 1. **Killed** as a
1-production for \(\{\theta,\varphi^{(9)}\}\) or for
\(\Theta(T)\equiv 1\).

## Verdict

`LEMMA` (\(P(q,2S)=P(q,S)\); \(P(q,2^k)=P(q)\); \(P(3,4p+1)=P(3,p)\);
\(P(3,4p+3)=P(3,p\lor 1)\); closed reduction to \(\{1,3\}\);
\(P(3,2^k)=1\); \(P(3,3\cdot 2^k)=0\)).
`KILLED` (\(P=1\) as a covering / identically-1 production).
`PREFIX` (Fermat covering for all \(k\ge 2\)).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_bn.md` (this note)
- `research/cycle_bn.py`
- `research/cycle_bn.json`
