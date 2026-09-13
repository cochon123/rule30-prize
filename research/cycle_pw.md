# Cycle PW: covering packed AND xor at \(p=52\) is \(1\) iff \(k=3\)

Cycle LM saw covering AND at UNIQUE_REST \(p=52\) on \(G=1\) is
always \(1001\) for \(k\ge 5\), with even count. Freeze AND
residues are \(t\bmod 8\in\{2,4\}\) (\(n\equiv 2,1\pmod{4}\)).
Column \(j=5U-26\) is even, so even \(n\) can fire. Bits
\(49..52\) freeze from \(t\ge 76\): bit \(49=1\) iff
\(t\bmod 8\ne 7\), bit \(50=1\) iff \(t\bmod 8\in\{0,1,5,7\}\),
bit \(51=1\) iff \(t\bmod 8\in\{0,3,5,7\}\), bit \(52=1\) iff
\(t\bmod 8\in\{2,3,4,5\}\). The left 53 bits are autonomous, and
the word at \(t=76\) equals \(t=84\), so even \(t\ge 76\) has the
\(p=52\) 4-tuple \(1110\) / \(1001\) / \(1001\) / \(1000\) on
\(t\bmod 8=0,2,4,6\), AND iff \(t\bmod 8\in\{2,4\}\). For
\(k\ge 6\) (\(t_0\ge 128\ge 76\)) packed AND on \(G=1\) is \(1001\)
iff \(n\equiv 1\) or \(2\pmod{4}\). Those \(n=4t+1\) and \(n=4t+2\)
both double twice to Green \(p=14\) at scale \(k-2\), whose xor is
\(1\) for \(k\ge 3\), so the two slices cancel and packed xor is
\(0\) for \(k\ge 5\). Early even AND-ones are
\(t\in\{26,32,44,48,50,52,62\}\); \(k=3\) xor \(=1\) and \(k=4\)
xor \(=0\). This is UNIQUE_REST \(p=52\). **Killed:** covering
\(p=52\) silent; unique-rest xor \(=0\) as a title for this column.

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

Certify: `python3 research/cycle_pw.py --certify`.
Dump: `research/cycle_pw.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/PC/PV/PS/PQ/PD/GU/HG/HH/HU (bits \(49..52\), even-\(t\)
\(p=52\) 4-tuple AND iff \(t\bmod 8\in\{2,4\}\); Green
\(n\equiv 1,2\pmod{4}\) via PC \(p=14\) xor; prefix PV \(p=58\) xor,
PC \(p=14\) Green; no Fermat table, no extra window, no \(n_0=16\)
window, no packed covering \(k=11\)).

## Lemma (bits \(49..52\))

For \(t\ge 76\): bit \(49=1\) iff \(t\bmod 8\ne 7\), bit \(50=1\)
iff \(t\bmod 8\in\{0,1,5,7\}\), bit \(51=1\) iff
\(t\bmod 8\in\{0,3,5,7\}\), bit \(52=1\) iff
\(t\bmod 8\in\{2,3,4,5\}\). Status: **lemma**. Checked on
\(0\le t\le 96\).

## Lemma (left 53-bit period \(8\) from \(t=76\))

Bits \(0..52\) are autonomous. The word at \(t=76\) equals \(t=84\),
so even \(t\ge 76\) is period \(8\). Status: **lemma**.

## Lemma (AND at \(p=52\) on even \(t\ge 76\))

Even \(t\ge 76\): the \(p=52\) 4-tuple is \(1110\) / \(1001\) /
\(1001\) / \(1000\), AND iff \(t\bmod 8\in\{2,4\}\). Early even
AND-ones are exactly \(t\in\{26,32,44,48,50,52,62\}\). Status:
**lemma**.

## Lemma (covering packed \(p=52\) xor \(=1\) iff \(k=3\))

Covering AND times after the freeze that hit \(G=1\) have
\(n\equiv 1\) or \(2\pmod{4}\). Both families double to parent
\(p=14\) at \(k-2\). Cycle PC's \(p=14\) Green xor is \(1\) for
\(k\ge 3\), so each slice xors to \(1\) for \(k\ge 5\) and they
cancel. Thin packed check on \(k\le 8\) gives xor \(=1\) only at
\(k=3\). Status: **lemma**. **Killed:** silent; unique-rest xor
\(=0\) as this column's title.

## Verdict

`LEMMA` (bits \(49..52\); left-53 period \(8\); AND \(p=52\) on even
\(t\ge 76\) iff \(t\bmod 8\in\{2,4\}\); Green \(n\equiv 1,2\pmod{4}\)
via \(p=14\); packed \(p=52\) xor \(=1\) iff \(k=3\); PV \(p=58\)
xor).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (covering \(p=52\) silent; unique-rest xor \(=0\) as this
column).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_pw.md` (this note)
- `research/cycle_pw.py`
- `research/cycle_pw.json`
