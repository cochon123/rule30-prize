# Cycle PU: covering packed AND xor at \(p=40\) is \(1\) iff \(k\in\{2,4\}\)

After Cycle PT, leftover xor still equals rest on \(q=10\) through
\(k\le 10\). At \(k=2\) the remaining leftover bit is packed
\(p=40\). Bits \(39,40\) freeze from \(t\ge 56\): bit \(39=1\) iff
\(t\bmod 8\in\{6,7\}\), bit \(40=1\) iff
\(t\bmod 8\in\{2,4\}\). Bits \(37,38\) already freeze from
\(t\ge 48\) (Cycle PN). The left 41 bits are autonomous, and the
word at \(t=56\) equals \(t=64\), so even \(t\ge 56\) has the
\(p=40\) 4-tuple \(0000\) / \(1101\) / \(1101\) / \(0110\) on
\(t\bmod 8=0,2,4,6\), never an AND-one. Early even AND-ones are
\(t\in\{28,32,38,42,44,48\}\). Covering \(k\ge 5\) starts at
\(t_0\ge 64>48\), so packed AND on \(G=1\) is empty for
\(k\ge 5\). Thin packed check on \(k\le 8\) gives xor \(=1\) iff
\(k\in\{2,4\}\). This is leftover, not UNIQUE_REST. **Killed:**
covering \(p=40\) silent for all \(k\) (\(k=2,4\) fire).

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

Certify: `python3 research/cycle_pu.py --certify` (~0.14s).
Dump: `research/cycle_pu.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/PN/PT/PD/GU/HG/HH/HU (bits \(39,40\), even-\(t\)
\(p=40\) 4-tuple never AND for \(t\ge 56\); prefix PT \(p=70\) xor,
PN \(p=38\) xor; no Fermat table, no extra window, no \(n_0=16\)
window, no packed covering \(k=11\)).

## Lemma (bits \(39,40\))

For \(t\ge 56\): bit \(39=1\) iff \(t\bmod 8\in\{6,7\}\), bit
\(40=1\) iff \(t\bmod 8\in\{2,4\}\). Status: **lemma**. Checked on
\(0\le t\le 80\).

## Lemma (left 41-bit period \(8\) from \(t=56\))

Bits \(0..40\) are autonomous. The word at \(t=56\) equals \(t=64\),
so even \(t\ge 56\) is period \(8\). Status: **lemma**.

## Lemma (AND at \(p=40\) on even \(t\ge 56\))

Even \(t\ge 56\): the \(p=40\) 4-tuple is \(0000\) / \(1101\) /
\(1101\) / \(0110\), never an AND-one. Early even AND-ones are
exactly \(t\in\{28,32,38,42,44,48\}\). Status: **lemma**.

## Lemma (covering packed \(p=40\) xor \(=1\) iff \(k\in\{2,4\}\))

Covering \(k\ge 5\) starts after the last early AND, so packed AND
on \(G=1\) is empty. Thin packed check on \(k\le 8\) gives xor
\(=1\) at \(k=2,4\) and \(0\) otherwise. Status: **lemma**.
**Killed:** silent for all \(k\).

## Verdict

`LEMMA` (bits \(39,40\); left-41 period \(8\); AND \(p=40\) on even
\(t\ge 56\) never; packed \(p=40\) silent for \(k\ge 5\); packed
\(p=40\) xor \(=1\) iff \(k\in\{2,4\}\); PT \(p=70\) xor).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (covering \(p=40\) silent for all \(k\)).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_pu.md` (this note)
- `research/cycle_pu.py`
- `research/cycle_pu.json`
