# Cycle HN: both-AND 6-tuples; odd AND forbids even AND at \(p-2\)

Odd-\(s\) AND at \(p\) and even-\(s\) AND at \(p-2\) cannot both be
1: `AND_ONES` never starts with \(11\). Both adjacent odd-\(s\) AND
iff the even-\(s\) 6-tuple is one of \(001001\), \(010010\),
\(010011\), \(100100\). Both-AND is **not** only \(100100\). It is
**not** only when \(G(n,j)=G(n,j+1)=1\). It is **not** only on
\(G=1\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for
all \(k\). Do **not** push the even-spine scan past \(k=18\). Do
**not** bump all \(n_0=16\) past 414990. Do **not** increment
consecutive `11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: a 4-row both-AND table plus a local AND
obstruction does not give a closed form along Green ones, so
covering never-fail stays open.

Helper: `BOTH_AND`. Certify: `python3 research/cycle_hn.py --certify` (~0.14s).
Dump: `research/cycle_hn.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles AL/CA/GU/HF/HG/HH/HM
(64-row table; covering \(k\le 6\); no Fermat table, no extra window,
no \(n_0=16\) window).

## Lemma (both-AND iff four 6-tuples; odd AND forbids even AND at \(p-2\))

64-row identity. `AND_ONES` has no \(11\) prefix, so odd-\(s\)
\(\mathrm{AND}(n,j)=1\) forces even-\(s\) AND at \(p-2\) dead.
Certified on \(J_6,J_{10}\) for \(k\le 6\). Odd-\(s\) \(J\) XOR
matches Cycles HF/HG.

## Killed

Both-AND only \(100100\): at \(k=1\), \(s=7\), \(n=2\), \(j=0\),
\(p=12\), six \(001001\). Both-AND only when
\(G(n,j)=G(n,j+1)=1\): at \(k=0\), \(s=5\), \(n=0\), \(j=0\),
\(G(0,1)=0\). Both-AND only on \(G=1\): at \(k=2\), \(s=9\), \(n=7\),
\(j=9\), \(p=6\), \(G=0\).

## Verdict

`LEMMA` (both-AND iff four 6-tuples; odd AND forbids even AND at
\(p-2\); `AND_ONES` no \(11\) prefix).
`KILLED` (both-AND only \(100100\); both-AND only when Green pair is
\(11\); both-AND only on \(G=1\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_hn.md` (this note)
- `research/cycle_hn.py`
- `research/cycle_hn.json`
