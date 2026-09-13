# Cycle QA: covering packed AND xor at \(p=86\) is \(1\) iff \(k=5\)

Cycle LS saw covering AND at UNIQUE_REST \(p=86\) on \(G=1\) is
always \(0011\) for \(k\ge 6\), with even count. Freeze AND
residues are \(t\bmod 8\in\{0,2,6\}\) (\(n\equiv 3,2,0\pmod{4}\)).
Column \(j=5U-43\) is odd, so even \(n\) have \(G=0\). Bits
\(83..86\) freeze from \(t\ge 125\): bit \(83=1\) iff
\(t\bmod 8\in\{1,2,3,5,6\}\), bit \(84=1\) iff \(t\bmod 8=4\),
bit \(85=1\) iff \(t\bmod 8\in\{0,1,3,5,7\}\), bit \(86=1\) iff
\(t\bmod 8\ne 5\). The left 87 bits are autonomous, and the word
at \(t=125\) equals \(t=133\), so even \(t\ge 126\) has the
\(p=86\) 4-tuple \(0011\) / \(1001\) / \(0101\) / \(1001\) on
\(t\bmod 8=0,2,4,6\), AND iff \(t\bmod 8\in\{0,2,6\}\). For
\(k\ge 6\) (\(t_0\ge 128\ge 125\)) packed AND on \(G=1\) is \(0011\)
iff \(n\equiv 3\pmod{4}\). Those \(n=4t+3\) double twice to Green
\(p=22\) xor Green \(p=24\) at scale \(k-2\). Both Green xors are
\(1\) for \(k\ge 4\), so the slices cancel and packed xor is \(0\)
for \(k\ge 6\). Packed \(p=22\) is silent for every \(k\) (Cycle PJ)
and packed \(p=24\) is silent for \(k\ge 4\) (Cycle PL) while both
Green columns fire. Early even AND-ones are
\(t\in\{42,44,56,58,70,72,76,84,114\}\); \(k=4\) xor \(=0\) and
\(k=5\) xor \(=1\). This is UNIQUE_REST \(p=86\). **Killed:**
covering \(p=86\) silent; unique-rest xor \(=0\) as a title for
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

Certify: `python3 research/cycle_qa.py --certify`.
Dump: `research/cycle_qa.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/PC/PN/PZ/PJ/PL/PQ/PD/GU/HG/HH/HU (bits \(83..86\),
even-\(t\) \(p=86\) 4-tuple AND iff \(t\bmod 8\in\{0,2,6\}\); Green
\(n\equiv 3\pmod{4}\) via new \(p=22\oplus 24\); prefix PZ \(p=76\)
xor, PJ packed \(p=22\) silent, PL packed \(p=24\) silent; no Fermat
table, no extra window, no \(n_0=16\) window, no packed covering
\(k=11\)).

## Lemma (bits \(83..86\))

For \(t\ge 125\): bit \(83=1\) iff \(t\bmod 8\in\{1,2,3,5,6\}\),
bit \(84=1\) iff \(t\bmod 8=4\), bit \(85=1\) iff
\(t\bmod 8\in\{0,1,3,5,7\}\), bit \(86=1\) iff \(t\bmod 8\ne 5\).
Status: **lemma**. Checked on \(0\le t\le 160\). Cycle PZ's bits
\(73..76\) from \(t\ge 104\) agree on that prefix.

## Lemma (left 87-bit period \(8\) from \(t=125\))

Bits \(0..86\) are autonomous. The word at \(t=125\) equals
\(t=133\), so even \(t\ge 126\) is period \(8\). Status: **lemma**.

## Lemma (AND at \(p=86\) on even \(t\ge 126\))

Even \(t\ge 126\): the \(p=86\) 4-tuple is \(0011\) / \(1001\) /
\(0101\) / \(1001\), AND iff \(t\bmod 8\in\{0,2,6\}\). Early even
AND-ones are exactly \(t\in\{42,44,56,58,70,72,76,84,114\}\).
Status: **lemma**.

## Lemma (Green \(p=22\) xor \(=1\) for \(k\ge 4\))

On the covering live window, \(G(n,5\cdot 2^k-11)=1\) matches
`in_p22` for \(k\ge 4\): even \(n\) vanish; odd \(n\) is parent
\(p=12\) at \(k-1\). The xor is \(0\) at \(k=3\) and \(1\) for
\(k\ge 4\). Packed \(p=22\) is silent for every \(k\) (Cycle PJ).
Status: **lemma**.

## Lemma (Green \(p=24\) xor \(=1\) for \(k\ge 4\))

On the covering live window, \(G(n,5\cdot 2^k-12)=1\) matches
`in_p24` for \(k\ge 4\): even \(n\) is parent \(p=12\) at \(k-1\);
odd \(n\) is parent \(p=12\) xor \(p=14\) at \(k-1\). The xor is
\(0\) at \(k=3\) and \(1\) for \(k\ge 4\). Packed \(p=24\) is silent
for \(k\ge 4\) (Cycle PL). Status: **lemma**.

## Lemma (covering packed \(p=86\) xor \(=1\) iff \(k=5\))

Covering AND times after the freeze that hit \(G=1\) have
\(n\equiv 3\pmod{4}\). That family doubles to parent \(p=22\) xor
\(p=24\) at \(k-2\). Those Green xors are both \(1\) for
\(k-2\ge 4\), so they cancel. Thin packed check on \(k\le 8\) gives
xor \(=1\) only at \(k=5\). Status: **lemma**. **Killed:** silent;
unique-rest xor \(=0\) as this column's title.

## Verdict

`LEMMA` (bits \(83..86\); left-87 period \(8\); AND \(p=86\) on even
\(t\ge 126\) iff \(t\bmod 8\in\{0,2,6\}\); Green \(p=22\) and
\(p=24\) xor \(=1\) for \(k\ge 4\); Green \(n\equiv 3\pmod{4}\) via
\(p=22\oplus 24\); packed \(p=86\) xor \(=1\) iff \(k=5\); PZ
\(p=76\) xor).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (covering \(p=86\) silent; unique-rest xor \(=0\) as this
column).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_qa.md` (this note)
- `research/cycle_qa.py`
- `research/cycle_qa.json`
