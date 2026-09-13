# Cycle PY: covering packed AND xor at \(p=72\) is \(1\) iff \(k=3\)

Cycle LP saw covering AND at UNIQUE_REST \(p=72\) on \(G=1\) is
always \(1001\) for \(k\ge 4\). Freeze AND residue is
\(t\bmod 8=2\) (\(n\equiv 2\pmod{4}\)). Column \(j=5U-36\) is even,
so even \(n\) can fire. Bits \(69..72\) freeze from \(t\ge 100\):
bit \(69=1\) iff \(t\bmod 8\in\{0,2,3,5,6\}\), bit \(70=1\) iff
\(t\bmod 8\in\{5,6,7\}\), bit \(71=1\) iff \(t\bmod 8\in\{0,3\}\),
bit \(72=1\) iff \(t\bmod 8\notin\{0,6\}\). The left 73 bits are
autonomous, and the word at \(t=100\) equals \(t=108\), so even
\(t\ge 100\) has the \(p=72\) 4-tuple \(1010\) / \(1001\) /
\(0001\) / \(1100\) on \(t\bmod 8=0,2,4,6\), AND iff
\(t\bmod 8=2\). For \(k\ge 6\) (\(t_0\ge 128\ge 100\)) packed AND
on \(G=1\) is \(1001\) iff \(n\equiv 2\pmod{4}\). Those \(n=4t+2\)
double twice to Green \(p=18\) xor Green \(p=20\) at scale \(k-2\).
Cycle PT's \(p=18\) Green xor is \(1\) for \(k\ge 3\); Green \(p=20\)
xor is \(1\) for \(k\ge 4\), so the slices cancel and packed xor is
\(0\) for \(k\ge 6\). Packed \(p=18\) is silent for \(k\ge 2\) and
packed \(p=20\) is silent for \(k\ge 4\) (Cycle PI) while both Green
columns fire. Early even AND-ones are
\(t\in\{58,60,80,84,88,90\}\); \(k=3\) xor \(=1\) and \(k=4,5\)
xor \(=0\). This is UNIQUE_REST \(p=72\). **Killed:** covering
\(p=72\) silent; unique-rest xor \(=0\) as a title for this column.

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

Certify: `python3 research/cycle_py.py --certify`.
Dump: `research/cycle_py.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/PC/PT/PN/PM/PX/PI/PQ/PD/GU/HG/HH/HU (bits \(69..72\),
even-\(t\) \(p=72\) 4-tuple AND iff \(t\bmod 8=2\); Green
\(n\equiv 2\pmod{4}\) via PT \(p=18\) xor new \(p=20\); prefix PX
\(p=60\) xor, PT \(p=18\) Green, PI packed \(p=20\) silent; no Fermat
table, no extra window, no \(n_0=16\) window, no packed covering
\(k=11\)).

## Lemma (bits \(69..72\))

For \(t\ge 100\): bit \(69=1\) iff \(t\bmod 8\in\{0,2,3,5,6\}\),
bit \(70=1\) iff \(t\bmod 8\in\{5,6,7\}\), bit \(71=1\) iff
\(t\bmod 8\in\{0,3\}\), bit \(72=1\) iff \(t\bmod 8\notin\{0,6\}\).
Status: **lemma**. Checked on \(0\le t\le 128\). Cycle PT's bits
\(67..70\) from \(t\ge 100\) agree on that prefix.

## Lemma (left 73-bit period \(8\) from \(t=100\))

Bits \(0..72\) are autonomous. The word at \(t=100\) equals
\(t=108\), so even \(t\ge 100\) is period \(8\). Status: **lemma**.

## Lemma (AND at \(p=72\) on even \(t\ge 100\))

Even \(t\ge 100\): the \(p=72\) 4-tuple is \(1010\) / \(1001\) /
\(0001\) / \(1100\), AND iff \(t\bmod 8=2\). Early even AND-ones
are exactly \(t\in\{58,60,80,84,88,90\}\). Status: **lemma**.

## Lemma (Green \(p=20\) xor \(=1\) for \(k\ge 4\))

On the covering live window, \(G(n,5\cdot 2^k-10)=1\) matches
`in_p20` for \(k\ge 4\): even \(n\) only if \(n\equiv 2\pmod{4}\),
via parent \(p=6\) at \(k-2\); odd \(n\) is parent \(p=10\) xor
\(p=12\) at \(k-1\). The xor is \(0\) at \(k=2,3\) and \(1\) for
\(k\ge 4\). Packed \(p=20\) is silent for \(k\ge 4\) (Cycle PI).
Status: **lemma**.

## Lemma (covering packed \(p=72\) xor \(=1\) iff \(k=3\))

Covering AND times after the freeze that hit \(G=1\) have
\(n\equiv 2\pmod{4}\). That family doubles to parent \(p=18\) xor
\(p=20\) at \(k-2\). Those Green xors are both \(1\) for
\(k-2\ge 4\), so they cancel. Thin packed check on \(k\le 8\) gives
xor \(=1\) only at \(k=3\). Status: **lemma**. **Killed:** silent;
unique-rest xor \(=0\) as this column's title.

## Verdict

`LEMMA` (bits \(69..72\); left-73 period \(8\); AND \(p=72\) on even
\(t\ge 100\) iff \(t\bmod 8=2\); Green \(p=20\) xor \(=1\) for
\(k\ge 4\); Green \(n\equiv 2\pmod{4}\) via \(p=18\oplus 20\);
packed \(p=72\) xor \(=1\) iff \(k=3\); PX \(p=60\) xor).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (covering \(p=72\) silent; unique-rest xor \(=0\) as this
column).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_py.md` (this note)
- `research/cycle_py.py`
- `research/cycle_py.json`
