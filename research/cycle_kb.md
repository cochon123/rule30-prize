# Cycle KB: \(G=1\) DIE \(1111\) hits all four \(\mathrm{g1\_green4}\) shapes

Trinomial AND's extra term \(1111\) occurs on isolated ones, all
three pair kinds, centers, and both \(n\)-parities. It is **not**
only on \(G=0\). It is **not** only isolated. It is **not** a
function of \(\mathrm{green4}\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: the linear-AND extra term is still unconstrained
by Green type, so covering never-fail stays open.

Certify: `python3 research/cycle_kb.py --certify` (~0.11s).
Dump: `research/cycle_kb.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HJ/HU/IG/IN/IR/KA (\(n<64\); covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (\(G=1\) \(\mathrm{green4}\) has four shapes)

For \(n<64\), every \(G=1\) column has
\(\mathrm{green4}=\mathrm{g1\_green4}\) in
\(\{0110,0111,1010,1011\}\). Isolated ones are exactly \(0111\)
(\(461\), including seed).

## Lemma (covering \(G=1\) \(1111\) hits all four shapes)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): \(G=1\) DIE \(1111\)
is \(1167\); also \(3614\) on \(G=0\). Split
\(0111\) \(359\), \(1011\) \(361\), \(0110\) \(313\), \(1010\)
\(134\); pair-starts left \(98\), right \(134\), iso \(263\);
isolated \(359\); centers \(30\); even \(n\) \(285\), odd \(n\)
\(882\). Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

\(1111\) only on \(G=0\): at \(k=1\), \(s=17\), \(n=1\), \(j=2\),
packed \(1111\), \(\mathrm{green4}\) \(0110\), \(p=16\). \(1111\)
only isolated: at \(k=3\), \(s=29\), \(n=9\), \(j=16\), left of a
triple, \(\mathrm{green4}\) \(1011\), \(p=16\). \(1111\) is a
function of \(\mathrm{green4}\): at \(k=2\), \(s=31\), \(n=4\),
\(j=0\), isolated packed \(1111\) vs \(\mathrm{green4}\) \(0111\),
\(p=40\).

## Verdict

`LEMMA` (\(G=1\) \(\mathrm{green4}\) has four shapes; covering
\(G=1\) \(1111\) hits all four shapes).
`KILLED` (\(1111\) only on \(G=0\); \(1111\) only isolated; \(1111\)
is a function of \(\mathrm{green4}\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_kb.md` (this note)
- `research/cycle_kb.py`
- `research/cycle_kb.json`
