# Cycle PV: covering packed AND xor at \(p=58\) is \(1\) iff \(k\ge 3\) and \(k\ne 5\)

Cycle LR saw covering AND at UNIQUE_REST \(p=58\) on \(G=1\) is
always \(0011\) for \(k\ge 6\), with odd count. Freeze AND residues
are \(t\bmod 8\in\{0,2,6\}\) (\(n\equiv 3,2,0\pmod{4}\)). Column
\(j=5U-29\) is odd, so even \(n\) vanish; the \(G=1\) fire is
\(t\bmod 8=0\) (\(n\equiv 3\pmod{4}\)). Bits \(55..58\) freeze from
\(t\ge 84\): bit \(55=1\) iff \(t\bmod 8\in\{1,2,3\}\), bit
\(56=1\) iff \(t\bmod 8\in\{4,5\}\), bit \(57=1\) iff
\(t\bmod 8\notin\{2,4\}\), bit \(58=1\) iff
\(t\bmod 8\notin\{5,6\}\). The left 59 bits are autonomous, and the
word at \(t=84\) equals \(t=92\), so even \(t\ge 84\) has the
\(p=58\) 4-tuple \(0011\) / \(1001\) / \(0101\) / \(0010\) on
\(t\bmod 8=0,2,4,6\), AND iff \(t\bmod 8\in\{0,2,6\}\). For
\(k\ge 6\) (\(t_0\ge 128\ge 84\)) packed AND on \(G=1\) is \(0011\)
iff \(n\equiv 3\pmod{4}\). Those \(n=4t+3\) double twice to Green
\(p=16\) at scale \(k-2\). Odd \(n\) at Green \(p=16\) is parent
\(p=8\) xor \(p=10\); even \(n\) doubles to \(p=8\). Green \(p=16\)
xor is \(1\) for \(k\ge 3\) (odd slice vanishes), so packed xor is
\(1\) for \(k\ge 6\). Early even AND-ones are
\(t\in\{28,30,52,60,62,64\}\); \(k=3,4\) xor \(=1\) and \(k=5\) xor
\(=0\). This is UNIQUE_REST \(p=58\). **Killed:** covering \(p=58\)
silent; unique-rest xor \(=0\) as a title for this column.

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

Certify: `python3 research/cycle_pv.py --certify`.
Dump: `research/cycle_pv.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/PC/PH/PM/PS/PU/PQ/PD/GU/HG/HH/HU (bits \(55..58\), even-\(t\)
\(p=58\) 4-tuple AND iff \(t\bmod 8\in\{0,2,6\}\); Green
\(n\equiv 3\pmod{4}\) via \(p=16\); prefix PU \(p=40\) xor, PH
packed \(p=16\), PM \(p=10\) Green; no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (bits \(55..58\))

For \(t\ge 84\): bit \(55=1\) iff \(t\bmod 8\in\{1,2,3\}\), bit
\(56=1\) iff \(t\bmod 8\in\{4,5\}\), bit \(57=1\) iff
\(t\bmod 8\notin\{2,4\}\), bit \(58=1\) iff
\(t\bmod 8\notin\{5,6\}\). Status: **lemma**. Checked on
\(0\le t\le 112\).

## Lemma (left 59-bit period \(8\) from \(t=84\))

Bits \(0..58\) are autonomous. The word at \(t=84\) equals \(t=92\),
so even \(t\ge 84\) is period \(8\). Status: **lemma**.

## Lemma (AND at \(p=58\) on even \(t\ge 84\))

Even \(t\ge 84\): the \(p=58\) 4-tuple is \(0011\) / \(1001\) /
\(0101\) / \(0010\), AND iff \(t\bmod 8\in\{0,2,6\}\). Early even
AND-ones are exactly \(t\in\{28,30,52,60,62,64\}\). Status:
**lemma**.

## Lemma (Green \(p=16\) xor \(=1\) for \(k\ge 3\))

Even \(n\) doubles to Green \(p=8\) at \(k-1\). Odd \(n=2m+1\) is
\(p=8\) xor \(p=10\) at \(k-1\); that odd slice xors to \(0\).
Packed \(p=16\) xor is the even slice, \(1\) for \(k\ge 3\). Status:
**lemma**.

## Lemma (covering packed \(p=58\) xor \(=1\) iff \(k\ge 3\) and \(k\ne 5\))

Covering AND times after the freeze that hit \(G=1\) have
\(n\equiv 3\pmod{4}\). Those \(n=4t+3\) double to parent \(p=16\)
at \(k-2\). Green \(p=16\) xor is \(1\) for \(k\ge 3\), so the
\(n\equiv 3\pmod{4}\) xor is \(1\) for \(k\ge 5\). Thin packed
check on \(k\le 8\) gives xor \(=1\) for \(k\ge 3\) except \(k=5\)
(\(t_0<84\)). Status: **lemma**. **Killed:** silent; unique-rest xor
\(=0\) as this column's title.

## Verdict

`LEMMA` (bits \(55..58\); left-59 period \(8\); AND \(p=58\) on even
\(t\ge 84\) iff \(t\bmod 8\in\{0,2,6\}\); Green \(p=16\) xor \(=1\)
for \(k\ge 3\); Green \(n\equiv 3\pmod{4}\) via \(p=16\); packed
\(p=58\) xor \(=1\) iff \(k\ge 3\) and \(k\ne 5\); PU \(p=40\) xor).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (covering \(p=58\) silent; unique-rest xor \(=0\) as this
column).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_pv.md` (this note)
- `research/cycle_pv.py`
- `research/cycle_pv.json`
