# Cycle PP: covering packed AND xor at \(p=34\) is \(1\) iff \(k\in\{3,4\}\)

Cycle PO froze bits \(61..64\) and showed covering packed AND xor
at \(p=64\) is \(1\) iff \(k\in\{3,5\}\). Bits \(33,34\) freeze from
\(t\ge 44\): bit \(33=1\) iff \(t\bmod 8\in\{0,3,7\}\), bit \(34=1\)
iff \(t\bmod 8\in\{0,3,4,5\}\). The left 35 bits are autonomous,
and the word at \(t=44\) equals \(t=52\), so even \(t\ge 44\) has
the \(p=34\) 4-tuple \(1111\) / \(0100\) / \(0001\) / \(1000\) on
\(t\bmod 8=0,2,4,6\), AND iff \(t\bmod 8=2\). Covering even
\(s=10U-2n-2\) has \(s\bmod 8=2\) iff \(n\equiv 2\pmod{4}\). Column
\(j=5U-17\) is odd, so even \(n\) have \(G=0\). For \(k\ge 5\)
(\(t_0=2U\ge 64\ge 44\)) packed AND on \(G=1\) is empty. Early even
AND-ones are \(t\in\{16,26,30,32,38,42\}\). Packed xor is therefore
\(1\) iff \(k\in\{3,4\}\). This is the \(2^a+2\) column after
\(p=18\), not a UNIQUE_REST slot. **Killed:** covering \(p=34\)
silent for all \(k\) (\(k=3,4\) fire).

**Not** rest \(=S\oplus T\). **Not** leftover after
\(p=16\oplus 32\oplus 30\oplus 38\oplus 64\oplus 34\) equals
\(S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
catalogue further \(S\)/\(T\) subregions unless the experiment
answers why \(E_k=0\). Do **not** claim pal-left leftover xor
vanishes for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\). Do **not** walk \(k=11\) covering packed. Do
**not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).

Certify: `python3 research/cycle_pp.py --certify`.
Dump: `research/cycle_pp.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/PK/PD/GU/HG/HH/HU (bits \(33,34\), even-\(t\) \(p=34\)
4-tuple AND iff \(t\bmod 8=2\); Green even \(n\) vanish at odd
\(j\); prefix PO \(p=64\) xor, PK \(p=32\) xor; no Fermat table,
no extra window, no \(n_0=16\) window, no packed covering
\(k=11\)).

## Lemma (bits \(33,34\))

For \(t\ge 44\): bit \(33=1\) iff \(t\bmod 8\in\{0,3,7\}\), bit
\(34=1\) iff \(t\bmod 8\in\{0,3,4,5\}\). Status: **lemma**.
Checked on \(0\le t\le 64\).

## Lemma (left 35-bit period \(8\) from \(t=44\))

Bits \(0..34\) are autonomous. The word at \(t=44\) equals \(t=52\),
so even \(t\ge 44\) is period \(8\). Status: **lemma**.

## Lemma (AND at \(p=34\) on even \(t\ge 44\))

Even \(t\ge 44\): the \(p=34\) 4-tuple is \(1111\) / \(0100\) /
\(0001\) / \(1000\), AND iff \(t\bmod 8=2\). Early even AND-ones
are exactly \(t\in\{16,26,30,32,38,42\}\). Status: **lemma**.

## Lemma (covering packed \(p=34\) xor \(=1\) iff \(k\in\{3,4\}\))

Covering AND times after the freeze have \(n\equiv 2\pmod{4}\),
hence even \(n\), at odd \(j\), so \(G=0\). Packed AND on \(G=1\)
is identically \(0\) for \(k\ge 5\). Thin packed check on
\(k\le 8\) gives xor \(=1\) at \(k=3,4\) and \(0\) otherwise.
Green \(G=1\) still fires at odd \(n\). Status: **lemma**.
**Killed:** silent for all \(k\).

## Verdict

`LEMMA` (bits \(33,34\); left-35 period \(8\); AND \(p=34\) on even
\(t\ge 44\) iff \(t\bmod 8=2\); covering \(p=34\) silent for
\(k\ge 5\); packed \(p=34\) xor \(=1\) iff \(k\in\{3,4\}\); PO
\(p=64\) xor).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (covering \(p=34\) silent for all \(k\)).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_pp.md` (this note)
- `research/cycle_pp.py`
- `research/cycle_pp.json`
