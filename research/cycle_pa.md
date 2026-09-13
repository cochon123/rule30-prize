# Cycle PA: covering r123 xor is \(1\) iff \(k\) even; covering \(S\) is Green 0-1

Cycle OZ writes covering even-parent rem of \(4s\) as the parent
at \(k-2\), so the \(r=0\) covering xor is ep(\(k-2\)). The
\(r=1,2,3\) xor remained a certificate. On the covering window,
that r123 of \(s\) at scale \(k\) equals the pal-right suffix
\(\bigoplus_{j=M+1}^{2s}G(s,j)\) xor \(G(s,M-1)\) unless
\((M-s)\bmod 3=2\), with \(M=5\cdot 2^{k-4}\). Pal-suffix doubles
for both even and odd first arguments, so the covering odd/even
folds differ from the parent r123 by the unique Green columns
\(G(t,3\cdot 2^{k-5}-1)\) and \(G(t,5\cdot 2^{k-5}-1)\). Both
columns fire at the same unique \(t=3\cdot 2^{k-5}-1\) on the
covering parent window (even \(t\) vanish on an odd second
argument; odd \(t\) halves to the same-shaped window). Covering
odd xor even therefore cancels the parent r123 and equals
\(1\oplus(k\bmod 2)\) for \(k\ge 6\).

With Cycle OZ's \(r=0\) xor, covering ep xor is \(1\) iff
\(k\ge 6\) and \(k\bmod 4=2\), all \(k\). Cycle OV's n7 recurrence
and Cycle OY's n3 xor then close covering rem, and Cycle OR's
unclipped bit xor rem closes covering \(S\): covering \(S=1\)
iff \(k\ge 6\) and \(k\bmod 8\in\{0,6\}\). This is **not**
\(E_k=0\) for all \(k\) (packed rest \(=S\oplus T\) remains).
**Not** the pal-suffix formula off the covering window. **Not**
even-\(s\) r123 vanishing pointwise (\(k=6\), \(s=12\)). Do
**not** catalogue further \(S\)/\(T\) subregions unless the
experiment answers why \(E_k=0\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).

Certify: `python3 research/cycle_pa.py --certify` (runtime in the
dump commit). Dump: `research/cycle_pa.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/OR/OV/OW/OZ/OG (unique columns, pal-suffix r123,
covering folds; prefix OZ r0 fold, OY n3, OR unclip, OV rem
recurrence, OG \(E_k\); no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (unique Green columns)

For \(a\ge 1\) and \(t\in[5\cdot 2^{a-1},2^{a+2})\),
\(G(t,3\cdot 2^a-1)=G(t,5\cdot 2^a-1)=1\) iff
\(t=3\cdot 2^a-1\). Even \(t\) vanish (odd second argument). Odd
\(t=2u+1\) halves to the same-shaped window at \(a-1\). Base
\(a=1\): the window is \(\{5,6,7\}\). Status: **lemma**. Checked
on \(1\le a\le 8\).

## Lemma (covering r123 is a pal-right suffix)

For \(k\ge 6\) and clip-active covering \(s\) at scale \(k-2\),
\(\mathrm{r123}(s,k)\) equals the pal-right suffix from
\(j=M+1\) xor \(G(s,M-1)\) unless \((M-s)\bmod 3=2\). Interior
pal-\(t\) coefficients of a full \(f\)-block are identically \(1\);
the left edge skips \(f=\Delta=M-s\) and the right edge is the
corner \(G(s,2s)\). Status: **lemma**. Checked on \(6\le k\le 8\).

## Lemma (pal-suffix doubles)

For \(k\ge 6\) and covering parent \(h\),
\(\mathrm{pal\_suffix}(2h,M+1)=\mathrm{pal\_suffix}(h,M/2+1)\)
and the same with \(2h+1\). Status: **lemma**. Checked on
\(6\le k\le 8\).

## Lemma (covering r123 xor is \(1\) iff \(k\) even)

The odd fold is parent r123 xor the unique column; the even fold
is parent r123 xor \((k\bmod 2)\) times that column. Covering odd
xor even therefore equals \(1\oplus(k\bmod 2)\) for \(k\ge 6\),
with no induction on r123. Status: **lemma**. Checked on
\(6\le k\le 10\).

## Lemma (covering ep xor and covering \(S\), all \(k\))

Covering ep xor \(=\) ep(\(k-2\)) xor r123(\(k\)), hence \(1\) iff
\(k\ge 6\) and \(k\bmod 4=2\). Covering rem tot
\(=\) n3 \(\oplus\) rem(\(k-2\)) \(\oplus\) ep, so rem \(=1\) iff
\(k\ge 2\) and \(k\bmod 8\in\{0,2\}\). Covering \(S=\) unclip
\(\oplus\) rem is \(1\) iff \(k\ge 6\) and
\(k\bmod 8\in\{0,6\}\). Status: **lemma**. Recurrences checked
through \(k=23\); rem walk through \(k\le 8\); covering split
through \(k\le 10\).

## Killed

Even-\(s\) r123 vanishes pointwise: at \(k=6\), \(s=12\) the
value is \(1\). (Covering even-s xor still vanishes at even \(k\).)

## Verdict

`LEMMA` (unique columns; pal-suffix r123; pal-suffix doubles;
covering r123 xor \(=1\) iff \(k\ge 6\) even; ep xor \(=1\) iff
\(k\ge 6\) and \(k\bmod 4=2\), all \(k\); covering \(S=1\) iff
\(k\ge 6\) and \(k\bmod 8\in\{0,6\}\), all \(k\); OZ r0 fold;
OY n3 xor; OR unclip; OV rem recurrence).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (even-\(s\) r123 vanishes pointwise).
`PREFIX` (\(E_k=0\) for all \(k\); packed rest \(=S\oplus T\) for
all \(k\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all
\(k\); seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_pa.md` (this note)
- `research/cycle_pa.py`
- `research/cycle_pa.json`
