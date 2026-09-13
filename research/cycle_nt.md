# Cycle NT: on \(q=10\) through \(k\le 10\), inner palindrome-right \(G(j-1)\) vanishes

On covering \(J_{10}\) through \(k\le 10\), XOR of \(G(n,j-1)\) over
covering \(G=1\) cells with \(n<j\le n+\lfloor n/2\rfloor\)
(\(p=T-2j\ge 0\); no packed row) is \(0\). Lift of Cycle MK
(\(k\le 8\)). Prefix MK \(q=10\) for \(k\le 8\); walk \(k=9\) and
\(k=10\). Outer xor still equals Cycle MJ's even-\(k\) form, so
that \(j>n\) xor is still the outer slice. This is **not** a
death at \(k=9\), **not** a death at \(k=10\), **not** rest
(\(k=2\): \(0\) vs \(1\)), **not** NS inner even-\(d\) \(G(j+1)\)
(\(k=3\), \(q=6\): \(1\) vs \(0\)), **not** empty (\(k=9\):
\(n_{\mathrm{in}}=78271\)), **not** pointwise \(0\) (\(k=1\):
MX inner odd-\(d\) \(n_{G(j-1)=1}=2\)), **not** inner vanish on
\(q=6\) (\(k=3\), \(q=6\) xor \(=1\)), and **not** the form for
all \(k\). Do **not** record Cycle MX's inner odd-\(d\) \(G(j-1)\)
as a standalone \(q=10\) lift (tautology of this vanish on
\(q=10\)). Do **not** claim \(T\) is \(1\) iff \(k=2\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim Green-only rest for all \(k\). Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_nt.py --certify` (~9.05s).
Dump: `research/cycle_nt.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/MK/MX/NS/MJ (packed-free covering \(q=10\); prefix MK inner
\(G(j-1)\) for \(k\le 8\); walk \(k=9,10\); MX \(k=1\) fire count
for not-pointwise; no Fermat table, no extra window, no \(n_0=16\)
window).

## Lemma (inner palindrome-right \(G(j-1)\) vanishes through \(k\le 10\))

Covering \(q=10\), \(k\le 10\). The walk does not read the packed
row. Same cells as Cycle MK. At \(k=1\), \(n_{\mathrm{in}}=3\) and
inner odd-\(d\) \(G(j-1)\) fires twice. At \(k=9\),
\(n_{\mathrm{in}}=78271\).

## Lemma (outer slice equals Cycle MJ even-\(k\) xor through \(k\le 10\))

Same \(q=10\), \(k\le 10\) census: \(j>n+\lfloor n/2\rfloor\) xor
of \(G(n,j-1)\) on \(G=1\) is \(1\) iff \(k\) even.

## Killed

Dies at \(k=9\): xor \(=0\). Dies at \(k=10\): xor \(=0\). Equals
rest: \(k=2\) is \(0\) vs \(1\). Equals NS inner even-\(d\)
\(G(j+1)\): \(k=3\), \(q=6\) is \(1\) vs \(0\). Inner vanish on
\(q=6\): \(k=3\), \(q=6\) is \(1\). Empty: \(k=9\) has
\(n_{\mathrm{in}}=78271\). Pointwise \(0\): \(k=1\) has
\(n_{G(j-1)=1}=2\). The form for all \(k\).

## Verdict

`LEMMA` (inner palindrome-right \(G(j-1)\) vanishes on \(q=10\) for
\(k\le 10\); that vanish holds on \(q=10\) for \(k\le 8\); outer
slice equals MJ even-\(k\) xor through \(k\le 10\); \(j>n\) xor is
\(1\) iff \(k\) even on both covering \(q\) for \(k\le 8\); inner
even-\(d\) \(G(j+1)\) vanishes on \(q=10\) for \(k\le 10\); rest10
census on \(k\le 10\); \(J\) closed form on \(k\le 6\)).
`KILLED` (dies at \(k=9\); dies at \(k=10\); equals rest; equals
NS inner even-\(d\) \(G(j+1)\); inner vanish on \(q=6\); empty;
pointwise \(0\); the form for all \(k\); unique-rest xor equals
\(J\); leftover equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_nt.md` (this note)
- `research/cycle_nt.py`
- `research/cycle_nt.json`
