# Cycle QY: covering Green rest on \(n\equiv 3\pmod{4}\) is \(1\) for every \(k\)

Cycle QH's odd clip identity \(\mathrm{clip\_bit}(2m+1,k)=\mathrm{clip\_bit}(m,k-1)\)
splits by \(m\) parity: child \(n\equiv 1\pmod{4}\) is even \(m\) and child
\(n\equiv 3\pmod{4}\) is odd \(m\), so \(G=1\) xor on \(n\equiv 1\) at \(k\)
equals even-\(n\) \(G=1\) xor at \(k-1\) (\(1\) iff \(k=2\)) and \(G=1\)
xor on \(n\equiv 3\) equals odd-\(n\) \(G=1\) xor at \(k-1\) (\(1\) iff
\(k\le 2\)). Cycle PC's forced sets for \(k\ge 3\) have xor \((0,1,1,1)\)
by \(n\bmod 4\). Green rest is \(G=1\) xor forced, so for \(k\ge 3\)
Green rest \(n\bmod 4\) is \((0,1,1,1)\) and Green \(n\equiv 3\) rest is
\(1\). The same bit is \(1\) at \(k=0,1,2\) from Cycle QX's walk.
Packed \(n\bmod 4\) is **not** this tuple. This is **not** rest
\(=S\oplus T\) for all \(k\). **Not** \(E_k=0\) for all \(k\). Do
**not** catalogue leftover \(p\) one-by-one. Do **not** catalogue
further \(S\)/\(T\) subregions unless the experiment answers why
\(E_k=0\). Do **not** claim pal-left leftover xor vanishes for all
\(k\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all
\(k\). Do **not** push the even-spine scan past \(k=18\). Do **not**
bump all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim Green rest \(n\bmod 4\) equals packed rest \(n\bmod 4\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\) for
all \(k\).

Certify: `python3 research/cycle_qy.py --certify`.
Dump: `research/cycle_qy.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/PC/QH/QV/QW/QX (odd clip split through \(k\le 8\); PC forced
\(n\bmod 4\) through \(k\le 64\); QX Green walk \(k\le 8\); no Fermat
table, no extra window, no \(n_0=16\) window, no packed covering
\(k=11\)).

## Certificate (Green rest on \(n\equiv 3\pmod{4}\) is \(1\) for every \(k\))

Odd clip splits \(G=1\) on \(n\equiv 3\) to parent odd \(G=1\) xor.
Forced xor on that residue is \(1\) for \(k\ge 3\), and the \(k\le 2\)
walk is \(1\). Hence Green rest \(n\bmod 4\) is \((0,1,1,1)\) for every
\(k\ge 3\). Status: **lemma**. **Killed:** Green rest \(n\bmod 4\)
equals packed rest \(n\bmod 4\).

## Verdict

`LEMMA` (covering Green rest on \(n\equiv 3\pmod{4}\) is \(1\) for
every \(k\); Green rest \(n\bmod 4\) is \((0,1,1,1)\) for every
\(k\ge 3\); \(G=1\) on \(n\equiv 1\) at \(k\) equals even-\(n\) \(G=1\)
at \(k-1\); \(G=1\) on \(n\equiv 3\) equals odd-\(n\) \(G=1\) at
\(k-1\)).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (Green rest \(n\bmod 4\) equals packed rest \(n\bmod 4\);
Green even-\(n\) rest equals packed even-\(n\) rest).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_qy.md` (this note)
- `research/cycle_qy.py`
- `research/cycle_qy.json`
