# Cycle OQ: pal-right residue-\(0\) xor is \(1\) iff popcount is even

Let \(R_r(t)\) be the xor of \(G(t,t+d)\) over \(1\le d\le t\) with
\(d\equiv r\pmod{3}\), and write \(A(t)=R_1(t)\oplus R_2(t)\). Cycle
OO gives \(A(t)=1\) for every \(t\ge 1\).

If \(t=2m\) is even, Green even-\(n\)/odd-\(d\) yields
\(R_0(2m)=R_0(m)\). If \(t=2u+1\) is odd, Green doubling writes
\(R_0(t)=R_0(u)\oplus A(u)\). For \(u\ge 1\) that is
\(R_0(u)\oplus 1\). Together with \(R_0(1)=0\), induction on \(t\)
gives \(R_0(t)=1\) iff \(t\) has even popcount, for every
\(t\ge 1\). Empty at \(t=0\).

Cycle OP then evaluates the remaining residues: \(R_1(2u+1)=1\oplus
R_0(u)\oplus A(u)\) (so \(R_1(t)=R_0((t-1)/2)\) for odd \(t\ge 3\)),
and even rows swap \(R_1,R_2\). Unclipped palindrome-right \(S\) on
every \(n\) is therefore a popcount / \(v_2\) function of \(n\).
Covering \(S\) still clips \(p\ge 0\).

This is **not** \(R_0=1\) at \(t=0\), **not** \(R_0=1\) iff
popcount is odd, **not** covering \(S\), and **not** \(E_k=0\) for
all \(k\). Do **not** catalogue further \(S\)/\(T\) subregions
unless the experiment answers why \(E_k=0\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).

Certify: `python3 research/cycle_oq.py --certify` (~0.15s).
Dump: `research/cycle_oq.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OK/OP/OO/ON/OJ/OG (\(R_0\) popcount; pal-right \(S\)
formula; prefix OP residue reduction, OO \(A(t)=1\), ON fold, OJ
covering \(T_k\), OG \(E_k\); no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (\(R_0(2m)=R_0(m)\))

Odd offsets vanish. Multiples of \(6\) halve to multiples of \(3\).
Status: **lemma** for every \(m\ge 0\). Checked on \(m<128\).

## Lemma (\(R_0(2u+1)=R_0(u)\oplus A(u)\))

Even offsets contribute \(R_0(u)\); odd offsets contribute
\(A(u)\). Status: **lemma** for every \(u\ge 0\). The pairing is a
Boolean identity on every endpoint-\(1\) parent string (checked on
all such strings of length \(\le 11\)).

## Lemma (\(R_0(t)=1\) iff popcount even, \(t\ge 1\))

Halving preserves popcount parity. Odd doubling plus \(A(u)=1\)
flips it, matching the extra \(1\)-bit of an odd argument. Status:
**lemma** for every \(t\ge 1\). Checked on \(t<256\).

## Lemma (unclipped pal-right \(S\) is popcount / \(v_2\))

Even \(n\) vanish; \(n=8t+3\) is \(1\) iff \(t>0\); \(n=8t+7\)
folds to \(S((n-3)/4)\); \(n=8t+1\) is \(R_1(t)\) and \(n=8t+5\)
is \(R_2(2t+1)\), with \(R_1,R_2\) from the popcount formula and
residue swap. Status: **lemma** for every \(n\). Checked on
\(n<128\). This is **not** covering \(S\).

## Killed

\(R_0(0)=1\): the xor is empty. \(R_0=1\) iff popcount is odd:
\(R_0(1)=0\) and \(R_0(3)=1\). Covering \(S\). \(E_k=0\) for all
\(k\).

## Verdict

`LEMMA` (\(R_0\) popcount; \(R_0\) even-half and odd fold;
unclipped pal-right \(S\); \(S(2m+1)=R_2(m/2)\); \(S(8t+3)=1\)
for \(t\ge 1\); \(S(4s+3)=S(s)\) for odd \(s\); covering
\(T_k=1\) iff \(k=2\)).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (\(R_0(0)=1\); \(R_0\) follows odd popcount).
`PREFIX` (covering \(S\); \(E_k=0\) for all \(k\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_oq.md` (this note)
- `research/cycle_oq.py`
- `research/cycle_oq.json`
