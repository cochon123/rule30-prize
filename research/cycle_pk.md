# Cycle PK: covering packed AND xor at \(p=32\) is \(1\) for \(k\ge 5\)

Cycle PJ froze bits \(19..22\) and showed covering \(p=22\) silent
for every \(k\). The left 33 bits are autonomous, and the word at
\(t=36\) equals \(t=44\), so even \(t\ge 36\) has the \(p=32\)
4-tuple \(0100\) iff \(t\bmod 8=4\), else \(0101\) / \(1110\) /
\(1111\). AND fires iff \(t\bmod 8=4\). Covering even
\(s=10U-2n-2\) has \(s\bmod 8=4\) iff \(n\equiv 1\pmod{4}\), so for
\(k\ge 5\) (\(t_0=2U\ge 64\ge 36\)) packed AND fires iff
\(n\equiv 1\pmod{4}\) among live \(G=1\). Odd \(n=4t+1\) doubles to
Cycle PH's even-\(n\) \(p=16\) at scale \(k-1\), whose xor is \(1\).
Cycle LG's \(k\le 6\) \(0100\) count is this all-\(k\) lemma for
\(k\ge 5\). **Killed:** xor \(=1\) for all \(k\ge 4\) (\(k=4\) is
\(0\)).

**Not** rest \(=S\oplus T\). **Not** leftover after \(p=16\oplus 32\)
equals \(S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
claim covering \(p=24\) silent for all \(k\). Do **not** catalogue
further \(S\)/\(T\) subregions unless the experiment answers why
\(E_k=0\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).

Certify: `python3 research/cycle_pk.py --certify`.
Dump: `research/cycle_pk.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/LG/PC/PH/PI/PJ/PD/GU/HG/HH/HU (bits \(29..32\), even-\(t\)
\(p=32\) 4-tuple, Green \(n\equiv 1\pmod{4}\) via PH even \(p=16\);
prefix PJ silent \(p=22\), PH \(p=16\) xor; no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (bits \(29..32\))

For \(t\ge 36\): bit \(29=1\) iff \(t\bmod 8\in\{0,1,3,6\}\), bit
\(30=1\), bit \(31=1\) iff \(t\bmod 8\in\{0,3,5,6\}\), bit \(32=1\)
iff \(t\bmod 8\in\{0,2,5\}\). Status: **lemma**. Checked on
\(0\le t\le 64\).

## Lemma (left 33-bit period \(8\) from \(t=36\))

Bits \(0..32\) are autonomous. The word at \(t=36\) equals \(t=44\),
so even \(t\ge 36\) is period \(8\). Status: **lemma**.

## Lemma (AND at \(p=32\) on even \(t\ge 36\))

Even \(t\ge 36\): the \(p=32\) 4-tuple is \(0100\) iff
\(t\bmod 8=4\), so AND fires iff \(t\bmod 8=4\). Status: **lemma**.

## Lemma (covering packed \(p=32\) xor \(=1\) for \(k\ge 5\))

For \(k\ge 5\), packed AND at \(p=32\) fires iff \(n\equiv 1\pmod{4}\)
among live \(G=1\). That Green xor is Cycle PH's even-\(n\) \(p=16\)
xor at \(k-1\), hence \(1\). Status: **lemma**. Thin packed check on
\(k\le 8\). **Killed:** xor \(=1\) for all \(k\ge 4\) (\(k=4\) xor
is \(0\)).

## Verdict

`LEMMA` (bits \(29..32\); left-33 period \(8\); AND \(p=32\) on even
\(t\ge 36\); packed \(p=32\) xor \(=1\) for \(k\ge 5\); PH \(p=16\)
xor; PJ \(p=22\) silent).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (packed \(p=32\) xor \(=1\) for all \(k\ge 4\)).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after \(p=16\oplus 32\) equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_pk.md` (this note)
- `research/cycle_pk.py`
- `research/cycle_pk.json`
