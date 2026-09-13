# Cycle QX: covering Green rest \(n\bmod 4\) is \((0,1,1,1)\) for \(k\ge 3\)

Cycle QV twice sends \(n\equiv 0\pmod{4}\) clipped \(G=1\) at \(k\) to
all clipped \(G=1\) at \(k-2\), so that xor is Cycle QH clip xor at
\(k-2\), \(1\) iff \(k=2\). Forced \(p=6\) and \(p=14\) have odd \(j\)
for \(k\ge 1\), and Cycle PC's even-\(n\) \(p=4\) is \(n=3U-2\) with
\((3U-2)\bmod 4=2\) for \(k\ge 2\) (at \(k=1\) it is \(n\equiv 0\pmod{4}\)),
so \(n\equiv 0\pmod{4}\) has no forced cell for \(k\ge 2\).
Green rest on \(n\equiv 0\pmod{4}\) is \(1\) iff \(k\le 2\).
\(n\equiv 2\pmod{4}\) \(G=1\) xor is odd \(G=1\) xor at \(k-1\), and
xor the unique \(p=4\) cell gives Green \(n\equiv 2\) rest \(1\) iff
\(k=1\) or \(k\ge 3\). For \(3\le k\le 8\) Green rest \(n\bmod 4\) is
\((0,1,1,1)\): each of \(n\bmod 4\in\{1,2,3\}\) has xor \(1\), and
\(n\equiv 3\pmod{4}\) is \(1\) at every \(k\le 8\). Packed \(n\bmod 4\)
is **not** this tuple (\(k=3\) packed is \((0,0,0,0)\)). This is
**not** rest \(=S\oplus T\) for all \(k\). **Not** \(E_k=0\) for all
\(k\). Do **not** catalogue leftover \(p\) one-by-one. Do **not**
catalogue further \(S\)/\(T\) subregions unless the experiment answers
why \(E_k=0\). Do **not** claim pal-left leftover xor vanishes for all
\(k\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all
\(k\). Do **not** push the even-spine scan past \(k=18\). Do **not**
bump all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim Green rest \(n\bmod 4\) equals packed rest \(n\bmod 4\).
Do **not** claim Green \(n\equiv 3\pmod{4}\) rest is \(1\) for all
\(k\). Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\) for
all \(k\).

Certify: `python3 research/cycle_qx.py --certify`.
Dump: `research/cycle_qx.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/LZ/QH/QO/QV/QW (Green rest \(n\bmod 4\) through \(k\le 8\);
packed kill from QO \(k\le 10\); no Fermat table, no extra window,
no \(n_0=16\) window, no packed covering \(k=11\)).

## Certificate (Green rest \(n\bmod 4\) is \((0,1,1,1)\) for \(3\le k\le 8\))

Green \(n\equiv 0\pmod{4}\) rest is \(1\) iff \(k\le 2\), by 4-fold
clip xor and no forced cell on that residue. Green \(n\equiv 2\pmod{4}\)
rest is \(1\) iff \(k=1\) or \(k\ge 3\), by Cycle QV's odd slice plus
the unique even-\(n\) \(p=4\) cell. Status: **lemma** (\(n\equiv 0\)
and \(n\equiv 2\)); **certified** (the 4-tuple through \(k\le 8\)).
**Killed:** packed rest \(n\bmod 4\) equals Green rest \(n\bmod 4\).

## Verdict

`LEMMA` (covering Green rest on \(n\equiv 0\pmod{4}\) is \(1\) iff
\(k\le 2\); Green rest on \(n\equiv 2\pmod{4}\) is \(1\) iff \(k=1\)
or \(k\ge 3\)).
`CERTIFIED` (Green rest \(n\bmod 4\) is \((0,1,1,1)\) for \(3\le k\le 8\);
Green \(n\equiv 3\pmod{4}\) rest is \(1\) for \(k\le 8\); \(E_k=0\) on
odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (Green rest \(n\bmod 4\) equals packed rest \(n\bmod 4\);
packed rest on \(n\equiv 0\pmod{4}\) equals \(S\oplus T\) at \(k-2\);
Green even-\(n\) rest equals packed even-\(n\) rest).
`PREFIX` (Green \(n\equiv 3\pmod{4}\) rest is \(1\) for all \(k\);
Green rest \(n\bmod 4\) is \((0,1,1,1)\) for all \(k\ge 3\); even-\(n\)
rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\) for all \(k\);
packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for all \(k\);
leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_qx.md` (this note)
- `research/cycle_qx.py`
- `research/cycle_qx.json`
