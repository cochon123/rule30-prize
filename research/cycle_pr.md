# Cycle PR: covering packed AND xor at \(p=42\) is \(1\) iff \(k=3\) or \(k\ge 5\)

Cycle PQ closed the covering clock \(s\bmod 8\) vs \(n\bmod 4\) and
the even-\(n\) vanishing family. The odd-\(n\) counterpart is freeze
AND at \(t\bmod 8=0\) (\(n\equiv 3\pmod{4}\)). Bits \(39..42\) freeze
from \(t\ge 58\): bit \(39=1\) iff \(t\bmod 8\in\{6,7\}\), bit
\(40=1\) iff \(t\bmod 8\in\{2,4\}\), bit \(41=1\) iff \(t\bmod 8\ne 7\),
bit \(42=1\) iff \(t\bmod 8\notin\{3,5\}\). The left 43 bits are
autonomous, and the word at \(t=58\) equals \(t=66\), so even
\(t\ge 58\) has the \(p=42\) 4-tuple \(0011\) / \(0111\) / \(0111\) /
\(1011\) on \(t\bmod 8=0,2,4,6\), AND iff \(t\bmod 8=0\). For
\(k\ge 5\) (\(t_0\ge 64\ge 58\)) packed AND on \(G=1\) is \(0011\)
iff \(n\equiv 3\pmod{4}\). Those \(n=4t+3\) double twice to Green
\(p=12\) at scale \(k-2\), whose xor is \(1\) for \(k\ge 3\), so
packed xor is \(1\) for \(k\ge 5\). Early even AND-ones are
\(t\in\{20,22,24,36,44,52,56\}\); \(k=3\) xor \(=1\) and \(k=4\)
xor \(=0\). This is UNIQUE_REST \(p=42\), not a leftover bulk
column. **Killed:** covering \(p=42\) silent; unique-rest xor \(=0\)
as a title for this column.

**Not** rest \(=S\oplus T\). **Not** leftover after
\(p=16\oplus 32\oplus 30\oplus 38\oplus 64\oplus 34\oplus 62\oplus 42\)
equals \(S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
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

Certify: `python3 research/cycle_pr.py --certify`.
Dump: `research/cycle_pr.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/PN/PQ/PC/PD/GU/HG/HH/HU (bits \(39..42\), even-\(t\)
\(p=42\) 4-tuple AND iff \(t\bmod 8=0\); Green \(n\equiv 3\pmod{4}\)
via PN \(p=12\) xor; prefix PQ clock / \(p=62\) xor, PN \(p=38\)
xor; no Fermat table, no extra window, no \(n_0=16\) window, no
packed covering \(k=11\)).

## Lemma (bits \(39..42\))

For \(t\ge 58\): bit \(39=1\) iff \(t\bmod 8\in\{6,7\}\), bit
\(40=1\) iff \(t\bmod 8\in\{2,4\}\), bit \(41=1\) iff \(t\bmod 8\ne 7\),
bit \(42=1\) iff \(t\bmod 8\notin\{3,5\}\). Status: **lemma**.
Checked on \(0\le t\le 80\).

## Lemma (left 43-bit period \(8\) from \(t=58\))

Bits \(0..42\) are autonomous. The word at \(t=58\) equals \(t=66\),
so even \(t\ge 58\) is period \(8\). Status: **lemma**.

## Lemma (AND at \(p=42\) on even \(t\ge 58\))

Even \(t\ge 58\): the \(p=42\) 4-tuple is \(0011\) / \(0111\) /
\(0111\) / \(1011\), AND iff \(t\bmod 8=0\). Early even AND-ones
are exactly \(t\in\{20,22,24,36,44,52,56\}\). Status: **lemma**.

## Lemma (covering packed \(p=42\) xor \(=1\) iff \(k=3\) or \(k\ge 5\))

Covering AND times after the freeze have \(n\equiv 3\pmod{4}\).
Those \(n=4t+3\) double to parent \(p=12\) at \(k-2\). Cycle PN's
\(p=12\) xor is \(1\) for \(k\ge 3\), so the \(n\equiv 3\pmod{4}\)
xor is \(1\) for \(k\ge 5\). Thin packed check on \(k\le 8\) gives
xor \(=1\) at \(k=3\) and \(k\ge 5\), and \(0\) at \(k=4\). Status:
**lemma**. **Killed:** silent; unique-rest xor \(=0\) as this
column's title.

## Verdict

`LEMMA` (bits \(39..42\); left-43 period \(8\); AND \(p=42\) on even
\(t\ge 58\) iff \(t\bmod 8=0\); Green \(n\equiv 3\pmod{4}\) via
\(p=12\); packed \(p=42\) xor \(=1\) iff \(k=3\) or \(k\ge 5\); PQ
clock / \(p=62\) xor).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (covering \(p=42\) silent; unique-rest xor \(=0\) as this
column).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_pr.md` (this note)
- `research/cycle_pr.py`
- `research/cycle_pr.json`
