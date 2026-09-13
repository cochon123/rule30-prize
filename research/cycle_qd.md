# Cycle QD: covering packed AND xor at \(p=106\) is \(1\) iff \(k=5\) or \(k\ge 7\)

Cycle LI saw covering AND at UNIQUE_REST \(p=106\) on \(G=1\) is
always \(1001\) for \(k\le 6\). Freeze AND residues are
\(t\bmod 8\in\{0,6\}\) (\(n\equiv 3,0\pmod{4}\)). Column
\(j=5U-53\) is odd, so even \(n\) have \(G=0\). Bits \(103..106\)
freeze from \(t\ge 147\): bit \(103=1\) iff \(t\bmod 8\in\{0,1,7\}\),
bit \(104=1\) iff \(t\bmod 8\in\{2,3,4\}\), bit \(105=1\) iff
\(t\bmod 8\notin\{0,2\}\), bit \(106=1\) iff
\(t\bmod 8\in\{0,1,2,6,7\}\). The left 107 bits are autonomous, and
the word at \(t=147\) equals \(t=155\), so even \(t\ge 148\) has the
\(p=106\) 4-tuple \(1001\) / \(0101\) / \(0110\) / \(0011\) on
\(t\bmod 8=0,2,4,6\), AND iff \(t\bmod 8\in\{0,6\}\). For
\(k\ge 7\) (\(t_0\ge 256\ge 147\)) packed AND on \(G=1\) is \(1001\)
iff \(n\equiv 3\pmod{4}\). Those \(n=4t+3\) double twice to Green
\(p=28\) at scale \(k-2\). Green \(p=28\) xor is \(1\) for \(k\ge 4\)
(even \(n\) via parent \(p=14\); odd \(n\) is \(p=14\) xor \(p=16\)
and cancels), so packed xor is \(1\) for \(k\ge 7\). Packed \(p=28\)
is silent for every \(k\) (Cycle PL) while Green \(p=28\) fires.
Early even AND-ones are \(t\in\{52,54,68,70,74,102,130\}\); \(k=5\)
xor \(=1\) and \(k=6\) xor \(=0\). This is UNIQUE_REST \(p=106\).
**Killed:** covering \(p=106\) silent; unique-rest xor \(=0\) as a
title for this column.

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

Certify: `python3 research/cycle_qd.py --certify` (~0.15s).
Dump: `research/cycle_qd.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/PC/PV/QC/PL/PQ/PD/GU/HG/HH/HU (bits \(103..106\), even-\(t\)
\(p=106\) 4-tuple AND iff \(t\bmod 8\in\{0,6\}\); Green
\(n\equiv 3\pmod{4}\) via new \(p=28\); prefix QC \(p=98\) xor, PL
packed \(p=28\) silent, PV Green \(p=16\), PC Green \(p=14\); no
Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (bits \(103..106\))

For \(t\ge 147\): bit \(103=1\) iff \(t\bmod 8\in\{0,1,7\}\), bit
\(104=1\) iff \(t\bmod 8\in\{2,3,4\}\), bit \(105=1\) iff
\(t\bmod 8\notin\{0,2\}\), bit \(106=1\) iff
\(t\bmod 8\in\{0,1,2,6,7\}\). Status: **lemma**. Checked on
\(0\le t\le 200\). Cycle QC's bits \(95..98\) from \(t\ge 132\)
agree on that prefix.

## Lemma (left 107-bit period \(8\) from \(t=147\))

Bits \(0..106\) are autonomous. The word at \(t=147\) equals
\(t=155\), so even \(t\ge 148\) is period \(8\). Status: **lemma**.

## Lemma (AND at \(p=106\) on even \(t\ge 148\))

Even \(t\ge 148\): the \(p=106\) 4-tuple is \(1001\) / \(0101\) /
\(0110\) / \(0011\), AND iff \(t\bmod 8\in\{0,6\}\). Early even
AND-ones are exactly \(t\in\{52,54,68,70,74,102,130\}\).
Status: **lemma**.

## Lemma (Green \(p=28\) xor \(=1\) for \(k\ge 4\))

On the covering live window, \(G(n,5\cdot 2^k-14)=1\) matches
`in_p28` for \(k\ge 4\): even \(n\) is parent \(p=14\) at \(k-1\);
odd \(n\) is parent \(p=14\) xor \(p=16\) at \(k-1\) and those xors
cancel. The tot xor is \(0\) at \(k=3\) and \(1\) for \(k\ge 4\).
Packed \(p=28\) is silent for every \(k\) (Cycle PL). Status:
**lemma**.

## Lemma (covering packed \(p=106\) xor \(=1\) iff \(k=5\) or \(k\ge 7\))

Covering AND times after the freeze that hit \(G=1\) have
\(n\equiv 3\pmod{4}\). That family doubles to parent \(p=28\) at
\(k-2\). Green \(p=28\) xor is \(1\) for \(k-2\ge 4\). Thin packed
check on \(k\le 8\) gives xor \(=1\) at \(k=5\) and for \(k\ge 7\),
and \(0\) at \(k=4,6\). Status: **lemma**. **Killed:** silent;
unique-rest xor \(=0\) as this column's title.

## Verdict

`LEMMA` (bits \(103..106\); left-107 period \(8\); AND \(p=106\) on
even \(t\ge 148\) iff \(t\bmod 8\in\{0,6\}\); Green \(p=28\) xor
\(=1\) for \(k\ge 4\); Green \(n\equiv 3\pmod{4}\) via \(p=28\);
packed \(p=106\) xor \(=1\) iff \(k=5\) or \(k\ge 7\); QC \(p=98\)
xor).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (covering \(p=106\) silent; unique-rest xor \(=0\) as this
column).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_qd.md` (this note)
- `research/cycle_qd.py`
- `research/cycle_qd.json`
