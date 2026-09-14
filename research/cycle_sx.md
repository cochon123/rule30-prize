# Cycle SX: odd pal-right \(p=14\) AND at dyadic covering times

Covering times of Cycle SW's odd pal-right \(p=14\) \(n\) are
\(2U+5\), \(4U+1\), \(4U+5\) if \(k\) odd, and \(4U+5+2^{i+1}\)
for \(i=1,\ldots,k-1\). Packed AND at \(p=14\) is bits \(13\land 14\).
Those bits are \(1\) at \(t=2^m+1\) (\(m\ge 4\)), \(t=2^m+5\)
(\(m\ge 3\)), and \(t=2^a+2^b+5\) (\(a>b\ge 2\)) through the
certified walk, so listed cells all fire and odd pal-right
\(p=14\) tot is \(1\). Do **not** claim those bit identities for
all exponents. Do **not** claim bits \(13,14\) freeze on all odd
\(t\). Do **not** claim \(p=14\) AND on all odd \(t\). Do **not**
claim the exact Green set for all \(k\). Do **not** claim odd
pal-pair rest equals raw for all \(k\). Do **not** claim
pal-center tot equals \(S\oplus T\). This is **not** rest
\(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
catalogue leftover \(p\) one-by-one. Do **not** catalogue further
\(S\)/\(T\) subregions unless the experiment answers why \(E_k=0\).
Do **not** claim pal-left leftover xor vanishes for all \(k\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\)
covering packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_sx.py --certify` (~0.41s).
Dump: `research/cycle_sx.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HU/KH/LF/OJ/PB/QV/SO/SS/SV/SW (odd pal-right \(p=14\) AND
at dyadic covering times; no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (covering times of odd pal-right \(p=14\))

On \(q=10\), the even snapshot is \(s=10U-2n-2\), so the odd
covering time is \(t=10U-2n-1\). Substituting Cycle SW's listed
set \(\{4U-3,3U-1\}\cup\{3U-3\text{ if }k\text{ odd}\}\cup\{3U-3-2^i:i=1,\ldots,k-1\}\)
gives
\[
\{2U+5,\,4U+1\}\cup\{4U+5\text{ if }k\text{ odd}\}\cup\{4U+5+2^{i+1}:i=1,\ldots,k-1\}.
\]
Equivalently \(t=2^{k+1}+5\), \(t=2^{k+2}+1\), \(t=2^{k+2}+5\) if
\(k\) odd, and \(t=2^{k+2}+2^{j}+5\) with \(j=2,\ldots,k\). The
family never uses exponent \(j=1\). Status: **lemma**. Algebra
through \(k\le 64\). Exactness of the \(n\)-set is Cycle SW
**certified** \(3\le k\le 12\).

## Lemma (packed AND at \(p=14\) is bits \(13\land 14\))

Cycle HH packed AND at column \(p\) is the odd-row bits \(p\) and
\(p-1\). At \(p=14\) that is bits \(13\land 14\). Equivalent to
the even-snapshot 4-tuple at bits \(11..14\) being an AND-one.
Status: **lemma**.

## Certified (dyadic bits \(13\land 14=1\); listed family fires)

One packed walk through \(t\le 2^{16}+7\): bits \(13\land 14=1\) at
every \(t=2^m+1\) for \(4\le m\le 16\), every \(t=2^m+5\) for
\(3\le m\le 16\), and every \(t=2^a+2^b+5\) for \(14\ge a>b\ge 2\).
The listed covering times of odd pal-right \(p=14\) sit in that
family for \(k\ge 3\), and the walk hits every such time for
\(3\le k\le 12\). The even 4-tuple is identically \(0011\) on those
cells (Cycle LF's AND-one). Hence listed cells all fire AND, the
count is odd, and odd pal-right \(p=14\) tot is \(1\) through
\(k\le 12\). With Cycle SW's \(p=6\) tot \(1\) and Cycle SV's
\(p=4\) tot \(0\), odd corr is \(0\) through that range.
**Prefix** the bit identities for all exponents. **Prefix** the
exact Green set for all \(k\). **Killed:** bits \(13,14\) freeze
like bits \(5,6\). **Killed:** AND at \(p=14\) on all odd \(t\)
(fails at \(t=9\)). **Killed:** AND at \(t=2^m+7\)
(\(b=1\); spat \(00\)).

## Verdict

`LEMMA` (covering times of odd pal-right \(p=14\); packed AND at
\(p=14\) is bits \(13\land 14\)).
`CERTIFIED` (dyadic bits \(13\land 14=1\) through \(m\le 16\),
\(a\le 14\); listed family AND \(1\) and 4-tuple \(0011\) through
\(k\le 12\); odd pal-right \(p=14\) tot \(1\) for \(3\le k\le 12\);
odd corr \(0\) for \(3\le k\le 10\); \(E_k=0\) on odd-\(s\) rest
for \(q=10\), \(k\le 10\)).
`KILLED` (AND at \(p=14\) on all odd \(t\); bits \(13,14\) freeze;
AND at \(t=2^m+7\); pal-center tot equals \(S\oplus T\)).
`PREFIX` (dyadic bit identities for all exponents; exact \(p=14\)
Green set for all \(k\); odd pal-right \(p=14\) tot \(1\) for all
\(k\ge 3\); odd pal-pair rest equals raw for all \(k\ge 3\);
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\); packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\)
for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all
\(k\); seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_sx.md` (this note)
- `research/cycle_sx.py`
- `research/cycle_sx.json`
