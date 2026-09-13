# Cycle MN: on \(q=10\) for \(k\le 8\), \(j>n\) xor \(d\bmod 3=1\) Green proxy equals rest except \(k=8\)

On covering \(J_{10}\) for \(k\le 8\), XOR of Cycle MJ's \(j>n\)
\(G(n,j-1)\) xor with Cycle MM's palindrome-right \(d\bmod 3=1\)
xor equals packed rest except at \(k=8\) (proxy \(=0\), rest
\(=1\)). Prefix MJ/MM/MD dumps; no \(k=8\) re-walk. This is
**not** Green-only rest, **not** proxy equals rest, **not** the
proxy on \(q=6\) (\(k=1\): proxy \(=1\), rest \(=0\)), and **not**
the form for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim a Green-only formula for rest. Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_mn.py --certify` (~0.13s).
Dump: `research/cycle_mn.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/MJ/MM/MD (prefix MJ \(j>n\) xor, MM \(d\bmod 3=1\) xor, and
rest10; no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (Green proxy equals rest except \(k=8\))

Covering \(q=10\), \(k\le 8\). Proxy is
\(\mathrm{want}_{j>n}\oplus\mathrm{want}_{d31}\). At \(k=8\)
proxy \(=0\) and rest \(=1\).

## Killed

Proxy equals rest: \(k=8\), \(q=10\) is \(0\) vs \(1\). Proxy
equals rest on \(q=6\): \(k=1\), \(q=6\) is \(1\) vs \(0\).
Green-only rest: the \(k=8\) cell still requires the packed row.

## Verdict

`LEMMA` (Green proxy equals rest except \(k=8\) on \(q=10\) for
\(k\le 8\); palindrome-right \(d\bmod 3=1\) xor is \(1\) iff
\(k\bmod 4=0\); \(j>n\) xor is \(1\) iff \(k\) even on both
covering \(q\); rest10 census on \(k\le 10\); \(J\) closed form on
\(k\le 6\)).
`KILLED` (proxy equals rest; proxy on \(q=6\); Green-only rest;
the form for all \(k\); unique-rest xor equals \(J\); leftover
equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_mn.md` (this note)
- `research/cycle_mn.py`
- `research/cycle_mn.json`
