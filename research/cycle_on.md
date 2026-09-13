# Cycle ON: pal-right \(S(4s+3)=S(s)\) for every odd \(s\)

Let \(s\) be odd, \(m=2s+1\), and \(n=2m+1=4s+3\). Cycle OK’s
doubling writes palindrome-right \(S(n)\) as an xor of four
\(r\bmod 6\) classes on the parent \(G(m,\cdot)\). The even-\(r\),
\(r\equiv 2\pmod{6}\) class is exactly the palindrome-right
\(S\)-cells of \(s\), each contributing \(G(s,j+1)\). The other
three classes xor to \(0\) by Green doubling of the pal-right
string of odd \(s\) plus a residue pairing. Hence
\(S(4s+3)=S(s)\) for every odd \(s\), and
\(S(8t+7)=S(2t+1)\) for every \(t\). Combined with Cycles OK/OL,
every odd \(n\) reduces to an even-parent residue xor or to an
\(n=8u+3\) off-residue-\(0\) row.

This is **not** the fold for even \(s\) (\(s=2\): \(S(11)=1\),
\(S(2)=0\)), **not** \(S(4s+3)=0\) (\(s=9\): xor \(=1\)), **not**
\(S(8t+3)=1\) for all \(t\ge 1\), and **not** covering \(S\)
(clip \(p\ge 0\) remains). Do **not** claim \(E_k=0\) for all
\(k\). Do **not** catalogue further \(S\)/\(T\) subregions unless
the experiment answers why \(E_k=0\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).

Certify: `python3 research/cycle_on.py --certify` (~0.15s).
Dump: `research/cycle_on.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OK/OJ/OL/OM/OG (fold \(S(4s+3)=S(s)\) for odd \(s\);
prefix OL even-parent and \(n=8t+3\), OM finite fold, OJ covering
\(T_k\), OG \(E_k\); no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (od_even class equals \(S(s)\))

Green doubling of odd \(m=2s+1\):
\[
G(m,2k)=G(s,k)\oplus G(s,k-1),\qquad G(m,2k+1)=G(s,k).
\]
Cycle OK’s odd-\(j\) \(11\)-fires with even \(r=2p\equiv 2\pmod{6}\)
have \(p\equiv 1\pmod{3}\) and
\((G(s,s+p-1),G(s,s+p))=(0,1)\). The contributed bit is
\(1\oplus G(m,m+2p+1)=G(s,s+p+1)\). The range \(p=1,\ldots,s\) is
exactly palindrome-right \(S\)-cells of \(s\). Status: **lemma**
for every odd \(s\). Checked on \(s<128\).

## Lemma (extras xor to \(0\))

The remaining classes are: \(01\) at pal-right offset \(\equiv 0\)
(contribute \(1\)); \(11\) starting at offset \(\equiv 1\)
(contribute \(1\)); \(10\) starting at offset \(\equiv 2\)
(contribute \(1\), including the corner \(G(s,2s)=1\),
\(G(s,2s+1)=0\) iff \(s\equiv 2\pmod{3}\)). Write \(s=2u+1\) and
\(c_j=G(u,u+j)\). Pal-right bits of \(s\) are the interleave
\(b_{2p}=c_p\), \(b_{2p+1}=c_p\oplus c_{p+1}\) with virtual
\(c_{u+1}=0\). On that doubled string, the three interior
transition xors equal \(u\bmod 3=2\). The corner \(10\) is the
same bit as \(s\bmod 3=2\), and \(s\equiv 2\pmod{3}\) iff
\(u\equiv 2\pmod{3}\). Status: **lemma** for every odd \(s\). The
parent pairing is a Boolean identity on every endpoint-\(1\)
parent string (checked on all such strings of length \(\le 11\)).

## Lemma (\(S(8t+7)=S(2t+1)\) for every \(t\))

\(n=8t+7\) is \(4s+3\) with odd \(s=2t+1\). Status: **lemma** for
every \(t\ge 0\). Checked on \(t<64\) (\(s<128\)).

## Killed

The fold for even \(s\): \(S(11)=1\) and \(S(2)=0\). Identically
\(0\): \(s=9\) has xor \(=1\). \(S(8t+3)=1\) for all \(t\ge 1\).
Covering \(S\). Closed odd-\(n\) \(S\) as a \(0\)-\(1\) value.
\(E_k=0\) for all \(k\).

## Verdict

`LEMMA` (\(S(4s+3)=S(s)\) for every odd \(s\); extras cancel;
od_even equals \(S(s)\); \(S(8t+7)=S(2t+1)\) for every \(t\);
even-parent residue xor; \(n=8t+3\) pal-right off residue \(0\);
covering \(T_k=1\) iff \(k=2\)).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (fold for even \(s\); \(S(4s+3)=0\)).
`PREFIX` (\(S(8t+3)=1\) for all \(t\ge 1\); closed odd-\(n\) \(S\);
covering \(S\); \(E_k=0\) for all \(k\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_on.md` (this note)
- `research/cycle_on.py`
- `research/cycle_on.json`
