# Cycle PL: bits \(23..26\) freeze; covering \(p=26\) silent for every \(k\)

Cycle PK froze bits \(29..32\) and showed covering packed AND xor
at \(p=32\) is \(1\) for \(k\ge 5\). Bit \(23=1\) iff \(t\) is even
for \(t\ge 30\); bit \(24=1\) iff \(t\bmod 4=3\); bit \(25=1\) iff
\(t\bmod 4\in\{0,3\}\); bit \(26=1\) iff \(t\bmod 4\neq 0\). The
left 27 bits are autonomous, and the word at \(t=30\) equals
\(t=34\), so even \(t\ge 30\) has the \(p=26\) 4-tuple \(1001\) iff
\(t\bmod 4=2\) else \(1010\). AND fires iff \(t\bmod 4=2\), hence
covering even \(s\) has \(p=26\) AND iff \(n\) is even, but
\(j=5U-13\) is odd so even \(n\) have \(G=0\). Early even AND-ones
are only \(12,14\), and \(G(13,7)=G(12,7)=0\). Hence covering
\(p=26\) is silent for every \(k\). Even \(t\ge 28\) has the
\(p=24\) 4-tuple \(1110\) or \(1010\), so covering \(p=24\) is
silent for \(k\ge 4\). Even \(t\ge 32\) has the \(p=28\) 4-tuple
\(1000\) or \(0110\), so covering \(p=28\) is silent for every
\(k\). **Killed:** covering \(p=24\) silent for all \(k\) (\(k=2\)
has one AND-one).

**Not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do
**not** claim covering \(p=30\) silent. Do **not** catalogue further
\(S\)/\(T\) subregions unless the experiment answers why \(E_k=0\).
Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\)
covering packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).

Certify: `python3 research/cycle_pl.py --certify`.
Dump: `research/cycle_pl.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/PJ/PK/PD/GU/HG/HH/HU (bits \(23..26\), even-\(t\)
\(p=26\) 4-tuple; prefix PK \(p=32\) xor, PJ silent \(p=22\); no
Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (bits \(23..26\))

For \(t\ge 30\): bit \(23=1\) iff \(t\) is even, bit \(24=1\) iff
\(t\bmod 4=3\), bit \(25=1\) iff \(t\bmod 4\in\{0,3\}\), bit
\(26=1\) iff \(t\bmod 4\neq 0\). Status: **lemma**. Checked on
\(0\le t\le 64\).

## Lemma (left 27-bit period \(4\) from \(t=30\))

Bits \(0..26\) are autonomous. The word at \(t=30\) equals \(t=34\),
so even \(t\ge 30\) is period \(4\). Status: **lemma**.

## Lemma (AND at \(p=26\) on even \(t\ge 30\))

Even \(t\ge 30\): the \(p=26\) 4-tuple is \(1001\) iff
\(t\bmod 4=2\) else \(1010\), so AND fires iff \(t\bmod 4=2\).
Early even AND-ones are exactly \(t\in\{12,14\}\). Status:
**lemma**.

## Lemma (covering \(p=26\) silent for every \(k\))

Covering even \(s\) has AND iff \(n\) is even, but \(j=5U-13\) is
odd so even \(n\) have \(G=0\). Early AND-ones miss \(G=1\).
Status: **lemma**. Thin packed check on \(k\le 8\).

## Lemma (covering \(p=24\) silent for \(k\ge 4\))

Even \(t\ge 28\): the \(p=24\) 4-tuple is \(1110\) or \(1010\),
AND \(=0\). The only even AND-one is \(t=16\). Covering \(k\ge 4\)
starts at \(2U\ge 32\). Status: **lemma**. **Killed:** silent for
all \(k\).

## Lemma (covering \(p=28\) silent for every \(k\))

Even \(t\ge 32\): the \(p=28\) 4-tuple is \(1000\) or \(0110\),
AND \(=0\). Early even AND-ones \(t\in\{14,22\}\) have \(G=0\).
Status: **lemma**. Thin packed check on \(k\le 8\).

## Verdict

`LEMMA` (bits \(23..26\); left-27 period \(4\); AND \(p=26\) on even
\(t\ge 30\); covering \(p=26\) silent for every \(k\); covering
\(p=24\) silent for \(k\ge 4\); covering \(p=28\) silent for every
\(k\); PK \(p=32\) xor).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (covering \(p=24\) silent for all \(k\)).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); covering \(p=30\) silent;
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_pl.md` (this note)
- `research/cycle_pl.py`
- `research/cycle_pl.json`
