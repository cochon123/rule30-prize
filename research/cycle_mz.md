# Cycle MZ: on \(q=10\) for \(k\le 8\), inner palindrome-right \(G=1\) count is odd iff \(k\) odd

On covering \(J_{10}\) for \(k\le 8\), the number of covering \(G=1\)
cells with \(n<j\le n+\lfloor n/2\rfloor\) (\(p=T-2j\ge 0\); no
packed row) is odd iff \(k\) is odd. Companion of Cycle MK's inner
\(G(j-1)\) xor vanish: the inner xor vanishes while the inner
count carries \(k\)-odd parity. This is **not** rest (\(k=1\):
par \(=1\), rest \(=0\)), **not** empty (\(k=1\):
\(n_{\mathrm{in}}=3\)), **not** MK inner xor (\(k=1\): par \(=1\),
xor\({}_{\mathrm{in}}=0\)), **not** \(j>n\) even-\(k\) (\(k=1\):
par \(=1\), jgtn \(=0\)), **not** \(k\)-odd on \(q=6\) (\(k=1\):
\(n_{\mathrm{in}}=0\)), **not** Green-only rest, and **not** the
form for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim a Green-only formula for rest. Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_mz.py --certify`.
Dump: `research/cycle_mz.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/MJ/MK/MY (packed-free covering \(q=10\) for \(k\le 8\);
prefix MK inner vanish and MJ \(j>n\); \(k=1\), \(q=6\) kill; no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (inner palindrome-right \(G=1\) count is odd iff \(k\) odd)

Covering \(q=10\), \(k\le 8\). The walk does not read the packed
row.

## Killed

Inner count parity equals rest: \(k=1\), \(q=10\) is \(1\) vs
\(0\). Empty: \(k=1\) has \(n_{\mathrm{in}}=3\). Equals MK inner
\(G(j-1)\) xor: \(k=1\) par \(=1\) and xor\({}_{\mathrm{in}}=0\).
Equals \(j>n\) even-\(k\): \(k=1\) par \(=1\) and jgtn \(=0\). The
\(k\)-odd form on \(q=6\): \(k=1\) has \(n_{\mathrm{in}}=0\).
Green-only rest: this parity is not rest.

## Verdict

`LEMMA` (inner palindrome-right \(G=1\) count is odd iff \(k\) odd
on \(q=10\) for \(k\le 8\); inner \(G(j-1)\) xor vanishes on
\(q=10\); leftover palindrome-right odd-\(d\) \(G(j+1)\) xor
vanishes on \(q=10\); \(j>n\) xor is \(1\) iff \(k\) even on both
covering \(q\); rest10 census on \(k\le 10\); \(J\) closed form on
\(k\le 6\)).
`KILLED` (inner count parity equals rest; inner empty; inner
count equals MK xor; inner count equals jgtn; \(k\)-odd on
\(q=6\); Green-only rest; the form for all \(k\); unique-rest xor
equals \(J\); leftover equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_mz.md` (this note)
- `research/cycle_mz.py`
- `research/cycle_mz.json`
