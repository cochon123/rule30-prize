# Cycle QT: leftover even-\(n\) tot is even rest xor UNIQUE_EVEN even-\(n\) tot

Partition of even-\(n\) rest into unique vs leftover, Cycle QR unique
odd even-\(n\) tot \(0\), and Cycle QS UNIQUE_EVEN even-\(n\) tot
(\(1\) iff \(k=3\) or \(k\ge 5\)) give leftover even-\(n\) tot \(=\)
even rest xor UNIQUE_EVEN even-\(n\) tot for every \(k\). Equivalently
leftover even-\(n\) equals even rest except when \(k=3\) or \(k\ge 5\),
where it flips. Leftover odd-\(n\) tot is odd rest xor UNIQUE_EVEN
odd-\(n\) xor UNIQUE_ODD odd-\(n\). This is **not** leftover even-\(n\)
equals even rest (\(k=3\): leftover \(=1\), even rest \(=0\)). **Not**
leftover even-\(n\) equals \(S\oplus T\) (\(k=8\): leftover \(=0\),
ST \(=1\)). **Not** leftover even-\(n\) equals unique even-\(n\)
(\(k=0\): leftover \(=1\), unique \(=0\)). **Not** rest \(=S\oplus T\).
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
equals leftover tot at \(k-1\).

Certify: `python3 research/cycle_qt.py --certify`.
Dump: `research/cycle_qt.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/MD/PB/QO/QR/QS (leftover even-\(n\) tot via QR unique odd
even-\(n\) tot \(0\) and QS UNIQUE_EVEN even-\(n\) tot; prefix QO
\(n\equiv 0\) tot kill; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (leftover even-\(n\) tot is even rest xor UNIQUE_EVEN even-\(n\) tot)

Leftover odd-\(n\) tot is odd rest xor unique odd-\(n\) tot. Status:
**lemma**. Packed covering on \(k\le 8\), closed forms on \(k\le 64\).
**Killed:** leftover even-\(n\) tot equals even rest. **Killed:**
leftover even-\(n\) tot equals \(S\oplus T\). **Killed:** leftover
even-\(n\) tot equals unique even-\(n\) tot.

## Verdict

`LEMMA` (leftover even-\(n\) tot is even rest xor UNIQUE_EVEN even-\(n\)
tot for every \(k\); leftover odd-\(n\) tot is odd rest xor unique
odd-\(n\) tot; QS UNIQUE_EVEN even-\(n\) tot; QR unique odd even-\(n\)
tot \(0\)).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (leftover even-\(n\) tot equals even rest; leftover even-\(n\)
tot equals \(S\oplus T\); leftover even-\(n\) tot equals unique
even-\(n\) tot; leftover even-\(n\) tot equals leftover tot at
\(k-1\); packed rest on \(n\equiv 0\pmod{4}\) equals \(S\oplus T\)
at \(k-2\)).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_qt.md` (this note)
- `research/cycle_qt.py`
- `research/cycle_qt.json`
