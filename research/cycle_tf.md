# Cycle TF: \(d=1\)/\(d=2\) pal-pairs split by \(n\bmod 4\)

All covering \(n\equiv 1\pmod{4}\) are \(d=1\) pal-pairs (count
\(2^k\)). Covering \(n\equiv 3\pmod{4}\) is partitioned by \(d=1\)
and \(d=2\), counts \(J_k\) and \(J_{k+1}\). Covering
\(n\equiv 2\pmod{4}\) carries every even \(d=2\) pal-pair (count
\(J_{k+1}\)). Covering \(n\equiv 0\pmod{4}\) has neither \(d=1\) nor
\(d=2\). Thus \(d=1\) lives on \(n\equiv 1,3\pmod{4}\) and \(d=2\)
lives on \(n\equiv 2,3\pmod{4}\). Do **not** claim \(d=1\) on all
odd \(n\). Do **not** claim \(d=2\) on all even \(n\). Do **not**
claim pal-center tot equals \(S\oplus T\). This is **not** rest
\(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
catalogue leftover \(p\) one-by-one. Do **not** catalogue leftover
\(d\). Do **not** catalogue further \(S\)/\(T\) subregions unless
the experiment answers why \(E_k=0\). Do **not** claim pal-left
leftover xor vanishes for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\). Do **not** walk \(k=11\) covering packed. Do
**not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_tf.py --certify` (~0.16s).
Dump: `research/cycle_tf.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/OJ/PB/QV/SO/SV/SY/TA/TB/TD/TE (\(d=1\)/\(d=2\) pal-pairs
split by \(n\bmod 4\); no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (every \(n\equiv 1\pmod{4}\) is a \(d=1\) pal-pair)

\(n=4\ell+1=2(2\ell)+1\) has even parent \(m=2\ell\), so
\(G(m,m-1)=0\) and \(G(n,n-1)=1\oplus 0=1\). Also
\(G(n,n-2)=G(m,m-1)=0\), so these clocks are never \(d=2\). Count
is \(2^k\). Status: **lemma**. Samples through \(k\le 64\); census
through \(k\le 12\). **Killed:** \(d=1\) on all odd \(n\).

## Lemma (\(n\equiv 3\pmod{4}\) is partitioned by \(d=1\) and \(d=2\))

\(n=4\ell+3\) is odd and at least \(3\), so
\(G(n,n-1)\oplus G(n,n-2)=1\). Counts: \(d=1\) is \(J_k\), \(d=2\)
is \(J_{k+1}\), and \(J_k+J_{k+1}=2^k\) matches the residue class.
Together with the previous lemma, \(2^k+J_k=J_{k+2}\) recovers the
Cycle TD \(d=1\) total. Status: **lemma**. Algebra through
\(k\le 64\); census through \(k\le 12\).

## Lemma (\(d=2\) lives on \(n\equiv 2,3\pmod{4}\); \(n\equiv 0\) is empty)

Even \(n=2m\) has \(G(n,n-1)=0\). If \(n\equiv 0\pmod{4}\) then
\(m\) is even, so \(G(n,n-2)=G(m,m-1)=0\) as well. If
\(n\equiv 2\pmod{4}\) then \(m\) is odd and
\(G(n,n-2)=G(m,m-1)\), count \(J_{k+1}\). Status: **lemma**. Census
through \(k\le 12\). **Killed:** \(d=2\) on all even \(n\).

## Verdict

`LEMMA` (every \(n\equiv 1\pmod{4}\) is a \(d=1\) pal-pair;
\(n\equiv 3\pmod{4}\) partitioned by \(d=1\) and \(d=2\); \(d=2\)
lives on \(n\equiv 2,3\pmod{4}\); \(n\equiv 0\pmod{4}\) has neither).
`CERTIFIED` (Green census through \(k\le 12\); \(E_k=0\) on
odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (\(d=1\) on all odd \(n\); \(d=2\) on all even \(n\);
\(d=1\) AND identically \(0\); \(d=2\) AND identically \(0\);
pal-center tot equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_tf.md` (this note)
- `research/cycle_tf.py`
- `research/cycle_tf.json`
