# Cycle QC: covering packed AND xor at \(p=98\) is \(1\) for \(k\ge 6\)

Cycle LJ saw covering AND at UNIQUE_REST \(p=98\) on \(G=1\) is
always \(0010\) for \(k\le 6\). Freeze AND residues are
\(t\bmod 8\in\{0,6\}\) (\(n\equiv 3,0\pmod{4}\)). Column
\(j=5U-49\) is odd, so even \(n\) have \(G=0\). Bits \(95..98\)
freeze from \(t\ge 132\): bit \(95=1\) iff \(t\bmod 8\in\{3,5\}\),
bit \(96=1\) iff \(t\bmod 8\in\{2,7\}\), bit \(97=1\) iff
\(t\bmod 8\notin\{4,5\}\), bit \(98=1\) iff \(t\bmod 8\notin\{0,3\}\).
The left 99 bits are autonomous, and the word at \(t=132\) equals
\(t=140\), so even \(t\ge 132\) has the \(p=98\) 4-tuple \(0010\) /
\(0111\) / \(0001\) / \(0011\) on \(t\bmod 8=0,2,4,6\), AND iff
\(t\bmod 8\in\{0,6\}\). For \(k\ge 7\) (\(t_0\ge 256\ge 132\))
packed AND on \(G=1\) is \(0010\) iff \(n\equiv 3\pmod{4}\). Those
\(n=4t+3\) double twice to Green \(p=26\) at scale \(k-2\). Green
\(p=26\) xor is \(1\) for \(k\ge 4\) (odd \(n\) via parent \(p=14\)
at \(k-1\)), so packed xor is \(1\) for \(k\ge 6\). Packed \(p=26\)
is silent for every \(k\) (Cycle PL) while Green \(p=26\) fires.
Early even AND-ones are
\(t\in\{48,52,64,66,68,88,90,92,98,114,116,130\}\); \(k=4\) and
\(k=5\) xor \(=0\). This is UNIQUE_REST \(p=98\). **Killed:**
covering \(p=98\) silent; unique-rest xor \(=0\) as a title for
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

Certify: `python3 research/cycle_qc.py --certify` (~0.15s).
Dump: `research/cycle_qc.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/PC/QB/PL/PQ/PD/GU/HG/HH/HU (bits \(95..98\), even-\(t\)
\(p=98\) 4-tuple AND iff \(t\bmod 8\in\{0,6\}\); Green
\(n\equiv 3\pmod{4}\) via new \(p=26\); prefix QB \(p=88\) xor, PL
packed \(p=26\) silent, PC Green \(p=14\); no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (bits \(95..98\))

For \(t\ge 132\): bit \(95=1\) iff \(t\bmod 8\in\{3,5\}\), bit
\(96=1\) iff \(t\bmod 8\in\{2,7\}\), bit \(97=1\) iff
\(t\bmod 8\notin\{4,5\}\), bit \(98=1\) iff \(t\bmod 8\notin\{0,3\}\).
Status: **lemma**. Checked on \(0\le t\le 180\). Cycle QB's bits
\(87..88\) from \(t\ge 127\) agree on that prefix.

## Lemma (left 99-bit period \(8\) from \(t=132\))

Bits \(0..98\) are autonomous. The word at \(t=132\) equals
\(t=140\), so even \(t\ge 132\) is period \(8\). Status: **lemma**.

## Lemma (AND at \(p=98\) on even \(t\ge 132\))

Even \(t\ge 132\): the \(p=98\) 4-tuple is \(0010\) / \(0111\) /
\(0001\) / \(0011\), AND iff \(t\bmod 8\in\{0,6\}\). Early even
AND-ones are exactly
\(t\in\{48,52,64,66,68,88,90,92,98,114,116,130\}\).
Status: **lemma**.

## Lemma (Green \(p=26\) xor \(=1\) for \(k\ge 4\))

On the covering live window, \(G(n,5\cdot 2^k-13)=1\) matches
`in_p26` for \(k\ge 4\): even \(n\) vanish; odd \(n\) is parent
\(p=14\) at \(k-1\). The xor is \(0\) at \(k=3\) and \(1\) for
\(k\ge 4\). Packed \(p=26\) is silent for every \(k\) (Cycle PL).
Status: **lemma**.

## Lemma (covering packed \(p=98\) xor \(=1\) for \(k\ge 6\))

Covering AND times after the freeze that hit \(G=1\) have
\(n\equiv 3\pmod{4}\). That family doubles to parent \(p=26\) at
\(k-2\). Green \(p=26\) xor is \(1\) for \(k-2\ge 4\). Thin packed
check on \(k\le 8\) gives xor \(=1\) for \(k\ge 6\) and \(0\) at
\(k=4,5\). Status: **lemma**. **Killed:** silent; unique-rest xor
\(=0\) as this column's title.

## Verdict

`LEMMA` (bits \(95..98\); left-99 period \(8\); AND \(p=98\) on even
\(t\ge 132\) iff \(t\bmod 8\in\{0,6\}\); Green \(p=26\) xor \(=1\)
for \(k\ge 4\); Green \(n\equiv 3\pmod{4}\) via \(p=26\); packed
\(p=98\) xor \(=1\) for \(k\ge 6\); QB \(p=88\) xor).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (covering \(p=98\) silent; unique-rest xor \(=0\) as this
column).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_qc.md` (this note)
- `research/cycle_qc.py`
- `research/cycle_qc.json`
