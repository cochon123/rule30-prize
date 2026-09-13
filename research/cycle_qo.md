# Cycle QO: covering packed rest xor on \(n\equiv 0\pmod{4}\) equals \(S\oplus T\) at \(k-2\) dies at \(k=10\)

Green doubling \(G(4t,4r)=G(t,r)\) maps the covering \(n\equiv 0\pmod{4}\)
window onto the parent covering window at \(k-2\), and for \(k\ge 3\)
Green rest on \(n\equiv 0\pmod{4}\) is \(A(k-2)=0\). Packed AND is
**not** cellwise 4-fold: at \(k=3\) already 14 of 36 parent \(G=1\)
cells mismatch (9 child-only, 5 parent-only). Packed rest xor on
\(n\equiv 0\pmod{4}\) equals \(S\oplus T\) at \(k-2\) (and parent
rest tot) on \(3\le k\le 9\), and **dies at \(k=10\)** (got \(0\),
\(S\oplus T\) at \(k=8\) is \(1\)). Unique packed \(n\equiv 0\) tot
is \(1\) for \(k\ge 6\), so leftover packed \(n\equiv 0\) tot equals
that bit xor \(1\) for \(k\ge 6\) and also dies at \(k=10\) (got
\(1\), would need \(0\)). This is **not** rest \(=S\oplus T\).
**Not** \(E_k=0\) for all \(k\). Do **not** catalogue leftover \(p\)
one-by-one. Do **not** catalogue further \(S\)/\(T\) subregions
unless the experiment answers why \(E_k=0\). Do **not** claim pal-left
leftover xor vanishes for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\). Do **not** walk \(k=11\) covering packed. Do
**not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim packed rest on \(n\equiv 0\pmod{4}\) equals
\(S\oplus T\) at \(k-2\).

Certify: `python3 research/cycle_qo.py --certify`.
Dump: `research/cycle_qo.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/MD/PB/QN (packed rest \(n\bmod 4\) through \(k\le 10\);
cellwise 4-fold kill at \(k=3\); prefix QN \(p=16\) \(n\equiv 0\) tot
and unique packed \(n\equiv 0\) for \(k\ge 6\); no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Kill (packed rest xor on \(n\equiv 0\pmod{4}\) equals \(S\oplus T\) at \(k-2\))

The tot identity holds on \(3\le k\le 9\) and fails at \(k=10\).
Cellwise 4-fold packed AND fails at \(k=3\). Leftover packed
\(n\equiv 0\) tot equals \(S\oplus T\) at \(k-2\) xor \(1\) for
\(k\ge 6\) fails at \(k=10\). Status: **killed**. Checked by covering
packed walks on \(k\le 10\).

## Verdict

`KILLED` (packed rest on \(n\equiv 0\pmod{4}\) tot equals \(S\oplus T\)
at \(k-2\); cellwise 4-fold packed AND; leftover packed \(n\equiv 0\)
tot equals \(S\oplus T\) at \(k-2\) xor \(1\) for \(k\ge 6\)).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\);
rest \(n\bmod 4\) table through \(k\le 10\)).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_qo.md` (this note)
- `research/cycle_qo.py`
- `research/cycle_qo.json`
