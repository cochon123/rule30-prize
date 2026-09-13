# Cycle PC: Green \(G=1\) sets on covering forced columns \(p=4,6,14\)

Cycle LC/LD/LF counted packed AND on \(G=1\) at \(p=4,6,14\) through
\(k\le 6\). Those are the forced slots of covering rest. On covering
\(q=10\), the Green \(G=1\) sets at the same three columns
\(j=5\cdot 2^k-2,-3,-7\) are closed for every \(k\).

For \(k\ge 1\), live \(n\) with \(G(n,5\cdot 2^k-2)=1\) (\(p=4\)) are
\(\{4U-1\}\cup\{3U-1-2^i:0\le i\le k-1\}\) and also \(3U-1\) iff \(k\)
is odd (\(k=0\): \(\{3\}\)). Even \(n\) is the unique \(3U-2\), from
Cycle PA's column \(G(t,5\cdot 2^{k-1}-1)\) on the window enlarged
by the vanishing left edge \(t=5\cdot 2^{k-2}-1\). Odd \(n=2p+1\)
doubles the parent \(p=4\) set xor \(\{3U-1\}\).

\(p=6\) is odd-only: \(G(2p+1,5U-3)=G(p,5\cdot 2^{k-1}-2)\), so the
set is \(\{2s+1:s\) in \(p=4\) at \(k-1\}\) (\(k=0\): \(\{1,2\}\)).

For \(k\ge 3\), \(p=14\) is
\(\{4U-3,3U-1\}\cup\{3U-3-2^i:1\le i\le k-1\}\) and also \(3U-3\)
iff \(k\) is odd. The \(k=2\) set is \(\{7,11,13,15\}\), not that
form.

Counts match Cycle LC/LD/LF `want_*` on \(q=10\) as **Green** \(G=1\)
counts (\(p=14\) only for \(k\ge 3\); at \(k=1,2\) Green has one
silent extra). Green xor is \(1\) at \(p=4\) for all \(k\); at
\(p=6\) iff \(k\ge 1\); at \(p=14\) iff \(k\ge 3\). Green tot is
\(0\) at \(k=1,2\) while packed forced xor is \(1\), so Green \(G=1\)
xor is **not** packed forced. **Not** silent-free or slot forms for
all \(k\). **Not** rest \(=S\oplus T\). **Not** \(E_k=0\) for all
\(k\). Do **not** catalogue further \(S\)/\(T\) subregions unless
the experiment answers why \(E_k=0\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim packed forced xor \(=1\) for all \(k\).

Certify: `python3 research/cycle_pc.py --certify`.
Dump: `research/cycle_pc.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/PA/PB/OG/LC/LD/LF (forced-column Green sets; prefix PA
unique columns, PB \(S\oplus T\), OG \(E_k\), LC/LD/LF counts; no
Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (\(p=4\) Green \(G=1\) set)

For \(k\ge 1\), \(G(n,5\cdot 2^k-2)=1\) on live covering \(n\) iff
\(n=4U-1\), or \(n=3U-1-2^i\) for some \(0\le i\le k-1\), or \(k\)
is odd and \(n=3U-1\). Count \(k+1+(k\bmod 2)\), xor \(1\). Status:
**lemma**. Sets checked on \(0\le k\le 12\); doubling and unique
edge on \(2\le k\le 12\) / \(a\le 8\).

## Lemma (\(p=6\) Green \(G=1\) set)

For \(k\ge 1\), even \(n\) vanish and odd \(n=2p+1\) fires iff \(p\)
is a \(p=4\) one at \(k-1\). Count \(k+1-(k\bmod 2)\), xor \(1\)
(\(k=0\): count \(2\), xor \(0\)). Status: **lemma**.

## Lemma (\(p=14\) Green \(G=1\) set, \(k\ge 3\))

For \(k\ge 3\), \(G(n,5\cdot 2^k-7)=1\) on live covering \(n\) iff
\(n\in\{4U-3,3U-1\}\), or \(n=3U-3-2^i\) for some \(1\le i\le k-1\),
or \(k\) is odd and \(n=3U-3\). Count \(k+1+(k\bmod 2)\), xor \(1\).
Status: **lemma**. Not \(k=2\).

## Lemma (Green forced-column xor)

Green \(G=1\) xor at the three columns is \(1\) iff \(k=0\) or
\(k\ge 3\). Status: **lemma**. Not packed forced xor.

## Killed

Green tot equals packed forced xor: at \(k=1\) Green tot is \(0\)
and packed forced is \(1\). The \(k\ge 3\) \(p=14\) set at \(k=2\):
ones are \(\{7,11,13,15\}\).

## Verdict

`LEMMA` (\(p=4\) set all \(k\); \(p=6\) set all \(k\); \(p=14\) set
for \(k\ge 3\); Green forced xor \(=1\) iff \(k=0\) or \(k\ge 3\);
PA unique columns; PB covering \(S\oplus T\)).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (Green tot \(=\) packed forced; \(p=14\) set at \(k=2\)).
`PREFIX` (packed forced \(=1\) for all \(k\); packed rest \(=S\oplus T\)
for all \(k\); \(E_k=0\) for all \(k\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_pc.md` (this note)
- `research/cycle_pc.py`
- `research/cycle_pc.json`
