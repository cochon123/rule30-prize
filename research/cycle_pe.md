# Cycle PE: right-edge bits \(e_0,\ldots,e_5\); pal-duals of \(p=4\) and \(p=6\)

Cycle PD froze packed bits \(1..6\) on the left. The right edge is
the opposite packed coordinate \(e_i(t)=\) bit \(2t-i\). The
recurrence \(e_i(t+1)=e_i(t)\oplus(e_{i-1}(t)\lor e_{i-2}(t))\)
with negative bits \(0\) and \(e_0=1\) closes the first six bits
for every \(t\): \(e_0=1\), \(e_1=e_2=t\bmod 2\),
\(e_3=(t\gg 1)\bmod 2\), \(e_4=1\) iff \(t\bmod 8\in\{2,4,5,7\}\),
\(e_5=1\) iff \(t\bmod 8\in\{3,5,7\}\). On even \(t\) the 4-tuple
at \(p=2t\) is \(1001\) iff \(t\bmod 4=2\), and the 4-tuple at
\(p=2t-2\) is an AND-one iff \(t\bmod 8\in\{4,6\}\).

Covering pal-dual packed columns sum to \(2s+4\), so \(p=4\)
duals with the right edge and \(p=6\) duals with \(p=2s-2\).
Cycle PC's unique even \(n\) in the \(p=4\) Green set is
\(n=3U-2\), live at \(j=U-2\), and the even covering time is
\(s=4U+2\equiv 2\pmod{4}\), hence packed AND \(=1\) for every
\(k\ge 1\). The unique \(n\equiv 1\pmod{4}\) in the \(p=6\) Green
set is \(n=3U-3\), live at \(j=U-3\) for \(k\ge 2\), with
\(s=4U+4\), hence packed AND \(=1\). Both cells sit off
\(\{4,6,14\}\). They cancel in rest xor for \(k\ge 2\).

Even-\(n\) rest is **not** \(1\) iff \(k\bmod 8\in\{0,1,2,7\}\):
at \(k=9\) the xor is \(0\). **Not** rest \(=S\oplus T\). **Not**
\(E_k=0\) for all \(k\). Do **not** catalogue further \(S\)/\(T\)
subregions unless the experiment answers why \(E_k=0\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim Cycle PE's dual cells xor to rest. Do **not**
claim \(e_i\) for \(i\ge 6\) has a small period.

Certify: `python3 research/cycle_pe.py --certify` (~1.71s).
Dump: `research/cycle_pe.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/PC/PD/PB/GU/HG/HH/HU/LZ (right-edge bits, pal-dual
cells; prefix PD forced xor, PC Green sets, PB \(S\oplus T\);
no Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (right-edge bits \(e_0,\ldots,e_5\))

For every \(t\ge 0\), packed bit \(2t-i\) equals the form above
for \(i=0,\ldots,5\). Status: **lemma**. Checked on
\(0\le t\le 64\).

## Lemma (AND at \(p=2t\) and \(p=2t-2\) on even \(t\))

Even \(t\ge 2\): AND at the right edge fires iff \(t\bmod 4=2\);
AND at \(p=2t-2\) fires iff \(t\bmod 8\in\{4,6\}\). Status:
**lemma**.

## Lemma (covering pal-dual columns)

On covering \(q=10\), \(p+(T-2(2n-j))=2s+4\) with
\(s=T-2n-2\). Hence \(p=4\) duals with \(p=2s\) and \(p=6\)
duals with \(p=2s-2\). Status: **lemma**.

## Lemma (unique pal-dual rest cells)

The covering cell \((n,j)=(3U-2,U-2)\) has packed AND \(=1\) for
every \(k\ge 1\). The covering cell \((3U-3,U-3)\) has packed
AND \(=1\) for every \(k\ge 2\). They cancel in rest xor for
\(k\ge 2\). Status: **lemma**. Thin packed check on \(k\le 12\).

## Killed

Even-\(n\) rest \(=1\) iff \(k\bmod 8\in\{0,1,2,7\}\): at \(k=9\)
the xor is \(0\).

## Verdict

`LEMMA` (right-edge \(e_0..e_5\); AND at \(r=0,2\); pal-dual sum;
unique \(p=4\)/\(p=6\) dual AND; PD forced xor; PC Green sets;
PB covering \(S\oplus T\)).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (even-\(n\) rest 8-period).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_pe.md` (this note)
- `research/cycle_pe.py`
- `research/cycle_pe.json`
