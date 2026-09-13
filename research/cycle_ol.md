# Cycle OL: pal-right \(S\) on \(n=8t+3\) is pal-right \(G\) xor off residue \(0\)

If \(m\) is even, Cycle OK’s doubling of \(n=2m+1\) kills every odd
\(r\) (parent odd index) and every \(11\) (parent \(G(m,k-1)\) is
odd-index \(0\)). The only surviving cells are even \(r\equiv 4\pmod{6}\),
and each contributes \(1\) iff \(G(m,m+r)=1\). Hence
\[
S(2m+1)=\bigoplus_{i\ge 0,\,4+6i\le m+1} G(m,m+4+6i).
\]
This covers every odd \(n\equiv 1\pmod{4}\).

If \(n=8t+3\), then \(m=4t+1\). The same doubling, now with even
parent \(2t\), leaves only palindrome-right bits of \(G(t,\cdot)\)
whose offset is not \(0\bmod 3\):
\[
S(8t+3)=\bigoplus_{\substack{t<j\le 2t\\ (j-t)\not\equiv 0\pmod{3}}} G(t,j).
\]
The \(t=0\) xor is empty, so \(S(3)=0\). For \(1\le t\le 127\)
(\(n=11,\ldots,1019\)) the xor is \(1\). Do **not** claim this for
all \(t\ge 1\). Do **not** claim a closed \(S\) for \(n\equiv 7\pmod{8}\).
Do **not** claim \(E_k=0\) for all \(k\). Do **not** catalogue
further \(S\)/\(T\) subregions unless the experiment answers why
\(E_k=0\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for
all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\). Do **not**
walk \(k=11\) covering packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).

Certify: `python3 research/cycle_ol.py --certify` (~0.18s).
Dump: `research/cycle_ol.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OK/OJ/OG (even-parent residue xor; \(n=8t+3\) off-residue
\(0\); prefix OK even-\(n\) \(S\)-vanish, OJ covering \(T_k\), OG
\(E_k\); no Fermat table, no extra window, no \(n_0=16\) window, no
packed covering \(k=11\)).

## Lemma (even \(m\): residue \(4+6i\))

Odd \(r\) and parent \(11\) vanish by even-\(m\) / odd-\(d\). The
remaining \(r\equiv 4\pmod{6}\) contribute \(G(m,m+r)\). Status:
**lemma** for every even \(m\). Checked on \(m<128\).

## Lemma (\(n=8t+3\): pal-right off residue \(0\))

Doubling through even \(2t\) retains pal-right \(G(t,j)\) with
\((j-t)\not\equiv 0\pmod{3}\). Status: **lemma** for every \(t\ge 0\).
Checked on \(t<128\).

## Certificate (\(S(8t+3)=1\) for \(1\le t\le 127\))

The off-residue xor is \(1\) at \(t=1,\ldots,127\) (\(n=11,\ldots,1019\))
and \(0\) at \(t=0\). Status: **certified** on this range, not a lemma
for all \(t\ge 1\). Even parent: \(64\) even \(m<128\), of which
\(32\) have \(S(2m+1)=1\).

## Killed

\(S=1\) for every \(n\equiv 3\pmod{8}\): \(n=3\) has xor \(=0\).
Closed odd-\(n\) \(S\): \(n=1\) is \(0\) and \(n=9\) is \(1\).
\(E_k=0\) for all \(k\).

## Verdict

`LEMMA` (even-parent residue xor; \(n=8t+3\) pal-right off residue
\(0\); even-\(n\) \(S\)-vanish; covering \(T_k=1\) iff \(k=2\)).
`CERTIFIED` (\(S(8t+3)=1\) for \(1\le t\le 127\); \(E_k=0\) on
odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (\(S=1\) on all \(n\equiv 3\pmod{8}\); closed odd-\(n\)
\(S\)).
`PREFIX` (\(S(8t+3)=1\) for all \(t\ge 1\); closed odd-\(n\) \(S\);
\(E_k=0\) for all \(k\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all
\(k\); 11-bit gap; formula for extra 414990; at-most-one-odd for
all \(k\); seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ol.md` (this note)
- `research/cycle_ol.py`
- `research/cycle_ol.json`
