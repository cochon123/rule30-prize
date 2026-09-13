# Cycle MJ: on \(q=6\) and \(q=10\) for \(k\le 8\), Green-only xor of \(G(n,j-1)\) on \(G=1\) with \(j>n\) is \(1\) iff \(k\) even

On covering \(J_6,J_{10}\) for \(k\le 8\), XOR of \(G(n,j-1)\) over
covering \(G=1\) cells with \(j>n\) (\(p=T-2j\ge 0\); no packed
row) is \(1\) iff \(k\) is even. XOR at \(j=n\) of \(G(n,n-1)\) is
identically \(1\). This is **not** rest (\(k=0\), \(q=10\): jgtn
\(=1\), rest \(=0\)), **not** identically \(0\), **not** the
all-\(G=1\) xor on \(q=6\) (Cycle MI: \(k=0\), \(q=6\) jm1 \(=0\)),
**not** \(j<n\) xor identically \(1\) on \(q=6\) (\(k=0\), \(q=6\)
jltn \(=0\)), **not** Green-only rest, and **not** the form for
all \(k\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\)
for all \(k\). Do **not** push the even-spine scan past \(k=18\).
Do **not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\). Do **not**
walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim a Green-only formula for rest. Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_mj.py --certify`.
Dump: `research/cycle_mj.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/MI (packed-free covering both \(q\) for \(k\le 8\);
prefix MI for \(q=10\) all-\(G=1\) xor; no Fermat table, no extra
window, no \(n_0=16\) window).

## Lemma (\(j>n\) xor of \(G(n,j-1)\) on \(G=1\) is \(1\) iff \(k\) even)

Both covering \(q\), \(k\le 8\). The walk does not read the packed
row.

## Lemma (\(j=n\) xor of \(G(n,n-1)\) is identically \(1\))

Same walks.

## Killed

\(j>n\) xor equals rest: \(k=0\), \(q=10\) is \(1\) vs \(0\). That
xor vanishes: \(k=0\) both \(q\) are \(1\). All-\(G=1\) xor is
\(k\bmod 2\) on \(q=6\): \(k=0\), \(q=6\) has jm1 \(=0\) and jgtn
\(=1\). \(j<n\) xor identically \(1\) on \(q=6\): \(k=0\), \(q=6\)
is \(0\). Green-only rest: this xor is not rest.

## Verdict

`LEMMA` (\(j>n\) xor of \(G(n,j-1)\) on \(G=1\) is \(1\) iff \(k\)
even on both covering \(q\) for \(k\le 8\); \(j=n\) xor of
\(G(n,n-1)\) is \(1\); Green-only xor of \(G(n,j-1)\) on \(G=1\) is
\(1\) iff \(k\) even on \(q=10\); leftover AND xor of \(G(n,j+1)\)
is \(1\) iff \(k\) even on \(q=10\); rest10 census on \(k\le 10\);
\(J\) closed form on \(k\le 6\)).
`KILLED` (jgtn xor equals rest; jgtn xor vanishes; all-\(G=1\) xor
is \(k\bmod 2\) on \(q=6\); \(j<n\) xor identically \(1\) on
\(q=6\); Green-only rest; the even-\(k\) form for all \(k\);
unique-rest xor equals \(J\); leftover equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_mj.md` (this note)
- `research/cycle_mj.py`
- `research/cycle_mj.json`
