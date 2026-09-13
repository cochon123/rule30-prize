# Cycle QE: covering packed AND xor at \(p=114\) is \(1\) iff \(k\ge 4\) and \(k\ne 6\)

Cycle LU saw covering AND at UNIQUE_REST \(p=114\) on \(G=1\) is
always \(0100\) for \(k\ge 6\), with even count at \(k=6\). Freeze
AND residue is \(t\bmod 8=0\) (\(n\equiv 3\pmod{4}\)). Column
\(j=5U-57\) is odd, so even \(n\) have \(G=0\). Bits \(111..114\)
freeze from \(t\ge 158\): bit \(111=1\) iff \(t\bmod 8\in\{2,3,4,5\}\),
bit \(112=1\) iff \(t\bmod 8\in\{0,5\}\), bit \(113=1\) iff
\(t\bmod 8\in\{1,2,4\}\), bit \(114=1\) iff
\(t\bmod 8\in\{1,2,3,4,5\}\). The left 115 bits are autonomous, and
the word at \(t=158\) equals \(t=166\), so even \(t\ge 158\) has the
\(p=114\) 4-tuple \(0100\) / \(1011\) / \(1011\) / \(0000\) on
\(t\bmod 8=0,2,4,6\), AND iff \(t\bmod 8=0\). For \(k\ge 7\)
(\(t_0\ge 256\ge 158\)) packed AND on \(G=1\) is \(0100\) iff
\(n\equiv 3\pmod{4}\). Those \(n=4t+3\) double twice to Green
\(p=30\) at scale \(k-2\). Green \(p=30\) xor is \(1\) for \(k\ge 4\)
(odd \(n\) via parent \(p=16\) at \(k-1\)), so packed xor is \(1\)
for \(k\ge 7\). Packed \(p=30\) xor is \(1\) iff \(k=2\) (Cycle PM)
while Green \(p=30\) fires for \(k\ge 4\). Early even AND-ones are
\(t\in\{56,62,78,96,106,112,122,130,150\}\); \(k=4\) and \(k=5\)
xor \(=1\), \(k=6\) xor \(=0\). This is UNIQUE_REST \(p=114\), the
last column of Cycle MD's unique-rest set. **Killed:** covering
\(p=114\) silent; unique-rest xor \(=0\) as a title for this column.

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
Do **not** claim UNIQUE_REST xor tot equals rest.

Certify: `python3 research/cycle_qe.py --certify` (~0.16s).
Dump: `research/cycle_qe.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/PC/PV/QD/PM/PQ/PD/GU/HG/HH/HU (bits \(111..114\), even-\(t\)
\(p=114\) 4-tuple AND iff \(t\bmod 8=0\); Green \(n\equiv 3\pmod{4}\)
via new \(p=30\); prefix QD \(p=106\) xor, PM packed \(p=30\) xor
iff \(k=2\), PV Green \(p=16\); no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (bits \(111..114\))

For \(t\ge 158\): bit \(111=1\) iff \(t\bmod 8\in\{2,3,4,5\}\), bit
\(112=1\) iff \(t\bmod 8\in\{0,5\}\), bit \(113=1\) iff
\(t\bmod 8\in\{1,2,4\}\), bit \(114=1\) iff
\(t\bmod 8\in\{1,2,3,4,5\}\). Status: **lemma**. Checked on
\(0\le t\le 220\). Cycle QD's bits \(103..106\) from \(t\ge 147\)
agree on that prefix.

## Lemma (left 115-bit period \(8\) from \(t=158\))

Bits \(0..114\) are autonomous. The word at \(t=158\) equals
\(t=166\), so even \(t\ge 158\) is period \(8\). Status: **lemma**.

## Lemma (AND at \(p=114\) on even \(t\ge 158\))

Even \(t\ge 158\): the \(p=114\) 4-tuple is \(0100\) / \(1011\) /
\(1011\) / \(0000\), AND iff \(t\bmod 8=0\). Early even AND-ones
are exactly \(t\in\{56,62,78,96,106,112,122,130,150\}\).
Status: **lemma**.

## Lemma (Green \(p=30\) xor \(=1\) for \(k\ge 4\))

On the covering live window, \(G(n,5\cdot 2^k-15)=1\) matches
`in_p30` for \(k\ge 4\): even \(n\) vanish; odd \(n\) is parent
\(p=16\) at \(k-1\). The xor is \(0\) at \(k=3\) and \(1\) for
\(k\ge 4\). Packed \(p=30\) xor is \(1\) iff \(k=2\) (Cycle PM).
Status: **lemma**.

## Lemma (covering packed \(p=114\) xor \(=1\) iff \(k\ge 4\) and \(k\ne 6\))

Covering AND times after the freeze that hit \(G=1\) have
\(n\equiv 3\pmod{4}\). That family doubles to parent \(p=30\) at
\(k-2\). Green \(p=30\) xor is \(1\) for \(k-2\ge 4\). Thin packed
check on \(k\le 8\) gives xor \(=1\) at \(k=4,5\) and for \(k\ge 7\),
and \(0\) at \(k=6\). Status: **lemma**. **Killed:** silent;
unique-rest xor \(=0\) as this column's title.

## Verdict

`LEMMA` (bits \(111..114\); left-115 period \(8\); AND \(p=114\) on
even \(t\ge 158\) iff \(t\bmod 8=0\); Green \(p=30\) xor \(=1\) for
\(k\ge 4\); Green \(n\equiv 3\pmod{4}\) via \(p=30\); packed
\(p=114\) xor \(=1\) iff \(k\ge 4\) and \(k\ne 6\); QD \(p=106\)
xor).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (covering \(p=114\) silent; unique-rest xor \(=0\) as this
column).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
UNIQUE_REST xor tot equals rest; \(J_6=J_{10}=0\Rightarrow J_{18}=1\)
for all \(k\); 11-bit gap; formula for extra 414990; at-most-one-odd
for all \(k\); seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_qe.md` (this note)
- `research/cycle_qe.py`
- `research/cycle_qe.json`
