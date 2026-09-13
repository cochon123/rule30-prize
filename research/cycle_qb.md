# Cycle QB: covering packed AND xor at \(p=88\) is \(1\) iff \(k=4\) or \(k\ge 6\)

Cycle LQ saw covering AND at UNIQUE_REST \(p=88\) on \(G=1\) is
always \(0100\) for \(k\ge 6\), with odd count. Freeze AND
residues are \(t\bmod 8\in\{2,4\}\) (\(n\equiv 2,1\pmod{4}\)).
Column \(j=5U-44\) is even, so even \(n\) can fire. Bits
\(85..88\) freeze from \(t\ge 127\): bit \(85=1\) iff
\(t\bmod 8\in\{0,1,3,5,7\}\), bit \(86=1\) iff \(t\bmod 8\ne 5\),
bit \(87=1\) iff \(t\bmod 8\in\{3,5,7\}\), bit \(88=1\) iff
\(t\bmod 8\in\{1,3,5,6\}\). The left 89 bits are autonomous, and
the word at \(t=127\) equals \(t=135\), so even \(t\ge 128\) has the
\(p=88\) 4-tuple \(1100\) / \(0100\) / \(0100\) / \(0101\) on
\(t\bmod 8=0,2,4,6\), AND iff \(t\bmod 8\in\{2,4\}\). For
\(k\ge 6\) (\(t_0\ge 128\ge 127\)) packed AND on \(G=1\) is \(0100\)
iff \(n\equiv 1\) or \(2\pmod{4}\). Those \(n=4t+1\) double twice
to Green \(p=22\) at scale \(k-2\); \(n=4t+2\) double twice to
Green \(p=22\) xor Green \(p=24\) at \(k-2\) and cancel. Packed
xor is therefore Green \(p=22\) xor at \(k-2\), which is \(1\) for
\(k\ge 6\). Packed \(p=22\) is silent for every \(k\) (Cycle PJ)
and packed \(p=24\) is silent for \(k\ge 4\) (Cycle PL) while both
Green columns fire. Early even AND-ones are
\(t\in\{66,70,78,88,100,114\}\); \(k=4\) xor \(=1\) and \(k=5\)
xor \(=0\). This is UNIQUE_REST \(p=88\). **Killed:** covering
\(p=88\) silent; unique-rest xor \(=0\) as a title for this column.

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

Certify: `python3 research/cycle_qb.py --certify` (~0.15s).
Dump: `research/cycle_qb.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/PC/QA/PQ/PD/GU/HG/HH/HU (bits \(85..88\), even-\(t\)
\(p=88\) 4-tuple AND iff \(t\bmod 8\in\{2,4\}\); Green
\(n\equiv 1\pmod{4}\) via QA \(p=22\); Green \(n\equiv 2\pmod{4}\)
via QA \(p=22\oplus 24\); prefix QA \(p=86\) xor and Green \(p=22,24\);
no Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (bits \(85..88\))

For \(t\ge 125\): bit \(85=1\) iff \(t\bmod 8\in\{0,1,3,5,7\}\),
bit \(86=1\) iff \(t\bmod 8\ne 5\) (Cycle QA). For \(t\ge 127\):
bit \(87=1\) iff \(t\bmod 8\in\{3,5,7\}\), bit \(88=1\) iff
\(t\bmod 8\in\{1,3,5,6\}\). Status: **lemma**. Checked on
\(0\le t\le 160\). Cycle QA's bits \(85..86\) from \(t\ge 125\)
agree on that prefix.

## Lemma (left 89-bit period \(8\) from \(t=127\))

Bits \(0..88\) are autonomous. The word at \(t=127\) equals
\(t=135\), so even \(t\ge 128\) is period \(8\). Status: **lemma**.

## Lemma (AND at \(p=88\) on even \(t\ge 128\))

Even \(t\ge 128\): the \(p=88\) 4-tuple is \(1100\) / \(0100\) /
\(0100\) / \(0101\), AND iff \(t\bmod 8\in\{2,4\}\). Early even
AND-ones are exactly \(t\in\{66,70,78,88,100,114\}\).
Status: **lemma**.

## Lemma (covering packed \(p=88\) xor \(=1\) iff \(k=4\) or \(k\ge 6\))

Covering AND times after the freeze that hit \(G=1\) have
\(n\equiv 1\) or \(2\pmod{4}\). The \(n\equiv 1\pmod{4}\) family
doubles to parent \(p=22\) at \(k-2\). The \(n\equiv 2\pmod{4}\)
family doubles to parent \(p=22\) xor \(p=24\) at \(k-2\) and
cancels. Packed xor is therefore Green \(p=22\) xor at \(k-2\),
which is \(1\) for \(k-2\ge 4\). Thin packed check on \(k\le 8\)
gives xor \(=1\) at \(k=4\) and for \(k\ge 6\), and \(0\) at
\(k=5\). Status: **lemma**. **Killed:** silent; unique-rest xor
\(=0\) as this column's title.

## Verdict

`LEMMA` (bits \(85..88\); left-89 period \(8\); AND \(p=88\) on even
\(t\ge 128\) iff \(t\bmod 8\in\{2,4\}\); Green \(n\equiv 1\pmod{4}\)
via \(p=22\); Green \(n\equiv 2\pmod{4}\) via \(p=22\oplus 24\);
packed \(p=88\) xor \(=1\) iff \(k=4\) or \(k\ge 6\); QA \(p=86\)
xor).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (covering \(p=88\) silent; unique-rest xor \(=0\) as this
column).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_qb.md` (this note)
- `research/cycle_qb.py`
- `research/cycle_qb.json`
