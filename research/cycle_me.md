# Cycle ME: on \(q=10\) for \(k\le 8\), unique-rest XOR is \(0\) so leftover XOR is rest

On covering \(J_{10}\) for \(k\le 8\), XOR of the LC–LU unique
packed AND slots off \(\{p=4,p=6,p=14\}\) vanishes, so rest
equals leftover AND xor. Dual of Cycle MD's \(k=2\), \(q=6\)
kill (that unique xor is \(1\)). This is **not** leftover
equals rest on \(q=6\), **not** unique-rest xor vs \(J\),
**not** the split for all \(k\), and **not** \(q=6\) unique xor
\(=0\). Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\)
for all \(k\). Do **not** push the even-spine scan past
\(k=18\). Do **not** bump all \(n_0=16\) past 414990. Do **not**
increment consecutive `11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: covering never-fail stays open. Do **not**
claim the \(q=10\) leftover split for all \(k\) without a new
probe. Do **not** record unique-slot XOR vs \(J\).

Certify: `python3 research/cycle_me.py --certify`.
Dump: `research/cycle_me.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/MD (covering \(q=10\) for \(k\le 8\); prefix MD for
rest10 and the \(q=6\) kills; no Fermat table, no extra window,
no \(n_0=16\) window).

## Lemma (\(q=10\) unique-rest XOR vanishes on \(k\le 8\))

Certified unique rest slots (Cycles LC–LU) XOR to \(0\) on
covering \(q=10\). Rest therefore equals leftover AND xor, and
equals \(\mathrm{want}_{\mathrm{rest}10}\).

## Lemma (rest10 census on \(k\le 10\))

Cycle MD.

## Killed

Unique-rest xor \(=0\) on \(q=6\): \(k=2\), \(q=6\) is \(1\).
Leftover xor equals rest on \(q=6\): same cell leftover \(=1\),
rest \(=0\). Unique-rest xor equals \(J\) on \(q=10\): \(k=0\),
\(q=10\) has unique \(=0\) and \(J=1\).

## Verdict

`LEMMA` (\(q=10\) unique-rest XOR vanishes on \(k\le 8\); rest10
census on \(k\le 10\); \(q=6\) rest \(=0\) at \(k=10\);
\(\mathrm{want}_{\mathrm{forced}}\) at \(k=8,9,10\); rest8 on
\(k\le 9\); \(J\) closed form on \(k\le 6\)).
`KILLED` (\(q=6\) unique xor \(=0\); leftover equals rest on
\(q=6\); unique-rest xor equals \(J\); unique-rest XOR always
\(0\); leftover equals rest on both \(q\); rest8 for all \(k\);
LZ form for all \(k\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_me.md` (this note)
- `research/cycle_me.py`
- `research/cycle_me.json`
