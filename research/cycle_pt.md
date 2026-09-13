# Cycle PT: covering packed AND xor at \(p=70\) is \(1\) for \(k\ge 6\)

Cycle PS closed leftover-family \(p=54\) via freeze AND
\(t\bmod 8=4\) (\(n\equiv 1\pmod{4}\)) doubling to Green \(p=14\).
The next leftover column with the same freeze residue is \(p=70\).
Bits \(67..70\) freeze from \(t\ge 100\): bit \(67=1\) iff
\(t\bmod 8\in\{0,1,3,6\}\), bit \(68=1\) iff
\(t\bmod 8\in\{0,2,3,4,7\}\), bit \(69=1\) iff
\(t\bmod 8\in\{0,2,3,5,6\}\), bit \(70=1\) iff
\(t\bmod 8\in\{5,6,7\}\). The left 71 bits are autonomous, and the
word at \(t=100\) equals \(t=108\), so even \(t\ge 100\) has the
\(p=70\) 4-tuple \(1110\) / \(0110\) / \(0100\) / \(1011\) on
\(t\bmod 8=0,2,4,6\), AND iff \(t\bmod 8=4\). For \(k\ge 6\)
(\(t_0\ge 128\ge 100\)) packed AND on \(G=1\) is \(0100\) iff
\(n\equiv 1\pmod{4}\). Those \(n=4t+1\) double twice to Green
\(p=18\) at scale \(k-2\). Odd \(n\) at Green \(p=18\) doubles to
parent \(p=10\), whose xor is \(1\) for \(k\ge 2\), so Green
\(p=18\) xor is \(1\) for \(k\ge 3\) and packed xor is \(1\) for
\(k\ge 6\). Packed \(p=18\) is silent for \(k\ge 2\) (Cycle PI)
while Green still fires. Early even AND-ones are
\(t\in\{34,36,50,52,62,64,84\}\); \(k\le 5\) xor \(=0\). This is
leftover, not UNIQUE_REST. **Killed:** covering \(p=70\) silent.

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

Certify: `python3 research/cycle_pt.py --certify`.
Dump: `research/cycle_pt.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/PC/PM/PI/PS/PO/PQ/PD/GU/HG/HH/HU (bits \(67..70\), even-\(t\)
\(p=70\) 4-tuple AND iff \(t\bmod 8=4\); Green \(n\equiv 1\pmod{4}\)
via \(p=18\) xor from PM \(p=10\); prefix PS \(p=54\) xor, PM
\(p=10\) Green, PI packed \(p=18\) silent; no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (bits \(67..70\))

For \(t\ge 100\): bit \(67=1\) iff \(t\bmod 8\in\{0,1,3,6\}\), bit
\(68=1\) iff \(t\bmod 8\in\{0,2,3,4,7\}\), bit \(69=1\) iff
\(t\bmod 8\in\{0,2,3,5,6\}\), bit \(70=1\) iff
\(t\bmod 8\in\{5,6,7\}\). Status: **lemma**. Checked on
\(0\le t\le 128\).

## Lemma (left 71-bit period \(8\) from \(t=100\))

Bits \(0..70\) are autonomous. The word at \(t=100\) equals \(t=108\),
so even \(t\ge 100\) is period \(8\). Status: **lemma**.

## Lemma (AND at \(p=70\) on even \(t\ge 100\))

Even \(t\ge 100\): the \(p=70\) 4-tuple is \(1110\) / \(0110\) /
\(0100\) / \(1011\), AND iff \(t\bmod 8=4\). Early even AND-ones
are exactly \(t\in\{34,36,50,52,62,64,84\}\). Status: **lemma**.

## Lemma (Green \(p=18\) xor \(=1\) for \(k\ge 3\))

Column \(j=5\cdot 2^k-9\) is odd, so even \(n\) vanish. Odd
\(n=2m+1\) doubles to Green \(p=10\) at \(k-1\). Cycle PM's
\(p=10\) Green xor is \(1\) for \(k\ge 2\), so \(p=18\) xor is
\(1\) for \(k\ge 3\). Packed \(p=18\) remains silent for \(k\ge 2\).
Status: **lemma**.

## Lemma (covering packed \(p=70\) xor \(=1\) for \(k\ge 6\))

Covering AND times after the freeze have \(n\equiv 1\pmod{4}\).
Those \(n=4t+1\) double to parent \(p=18\) at \(k-2\). Green
\(p=18\) xor is \(1\) for \(k\ge 3\), so the
\(n\equiv 1\pmod{4}\) xor is \(1\) for \(k\ge 5\). Thin packed
check on \(k\le 8\) gives xor \(=1\) for \(k\ge 6\) and \(0\)
otherwise (\(t_0<100\) at \(k\le 5\)). Status: **lemma**.
**Killed:** silent.

## Verdict

`LEMMA` (bits \(67..70\); left-71 period \(8\); AND \(p=70\) on even
\(t\ge 100\) iff \(t\bmod 8=4\); Green \(p=18\) xor \(=1\) for
\(k\ge 3\); Green \(n\equiv 1\pmod{4}\) via \(p=18\); packed
\(p=70\) xor \(=1\) for \(k\ge 6\); PS \(p=54\) xor).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (covering \(p=70\) silent).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_pt.md` (this note)
- `research/cycle_pt.py`
- `research/cycle_pt.json`
