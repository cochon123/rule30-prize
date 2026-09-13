# Cycle NC: on \(q=6\) and \(q=10\) for \(k\le 8\), NA's \(S\) restricted to \(n<U\) is \(1\) iff \(k>0\) and \(k\bmod 4=0\)

On covering \(J_6,J_{10}\) for \(k\le 8\), XOR of \(G(n,j+1)\) over
palindrome-right cells with \((j-n)\bmod 3=1\), \(G(n,j-1)=0\), and
\(n<U\) (\(p=T-2j\ge 0\); no packed row) is \(1\) iff \(k>0\) and
\(k\bmod 4=0\). This is the \(n<U\) slice of Cycle NA's \(S\), and
the two covering \(q\) agree on xor and on \(n_S\). This is **not**
rest (\(k=4\), \(q=10\): xor \(=1\), rest \(=0\)), **not** Green
d31 (\(k=0\): \(0\) vs \(1\)), **not** MQ \(d\bmod 3=1\) \(G(j+1)\)
(\(k=4\): \(1\) vs \(0\)), **not** \(j>n\) even-\(k\) (\(k=2\):
\(0\) vs \(1\)), **not** NA \(S\) (\(k=6\), \(q=10\): \(0\) vs
\(1\)), **not** identically \(0\), **not** empty (\(k=3\):
\(n_S=2\)), **not** Green-only rest, and **not** the form for all
\(k\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for
all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\). Do **not**
walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim Green-only rest for all \(k\). Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_nc.py --certify`.
Dump: `research/cycle_nc.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/MJ/MQ/NA/NB (packed-free covering both \(q\) for
\(k\le 8\); prefix NB Green-only rest through \(k\le 10\), NA
\(S\), MJ \(j>n\), and MQ \(d31\) \(G(j+1)\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (\(S\) on \(n<U\) is \(1\) iff \(k>0\) and \(k\bmod 4=0\))

Both covering \(q\), \(k\le 8\). The walk does not read the packed
row. At \(k=3\), \(n_S=2\) but \(G(j+1)\) never fires. The \(n<U\)
counts agree on \(q=6\) and \(q=10\).

## Killed

Equals rest: \(k=4\), \(q=10\) is \(1\) vs \(0\). Equals Green
d31: \(k=0\) is \(0\) vs \(1\). Equals MQ \(d31\) \(G(j+1)\):
\(k=4\) is \(1\) vs \(0\). Equals \(j>n\) even-\(k\): \(k=2\) is
\(0\) vs \(1\). Equals NA \(S\): \(k=6\), \(q=10\) is \(0\) vs
\(1\). Vanishes: \(k=4\) is \(1\). Empty: \(k=3\) has \(n_S=2\).
Dies on \(q=6\): \(k=4\) xor \(=1\) equals the form. The form for
all \(k\).

## Verdict

`LEMMA` (\(S\) on \(n<U\) is \(1\) iff \(k>0\) and \(k\bmod 4=0\)
on both covering \(q\) for \(k\le 8\); Green-only rest on \(q=10\)
through \(k\le 10\); \(j>n\) xor is \(1\) iff \(k\) even; MQ
\(d31\) \(G(j+1)\); rest10 census on \(k\le 10\); \(J\) closed form
on \(k\le 6\)).
`KILLED` (equals rest; equals Green d31; equals MQ \(d31\)
\(G(j+1)\); equals jgtn; equals NA \(S\); vanishes; empty; dies on
\(q=6\); the form for all \(k\); unique-rest xor equals \(J\);
leftover equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_nc.md` (this note)
- `research/cycle_nc.py`
- `research/cycle_nc.json`
