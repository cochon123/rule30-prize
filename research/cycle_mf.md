# Cycle MF: unique-rest XOR vanishes at \(k=9\) for both covering \(q\)

On covering \(J_6,J_{10}\) at \(k=9\), XOR of the LC–LU unique
packed AND slots off \(\{p=4,p=6,p=14\}\) is \(0\), so leftover
XOR equals rest \(=0\). Cycle ME therefore holds at \(k=9\) on
\(q=10\); \(q=6\) unique xor is also \(0\) (unlike \(k=2\),
\(q=6\)). This is **not** ME for all \(k\), **not** unique \(=0\)
on all \(q=6\), **not** unique xor vs \(J\), and **not** leftover
equals rest on \(q=6\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: covering never-fail stays open. Do **not**
claim the leftover split for all \(k\) without a new probe. Do
**not** record unique-slot XOR vs \(J\). Do **not** walk \(k=10\)
split here.

Certify: `python3 research/cycle_mf.py --certify` (~6.57s).
Dump: `research/cycle_mf.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/MD (k=9 covering split walks; prefix ME for \(q=10\)
\(k\le 8\) and MB for \(k=9\) \(J\); no Fermat table, no extra
window, no \(n_0=16\) window).

## Lemma (unique-rest XOR vanishes at \(k=9\))

Both covering \(q\). Leftover XOR equals rest \(=0\). Cycle ME's
\(q=10\) leftover split holds at \(k=9\).

## Lemma (\(q=10\) unique-rest XOR vanishes on \(k\le 8\))

Cycle ME.

## Killed

ME dies at \(k=9\), \(q=10\): unique xor is \(0\). \(q=6\) unique
xor always \(1\): \(k=9\), \(q=6\) is \(0\). Unique-rest xor
equals \(J\) at \(k=9\): unique \(=0\) and \(J=1\).

## Verdict

`LEMMA` (unique-rest XOR vanishes at \(k=9\); \(q=10\) leftover
split on \(k\le 8\); rest10 census on \(k\le 10\); LZ form with
rest8 at \(k=9\); \(J\) closed form on \(k\le 6\)).
`KILLED` (ME dies at \(k=9\); \(q=6\) unique xor always \(1\);
unique-rest xor equals \(J\); unique-rest XOR always \(0\);
leftover equals rest on both \(q\); rest8 for all \(k\); LZ form
for all \(k\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_mf.md` (this note)
- `research/cycle_mf.py`
- `research/cycle_mf.json`
