# Cycle TG: \(d=2\) pal-pairs are both children of parent \(d=1\)

At \(k\ge 1\), every \(d=1\) pal-pair \(N\) at \(k-1\) has even
child \(n=2N\) (\(j=2N-2\)) and odd child \(n=2N+1\) (\(j=2N-1\)),
both \(d=2\) pal-pairs at \(k\). Conversely every \(d=2\) pal-pair
at \(k\) is one of those children. Covering times are Cycle SZ's
2-fold. Parent \(d=1\) is never clip-edge (\(n=5U-1\) is outside
covering), so the odd child stays a pair. Count \(2J_{k+1}\) is
twice the parent \(d=1\) count \(J_{k+1}\). Do **not** claim
cellwise spat 2-fold. Do **not** claim \(d=2\) AND identically
\(0\). Do **not** claim pal-center tot equals \(S\oplus T\). This
is **not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\).
Do **not** catalogue leftover \(p\) one-by-one. Do **not**
catalogue leftover \(d\). Do **not** catalogue further \(S\)/\(T\)
subregions unless the experiment answers why \(E_k=0\). Do **not**
claim pal-left leftover xor vanishes for all \(k\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\)
covering packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_tg.py --certify`.
Dump: `research/cycle_tg.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/OJ/PB/QV/SO/SV/SX/SY/SZ/TA/TB/TC/TD/TE/TF (\(d=2\)
pal-pairs are both children of parent \(d=1\); no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (\(d=2\) at \(k\) is both children of \(d=1\) at \(k-1\))

Parent pal-left \(j=N-1\). Even child: \(n=2N\), \(j=2N-2\),
\(G(2N,2N-2)=G(N,N-1)=1\), distance \(2\). Odd child: \(n=2N+1\),
\(j=2N-1\), \(G(2N+1,2N-1)=G(N,N-1)=1\), distance \(2\). Parent
\(d=1\) never meets clip-edge, so the odd child is a pair not
unpaired. Every \(d=2\) cell arises this way: even \(d=2\) has
parent \(d=1\) under \(G(2m,2r)=G(m,r)\); odd \(d=2\) has odd
\(j=2r+1\) and parent distance \(m-r=1\). Status: **lemma**.
Algebra through \(k\le 64\); set equality through \(k\le 12\).

## Lemma (count \(2J_{k+1}\) is twice parent \(d=1\))

Parent \(d=1\) count is \(J_{k+1}\). Each produces two children, so
\(d=2\) count is \(2J_{k+1}\). Even children land on
\(n\equiv 2\pmod{4}\) and odd children on \(n\equiv 3\pmod{4}\),
matching Cycle TF. Covering times are
\(t_k(2N)=2t_{k-1}(N)+1\) and \(t_k(2N+1)=2t_{k-1}(N)-1\). Status:
**lemma**. Count through \(k\le 12\). **Killed:** cellwise spat
2-fold (Cycle TA). **Killed:** \(d=2\) AND identically \(0\).

## Verdict

`LEMMA` (\(d=2\) at \(k\) is both children of \(d=1\) at \(k-1\);
count \(2J_{k+1}\) is twice parent \(d=1\); parent \(d=1\) never
clip-edge; covering times 2-fold).
`CERTIFIED` (set equality through \(k\le 12\); \(E_k=0\) on
odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (cellwise spat 2-fold; \(d=2\) AND identically \(0\);
\(d=1\) on all odd \(n\); \(d=2\) on all even \(n\); pal-center tot
equals \(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_tg.md` (this note)
- `research/cycle_tg.py`
- `research/cycle_tg.json`
