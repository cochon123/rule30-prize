# Cycle QS: covering UNIQUE_EVEN packed AND xor on even \(n\) is \(1\) iff \(k=3\) or \(k\ge 5\)

Cycle QQ gave even tot \(1\) for \(k\ge 6\). Packed covering \(k\le 8\)
matches \(1\) iff \(k=3\) or \(k\ge 5\) (\(k=4\) even tot \(0\), odd tot
\(1\)). Odd tot is \(1\) iff \(k=4\) or \(k\ge 6\), and they xor to
Cycle QP unique even packed tot. Leftover even-\(n\) tot is even rest
xor this bit for every \(k\) (Cycle QR unique odd even-\(n\) tot is
\(0\)), **not** this bit itself (\(k=0\): leftover even-\(n\) \(=1\),
unique even-\(n\) \(=0\)) and **not** \(S\oplus T\) (\(k=8\): leftover
even-\(n\) \(=0\), ST \(=1\)). This is **not** rest \(=S\oplus T\).
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
\(S\oplus T\) at \(k-2\). Do **not** claim leftover even-\(n\) tot
equals unique even-\(n\) tot.

Certify: `python3 research/cycle_qs.py --certify` (~0.18s).
Dump: `research/cycle_qs.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/MD/PB/QJ/QO/QP/QQ/QR (UNIQUE_EVEN even-\(n\) tot lifts QQ
\(k\ge 6\); prefix QR unique odd even-\(n\) tot \(0\); no Fermat
table, no extra window, no \(n_0=16\) window, no packed covering
\(k=11\)).

## Lemma (UNIQUE_EVEN packed AND xor on even \(n\) is \(1\) iff \(k=3\) or \(k\ge 5\))

Odd tot is \(1\) iff \(k=4\) or \(k\ge 6\). Xor is Cycle QP unique
even packed tot. Status: **lemma**. Packed covering on \(k\le 8\),
freeze on \(k=6..12\), closed forms on \(k\le 64\). **Killed:**
leftover even-\(n\) tot equals unique even-\(n\) tot. **Killed:**
leftover even-\(n\) tot equals \(S\oplus T\).

## Verdict

`LEMMA` (UNIQUE_EVEN packed xor on even \(n\) is \(1\) iff \(k=3\)
or \(k\ge 5\); on odd \(n\) is \(1\) iff \(k=4\) or \(k\ge 6\); QP
unique even packed tot; QQ \(k\ge 6\); QR unique odd even-\(n\) tot
\(0\)).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (leftover even-\(n\) tot equals unique even-\(n\) tot;
leftover even-\(n\) tot equals \(S\oplus T\); leftover even-\(n\) tot
equals leftover tot at \(k-1\); packed rest on \(n\equiv 0\pmod{4}\)
equals \(S\oplus T\) at \(k-2\)).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_qs.md` (this note)
- `research/cycle_qs.py`
- `research/cycle_qs.json`
