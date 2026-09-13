# Cycle PZ: covering packed AND xor at \(p=76\) is \(1\) iff \(k\ge 3\) and \(k\ne 4\)

Cycle LT saw covering AND at UNIQUE_REST \(p=76\) on \(G=1\) is
always \(0011\) for \(k\ge 6\), with odd count. Freeze AND residue
is \(t\bmod 8=4\) (\(n\equiv 1\pmod{4}\)). Column \(j=5U-38\) is
even and \(j/2\) is odd, so \(n\equiv 0\pmod{4}\) has \(G=0\). Bits
\(73..76\) freeze from \(t\ge 104\): bit \(73=1\) iff
\(t\bmod 8\notin\{1,4\}\), bit \(74=1\) iff
\(t\bmod 8\in\{1,5,7\}\), bit \(75=1\) iff
\(t\bmod 8\in\{1,2,4,5,7\}\), bit \(76=1\) iff
\(t\bmod 8\in\{3,4,5\}\). The left 77 bits are autonomous, and the
word at \(t=104\) equals \(t=112\), so even \(t\ge 104\) has the
\(p=76\) 4-tuple \(1000\) / \(1010\) / \(0011\) / \(1000\) on
\(t\bmod 8=0,2,4,6\), AND iff \(t\bmod 8=4\). For \(k\ge 6\)
(\(t_0\ge 128\ge 104\)) packed AND on \(G=1\) is \(0011\) iff
\(n\equiv 1\pmod{4}\). Those \(n=4t+1\) double twice to Green
\(p=20\) at scale \(k-2\), whose xor is \(1\) for \(k\ge 4\), so
packed xor is \(1\) for \(k\ge 6\). Early even AND-ones are
\(t\in\{38,42,60,76,82,84,90,96,100,102\}\); \(k=3\) xor \(=1\),
\(k=4\) xor \(=0\), \(k=5\) xor \(=1\). This is UNIQUE_REST
\(p=76\). **Killed:** covering \(p=76\) silent; unique-rest xor
\(=0\) as a title for this column.

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

Certify: `python3 research/cycle_pz.py --certify` (~0.14s).
Dump: `research/cycle_pz.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/PC/PY/PQ/PD/GU/HG/HH/HU (bits \(73..76\), even-\(t\)
\(p=76\) 4-tuple AND iff \(t\bmod 8=4\); Green \(n\equiv 1\pmod{4}\)
via PY \(p=20\) xor; prefix PY \(p=72\) xor and \(p=20\) Green; no
Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (bits \(73..76\))

For \(t\ge 104\): bit \(73=1\) iff \(t\bmod 8\notin\{1,4\}\), bit
\(74=1\) iff \(t\bmod 8\in\{1,5,7\}\), bit \(75=1\) iff
\(t\bmod 8\in\{1,2,4,5,7\}\), bit \(76=1\) iff
\(t\bmod 8\in\{3,4,5\}\). Status: **lemma**. Checked on
\(0\le t\le 128\). Cycle PY's bits \(71,72\) from \(t\ge 100\) agree
on that prefix.

## Lemma (left 77-bit period \(8\) from \(t=104\))

Bits \(0..76\) are autonomous. The word at \(t=104\) equals
\(t=112\), so even \(t\ge 104\) is period \(8\). Status: **lemma**.

## Lemma (AND at \(p=76\) on even \(t\ge 104\))

Even \(t\ge 104\): the \(p=76\) 4-tuple is \(1000\) / \(1010\) /
\(0011\) / \(1000\), AND iff \(t\bmod 8=4\). Early even AND-ones
are exactly \(t\in\{38,42,60,76,82,84,90,96,100,102\}\). Status:
**lemma**.

## Lemma (covering packed \(p=76\) xor \(=1\) iff \(k\ge 3\) and \(k\ne 4\))

Covering AND times after the freeze that hit \(G=1\) have
\(n\equiv 1\pmod{4}\). That family doubles to parent \(p=20\) at
\(k-2\). Cycle PY's \(p=20\) Green xor is \(1\) for \(k\ge 4\), so
packed xor is \(1\) for \(k\ge 6\). Thin packed check on \(k\le 8\)
gives xor \(=1\) at \(k=3\) and every \(k\ge 5\), and \(0\) at
\(k=4\). Status: **lemma**. **Killed:** silent; unique-rest xor
\(=0\) as this column's title.

## Verdict

`LEMMA` (bits \(73..76\); left-77 period \(8\); AND \(p=76\) on even
\(t\ge 104\) iff \(t\bmod 8=4\); Green \(n\equiv 1\pmod{4}\) via
\(p=20\); packed \(p=76\) xor \(=1\) iff \(k\ge 3\) and \(k\ne 4\);
PY \(p=72\) xor).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (covering \(p=76\) silent; unique-rest xor \(=0\) as this
column).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_pz.md` (this note)
- `research/cycle_pz.py`
- `research/cycle_pz.json`
