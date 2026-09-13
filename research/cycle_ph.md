# Cycle PH: covering packed AND xor at \(p=16\) is \(1\) for \(k\ge 3\)

Cycle PG froze bit \(10\) and showed covering \(p=12\) silent. The
left 17 bits are autonomous, and the word at \(t=16\) equals
\(t=20\), so even \(t\ge 16\) has bits \(13..16\) equal to \(1001\)
iff \(t\bmod 4=2\) else \(1111\). AND at \(p=16\) fires iff
\(t\bmod 4=2\). Covering even \(s=10U-2n-2\) has \(s\bmod 4=2\) iff
\(n\) is even, so for \(k\ge 3\) (\(t_0=2U\ge 16\)) packed AND
fires iff \(n\) is even among live \(G=1\). Odd \(G=1\) are all
silent.

Even-\(n\) Green \(G(n,5U-8)=1\) iff the parent covering \(p=8\)
cell fires. For \(k\ge 2\), odd Green at \(p=8\) is \(\{3U-3,3U-1\}\)
(\(\mathrm{in\_p4}\oplus\mathrm{in\_p6}\) of the parent), and even
Green is \(\{2s:\mathrm{in\_p4}(s,k-1)\}\), so parent xor is \(1\).
Packed \(p=16\) xor is therefore \(1\) for \(k\ge 3\). Cycle LE's
\(k\le 6\) count is this all-\(k\) lemma.

**Not** rest \(=S\oplus T\). **Not** leftover after \(p=16\) equals
\(S\oplus T\) (unique-rest xor already vanishes on \(q=10\) through
\(k\le 10\)). **Not** \(E_k=0\) for all \(k\). Do **not** claim
covering \(p=16\) silent. Do **not** claim covering \(p=18\) or
\(p=32\) xor for all \(k\). Do **not** catalogue further \(S\)/\(T\)
subregions unless the experiment answers why \(E_k=0\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).

Certify: `python3 research/cycle_ph.py --certify` (~0.18s).
Dump: `research/cycle_ph.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/LE/PC/PF/PG/PD/GU/HG/HH/HU (bits \(13..16\), even-\(t\)
\(p=16\) 4-tuple, Green \(p=8\) / even-\(n\) \(p=16\); prefix PG
silent \(p=12\), PD bits \(11..14\); no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (bits \(13..16\))

For \(t\ge 16\): bit \(13=1\) iff \(t\bmod 4\neq 3\), bit \(14=1\)
iff \(t\bmod 4\in\{0,1\}\), bit \(15=1\) iff \(t\bmod 4\in\{0,3\}\),
bit \(16=1\) iff \(t\bmod 4\neq 1\). Status: **lemma**. Checked on
\(0\le t\le 64\).

## Lemma (left 17-bit period \(4\) from \(t=16\))

Bits \(0..16\) are autonomous. The word at \(t=16\) equals \(t=20\),
so even \(t\ge 16\) is period \(4\). Status: **lemma**.

## Lemma (AND at \(p=16\) on even \(t\ge 16\))

Even \(t\ge 16\): the \(p=16\) 4-tuple is \(1001\) iff
\(t\bmod 4=2\) else \(1111\), so AND fires iff \(t\bmod 4=2\).
Status: **lemma**.

## Lemma (covering \(p=8\) odd Green, \(k\ge 2\))

Odd live \(n\) with \(G(n,5U-4)=1\) are exactly \(\{3U-3,3U-1\}\).
Even live ones are \(\{2s:\mathrm{in\_p4}(s,k-1)\}\). Status:
**lemma**. Green check on \(k\le 12\).

## Lemma (covering packed \(p=16\) xor \(=1\) for \(k\ge 3\))

For \(k\ge 3\), packed AND at \(p=16\) fires iff \(n\) is even among
live \(G=1\). Even-\(n\) Green xor is the parent \(p=8\) xor, which
is \(1\). Status: **lemma**. Thin packed check on \(k\le 8\).
**Killed:** covering \(p=16\) silent (\(k=3\) has five AND-ones).

## Verdict

`LEMMA` (bits \(13..16\); left-17 period \(4\); AND \(p=16\) on even
\(t\ge 16\); covering \(p=8\) odd Green two-point; packed \(p=16\)
xor \(=1\) for \(k\ge 3\)).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (covering \(p=16\) silent).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after \(p=16\) equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ph.md` (this note)
- `research/cycle_ph.py`
- `research/cycle_ph.json`
