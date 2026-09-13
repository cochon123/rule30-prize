# Cycle NX: on \(q=10\) through \(k\le 10\), inner palindrome-right \(G=1\) count is odd iff \(k\) odd

On covering \(J_{10}\) through \(k\le 10\), the number of covering
\(G=1\) cells with \(n<j\le n+\lfloor n/2\rfloor\)
(\(p=T-2j\ge 0\); no packed row) is odd iff \(k\) is odd. Lift of
Cycle MZ (\(k\le 8\)). Prefix MZ \(q=10\) for \(k\le 8\); walk
\(k=9\) and \(k=10\). Companion of Cycle NT's inner \(G(j-1)\) xor
vanish: the inner xor still vanishes while the inner count carries
\(k\)-odd parity. This is **not** a death at \(k=9\), **not** a
death at \(k=10\), **not** rest (\(k=1\): par \(=1\), rest \(=0\)),
**not** NT inner xor (\(k=9\): par \(=1\), xor\({}_{\mathrm{in}}=0\)),
**not** \(j>n\) even-\(k\) (\(k=9\): par \(=1\), jgtn \(=0\)),
**not** \(k\)-odd on \(q=6\) (\(k=1\): \(n_{\mathrm{in}}=0\)),
**not** empty (\(k=9\): \(n_{\mathrm{in}}=78271\)), and **not** the
form for all \(k\). Do **not** claim \(T\) is \(1\) iff \(k=2\).
Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim Green-only rest for all \(k\). Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_nx.py --certify` (~9.02s).
Dump: `research/cycle_nx.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/MZ/NT/NW/MK/MJ (packed-free covering \(q=10\); prefix MZ
inner count parity for \(k\le 8\); walk \(k=9,10\); no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (inner palindrome-right \(G=1\) count is odd iff \(k\) odd through \(k\le 10\))

Covering \(q=10\), \(k\le 10\). The walk does not read the packed
row. Same cells as Cycle MZ. At \(k=1\), \(n_{\mathrm{in}}=3\)
(odd). At \(k=9\), \(n_{\mathrm{in}}=78271\) (odd). Companion
inner \(G(j-1)\) xor vanishes (Cycle NT).

## Killed

Dies at \(k=9\): par \(=1=\) want. Dies at \(k=10\): par \(=0=\)
want. Equals rest: \(k=1\) is \(1\) vs \(0\). Equals NT inner xor:
\(k=9\) par \(=1\) and xor\({}_{\mathrm{in}}=0\). Equals \(j>n\)
even-\(k\): \(k=9\) par \(=1\) and jgtn \(=0\). Empty: \(k=9\) has
\(n_{\mathrm{in}}=78271\). The \(k\)-odd form on \(q=6\): \(k=1\)
has \(n_{\mathrm{in}}=0\). The form for all \(k\).

## Verdict

`LEMMA` (inner palindrome-right \(G=1\) count is odd iff \(k\) odd
on \(q=10\) for \(k\le 10\); that form holds on \(q=10\) for
\(k\le 8\); inner \(G(j-1)\) xor vanishes on \(q=10\) for
\(k\le 10\); palindrome-right \(d\bmod 3=0\) \(G(j-1)\) is \(1\)
iff \(k\bmod 4\in\{1,2\}\) on \(q=10\) for \(k\le 10\); rest10
census on \(k\le 10\); \(J\) closed form on \(k\le 6\)).
`KILLED` (dies at \(k=9\); dies at \(k=10\); equals rest; equals
NT inner xor; equals \(j>n\) even-\(k\); empty; \(k\)-odd on
\(q=6\); the form for all \(k\); unique-rest xor equals \(J\);
leftover equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_nx.md` (this note)
- `research/cycle_nx.py`
- `research/cycle_nx.json`
