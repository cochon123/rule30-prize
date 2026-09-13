# Cycle QH: covering clipped \(G=1\) xor vanishes for \(k\ge 1\); Green leftover is \(1\) iff \(k\ge 6\)

Unclipped Green row xor of \(G=1\) is \(1\) (palindrome plus
\(G(n,n)=1\)). Covering clip is \(j\le 5U\). Write \(A(k)\) for the
xor of clipped \(G=1\) over covering \(n<4U\). Even \(n=2m\) maps
onto the parent clip window, so the even contrib is \(A(k-1)\).
Odd \(n=2m+1\) has clipped xor equal to the parent clip xor of
\(m\): Green doubling telescopes the even/odd bits to
\(\bigoplus_{l\le 5U'}G(m,l)\), including the \(2m=5U'\)
off-by-one. Hence both parities equal \(A(k-1)\) and \(A(k)=0\)
for \(k\ge 1\). Cycle PC's Green forced xor is \(1\) iff \(k=0\)
or \(k\ge 3\), so Green rest off \(\{4,6,14\}\) is \(1\) iff
\(k\ge 3\). Cycle QG's UNIQUE_REST Green tot is \(1\) iff
\(k\in\{3,4,5\}\), so Green leftover xor is \(1\) iff \(k\ge 6\).
This is **not** packed leftover tot (packed rest is not \(1\) for
every \(k\ge 6\)). **Not** rest \(=S\oplus T\). **Not** \(E_k=0\)
for all \(k\). Do **not** catalogue leftover \(p\) one-by-one. Do
**not** catalogue further \(S\)/\(T\) subregions unless the
experiment answers why \(E_k=0\). Do **not** claim pal-left
leftover xor vanishes for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim Green leftover tot equals packed leftover tot.

Certify: `python3 research/cycle_qh.py --certify`.
Dump: `research/cycle_qh.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/MD/PB/PC/QG (clipped \(G=1\) xor; prefix QG unique
Green tot, PC forced Green xor; no Fermat table, no extra window,
no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (unclipped Green row xor of \(G=1\) is \(1\))

Palindrome plus centre \(G(n,n)=1\) gives an odd number of ones.
Status: **lemma**.

## Lemma (covering clipped \(G=1\) xor \(A(k)=0\) for \(k\ge 1\))

Even and odd covering contribs both equal \(A(k-1)\). Status:
**lemma**. Checked on \(k\le 8\), including pointwise odd
\(n=2m+1\) vs parent \(m\).

## Lemma (Green rest is \(1\) iff \(k\ge 3\); leftover is \(1\) iff \(k\ge 6\))

\(A\) xor forced (Cycle PC) xor UNIQUE_REST (Cycle QG). Status:
**lemma**. **Killed:** Green leftover tot equals packed leftover
or \(S\oplus T\) (\(k=7\): Green leftover \(=1\), rest \(=0\)).

## Verdict

`LEMMA` (unclipped row xor \(=1\); clipped covering \(G=1\) xor
vanishes for \(k\ge 1\); Green rest iff \(k\ge 3\); Green leftover
iff \(k\ge 6\); QG unique Green tot; PC forced Green xor).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (Green leftover tot equals \(S\oplus T\) / packed rest).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_qh.md` (this note)
- `research/cycle_qh.py`
- `research/cycle_qh.json`
