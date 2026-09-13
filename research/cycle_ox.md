# Cycle OX: covering \(n=8t+3\) rem is two-threshold \(R_1\)/\(R_2\) tails

Cycle OU writes clip-removed \(S(8t+3)\) as the 8-scale off0 image
of \(G(t)\). On covering \(j_{\max}=5\cdot 2^k\) (\(k\ge 3\)) that
image is past the clip iff \(d\ge L-t\) on residue 1 and
\(d\ge L-t+1\) on residue 2, with \(L=5\cdot 2^{k-3}\). So
covering rem is \(r_1\mathrm{-tail}(t,L-t)\oplus r_2\mathrm{-tail}(t,L-t+1)\).
Clip-active \(t\) for \(k\ge 4\) is \(\{5\cdot 2^{k-4},\ldots,2^{k-1}-1\}\),
count \(3\cdot 2^{k-4}\). Always \(L>t\), so neither residue is
the full \(R_1\) or \(R_2\).

On \(k\le 12\) that xor is \(1\) iff \(k\ge 2\) is even. This is
**not** a single \(d_{\min}\) tail. **Not** the xor of unclipped
\(A(t)\) over clip \(t\) (at \(k=6\) that xor is \(0\) while rem
xor is \(1\)). **Not** n3 xor for all \(k\). **Not** covering
\(S\) for all \(k\). **Not** \(E_k=0\) for all \(k\). Do **not**
catalogue further \(S\)/\(T\) subregions unless the experiment
answers why \(E_k=0\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).

Certify: `python3 research/cycle_ox.py --certify` (~1.1s).
Dump: `research/cycle_ox.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/OL/OU/OW/OG (two-threshold n3 tails; prefix OW ep
shape, OU 8-scale image, OG \(E_k\); no Fermat table, no extra
window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (covering n3 rem is two-threshold tails)

For \(k\ge 3\), clip-removed \(S(8t+3)\) at \(5\cdot 2^k\) equals
the residue-1 tail of \(G(t)\) from \(d=L-t\) xor the residue-2
tail from \(d=L-t+1\), \(L=5\cdot 2^{k-3}\). For \(k\ge 4\),
clip-active \(t\) is \(\{5\cdot 2^{k-4},\ldots,2^{k-1}-1\}\).
Status: **lemma**. Checked on \(4\le k\le 12\).

## Certified (covering n3 xor)

On \(k\le 12\), that xor is \(1\) iff \(k\ge 2\) is even.
Status: **certified**. Not all \(k\).

## Killed

Xor of unclipped \(A(t)\) over clip-active \(t\) at \(k=6\) is
\(0\), while covering n3 rem xor is \(1\).

## Verdict

`LEMMA` (two-threshold covering n3 tails; OU 8-scale image; OW
even-parent covering shape).
`CERTIFIED` (n3 xor \(=1\) iff \(k\ge 2\) even on \(k\le 12\);
\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (full \(A(t)\) xor over clip \(t\)).
`PREFIX` (n3 xor for all \(k\); covering \(S\) for all \(k\);
\(E_k=0\) for all \(k\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for
all \(k\); 11-bit gap; formula for extra 414990; at-most-one-odd
for all \(k\); seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ox.md` (this note)
- `research/cycle_ox.py`
- `research/cycle_ox.json`
