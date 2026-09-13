# Cycle QR: covering UNIQUE_ODD packed AND xor on even \(n\) is \(0\) for every \(k\)

All nine UNIQUE_ODD freeze helpers require \(n\equiv 1,3\pmod{4}\),
so even tot is \(0\) for \(k\ge 7\). For \(k\ge 6\) the \(n\equiv 1\)
slice is \(p=54\) (xor \(1\)) and the \(n\equiv 3\) slice is
\(p=42\oplus 58\oplus 98\oplus 106\oplus 114\) (xor \(1\)); they
cancel to Cycle QP unique odd packed tot \(0\). Packed covering
\(k\le 8\) has even tot \(0\), including \(k=6\) where \(p=106\) and
\(p=114\) are not yet frozen. Leftover even-\(n\) tot is therefore
even rest xor UNIQUE_EVEN even-\(n\) tot, **not** \(S\oplus T\)
(\(k=8\): leftover even-\(n\) \(=0\), ST \(=1\)) and **not** leftover
tot at \(k-1\) (\(k=6\): leftover even-\(n\) \(=1\), ST(\(5\))= \(0\)).
This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\).
Do **not** catalogue leftover \(p\) one-by-one. Do **not** catalogue
further \(S\)/\(T\) subregions unless the experiment answers why
\(E_k=0\). Do **not** claim pal-left leftover xor vanishes for all
\(k\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all
\(k\). Do **not** push the even-spine scan past \(k=18\). Do **not**
bump all \(n_0=16\) past 414990. Do **not** increment consecutive
`11` to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\)
covering packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim packed rest on \(n\equiv 0\pmod{4}\) equals
\(S\oplus T\) at \(k-2\). Do **not** claim leftover even-\(n\) tot
equals even rest xor unique even packed tot.

Certify: `python3 research/cycle_qr.py --certify`.
Dump: `research/cycle_qr.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/MD/PB/PM/PN/PR/PS/PV/QA/QC/QD/QE/QJ/QO/QP/QQ (UNIQUE_ODD
even-\(n\) tot via freeze doubling; prefix QQ unique even-\(n\) tot,
QP unique odd packed tot; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (UNIQUE_ODD packed AND xor on even \(n\) is \(0\) for every \(k\))

Freeze AND lives on odd \(n\). Odd tot is \(1\) iff
\(k\in\{3,4,5\}\), equal to Cycle QP unique odd packed tot. Status:
**lemma**. Packed covering on \(k\le 8\), freeze on \(k=6..12\),
closed forms on \(k\le 64\). **Killed:** leftover even-\(n\) tot
equals \(S\oplus T\). **Killed:** leftover even-\(n\) tot equals
leftover tot at \(k-1\).

## Verdict

`LEMMA` (UNIQUE_ODD packed xor on even \(n\) is \(0\) for every \(k\);
on odd \(n\) is \(1\) iff \(k\in\{3,4,5\}\); QP unique odd packed tot;
QQ UNIQUE_EVEN even-\(n\) tot).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (leftover even-\(n\) tot equals \(S\oplus T\); leftover
even-\(n\) tot equals leftover tot at \(k-1\); leftover even-\(n\) tot
equals even rest xor unique even packed tot; packed rest on
\(n\equiv 0\pmod{4}\) equals \(S\oplus T\) at \(k-2\)).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_qr.md` (this note)
- `research/cycle_qr.py`
- `research/cycle_qr.json`
