# Cycle OZ: covering even-parent rem of \(4s\) folds by two; \(r=0\) xor is ep(\(k-2\))

Cycle OW writes covering rem of even-parent \(n=4p+1\) as the
partial \(R_2\) tail of \(G(p)\) with \(d_{\min}=5\cdot 2^{k-2}-p+1\).
Even-halve twice sends pal-right of \(p=4s\) to pal-right of \(s\)
at offsets \(d\equiv 0\pmod{4}\), and covering thresholds scale by
four, so \(\mathrm{ep\_cover\_rem}(4s,k)=\mathrm{ep\_cover\_rem}(s,k-2)\)
for \(k\ge 4\). For \(k\ge 5\), clip-active \(p\) is the disjoint
4-groups of clip-active \(s\) at scale \(k-2\). The \(r=0\) covering
xor is therefore ep xor at \(k-2\).

The \(r=1,2,3\) covering xor is \(1\) iff \(k\ge 6\) is even, on
\(k\le 12\). Hence covering ep xor is \(1\) iff \(k\ge 6\) and
\(k\bmod 4=2\) on that range, matching Cycle OW through \(k=10\)
and adding \(k=11,12\). This is **not** the pointwise 4-to-1 fold
(\(k=6\), \(s=11\): children xor to \(0\), parent rem is \(1\)).
**Not** ep xor for all \(k\). **Not** covering \(S\) for all \(k\).
**Not** \(E_k=0\) for all \(k\). Do **not** catalogue further
\(S\)/\(T\) subregions unless the experiment answers why
\(E_k=0\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).

Certify: `python3 research/cycle_oz.py --certify`.
Dump: `research/cycle_oz.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/OS/OW/OY/OG (r0 fold, covering split; prefix OY n3
xor all \(k\), OW ep form, OS \(R_2\) tail, OG \(E_k\); no Fermat
table, no extra window, no \(n_0=16\) window, no packed covering
\(k=11\)).

## Lemma (covering even-parent rem of \(4s\) folds by two)

For \(k\ge 4\) and every \(s\ge 0\),
\(\mathrm{ep\_cover\_rem}(4s,k)=\mathrm{ep\_cover\_rem}(s,k-2)\).
Status: **lemma**. Checked on \(4\le k\le 8\).

## Lemma (covering \(r=0\) xor is ep at \(k-2\))

For \(k\ge 5\), clip-active \(p\) is the 4-groups of clip-active
\(s\) at \(k-2\), so the \(p\equiv 0\pmod{4}\) covering rem xor
equals ep xor at \(k-2\). Status: **lemma**. Checked on
\(5\le k\le 12\).

## Certified (covering r123 and ep xor)

On \(k\le 12\), the \(r=1,2,3\) covering xor is \(1\) iff \(k\ge 6\)
is even, and covering ep xor is \(1\) iff \(k\ge 6\) and
\(k\bmod 4=2\). Status: **certified**. Not all \(k\).

## Killed

Pointwise 4-to-1 fold: at \(k=6\), \(s=11\) the four children xor
to \(0\) while parent rem is \(1\).

## Verdict

`LEMMA` (r0 fold by two; covering r0 xor \(=\) ep(\(k-2\)); OY n3
xor all \(k\); OS \(R_2\) tail).
`CERTIFIED` (r123 xor \(=1\) iff \(k\ge 6\) even on \(k\le 12\);
ep xor \(=1\) iff \(k\ge 6\) and \(k\bmod 4=2\) on \(k\le 12\);
\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (pointwise 4-to-1 fold).
`PREFIX` (ep xor for all \(k\); covering \(S\) for all \(k\);
\(E_k=0\) for all \(k\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for
all \(k\); 11-bit gap; formula for extra 414990; at-most-one-odd
for all \(k\); seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_oz.md` (this note)
- `research/cycle_oz.py`
- `research/cycle_oz.json`
