# Cycle PD: covering packed forced xor is \(1\) for every \(k\) on \(q=10\)

Cycle PC closed the Green \(G=1\) sets at covering \(p=4,6,14\). Packed
AND at those slots equals Green iff the even-\(s\) 4-tuple is an
AND-one whenever \(G=1\). Rule 30 on packed bits gives that for
\(p=4,6\) at every even time \(t\ge 2\), and for \(p=14\) at covering
scale \(k\ge 3\).

Bit \(0\) stays \(1\). Bit \(1\) is \(1\) for \(t\ge 1\) (reads bit
\(0\)). Bit \(2\) is \(0\) for \(t\ge 2\). Then bit \(3\) alternates
(\(0\) on even \(t\ge 2\)), bit \(4\) stays \(1\), and bits \(5,6\)
equal \(t\bmod 2\) for \(t\ge 3\). Every even \(t\ge 2\) has bits
\(1..6=100100\), so the \(p=4\) 4-tuple is \(1001\) and the \(p=6\)
4-tuple is \(0100\). Both are AND-ones.

The left \(15\) bits are autonomous. The word at \(t=12\) equals the
word at \(t=16\), so even \(t\ge 12\) has bits \(11..14=0011\) iff
\(t\bmod 4=0\) else \(1110\). Covering even \(s\) starts at
\(2U\ge 16\) for \(k\ge 3\), hence \(p=14\) AND fires iff \(n\) is
odd. Even \(n\) have \(G=0\) at the odd column \(5U-7\). Cycle PC's
Green xor at \(p=14\) is \(1\), so packed AND xor equals Green xor.
With \(p=4\) and \(p=6\) always AND on live \(n\), packed forced xor
is \(1\) for \(k\ge 3\). Scales \(k=0,1,2\) are finite (one silent
\(p=14\) cell at \(k=1,2\)).

Thus rest \(=1\oplus J_{\mathrm{odd}}\) for every \(k\) on \(q=10\),
and \(E_k=0\) iff \(J_{\mathrm{odd}}=1\oplus S\oplus T\). **Not**
rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). **Not** bits
\(11..14\) constant on even \(t\). Do **not** catalogue further
\(S\)/\(T\) subregions unless the experiment answers why \(E_k=0\).
Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).

Certify: `python3 research/cycle_pd.py --certify` (~0.14s).
Dump: `research/cycle_pd.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/PC/PB/OG/GU/HG/HH/HU/LZ (frozen low bits, left-15 period
4, thin forced xor; prefix PC Green sets, PB \(S\oplus T\), OG
\(E_k\); no Fermat table, no extra window, no \(n_0=16\) window, no
packed covering \(k=11\)).

## Lemma (frozen bits \(1..6\) on even \(t\ge 2\))

Packed bits \(1..6=100100\) for every even \(t\ge 2\). Hence covering
\(p=4\) is always \(1001\) and \(p=6\) is always \(0100\). Status:
**lemma**. Checked on \(0\le t\le 64\).

## Lemma (\(p=14\) period \(4\) on even \(t\ge 12\))

Left \(15\) bits autonomous; word at \(t=12\) equals \(t=16\). Even
\(t\ge 12\) has bits \(11..14=0011\) iff \(t\bmod 4=0\) else \(1110\).
Covering \(k\ge 3\) therefore has \(p=14\) AND iff \(n\) is odd.
Status: **lemma**. Autonomy and period checked on \(t\le 48\).

## Lemma (packed forced xor \(=1\), all \(k\))

Covering \(q=10\), packed AND xor on \(G=1\) at \(p\in\{4,6,14\}\) is
\(1\) for every \(k\). Rest \(=1\oplus J_{\mathrm{odd}}\). Status:
**lemma**. Thin packed check on \(k\le 8\); \(k\ge 3\) from the
period-4 identity plus Cycle PC Green xor.

## Killed

Bits \(11..14\) constant on even \(t\ge 12\): \(t=12\) is \(0011\),
\(t=14\) is \(1110\).

## Verdict

`LEMMA` (frozen bits \(1..6\); \(p=14\) period \(4\); packed forced
xor \(=1\) all \(k\); rest \(=1\oplus J_{\mathrm{odd}}\); PC Green
sets; PB covering \(S\oplus T\)).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (\(p=14\) 4-tuple constant).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_pd.md` (this note)
- `research/cycle_pd.py`
- `research/cycle_pd.json`
