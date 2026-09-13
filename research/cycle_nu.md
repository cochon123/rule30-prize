# Cycle NU: on \(q=10\) through \(k\le 10\), palindrome-right \(d\bmod 3=1\) \(G(j+1)\) is \(1\) iff \(k\bmod 4\in\{1,2\}\)

On covering \(J_{10}\) through \(k\le 10\), XOR of \(G(n,j+1)\) over
covering \(G=1\) cells with \(j>n\) and \((j-n)\bmod 3=1\)
(\(p=T-2j\ge 0\); no packed row) is \(1\) iff \(k\bmod 4\in\{1,2\}\).
Lift of Cycle MQ (\(k\le 8\)). Prefix MQ \(q=10\) for \(k\le 8\);
walk \(k=9\) and \(k=10\). Dual of Cycle MM's Green \(d31=1_{k\bmod 4=0}\)
on \(G(n,j-1)\), which still holds as a companion at those \(k\)
(\(xor_{j-1}=0\); not recorded here). This is **not** a death at
\(k=9\), **not** a death at \(k=10\), **not** rest (\(k=1\): \(1\)
vs \(0\)), **not** NQ \(T\)-cell \(d31\) \(G(j+1)\) (\(k=9\): \(1\)
vs \(0\)), **not** MM Green d31 (\(k=9\): \(1\) vs \(0\)), **not**
NT inner \(G(j-1)\) vanish (\(k=9\): \(1\) vs \(0\)), **not**
identically \(0\), **not** empty (\(k=9\): \(n_{\mathrm{d31}}=50742\)),
**not** the \(\{1,2\}\) form on \(q=6\), and **not** the form for
all \(k\). Do **not** claim \(T\) is \(1\) iff \(k=2\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim Green-only rest for all \(k\). Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_nu.py --certify` (~9.03s).
Dump: `research/cycle_nu.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/MQ/NT/MM/NQ/MJ (packed-free covering \(q=10\); prefix MQ
d31 \(G(j+1)\) for \(k\le 8\); walk \(k=9,10\); no Fermat table,
no extra window, no \(n_0=16\) window).

## Lemma (palindrome-right \(d\bmod 3=1\) \(G(j+1)\) is \(1\) iff \(k\bmod 4\in\{1,2\}\) through \(k\le 10\))

Covering \(q=10\), \(k\le 10\). The walk does not read the packed
row. Same cells as Cycle MQ. At \(k=1\), \(n_{\mathrm{d31}}=6\) and
xor \(=1\). At \(k=9\), \(n_{\mathrm{d31}}=50742\) and xor \(=1\).
Companion \(G(j-1)\) xor on those cells is \(0\) at \(k=9,10\)
(Cycle MM form; not recorded here).

## Killed

Dies at \(k=9\): xor \(=1=\) want. Dies at \(k=10\): xor \(=1=\)
want. Equals rest: \(k=1\) is \(1\) vs \(0\). Equals NQ \(T\)-cell
\(d31\) \(G(j+1)\): \(k=9\) is \(1\) vs \(0\). Equals MM Green
d31: \(k=9\) jp1 \(=1\) and jm1 \(=0\). Equals NT inner vanish:
\(k=9\) is \(1\). Vanishes: \(k=9\) is \(1\). Empty: \(k=9\) has
\(n_{\mathrm{d31}}=50742\). The \(\{1,2\}\) form on \(q=6\):
\(k=1\), \(q=6\) jp1 \(=0\). The form for all \(k\).

## Verdict

`LEMMA` (palindrome-right \(d\bmod 3=1\) xor of \(G(j+1)\) is \(1\)
iff \(k\bmod 4\in\{1,2\}\) on \(q=10\) for \(k\le 10\); that form
holds on \(q=10\) for \(k\le 8\); Green d31 \(G(j-1)\) is \(1\) iff
\(k\bmod 4=0\) on \(q=10\) for \(k\le 8\); inner palindrome-right
\(G(j-1)\) vanishes on \(q=10\) for \(k\le 10\); rest10 census on
\(k\le 10\); \(J\) closed form on \(k\le 6\)).
`KILLED` (dies at \(k=9\); dies at \(k=10\); equals rest; equals
NQ \(T\)-cell \(d31\) \(G(j+1)\); equals MM Green d31; equals NT
inner vanish; vanishes; empty; \(\{1,2\}\) form on \(q=6\); the
form for all \(k\); unique-rest xor equals \(J\); leftover equals
rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_nu.md` (this note)
- `research/cycle_nu.py`
- `research/cycle_nu.json`
