# Cycle OY: covering \(n=8t+3\) rem of \(4s\) folds by two; n3 xor is \(1\) iff \(k\ge 2\) even

Cycle OX writes covering rem of \(n=8t+3\) as two-threshold
\(R_1\)/\(R_2\) tails of \(G(t)\). Even-halve twice sends pal-right
of \(t=4s\) to pal-right of \(s\) at offsets \(d\equiv 0\pmod{4}\),
and covering thresholds scale by four, so
\(\mathrm{n3\_cover\_rem}(4s,k)=\mathrm{n3\_cover\_rem}(s,k-2)\)
for \(k\ge 5\). For \(k\ge 6\), clip-active \(t\) is the disjoint
4-groups of clip-active \(s\) at scale \(k-2\). The \(r=0\) covering
xor is therefore n3 xor at \(k-2\).

The \(r=1,2,3\) rem xor of each group equals
\(G(s,L_p-1)\oplus G(s,L_p)\) with \(L_p=5\cdot 2^{k-5}\), from the
Green doubling tables of \(4s+r\) plus a residue/\(f\bmod 3\)
coefficient count: only \(f=D-1\) and \(f=D\) (\(D=L_p-s\)) survive
in range. On the covering parent window
\([5\cdot 2^{k-6},2^{k-3})\) those two Green columns each xor to
\(P_{\mathrm{pop}}(5)=1\) (Cycle AL prefix at \(q=5\), plus one
even-halve for the even second argument), so they cancel. Hence
covering n3 xor at \(k\) equals n3 xor at \(k-2\) for \(k\ge 6\).
With bases n3(\(2\))=1 and n3(\(3\))=0, covering n3 xor is \(1\)
iff \(k\ge 2\) is even, for every \(k\).

This is **not** the pointwise 4-to-1 fold (\(k=6\), \(s=6\): children
xor to \(0\), parent rem is \(1\)). **Not** one-step even-halve
(\(t=10\) at \(k=5\)). **Not** covering \(S\) for all \(k\) (even-parent
xor remains). **Not** \(E_k=0\) for all \(k\). Do **not** catalogue
further \(S\)/\(T\) subregions unless the experiment answers why
\(E_k=0\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).

Certify: `python3 research/cycle_oy.py --certify`.
Dump: `research/cycle_oy.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/OU/OW/OX/OG (r0 fold, r123 Green column, AL prefix;
prefix OX two-threshold tails, OU 8-scale rem, OW n3 form, OG
\(E_k\); no Fermat
table, no extra window, no \(n_0=16\) window, no packed covering
\(k=11\)).

## Lemma (covering n3 rem of \(4s\) folds by two)

For \(k\ge 5\) and every \(s\ge 0\),
\(\mathrm{n3\_cover\_rem}(4s,k)=\mathrm{n3\_cover\_rem}(s,k-2)\).
Status: **lemma**. Checked on \(5\le k\le 8\).

## Lemma (r=1,2,3 rem xor is a two-bit Green column)

For \(k\ge 6\) and clip-active covering \(s\) at scale \(k-2\),
\(\mathrm{n3\_rem}(4s+1)\oplus\mathrm{n3\_rem}(4s+2)\oplus\mathrm{n3\_rem}(4s+3)\)
at \(5\cdot 2^k\) equals \(G(s,L_p-1)\oplus G(s,L_p)\). Status:
**lemma**. Checked on \(6\le k\le 10\).

## Lemma (covering Green column xor vanishes)

On \(s\in[5\cdot 2^{a-1},2^{a+2})\) with \(L_p=5\cdot 2^a\) and
\(a\ge 1\), \(\bigoplus G(s,L_p-1)=\bigoplus G(s,L_p)=1\). Prefix
below \(s_{\min}\) vanishes (\(L_p>2s\)). Prefix through
\(2^{a+2}\) is \(P_{\mathrm{pop}}(5)=1\) by Cycle AL. Status:
**lemma**. Checked on \(1\le a\le 7\).

## Lemma (covering n3 xor is \(1\) iff \(k\ge 2\) even)

Covering n3 xor at \(k\ge 6\) equals n3 xor at \(k-2\). With bases
n3(\(2\))=1, n3(\(3\))=0, the xor is \(1\) iff \(k\ge 2\) is even,
all \(k\). Status: **lemma**. Recurrence checked on \(k\le 10\).

## Killed

Pointwise 4-to-1 fold: at \(k=6\), \(s=6\) the four children xor
to \(0\) while parent rem is \(1\). One-step even-halve: covering
n3 rem of \(t=10\) at \(k=5\) is \(1\), not rem of \(s=5\) at
\(k=4\).

## Verdict

`LEMMA` (r0 fold by two; r123 Green column; covering column xor
\(0\); covering n3 xor \(=1\) iff \(k\ge 2\) even, all \(k\); OX
two-threshold tails).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (pointwise 4-to-1 fold; one-step even-halve).
`PREFIX` (ep xor for all \(k\); covering \(S\) for all \(k\);
\(E_k=0\) for all \(k\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for
all \(k\); 11-bit gap; formula for extra 414990; at-most-one-odd
for all \(k\); seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_oy.md` (this note)
- `research/cycle_oy.py`
- `research/cycle_oy.json`
