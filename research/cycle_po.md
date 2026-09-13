# Cycle PO: covering packed AND xor at \(p=64\) is \(1\) iff \(k\in\{3,5\}\)

Cycle PN froze bits \(35..38\) and showed covering packed AND xor
at \(p=38\) is \(1\) iff \(k\in\{2,3\}\). Bits \(61..64\) freeze from
\(t\ge 92\): bit \(61=1\) iff \(t\bmod 8\in\{2,3,7\}\), bit \(62=1\)
iff \(t\bmod 8\in\{2,3,6\}\), bit \(63=1\) iff \(t\bmod 8=7\), bit
\(64=1\) iff \(t\bmod 8\notin\{3,7\}\). The left 65 bits are
autonomous, and the word at \(t=92\) equals \(t=100\), so even
\(t\ge 92\) has the \(p=64\) 4-tuple \(0001\) / \(1101\) / \(0001\) /
\(0101\) on \(t\bmod 8=0,2,4,6\), never an AND-one. Early even
AND-ones are \(t\in\{38,40,42,48,54,58,60,68,70,72,88\}\). Covering
\(k\ge 6\) starts at \(2U\ge 128>88\), so \(p=64\) is silent for
\(k\ge 6\). Packed xor is therefore \(1\) iff \(k\in\{3,5\}\). This
is a bulk leftover power-of-two column, not a UNIQUE_REST slot.
**Killed:** covering \(p=64\) silent for all \(k\) (\(k=3,5\) fire).

**Not** rest \(=S\oplus T\). **Not** leftover after
\(p=16\oplus 32\oplus 30\oplus 38\oplus 64\) equals \(S\oplus T\).
**Not** \(E_k=0\) for all \(k\). Do **not** catalogue further
\(S\)/\(T\) subregions unless the experiment answers why \(E_k=0\).
Do **not** claim pal-left leftover xor vanishes for all \(k\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\)
covering packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).

Certify: `python3 research/cycle_po.py --certify`.
Dump: `research/cycle_po.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/PN/PD/GU/HG/HH/HU (bits \(61..64\), even-\(t\) \(p=64\)
4-tuple never AND from \(t\ge 92\); prefix PN \(p=38\) xor, PM
\(p=30\) xor; no Fermat table, no extra window, no \(n_0=16\)
window, no packed covering \(k=11\)).

## Lemma (bits \(61..64\))

For \(t\ge 92\): bit \(61=1\) iff \(t\bmod 8\in\{2,3,7\}\), bit
\(62=1\) iff \(t\bmod 8\in\{2,3,6\}\), bit \(63=1\) iff
\(t\bmod 8=7\), bit \(64=1\) iff \(t\bmod 8\notin\{3,7\}\). Status:
**lemma**. Checked on \(0\le t\le 128\).

## Lemma (left 65-bit period \(8\) from \(t=92\))

Bits \(0..64\) are autonomous. The word at \(t=92\) equals \(t=100\),
so even \(t\ge 92\) is period \(8\). Status: **lemma**.

## Lemma (AND at \(p=64\) on even \(t\ge 92\))

Even \(t\ge 92\): the \(p=64\) 4-tuple is \(0001\) / \(1101\) /
\(0001\) / \(0101\), AND \(=0\). Early even AND-ones are exactly
\(t\in\{38,40,42,48,54,58,60,68,70,72,88\}\). Status: **lemma**.

## Lemma (covering packed \(p=64\) xor \(=1\) iff \(k\in\{3,5\}\))

Covering \(k\ge 6\) starts after the last AND-one, so packed AND is
identically \(0\). Thin packed check on \(k\le 8\) gives xor \(=1\)
at \(k=3,5\) and \(0\) otherwise. Status: **lemma**. **Killed:**
silent for all \(k\).

## Verdict

`LEMMA` (bits \(61..64\); left-65 period \(8\); AND \(p=64\) on even
\(t\ge 92\) is \(0\); covering \(p=64\) silent for \(k\ge 6\); packed
\(p=64\) xor \(=1\) iff \(k\in\{3,5\}\); PN \(p=38\) xor).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (covering \(p=64\) silent for all \(k\)).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_po.md` (this note)
- `research/cycle_po.py`
- `research/cycle_po.json`
