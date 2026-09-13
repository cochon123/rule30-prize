# Cycle PM: covering packed AND xor at \(p=30\) is \(1\) iff \(k=2\)

Cycle PL froze bits \(23..26\) and showed covering \(p=26\) and
\(p=28\) silent for every \(k\). Bit \(27=1\) iff \(t\bmod 4\neq 0\)
for \(t\ge 32\); bit \(28=0\) for \(t\ge 32\). The left 31 bits are
autonomous, and the word at \(t=40\) equals \(t=48\), so even
\(t\ge 40\) has the \(p=30\) 4-tuple \(0011\) / \(1001\) / \(0001\) /
\(1011\) on \(t\bmod 8=0,2,4,6\). AND fires iff \(t\bmod 8\in\{0,2\}\)
already from even \(t\ge 32\). Covering even \(s=10U-2n-2\) has
\(s\bmod 8\in\{0,2\}\) iff \(n\bmod 4\in\{3,2\}\). The column
\(j=5U-15\) is odd, so even \(n\) have \(G=0\). For \(k\ge 4\)
(\(t_0=2U\ge 32\)) packed AND fires iff \(n\equiv 3\pmod{4}\) among
live \(G=1\). Those \(n=4t+3\) double to parent \(p=8\oplus p=10\) at
scale \(k-2\); Green xor at \(p=10\) is \(1\) for \(k\ge 2\) by
parent \(p=6\), and Cycle PH's \(p=8\) xor is \(1\) for \(k\ge 2\),
so the \(n\equiv 3\pmod{4}\) xor is \(0\). Hence packed xor is \(1\)
iff \(k=2\). Cycle LK's \(k\le 6\) \(0011\) xor \(=0\) is this
all-\(k\) lemma for \(k\ge 5\). **Killed:** covering \(p=30\) silent;
xor \(=0\) for all \(k\) (\(k=2\) is \(1\)).

**Not** rest \(=S\oplus T\). **Not** leftover after
\(p=16\oplus 32\oplus 30\) equals \(S\oplus T\). **Not** \(E_k=0\)
for all \(k\). Do **not** catalogue further \(S\)/\(T\) subregions
unless the experiment answers why \(E_k=0\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).

Certify: `python3 research/cycle_pm.py --certify`.
Dump: `research/cycle_pm.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/LK/PC/PH/PK/PL/PD/GU/HG/HH/HU (bits \(27,28\), even-\(t\)
\(p=30\) 4-tuple, Green \(n\equiv 3\pmod{4}\) via PH \(p=8\) xor
parent \(p=6\) at \(p=10\); prefix PL silent \(p=26\), PK \(p=32\)
xor; no Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (bits \(27,28\))

For \(t\ge 32\): bit \(27=1\) iff \(t\bmod 4\neq 0\), bit \(28=0\).
Status: **lemma**. Checked on \(0\le t\le 64\).

## Lemma (left 31-bit period \(8\) from \(t=40\))

Bits \(0..30\) are autonomous. The word at \(t=40\) equals \(t=48\),
so even \(t\ge 40\) is period \(8\). Status: **lemma**.

## Lemma (AND at \(p=30\) on even \(t\ge 32\))

Even \(t\ge 32\): AND fires iff \(t\bmod 8\in\{0,2\}\). Even
\(t\ge 40\): the 4-tuple is \(0011\) iff \(t\bmod 8=0\), else
\(1001\) / \(0001\) / \(1011\). Early even AND-ones are exactly
\(t\in\{14,26\}\). Status: **lemma**.

## Lemma (covering Green \(p=10\) xor \(=1\) for \(k\ge 2\))

Odd \(n=2m+1\) has \(G(n,5U-5)=G(m,5\cdot 2^{k-1}-3)\), so the set
is parent \(p=6\). Cycle PC's \(p=6\) xor is \(1\) iff \(k\ge 1\),
hence \(p=10\) xor is \(1\) for \(k\ge 2\). Status: **lemma**.

## Lemma (covering packed \(p=30\) xor \(=1\) iff \(k=2\))

For \(k\ge 4\), packed AND at \(p=30\) fires iff \(n\equiv 3\pmod{4}\)
among live \(G=1\). That Green xor is parent \(p=8\oplus p=10\) at
\(k-2\), hence \(0\). \(k=3\) has \(n_{\mathrm{and}}=0\); \(k=2\)
xor is \(1\). Status: **lemma**. Thin packed check on \(k\le 8\).
**Killed:** silent for all \(k\); xor \(=0\) for all \(k\).

## Verdict

`LEMMA` (bits \(27,28\); left-31 period \(8\); AND \(p=30\) on even
\(t\ge 32\); Green \(p=10\) xor \(=1\) for \(k\ge 2\); packed
\(p=30\) xor \(=1\) iff \(k=2\); PL \(p=26\) silent; PK \(p=32\)
xor).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (covering \(p=30\) silent for all \(k\); packed \(p=30\)
xor \(=0\) for all \(k\)).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after \(p=16\oplus 32\oplus 30\) equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_pm.md` (this note)
- `research/cycle_pm.py`
- `research/cycle_pm.json`
