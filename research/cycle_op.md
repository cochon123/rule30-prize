# Cycle OP: even-parent pal-right \(S\) is residue \(2\) of \(m/2\)

Cycle OL’s even-parent formula is
\[
S(2m+1)=\bigoplus_{i\ge 0,\,4+6i\le m+1} G(m,m+4+6i)
\]
for even \(m\). Let \(m=2p\). Green even-\(n\)/odd-\(d\) kills odd
offsets, and the surviving offsets \(4+6i\) halve to palindrome-right
offsets \(\equiv 2\pmod{3}\) of \(p\). Hence \(S(2m+1)=R_2(p)\),
where \(R_r(t)\) is the xor of \(G(t,t+d)\) over \(1\le d\le t\)
with \(d\equiv r\pmod{3}\).

The same halving swaps residues on even rows:
\(R_1(2p)=R_2(p)\) and \(R_2(2p)=R_1(p)\). Therefore
\(S(8t+1)=R_1(t)\) and \(S(8t+5)=R_2(2t+1)\). Combined with
Cycles OO/ON, palindrome-right \(S\) on every odd \(n\) is a
single Green residue xor (or a \(0\)-\(1\) value). Those
residues are **not** themselves a \(0\)-\(1\) form
(\(R_1(1)=1\), \(R_1(2)=0\)).

This is **not** \(R_1=1\) for all \(t\ge 1\), **not** even-parent
\(S=0\), **not** a \(0\)-\(1\) closed odd-\(n\) \(S\), **not**
covering \(S\) (clip \(p\ge 0\) remains), and **not** \(E_k=0\)
for all \(k\). Do **not** catalogue further \(S\)/\(T\)
subregions unless the experiment answers why \(E_k=0\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not**
bump all \(n_0=16\) past 414990. Do **not** increment consecutive
`11` to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\)
covering packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).

Certify: `python3 research/cycle_op.py --certify` (~0.15s).
Dump: `research/cycle_op.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OK/OL/OO/ON/OJ/OG (even-parent \(B=R_2(m/2)\); residue
swap; prefix OO \(S(8t+3)=1\), ON fold, OJ covering \(T_k\), OG
\(E_k\); no Fermat table, no extra window, no \(n_0=16\) window,
no packed covering \(k=11\)).

## Lemma (even \(m=2p\): \(S(2m+1)=R_2(p)\))

Odd offsets vanish. Even offsets \(4+6i\) are \(2+3i\) on the
parent, i.e. residue \(2\). Status: **lemma** for every even
\(m\). Checked on \(m<128\).

## Lemma (even rows swap residues)

\(R_1(2p)=R_2(p)\) and \(R_2(2p)=R_1(p)\). Status: **lemma** for
every \(p\ge 0\). Checked on \(p<128\). Recovers Cycle OO’s
\(A(2p)=A(p)\).

## Lemma (\(S(8t+1)=R_1(t)\), \(S(8t+5)=R_2(2t+1)\))

\(S(8t+1)=B(4t)=R_2(2t)=R_1(t)\) and
\(S(8t+5)=B(4t+2)=R_2(2t+1)\). Status: **lemma** for every
\(t\ge 0\). Checked on \(t<64\).

## Killed

\(R_1=1\) for all \(t\ge 1\): \(R_1(2)=0\). Even-parent \(S=0\):
\(S(9)=1\). Closed odd-\(n\) \(S\) as a \(0\)-\(1\) value:
\(S(1)=0\) and \(S(9)=1\). Covering \(S\). \(E_k=0\) for all
\(k\).

## Verdict

`LEMMA` (\(S(2m+1)=R_2(m/2)\); residue swap; \(S(8t+1)=R_1(t)\);
\(S(8t+5)=R_2(2t+1)\); \(S(8t+3)=1\) for \(t\ge 1\);
\(S(4s+3)=S(s)\) for odd \(s\); covering \(T_k=1\) iff \(k=2\)).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (\(R_1=1\) for all \(t\ge 1\); even-parent \(S=0\)).
`PREFIX` (closed odd-\(n\) \(S\); covering \(S\); \(E_k=0\) for
all \(k\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all
\(k\); seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_op.md` (this note)
- `research/cycle_op.py`
- `research/cycle_op.json`
