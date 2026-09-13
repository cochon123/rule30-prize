# Cycle MY: on \(q=10\) for \(k\le 8\), leftover palindrome-right odd-\(d\) xor of \(G(n,j+1)\) vanishes

On covering \(J_{10}\) for \(k\le 8\), XOR of \(G(n,j+1)\) on leftover
packed AND (\(G=1\), \(p\) off \(\{4,6,14\}\) and UNIQUE_REST) with
\(j>n\) and \((j-n)\) odd is \(0\). Dual of Cycle MH's leftover
all-cell \(G(j+1)\) even-\(k\) xor: the odd palindrome-right slice
vanishes, so MH even-\(k\) is leftover \(j\le n\) plus even-\(d\)
palindrome-right. This is **not** rest (\(k=2\): xor \(=0\), rest
\(=1\)), **not** empty (\(k=3\): \(n_{\mathrm{odd}}=4\)), **not**
pointwise \(0\) (\(k=3\): \(n_{G(j+1)=1}=2\)), **not** vanish on
\(q=6\) (\(k=7\) xor \(=1\)), **not** MH leftover \(G(j+1)\), **not**
Green-only rest, and **not** the form for all \(k\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\).

Not a prize claim: covering never-fail stays open. Do **not**
claim a Green-only formula for rest. Do **not** record unique-slot
XOR vs \(J\).

Certify: `python3 research/cycle_my.py --certify`.
Dump: `research/cycle_my.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/MH/MX (covering leftover \(q=10\) for \(k\le 8\); prefix
MH leftover \(G(j+1)\) even-\(k\); \(k=7\), \(q=6\) kill; no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (leftover palindrome-right odd-\(d\) xor of \(G(n,j+1)\) vanishes)

Covering \(q=10\), \(k\le 8\). Still filters leftover AND by the
packed row.

## Killed

Leftover odd-\(d\) \(G(j+1)\) xor equals rest: \(k=2\), \(q=10\) is
\(0\) vs \(1\). Empty: \(k=3\) has \(n_{\mathrm{odd}}=4\). Pointwise
\(0\): \(k=3\) has two \(G(j+1)=1\) cells. Vanish on \(q=6\):
\(k=7\) xor \(=1\). Equals MH leftover \(G(j+1)\): \(k=0\) is \(0\)
vs \(1\). Green-only rest: this xor still reads leftover packed
AND and is not rest.

## Verdict

`LEMMA` (leftover palindrome-right odd-\(d\) xor of \(G(n,j+1)\)
vanishes on \(q=10\) for \(k\le 8\); leftover AND xor of
\(G(n,j+1)\) is \(1\) iff \(k\) even on \(q=10\); inner odd-\(d\)
\(G(j-1)\) xor vanishes on both covering \(q\); rest10 census on
\(k\le 10\); \(J\) closed form on \(k\le 6\)).
`KILLED` (leftover odd-\(d\) \(G(j+1)\) equals rest; leftover
odd-\(d\) empty; leftover odd-\(d\) pointwise \(0\); leftover
odd-\(d\) vanishes on \(q=6\); leftover odd-\(d\) equals MH
\(G(j+1)\); Green-only rest; the form for all \(k\); unique-rest
xor equals \(J\); leftover equals rest on both \(q\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_my.md` (this note)
- `research/cycle_my.py`
- `research/cycle_my.json`
