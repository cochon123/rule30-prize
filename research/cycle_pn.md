# Cycle PN: covering packed AND xor at \(p=38\) is \(1\) iff \(k\in\{2,3\}\)

Cycle PM froze bits \(27,28\) and showed covering packed AND xor at
\(p=30\) is \(1\) iff \(k=2\). Bits \(35..38\) freeze from \(t\ge 48\):
bit \(35=1\) iff \(t\bmod 8\in\{5,6,7\}\), bit \(36=1\) iff
\(t\bmod 8\in\{0,4,7\}\), bit \(37=1\) iff \(t\bmod 8\notin\{0,6\}\),
bit \(38=1\) iff \(t\bmod 8\notin\{0,5\}\). The left 39 bits are
autonomous, and the word at \(t=48\) equals \(t=56\), so even
\(t\ge 48\) has the \(p=38\) 4-tuple \(0100\) / \(0011\) / \(0111\) /
\(1001\) on \(t\bmod 8=0,2,4,6\). AND fires iff
\(t\bmod 8\in\{0,2,6\}\). Covering even \(s=10U-2n-2\) has AND iff
\(n\not\equiv 1\pmod{4}\). The column \(j=5U-19\) is odd, so even
\(n\) have \(G=0\). For \(k\ge 5\) (\(t_0=2U\ge 64\ge 48\)) packed AND
fires iff \(n\equiv 3\pmod{4}\) among live \(G=1\), always as
\(0100\). Those \(n=4t+3\) double to parent \(p=10\oplus p=12\) at
scale \(k-2\). Green xor at \(p=12\) equals parent \(p=8\) xor, hence
\(1\) for \(k\ge 3\), and Cycle PM's \(p=10\) xor is \(1\) for
\(k\ge 2\), so the \(n\equiv 3\pmod{4}\) xor is \(0\) for \(k\ge 5\).
Packed xor is therefore \(1\) iff \(k\in\{2,3\}\). Cycle LN's
\(k\le 6\) \(0100\) xor \(=0\) is this all-\(k\) lemma for \(k\ge 5\).
**Killed:** covering \(p=38\) silent; xor \(=0\) for all \(k\)
(\(k=2,3\) are \(1\)). Pal-left leftover AND xor dies at \(k=7\).

**Not** rest \(=S\oplus T\). **Not** leftover after
\(p=16\oplus 32\oplus 30\oplus 38\) equals \(S\oplus T\). **Not**
\(E_k=0\) for all \(k\). Do **not** catalogue further \(S\)/\(T\)
subregions unless the experiment answers why \(E_k=0\). Do **not**
claim pal-left leftover xor vanishes for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).

Certify: `python3 research/cycle_pn.py --certify` (~0.18s).
Dump: `research/cycle_pn.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/LN/PC/PH/PM/PD/GU/HG/HH/HU (bits \(35..38\), even-\(t\)
\(p=38\) 4-tuple, Green \(n\equiv 3\pmod{4}\) via PM \(p=10\) xor
parent \(p=8\) at \(p=12\); prefix PM \(p=30\) xor, PL silent
\(p=26\); no Fermat table, no extra window, no \(n_0=16\) window, no
packed covering \(k=11\)).

## Lemma (bits \(35..38\))

For \(t\ge 48\): bit \(35=1\) iff \(t\bmod 8\in\{5,6,7\}\), bit
\(36=1\) iff \(t\bmod 8\in\{0,4,7\}\), bit \(37=1\) iff
\(t\bmod 8\notin\{0,6\}\), bit \(38=1\) iff \(t\bmod 8\notin\{0,5\}\).
Status: **lemma**. Checked on \(0\le t\le 64\).

## Lemma (left 39-bit period \(8\) from \(t=48\))

Bits \(0..38\) are autonomous. The word at \(t=48\) equals \(t=56\),
so even \(t\ge 48\) is period \(8\). Status: **lemma**.

## Lemma (AND at \(p=38\) on even \(t\ge 48\))

Even \(t\ge 48\): the \(p=38\) 4-tuple is \(0100\) iff
\(t\bmod 8=0\), else \(0011\) / \(0111\) / \(1001\), so AND fires
iff \(t\bmod 8\in\{0,2,6\}\). Early even AND-ones are exactly
\(t\in\{18,20,34,40,44\}\). Status: **lemma**.

## Lemma (covering Green \(p=12\) xor \(=1\) for \(k\ge 3\))

Even \(n=2m\) has \(G(n,5U-6)=G(m,5\cdot 2^{k-1}-3)\) (parent
\(p=6\)). Odd \(n=2m+1\) has Green \(p=6\oplus p=8\) at \(k-1\).
Tot xor equals parent \(p=8\) xor, hence \(1\) for \(k\ge 3\).
Status: **lemma**.

## Lemma (covering packed \(p=38\) xor \(=1\) iff \(k\in\{2,3\}\))

For \(k\ge 5\), packed AND at \(p=38\) fires iff \(n\equiv 3\pmod{4}\)
among live \(G=1\), as \(0100\). That Green xor is parent
\(p=10\oplus p=12\) at \(k-2\), hence \(0\). Status: **lemma**. Thin
packed check on \(k\le 8\). **Killed:** silent for all \(k\); xor
\(=0\) for all \(k\).

## Verdict

`LEMMA` (bits \(35..38\); left-39 period \(8\); AND \(p=38\) on even
\(t\ge 48\); Green \(p=12\) xor \(=1\) for \(k\ge 3\); packed
\(p=38\) xor \(=1\) iff \(k\in\{2,3\}\); PM \(p=30\) xor).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (covering \(p=38\) silent for all \(k\); packed \(p=38\)
xor \(=0\) for all \(k\); pal-left leftover xor for all \(k\)).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after \(p=16\oplus 32\oplus 30\oplus 38\) equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_pn.md` (this note)
- `research/cycle_pn.py`
- `research/cycle_pn.json`
