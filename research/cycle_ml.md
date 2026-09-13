# Cycle ML: on \(q=6\) and \(q=10\) for \(k\le 8\), xor of \(G(n,j-1)\) on \(G=1\) at \(j=n+2\) vanishes

On covering \(J_6,J_{10}\) for \(k\le 8\), XOR of \(G(n,j-1)\) over
covering \(G=1\) cells with \(j=n+2\) (\(p=T-2j\ge 0\); no packed
row) is \(0\). Counts are even (empty only at \(k=0\), \(q=6\)).
This is **not** rest, **not** \(d=2\) empty on \(q=10\) (\(k=0\)
has \(n_{\mathrm{off}}=2\)), **not** all palindrome offsets
(\(d=4\) at \(k=1\), \(q=10\) xor \(=1\)), **not** Green-only rest,
and **not** the form for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim a Green-only formula for rest. Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_ml.py --certify`.
Dump: `research/cycle_ml.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/MJ/MK (packed-free covering both \(q\) for \(k\le 8\);
prefix MJ sizes and MK inner vanish; no Fermat table, no extra
window, no \(n_0=16\) window).

## Lemma (\(j=n+2\) xor of \(G(n,j-1)\) on \(G=1\) vanishes)

Both covering \(q\), \(k\le 8\). Equivalently, XOR of \(G(n,n-1)\)
over covering clocks with \(G(n,n-2)=1\) is \(0\). The walk does
not read the packed row.

## Killed

\(d=2\) xor equals rest: xor is \(0\) and rest is \(1\) at
\(k=2\), \(q=10\). \(d=2\) \(G=1\) empty on \(q=10\): \(k=0\) has
\(n_{\mathrm{off}}=2\). All palindrome offsets vanish: \(d=4\) at
\(k=1\), \(q=10\) has xor \(=1\) and \(n_{\mathrm{off}}=3\).
Green-only rest: this xor is not rest.

## Verdict

`LEMMA` (\(j=n+2\) xor of \(G(n,j-1)\) on \(G=1\) vanishes on both
covering \(q\) for \(k\le 8\); inner palindrome-right xor vanishes
on \(q=10\); \(j>n\) xor is \(1\) iff \(k\) even on both covering
\(q\); rest10 census on \(k\le 10\); \(J\) closed form on
\(k\le 6\)).
`KILLED` (\(d=2\) xor equals rest; \(d=2\) empty on \(q=10\); all
palindrome offsets vanish; Green-only rest; the form for all \(k\);
unique-rest xor equals \(J\); leftover equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ml.md` (this note)
- `research/cycle_ml.py`
- `research/cycle_ml.json`
