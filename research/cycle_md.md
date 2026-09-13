# Cycle MD: covering rest through \(k\le 10\) is \(1\) iff \(q=10\) and \(k\in\{2,6,8\}\)

On covering \(J_6,J_{10}\) for \(k\le 10\), packed AND xor off
\(\{p=4,p=6,p=14\}\) is \(1\) exactly at
\((k,q)=(2,10),(6,10),(8,10)\). Prefix Cycles LZ/MA/MB/MC; no
\(k=10\) re-walk. Unique-rest XOR is **not** always \(0\)
(\(k=2\), \(q=6\) is \(1\)); leftover XOR is **not** rest (same
cell leftover \(=1\), rest \(=0\)). This is **not** rest10 for
all \(k\), **not** \(k\equiv 2\pmod{4}\) on \(k\le 10\), and
**not** unique-rest xor vs \(J\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: covering never-fail stays open. Do **not**
guess a replacement modulus form for all \(k\) without a new
probe.

Certify: `python3 research/cycle_md.py --certify` (~0.13s).
Dump: `research/cycle_md.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HG/HH/HU/KH/LZ/MB (prefix dumps for \(k\le 10\); one
\(k=2\), \(q=6\) split walk; no Fermat table, no extra window,
no \(n_0=16\) window).

## Lemma (rest10 census on \(k\le 10\))

AND xor off \(\{4,6,14\}\) is \(1\) iff \(q=10\) and
\(k\in\{2,6,8\}\). Equals Cycle LZ rest on \(k\le 7\); picks up
Cycle MA's \(k=8\), \(q=10\); misses rest8's false \(1\) at
\(k=10\), \(q=10\).

## Killed

Rest \(=1\) iff \(q=10\) and \(k\equiv 2\pmod{4}\) on
\(k\le 10\): \(k=8\) is an extra \(1\), \(k=10\) is missing.
\(q=10\) rest empty through \(k\le 10\): \((2,10)\) is \(1\).
Unique-rest XOR always \(0\): \(k=2\), \(q=6\) is \(1\).
Leftover XOR equals rest: \(k=2\), \(q=6\) leftover \(=1\),
rest \(=0\).

## Verdict

`LEMMA` (rest10 census on \(k\le 10\); \(q=6\) rest \(=0\) at
\(k=10\); \(\mathrm{want}_{\mathrm{forced}}\) at \(k=8,9,10\);
rest8 on \(k\le 9\); \(J\) closed form on \(k\le 6\)).
`KILLED` (\(k\equiv 2\pmod{4}\) rest on \(k\le 10\); \(q=10\)
rest empty; unique-rest XOR always \(0\); leftover equals rest;
rest8 for all \(k\); \(\mathrm{want}_{J8}\) for all \(k\); LZ
form for all \(k\); LZ rest for all \(k\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_md.md` (this note)
- `research/cycle_md.py`
- `research/cycle_md.json`
