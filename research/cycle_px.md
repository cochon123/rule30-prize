# Cycle PX: covering packed AND xor at \(p=60\) is \(1\) iff \(k=4\)

Cycle LL saw covering AND at UNIQUE_REST \(p=60\) on \(G=1\) is
always \(0100\) for \(k\ge 5\), with even count. Freeze AND
residues are \(t\bmod 8\in\{2,4,6\}\) (\(n\equiv 2,1,0\pmod{4}\)).
Column \(j=5U-30\) is even, so even \(n\) can fire, but
\(n\equiv 0\pmod{4}\) halves to an even first argument at an odd
second argument and \(G=0\). Bits \(57..60\) freeze from
\(t\ge 86\): bit \(57=1\) iff \(t\bmod 8\notin\{2,4\}\), bit
\(58=1\) iff \(t\bmod 8\notin\{5,6\}\), bit \(59=1\) iff
\(t\bmod 8\in\{3,5,7\}\), bit \(60=1\) iff
\(t\bmod 8\in\{1,3,5,6,7\}\). The left 61 bits are autonomous, and
the word at \(t=86\) equals \(t=94\), so even \(t\ge 86\) has the
\(p=60\) 4-tuple \(1100\) / \(0100\) / \(0100\) / \(1001\) on
\(t\bmod 8=0,2,4,6\), AND iff \(t\bmod 8\in\{2,4,6\}\). For
\(k\ge 6\) (\(t_0\ge 128\ge 86\)) packed AND on \(G=1\) is \(0100\)
iff \(n\equiv 1\) or \(2\pmod{4}\). Those \(n=4t+1\) and \(n=4t+2\)
both double twice to Green \(p=16\) at scale \(k-2\), whose xor is
\(1\) for \(k\ge 3\), so the two slices cancel and packed xor is
\(0\) for \(k\ge 5\). Early even AND-ones are
\(t\in\{30,36,42,48,52,80\}\); \(k=3\) xor \(=0\) and \(k=4\)
xor \(=1\). This is UNIQUE_REST \(p=60\). **Killed:** covering
\(p=60\) silent; unique-rest xor \(=0\) as a title for this column.

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

Certify: `python3 research/cycle_px.py --certify`.
Dump: `research/cycle_px.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/PC/PV/PW/PQ/PD/GU/HG/HH/HU (bits \(57..60\), even-\(t\)
\(p=60\) 4-tuple AND iff \(t\bmod 8\in\{2,4,6\}\); Green
\(n\equiv 1,2\pmod{4}\) via PV \(p=16\) xor; prefix PW \(p=52\) xor,
PV \(p=16\) Green; no Fermat table, no extra window, no \(n_0=16\)
window, no packed covering \(k=11\)).

## Lemma (bits \(57..60\))

For \(t\ge 86\): bit \(57=1\) iff \(t\bmod 8\notin\{2,4\}\), bit
\(58=1\) iff \(t\bmod 8\notin\{5,6\}\), bit \(59=1\) iff
\(t\bmod 8\in\{3,5,7\}\), bit \(60=1\) iff
\(t\bmod 8\in\{1,3,5,6,7\}\). Status: **lemma**. Checked on
\(0\le t\le 112\). Cycle PV's bits \(57,58\) from \(t\ge 84\) and
Cycle PQ's bits \(59,60\) from \(t\ge 88\) agree on those prefixes.

## Lemma (left 61-bit period \(8\) from \(t=86\))

Bits \(0..60\) are autonomous. The word at \(t=86\) equals \(t=94\),
so even \(t\ge 86\) is period \(8\). Status: **lemma**.

## Lemma (AND at \(p=60\) on even \(t\ge 86\))

Even \(t\ge 86\): the \(p=60\) 4-tuple is \(1100\) / \(0100\) /
\(0100\) / \(1001\), AND iff \(t\bmod 8\in\{2,4,6\}\). Early even
AND-ones are exactly \(t\in\{30,36,42,48,52,80\}\). Status:
**lemma**.

## Lemma (covering packed \(p=60\) xor \(=1\) iff \(k=4\))

Covering AND times after the freeze that hit \(G=1\) have
\(n\equiv 1\) or \(2\pmod{4}\). Both families double to parent
\(p=16\) at \(k-2\). Cycle PV's \(p=16\) Green xor is \(1\) for
\(k\ge 3\), so each slice xors to \(1\) for \(k\ge 5\) and they
cancel. Thin packed check on \(k\le 8\) gives xor \(=1\) only at
\(k=4\). Status: **lemma**. **Killed:** silent; unique-rest xor
\(=0\) as this column's title.

## Verdict

`LEMMA` (bits \(57..60\); left-61 period \(8\); AND \(p=60\) on even
\(t\ge 86\) iff \(t\bmod 8\in\{2,4,6\}\); Green \(n\equiv 1,2\pmod{4}\)
via \(p=16\); packed \(p=60\) xor \(=1\) iff \(k=4\); PW \(p=52\)
xor).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (covering \(p=60\) silent; unique-rest xor \(=0\) as this
column).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_px.md` (this note)
- `research/cycle_px.py`
- `research/cycle_px.json`
