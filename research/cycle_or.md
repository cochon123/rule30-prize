# Cycle OR: unclipped covering-window pal-right \(S\) is \(1\) iff \(k\equiv 2\pmod{4}\)

Let \(P(N)\) be the xor of unclipped palindrome-right \(S\) on
\(0\le n<N\). Cycle OQ evaluates each \(S(n)\) by popcount / \(v_2\).
Even \(n\) vanish, so only the four odd classes contribute.

The class \(n=8t+3\) contributes \(1\) for every \(t\ge 1\). On a
dyadic interval the remaining classes reduce to the prefix xor
\(Q_1(2^a)=\bigoplus_{t<2^a} R_1(t)\) and to \(P\) at a smaller
power of two, via Cycle ON's fold \(S(8t+7)=S(2t+1)\). Grouping
\(R_1\) by \(v_2(t)\) gives \(Q_1(2^a)=1\) iff \(a\) is even, except
\(Q_1(2)=1\) and \(Q_1(1)=1\). Induction then yields
\(P(2^k)=1\) iff \(k\ge 4\) and \(k\equiv 0\pmod{4}\).

Covering \(n\) on \(q=10\) runs through \([0,4U)\). The unclipped
covering-window xor is therefore \(P(4U)=P(2^{k+2})\), which is
\(1\) iff \(k\ge 2\) and \(k\equiv 2\pmod{4}\). The clip window
\(5U/2<n<4U\) has unclipped xor \(0\), because
\(P(5\cdot 2^a+1)=P(2^{a+3})\) (the same \(R_1\) high-bit identity
that evaluates \(Q_1(5\cdot 2^b)\)). Covering \(S\) is that bit xor
the clip-removed pal-right \(S\) xor. Clip still kills nothing on
even \(n\): \(G(n,j+1)=0\) whenever \(n\) is even and \(G(n,j)=1\).

This is **not** covering \(S\) itself: clip-removed is \(1\) at
\(k=2,8\) on \(k\le 8\), so covering \(S\) is \(0,0,0,0,0,0,1,0,1\)
through \(k\le 8\) (matching \(E_k=0\)), not the unclipped
\(0,0,1,0,0,0,1,0,0\). Not \(E_k=0\) for all \(k\). Do **not**
catalogue further \(S\)/\(T\) subregions unless the experiment
answers why \(E_k=0\). Do **not** claim \(J_6=J_{10}=0\Rightarrow
J_{18}=1\) for all \(k\). Do **not** push the even-spine scan past
\(k=18\). Do **not** bump all \(n_0=16\) past 414990. Do **not**
increment consecutive `11` to \(n_8\). Do **not** walk \(32U\).
Do **not** walk \(k=11\) covering packed. Do **not** walk \(k=12\)
\(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).

Certify: `python3 research/cycle_or.py --certify`.
Dump: `research/cycle_or.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/MD/OJ/OK/OQ/OG/NA (\(P(2^k)\); unclipped covering window;
clip window unclipped-zero; prefix OQ popcount \(S\), OJ covering
\(T_k\), OG \(E_k\), NA covering \(S\) on \(k\le 8\); no Fermat
table, no extra window, no \(n_0=16\) window, no packed covering
\(k=11\)).

## Lemma (\(P(2^k)=1\) iff \(k\ge 4\) and \(k\equiv 0\pmod{4}\))

Class split plus \(Q_1(2^a)\) plus Cycle ON's fold. Status:
**lemma** for every \(k\ge 0\). Checked on \(k\le 12\).

## Lemma (unclipped covering-window \(S\) is \(1\) iff \(k\equiv 2\pmod{4}\))

\(P(4U)=P(2^{k+2})\). Status: **lemma** for every \(k\ge 0\). Empty
below \(k=2\).

## Lemma (clip-window unclipped xor vanishes)

\(P(5\cdot 2^a+1)=P(2^{a+3})\). Status: **lemma** for every
\(a\ge 0\). Checked on \(a\le 12\).

## Lemma (even \(n\) still vanish under clip)

Each even-\(n\) \(S\)-term is \(G(n,j+1)=0\). Status: **lemma** for
every even \(n\). Checked on covering even \(n\) for \(k\le 5\).

## Killed

Covering \(S\) equals the unclipped window: \(k=2\) has unclip \(1\)
and covering \(S=0\); \(k=8\) has unclip \(0\) and covering \(S=1\).
Covering \(S=1\) iff \(k\equiv 2\pmod{4}\): same \(k=2\) counterexample.

## Verdict

`LEMMA` (\(P(2^k)\); unclipped covering-window \(S\); clip-window
unclipped xor \(0\); even-\(n\) clip vanish; unclipped pal-right
\(S\); \(R_0\) popcount; covering \(T_k=1\) iff \(k=2\)).
`CERTIFIED` (covering \(S\) on \(q=10\), \(k\le 8\); \(E_k=0\) on
odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (covering \(S\) equals unclipped window; covering \(S\)
follows \(k\equiv 2\pmod{4}\)).
`PREFIX` (covering \(S\) for all \(k\); \(E_k=0\) for all \(k\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_or.md` (this note)
- `research/cycle_or.py`
- `research/cycle_or.json`
