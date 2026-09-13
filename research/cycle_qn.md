# Cycle QN: covering packed \(p=16\) AND xor on \(n\equiv 0\pmod{4}\) is \(1\) for \(k\ge 3\)

Cycle PH packed AND at \(p=16\) fires iff \(n\) is even for \(k\ge 3\),
and Green even \(n\) is parent \(p=8\). Cycle PH odd Green at \(p=8\)
is \(\{3U-3,3U-1\}\), xor \(0\); both odd parents map to child
\(n\equiv 2\pmod{4}\), so packed \(p=16\) on \(n\equiv 2\pmod{4}\)
vanishes. Even Green at \(p=8\) is parent \(p=4\), whose even \(n\)
is \(3U'-2\) mapping to \(n\equiv 0\pmod{4}\), tot \(1\) for
\(k\ge 2\). Hence packed \(p=16\) AND xor on \(n\equiv 0\pmod{4}\)
is \(1\) for \(k\ge 3\). Other UNIQUE_EVEN freeze AND \(n\bmod 4\)
miss \(0\) for \(k\ge 6\), so unique packed \(n\equiv 0\pmod{4}\) tot
equals this bit for \(k\ge 6\). This is **not** rest \(=S\oplus T\)
(\(k=3\): \(p=16\) \(n\equiv 0\) is \(1\), rest \(=0\); \(k=7\):
\(1\) vs \(0\)). **Not** unique packed \(n\equiv 0\) tot equals
\(p=16\) \(n\equiv 0\) tot for all \(k\) (\(k=4\): unique \(n0=0\)).
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

Certify: `python3 research/cycle_qn.py --certify`.
Dump: `research/cycle_qn.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/MD/PB/PC/PH/PK/PW/PX/PY/PZ/QB/QK/QM (\(p=8\) even tot on
\(n\equiv 0\); packed \(p=16\) on \(n\equiv 0\); unique packed
\(n\equiv 0\) for \(k\ge 6\); prefix PH \(p=16\) tot, PH two odd
\(p=8\) cells; no Fermat table, no extra window, no \(n_0=16\)
window, no packed covering \(k=11\)).

## Lemma (Green \(p=8\) xor on \(n\equiv 0\pmod{4}\) is \(1\) iff \(k\ge 2\))

Odd Green is \(\{3U-3,3U-1\}\), xor \(0\). Even Green is parent
\(p=4\) even \(n=3U'-2\), child \(n=3\cdot 2^k-4\equiv 0\pmod{4}\).
Odd parent \(p=4\) tot vanishes, so \(n\equiv 2\pmod{4}\) tot is
\(0\). Status: **lemma**. Checked on \(k\le 12\).

## Lemma (packed \(p=16\) AND xor on \(n\equiv 0\pmod{4}\) is \(1\) for \(k\ge 3\); on \(n\equiv 2\pmod{4}\) vanishes)

Parent \(p=8\) even tot on \(n\equiv 0\) at \(k-1\). The two odd
\(p=8\) cells map to \(n\equiv 2\pmod{4}\) and cancel. Status:
**lemma**. Checked on \(k\le 12\), closed forms on \(k\le 64\).
**Killed:** \(p=16\) \(n\equiv 0\) tot equals \(S\oplus T\) /
packed rest.

## Lemma (UNIQUE_EVEN packed AND xor on \(n\equiv 0\pmod{4}\) is \(1\) for \(k\ge 6\))

Freeze AND \(n\bmod 4\) at \(p=32,52,60,72,76,88\) misses \(0\).
Status: **lemma**. **Killed:** unique packed \(n\equiv 0\) tot
equals \(p=16\) \(n\equiv 0\) tot for all \(k\) (\(k=4\)).

## Verdict

`LEMMA` (Green \(p=8\) on \(n\equiv 0\pmod{4}\) tot is \(1\) for
\(k\ge 2\); packed \(p=16\) on \(n\equiv 0\) tot is \(1\) for
\(k\ge 3\); packed \(p=16\) on \(n\equiv 2\) tot is \(0\); unique
packed \(n\equiv 0\) tot is \(1\) for \(k\ge 6\); PH \(p=16\) tot;
PH two odd \(p=8\) cells).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (\(p=16\) \(n\equiv 0\) tot equals \(S\oplus T\) / packed
rest; unique packed \(n\equiv 0\) tot equals \(p=16\) \(n\equiv 0\)
tot for all \(k\)).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
packed rest on \(n\equiv 0\pmod{4}\) equals \(S\oplus T\) at
\(k-2\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_qn.md` (this note)
- `research/cycle_qn.py`
- `research/cycle_qn.json`
