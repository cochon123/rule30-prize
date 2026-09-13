# Cycle PQ: covering packed AND xor at \(p=62\) is \(1\) iff \(k\in\{3,4\}\)

Cycle PP froze bits \(33,34\) and showed covering packed AND xor at
\(p=34\) is \(1\) iff \(k\in\{3,4\}\), because freeze AND requires
even \(n\) at odd \(j\). That vanishing is a family. Covering even
\(s=10U-2n-2\) for \(k\ge 3\) has \(s\bmod 8\in\{0,2,4,6\}\) iff
\(n\bmod 4\) is \(3,2,1,0\). Packed \(p\equiv 2\pmod{4}\) has odd
\(j=5U-p/2\), so even \(n\) have \(G=0\). Freeze AND residues in
\(\{2,6\}\) therefore make packed AND on \(G=1\) empty once \(t_0\)
exceeds the freeze (\(p=10,18,22,26,34\) already recorded; this
cycle adds \(p=62\)).

Bits \(59..62\) freeze from \(t\ge 88\): bit \(59=1\) iff
\(t\bmod 8\in\{3,5,7\}\), bit \(60=1\) iff
\(t\bmod 8\in\{1,3,5,6,7\}\), bit \(61=1\) iff
\(t\bmod 8\in\{2,3,7\}\), bit \(62=1\) iff
\(t\bmod 8\in\{2,3,6\}\). The left 63 bits are autonomous, and the
word at \(t=88\) equals \(t=96\), so even \(t\ge 88\) has the
\(p=62\) 4-tuple \(0000\) / \(0011\) / \(0000\) / \(0101\) on
\(t\bmod 8=0,2,4,6\), AND iff \(t\bmod 8=2\). Early even AND-ones
are \(t\in\{30,46,48,66,82\}\). Packed xor is therefore \(1\) iff
\(k\in\{3,4\}\). This is the \(2^a-2\) column after \(p=30\), not a
UNIQUE_REST slot. **Killed:** covering \(p=62\) silent for all \(k\)
(\(k=3,4\) fire).

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

Certify: `python3 research/cycle_pq.py --certify` (~0.14s).
Dump: `research/cycle_pq.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/PP/PO/PD/GU/HG/HH/HU (covering clock \(s\bmod 8\) vs
\(n\bmod 4\); bits \(59..62\); even-\(t\) \(p=62\) 4-tuple AND iff
\(t\bmod 8=2\); prefix PP \(p=34\) xor, PO \(p=64\) xor; no Fermat
table, no extra window, no \(n_0=16\) window, no packed covering
\(k=11\)).

## Lemma (covering clock \(s\bmod 8\) vs \(n\bmod 4\))

For \(k\ge 3\), covering even \(s=10U-2n-2\) has \(s\bmod 8=0,2,4,6\)
iff \(n\bmod 4=3,2,1,0\). Packed \(p\equiv 2\pmod{4}\) has odd \(j\).
Freeze AND residues in \(\{2,6\}\) hit only even \(n\), hence
\(G=0\). Status: **lemma**. Checked on \(3\le k\le 12\).

## Lemma (bits \(59..62\))

For \(t\ge 88\): bit \(59=1\) iff \(t\bmod 8\in\{3,5,7\}\), bit
\(60=1\) iff \(t\bmod 8\in\{1,3,5,6,7\}\), bit \(61=1\) iff
\(t\bmod 8\in\{2,3,7\}\), bit \(62=1\) iff
\(t\bmod 8\in\{2,3,6\}\). Status: **lemma**. Checked on
\(0\le t\le 128\).

## Lemma (left 63-bit period \(8\) from \(t=88\))

Bits \(0..62\) are autonomous. The word at \(t=88\) equals \(t=96\),
so even \(t\ge 88\) is period \(8\). Status: **lemma**.

## Lemma (AND at \(p=62\) on even \(t\ge 88\))

Even \(t\ge 88\): the \(p=62\) 4-tuple is \(0000\) / \(0011\) /
\(0000\) / \(0101\), AND iff \(t\bmod 8=2\). Early even AND-ones
are exactly \(t\in\{30,46,48,66,82\}\). Status: **lemma**.

## Lemma (covering packed \(p=62\) xor \(=1\) iff \(k\in\{3,4\}\))

Covering AND times after the freeze have \(n\equiv 2\pmod{4}\),
hence even \(n\), at odd \(j\), so \(G=0\). Packed AND on \(G=1\)
is identically \(0\) for \(k\ge 5\). Thin packed check on
\(k\le 8\) gives xor \(=1\) at \(k=3,4\) and \(0\) otherwise.
Green \(G=1\) still fires at odd \(n\). Status: **lemma**.
**Killed:** silent for all \(k\).

## Verdict

`LEMMA` (covering clock \(s\bmod 8\) vs \(n\bmod 4\); \(p\equiv 2
\pmod{4}\) has odd \(j\); bits \(59..62\); left-63 period \(8\);
AND \(p=62\) on even \(t\ge 88\) iff \(t\bmod 8=2\); covering
\(p=62\) silent for \(k\ge 5\); packed \(p=62\) xor \(=1\) iff
\(k\in\{3,4\}\); PP \(p=34\) xor).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (covering \(p=62\) silent for all \(k\)).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_pq.md` (this note)
- `research/cycle_pq.py`
- `research/cycle_pq.json`
