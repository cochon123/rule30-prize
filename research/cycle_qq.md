# Cycle QQ: covering UNIQUE_EVEN packed AND xor on even \(n\) is \(1\) for \(k\ge 6\)

For \(k\ge 6\) freeze AND at UNIQUE_EVEN splits: \(p=16\) even tot is
\(1\) (Cycle QN \(n\equiv 0\pmod{4}\)), \(p=32\) and \(p=76\) are
\(n\equiv 1\pmod{4}\), \(p=88\) even slice cancels (Green \(p=22\) xor
\(p=24\)), \(p=72\) tot is \(0\). \(p=52\) and \(p=60\) have tot \(0\)
but both \(n\equiv 1,2\pmod{4}\) fire, each slice equal to Green
\(p=14\) and \(p=16\) at \(k-2\) (xor \(1\)). Even tot is
\(p=16\oplus p=52_{n2}\oplus p=60_{n2}=1\). Odd tot is the same bit,
and they cancel to Cycle QP unique even packed tot \(0\). Leftover
even-\(n\) tot is even-\(n\) rest xor this bit, **not** even-\(n\)
rest xor unique even packed tot (\(k=6\): unique even-\(n\) \(=1\),
unique even packed tot \(=0\), even rest \(=0\)). This is **not**
rest \(=S\oplus T\) (\(k=6\): unique even-\(n\) \(=1\), rest \(=1\)
is even xor odd, not this bit). **Not** \(E_k=0\) for all \(k\). Do
**not** catalogue leftover \(p\) one-by-one. Do **not** catalogue
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
equals even-\(n\) rest xor unique even packed tot.

Certify: `python3 research/cycle_qq.py --certify` (~0.17s).
Dump: `research/cycle_qq.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/MD/PB/PC/PH/PK/PV/PW/PX/PY/PZ/QA/QB/QN/QO/QP (UNIQUE_EVEN
even-\(n\) tot via freeze doubling; prefix QP unique even packed tot,
QN \(p=16\) \(n\equiv 0\); no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (UNIQUE_EVEN packed AND xor on even \(n\) is \(1\) for \(k\ge 6\))

\(p=16\) even tot \(1\), \(p=52\) and \(p=60\) even slices \(1\),
\(p=72\) and \(p=88\) even silent. Odd tot is also \(1\). Status:
**lemma**. Checked on \(k=6..12\), closed forms on \(k\le 64\).
**Killed:** leftover even-\(n\) tot equals even rest xor unique even
packed tot.

## Verdict

`LEMMA` (UNIQUE_EVEN packed xor on even \(n\) is \(1\) for \(k\ge 6\);
on odd \(n\) is \(1\) for \(k\ge 6\); QP unique even packed tot;
QN \(p=16\) \(n\equiv 0\) tot).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (leftover even-\(n\) tot equals even rest xor unique even
packed tot; packed rest on \(n\equiv 0\pmod{4}\) equals \(S\oplus T\)
at \(k-2\)).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_qq.md` (this note)
- `research/cycle_qq.py`
- `research/cycle_qq.json`
