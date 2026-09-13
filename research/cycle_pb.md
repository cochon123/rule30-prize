# Cycle PB: covering \(S\oplus T\) is \(1\) iff \(k=2\) or (\(k\ge 6\) and \(k\bmod 8\in\{0,6\}\))

Cycle PA closed covering \(S\) as \(1\) iff \(k\ge 6\) and
\(k\bmod 8\in\{0,6\}\). Cycle OJ closed covering \(T\) as \(1\)
iff \(k=2\). Their xor is the Green residual that packed rest
must match for \(E_k=0\): covering \(S\oplus T=1\) iff \(k=2\)
or (\(k\ge 6\) and \(k\bmod 8\in\{0,6\}\)), all \(k\). That bit
equals Cycle MD's rest10 on \(k\le 10\).

Pal-left packed rest xor vanishes through \(k\le 6\) and dies at
\(k=7\) (xor \(1\), cancelled by pal-right error). Pal-left
cancel is **not** why \(E_k=0\). Even \(n\) still has \(S=T=0\)
(Cycles OK/OJ), so \(E=0\) iff even-\(n\) rest equals odd-\(n\)
error; that rewrite is not a packed identity. **Not** rest
\(=S\oplus T\) for all \(k\). **Not** \(E_k=0\) for all \(k\).
Do **not** catalogue further \(S\)/\(T\) subregions unless the
experiment answers why \(E_k=0\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).

Certify: `python3 research/cycle_pb.py --certify` (runtime in the
dump commit). Dump: `research/cycle_pb.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/PA/OG/MD/GU/HG/HH/HU/LZ (S xor T form, pal-left rest;
prefix PA covering \(S\), OJ covering \(T\), OG \(E_k\), MD rest10;
no Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (covering \(S\oplus T\) is a Green 0-1)

Covering \(S_k\oplus T_k=1\) iff \(k=2\) or (\(k\ge 6\) and
\(k\bmod 8\in\{0,6\}\)), for every \(k\). Equals rest10 on
\(k\le 10\). Status: **lemma**. Form checked on \(0\le k\le 24\).

## Certified (pal-left packed rest xor)

Pal-left packed rest xor is \(0\) on \(k\le 6\) and \(1\) at
\(k=7\). Status: **certified**. Not all \(k\).

## Killed

Pal-left packed rest xor vanishes for all \(k\): at \(k=7\) the
xor is \(1\).

## Verdict

`LEMMA` (covering \(S\oplus T=1\) iff \(k=2\) or (\(k\ge 6\) and
\(k\bmod 8\in\{0,6\}\)), all \(k\); PA covering \(S\); OJ covering
\(T\)).
`CERTIFIED` (pal-left rest xor on \(k\le 7\); \(E_k=0\) on odd-\(s\)
rest for \(q=10\), \(k\le 10\)).
`KILLED` (pal-left rest xor for all \(k\)).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all
\(k\); seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_pb.md` (this note)
- `research/cycle_pb.py`
- `research/cycle_pb.json`
