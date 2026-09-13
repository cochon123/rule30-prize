# Cycle OO: pal-right off-residue-\(0\) xor is \(1\) for every \(t\ge 1\)

Let \(A(t)\) be the xor of \(G(t,j)\) over palindrome-right
\(j\in(t,2t]\) with \((j-t)\not\equiv 0\pmod{3}\). Cycle OL already
identifies palindrome-right \(S(8t+3)\) with \(A(t)\).

If \(t=2m\) is even, Green even-\(n\)/odd-\(d\) kills every odd
offset, and the even offsets \(d=2e\) with \(e\not\equiv 0\pmod{3}\)
are exactly the palindrome-right off-residue-\(0\) cells of \(m\).
Hence \(A(2m)=A(m)\).

If \(t=2u+1\) is odd, Green doubling writes the pal-right string as
the interleave \(b_{2p}=G(u,u+p)\),
\(b_{2p+1}=G(u,u+p)\oplus G(u,u+p+1)\) with virtual
\(G(u,2u+1)=0\). Even offsets contribute \(A(u)\); odd offsets
contribute \(1\oplus A(u)\). So \(A(t)=A(u)\oplus(1\oplus A(u))=1\).
The odd-offset cancellation is a Boolean identity on every
endpoint-\(1\) parent string.

Therefore \(A(t)=1\) for every \(t\ge 1\) (halve until odd). The
\(t=0\) xor is empty, so \(S(3)=0\). Combined with Cycles OK/ON,
every odd \(n\not\equiv 1,5\pmod{8}\) is now a \(0\)-\(1\) value;
the even-parent residue xor on \(n\equiv 1,5\pmod{8}\) remains.

This is **not** \(S(8t+3)=1\) at \(t=0\), **not** a \(0\)-\(1\)
closed \(S\) for every odd \(n\), **not** covering \(S\) (clip
\(p\ge 0\) remains), and **not** \(E_k=0\) for all \(k\). Do
**not** catalogue further \(S\)/\(T\) subregions unless the
experiment answers why \(E_k=0\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).

Certify: `python3 research/cycle_oo.py --certify` (~0.19s).
Dump: `research/cycle_oo.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OK/OL/ON/OJ/OG (halving \(A(2m)=A(m)\); odd \(A=1\);
prefix ON fold, OL off-residue \(0\), OJ covering \(T_k\), OG
\(E_k\); no Fermat table, no extra window, no \(n_0=16\) window,
no packed covering \(k=11\)).

## Lemma (even \(t\): \(A(2m)=A(m)\))

Odd offsets vanish. Even offsets with \(d\not\equiv 0\pmod{3}\)
are the off-residue-\(0\) cells of \(m\). Status: **lemma** for
every \(m\ge 0\). Checked on \(m<128\).

## Lemma (odd \(t\): \(A(t)=1\))

Doubling plus the Boolean pairing
\(A(t)=A(u)\oplus(1\oplus A(u))=1\). Status: **lemma** for every
odd \(t\). Checked on odd \(t<256\), and on all endpoint-\(1\)
parent strings of length \(\le 11\).

## Lemma (\(S(8t+3)=1\) for every \(t\ge 1\))

\(A(t)=1\) after reducing by \(v_2(t)\), and Cycle OL’s
identification \(S(8t+3)=A(t)\). Status: **lemma** for every
\(t\ge 1\). Empty at \(t=0\). Checked on \(t<128\).

## Killed

\(S(8t+3)=1\) at \(t=0\): \(S(3)=0\). Closed odd-\(n\) \(S\) as a
\(0\)-\(1\) value: \(S(1)=0\) and \(S(9)=1\). Covering \(S\).
\(E_k=0\) for all \(k\).

## Verdict

`LEMMA` (\(A(2m)=A(m)\); odd \(A=1\); \(S(8t+3)=1\) for every
\(t\ge 1\); off-residue \(0\); \(S(4s+3)=S(s)\) for odd \(s\);
covering \(T_k=1\) iff \(k=2\)).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (\(S(3)=1\); closed odd-\(n\) \(S\)).
`PREFIX` (closed odd-\(n\) \(S\); covering \(S\); \(E_k=0\) for
all \(k\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all
\(k\); seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_oo.md` (this note)
- `research/cycle_oo.py`
- `research/cycle_oo.json`
