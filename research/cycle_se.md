# Cycle SE: even-child odd-\(j\) consecutive Green is \((G(m,r+2),0,G(m,r+1),0)\)

Cycle QV \(G(2m,2r)=G(m,r)\) and \(G(2m,\mathrm{odd})=0\), so at even
child \(n=2m\) and odd \(j=2r+1\) the consecutive Green bits
\((G(n,j+3),G(n,j+2),G(n,j+1),G(n,j))\) equal
\((G(m,r+2),0,G(m,r+1),0)\). Last bit is \(0\), so there are no
\(G=1\) cells. The type \((0,0,1,0)\) is in AND_ONES when
\(G(m,r+2)=0\) and \(G(m,r+1)=1\); \((0,1,0,0)\) never occurs.
Cycle RX even-\(j\) form is \((0,G(m,r+1),0,G(m,r))\), **not** this
4-tuple. Packed AND at consecutive-\(p\) can still fire (Cycle QV
mismatch). This is **not** rest \(=S\oplus T\). **Not** \(E_k=0\)
for all \(k\). Do **not** catalogue leftover \(p\) one-by-one. Do
**not** catalogue further \(S\)/\(T\) subregions unless the
experiment answers why \(E_k=0\). Do **not** claim pal-left leftover
xor vanishes for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\). Do **not** walk \(k=11\) covering packed. Do
**not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim cellwise 2-fold packed AND. Do **not** claim
even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at \(k-1\)
for all \(k\). Do **not** claim UNIQUE_REST 2-fold all stay unique.

Certify: `python3 research/cycle_se.py --certify`.
Dump: `research/cycle_se.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/AL/HH/HJ/HS/HU/KH/OJ/QV/RX/SD (even-child odd-\(j\) consecutive
Green is \((G(m,r+2),0,G(m,r+1),0)\); AND iff \(0010\); never
\(G=1\); no Fermat table, no extra window, no \(n_0=16\) window,
no packed covering \(k=11\)).

## Lemma (even-child odd-\(j\) consecutive Green)

At \(n=2m\), odd \(j=2r+1\), consecutive Green bits equal
\((G(m,r+2),0,G(m,r+1),0)\). AND fires iff the 4-tuple is \(0010\).
There are no \(G=1\) cells. Status: **lemma**. **Killed:** that
4-tuple never meets AND_ONES. **Killed:** it equals Cycle RX
even-\(j\) consecutive Green. **Killed:** it equals Cycle SD
odd-child consecutive Green. **Killed:** identically
\((0,0,0,0)\). **Killed:** it meets \(0100\).

## Verdict

`LEMMA` (even-child odd-\(j\) consecutive Green is
\((G(m,r+2),0,G(m,r+1),0)\); never \(G=1\); AND iff \(0010\);
RX/SD closed forms).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (never AND; equals RX even-\(j\); equals SD; identically
\((0,0,0,0)\); meets \(0100\); cellwise 2-fold packed AND).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_se.md` (this note)
- `research/cycle_se.py`
- `research/cycle_se.json`
