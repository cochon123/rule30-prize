# Cycle SZ: odd-child covering snapshot doubles parent even snapshot

On \(q=10\), even snapshot \(s=10U-2n-2\). Odd child \(n=2m+1\)
at \(k\) has \(s_k(2m+1)=2\,s_{k-1}(m)\). Covering times fold
\(t_k(2m)=2t_{k-1}(m)+1\) and \(t_k(2m+1)=2t_{k-1}(m)-1\).
Pal-center tot is the xor of \(c_t\land x(t,1)\) on every covering
time, hence \(P(5U)\oplus P(U)\) with \(P(M)\) the prefix xor of
that bit on odd \(t=1,3,\ldots,2M-1\). Pal-center even tot is xor
of \(\mathrm{cand}(2t+1)\) over parent covering times; odd tot is
xor of \(\mathrm{cand}(2t-1)\). Do **not** claim pal-center tot
equals \(k\bmod 2\) (dies at \(k=12\)). Do **not** claim pal-center
even tot has period \(8\) (dies at \(k=13\)). Do **not** claim
pal-center tot is \(1\) iff \(k\) is even and \(k\ge 10\) (dies at
\(k=13\)). Do **not** claim pal-center tot equals \(S\oplus T\).
This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all
\(k\). Do **not** catalogue leftover \(p\) one-by-one. Do **not**
catalogue further \(S\)/\(T\) subregions unless the experiment
answers why \(E_k=0\). Do **not** claim pal-left leftover xor
vanishes for all \(k\). Do **not** claim
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

Certify: `python3 research/cycle_sz.py --certify` (~0.59s).
Dump: `research/cycle_sz.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/HH/HU/KH/OJ/PB/QV/SO/SS/ST/SV/SX/SY (odd-child covering snapshot
doubles parent even snapshot; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (odd-child covering snapshot doubles parent even snapshot)

On \(q=10\), \(s=10U-2n-2\). For \(k\ge 1\) and parent \(m\) in the
covering window, odd child \(n=2m+1\) has
\(s_k(2m+1)=10\cdot 2^k-4m-4=2s_{k-1}(m)\). Cycle QV already
doubles even-child snapshot onto the parent odd covering time.
Pal-center packed \(p=s+2\), so odd pal-center \(p=2t_{k-1}(m)\)
and even pal-center \(p=2t_{k-1}(m)+2\). Status: **lemma**.
Algebra through \(k\le 64\).

## Lemma (covering times 2-fold)

Odd covering time \(t=s+1=10U-2n-1\). Hence
\(t_k(2m)=2t_{k-1}(m)+1\) and \(t_k(2m+1)=2t_{k-1}(m)-1\). Status:
**lemma**. Algebra through \(k\le 64\).

## Lemma (pal-center tot is \(P(5U)\oplus P(U)\))

Every covering \(n\) is a pal-center (\(G(n,n)=1\)). Covering times
are all odd \(t\) in \([2U+1,10U-1]\). Pal-center tot is therefore
xor of \(c_t\land x(t,1)\) on that interval, which is
\(P(5U)\oplus P(U)\) with \(P(M)\) the prefix xor on odd
\(t\le 2M-1\). Even tot is xor of \(\mathrm{cand}(2t+1)\) over
parent covering times; odd tot is xor of \(\mathrm{cand}(2t-1)\).
Status: **lemma**. Prefix identity and fold through \(k\le 13\).
**Killed:** pal-center even tot period \(8\) (dies at \(k=13\)).
**Killed:** pal-center tot is \(1\) iff \(k\) even and \(k\ge 10\)
(dies at \(k=13\)). **Killed:** \(\mathrm{cand}(2t+1)\) is a
function of the 5-tuple around the centre.

## Verdict

`LEMMA` (odd-child covering snapshot doubles parent even snapshot;
covering times 2-fold; pal-center tot \(=P(5U)\oplus P(U)\);
pal-center even/odd tot is xor of \(\mathrm{cand}(2t\pm 1)\) over
parent covering times).
`CERTIFIED` (pal-center AP through \(k\le 13\); \(E_k=0\) on
odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (pal-center even tot period \(8\); pal-center tot is \(1\)
iff \(k\) even and \(k\ge 10\); pal-center tot equals \(k\bmod 2\);
\(\mathrm{cand}(2t+1)\) local on a 5-tuple; pal-center tot equals
\(S\oplus T\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_sz.md` (this note)
- `research/cycle_sz.py`
- `research/cycle_sz.json`
