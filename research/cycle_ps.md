# Cycle PS: covering packed AND xor at \(p=54\) is \(1\) for \(k\ge 4\)

Cycle PR closed UNIQUE_REST \(p=42\) via freeze AND \(t\bmod 8=0\)
(\(n\equiv 3\pmod{4}\)) doubling to Green \(p=12\). The \(n\equiv 1
\pmod{4}\) counterpart is freeze AND at \(t\bmod 8=4\). Bits
\(51..54\) freeze from \(t\ge 78\): bit \(51=1\) iff
\(t\bmod 8\in\{0,3,5,7\}\), bit \(52=1\) iff
\(t\bmod 8\in\{2,3,4,5\}\), bit \(53=1\) iff
\(t\bmod 8\in\{0,3,5\}\), bit \(54=1\) iff
\(t\bmod 8\in\{1,2,5\}\). The left 55 bits are autonomous, and the
word at \(t=78\) equals \(t=86\), so even \(t\ge 78\) has the
\(p=54\) 4-tuple \(1010\) / \(0101\) / \(0100\) / \(0000\) on
\(t\bmod 8=0,2,4,6\), AND iff \(t\bmod 8=4\). For \(k\ge 6\)
(\(t_0\ge 128\ge 78\)) packed AND on \(G=1\) is \(0100\) iff
\(n\equiv 1\pmod{4}\). Those \(n=4t+1\) double twice to Green
\(p=14\) at scale \(k-2\), whose xor is \(1\) for \(k\ge 3\), so
packed xor is \(1\) for \(k\ge 6\). Early even AND-ones are
\(t\in\{26,28,38,46,58,62,74\}\); \(k=4,5\) xor \(=1\) and
\(k\le 3\) xor \(=0\). This is UNIQUE_REST \(p=54\). **Killed:**
covering \(p=54\) silent; unique-rest xor \(=0\) as a title for
this column.

**Not** rest \(=S\oplus T\). **Not** leftover after classified
columns equals \(S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do
**not** catalogue further \(S\)/\(T\) subregions unless the
experiment answers why \(E_k=0\). Do **not** claim pal-left leftover
xor vanishes for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\). Do **not** walk \(k=11\) covering packed. Do
**not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).

Certify: `python3 research/cycle_ps.py --certify` (~0.14s).
Dump: `research/cycle_ps.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/PC/PR/PQ/PD/GU/HG/HH/HU (bits \(51..54\), even-\(t\)
\(p=54\) 4-tuple AND iff \(t\bmod 8=4\); Green \(n\equiv 1\pmod{4}\)
via PC \(p=14\) xor; prefix PR \(p=42\) xor, PC \(p=14\) Green;
no Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (bits \(51..54\))

For \(t\ge 78\): bit \(51=1\) iff \(t\bmod 8\in\{0,3,5,7\}\), bit
\(52=1\) iff \(t\bmod 8\in\{2,3,4,5\}\), bit \(53=1\) iff
\(t\bmod 8\in\{0,3,5\}\), bit \(54=1\) iff
\(t\bmod 8\in\{1,2,5\}\). Status: **lemma**. Checked on
\(0\le t\le 96\).

## Lemma (left 55-bit period \(8\) from \(t=78\))

Bits \(0..54\) are autonomous. The word at \(t=78\) equals \(t=86\),
so even \(t\ge 78\) is period \(8\). Status: **lemma**.

## Lemma (AND at \(p=54\) on even \(t\ge 78\))

Even \(t\ge 78\): the \(p=54\) 4-tuple is \(1010\) / \(0101\) /
\(0100\) / \(0000\), AND iff \(t\bmod 8=4\). Early even AND-ones
are exactly \(t\in\{26,28,38,46,58,62,74\}\). Status: **lemma**.

## Lemma (covering packed \(p=54\) xor \(=1\) for \(k\ge 4\))

Covering AND times after the freeze have \(n\equiv 1\pmod{4}\).
Those \(n=4t+1\) double to parent \(p=14\) at \(k-2\). Cycle PC's
\(p=14\) Green xor is \(1\) for \(k\ge 3\), so the
\(n\equiv 1\pmod{4}\) xor is \(1\) for \(k\ge 5\). Thin packed
check on \(k\le 8\) gives xor \(=1\) for \(k\ge 4\) and \(0\)
otherwise. Status: **lemma**. **Killed:** silent; unique-rest xor
\(=0\) as this column's title.

## Verdict

`LEMMA` (bits \(51..54\); left-55 period \(8\); AND \(p=54\) on even
\(t\ge 78\) iff \(t\bmod 8=4\); Green \(n\equiv 1\pmod{4}\) via
\(p=14\); packed \(p=54\) xor \(=1\) for \(k\ge 4\); PR \(p=42\)
xor).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (covering \(p=54\) silent; unique-rest xor \(=0\) as this
column).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ps.md` (this note)
- `research/cycle_ps.py`
- `research/cycle_ps.json`
