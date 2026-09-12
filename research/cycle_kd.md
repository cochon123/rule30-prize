# Cycle KD: \(G=1\) CONT \(0011\) hits all four \(\mathrm{g1\_green4}\) shapes

Packed AND's extra term CONT occurs on isolated ones, all three
pair kinds, centers, and both \(n\)-parities. It is **not** only on
\(G=0\). It is **not** only isolated. It is **not** a function of
\(\mathrm{green4}\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: the packed-AND extra term is still unconstrained
by Green type, so covering never-fail stays open.

Certify: `python3 research/cycle_kd.py --certify` (~0.11s).
Dump: `research/cycle_kd.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HI/HJ/HU/IG/IN/IR/KB/KC (\(n<64\); covering
\(k\le 6\); no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (\(G=1\) \(\mathrm{green4}\) has four shapes)

For \(n<64\), every \(G=1\) column has
\(\mathrm{green4}=\mathrm{g1\_green4}\) in
\(\{0110,0111,1010,1011\}\). Isolated ones are exactly \(0111\)
(\(461\), including seed). (Cycle KB.)

## Lemma (covering \(G=1\) CONT hits all four shapes)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): \(G=1\) CONT \(0011\)
is \(1146\); also \(3829\) on \(G=0\). Split
\(0111\) \(343\), \(1011\) \(288\), \(0110\) \(364\), \(1010\)
\(151\); pair-starts left \(89\), right \(151\), iso \(199\);
isolated \(343\); centers \(53\); even \(n\) \(279\), odd \(n\)
\(867\). Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

CONT only on \(G=0\): at \(k=1\), \(s=13\), \(n=3\), \(j=1\), packed
\(0011\), \(\mathrm{green4}\) \(0110\), \(p=18\). CONT only isolated:
at \(k=3\), \(s=61\), \(n=9\), \(j=8\), left of a triple,
\(\mathrm{green4}\) \(1011\), \(p=64\). CONT is a function of
\(\mathrm{green4}\): at \(k=1\), \(s=13\), \(n=3\), \(j=3\), isolated
packed \(0011\) vs \(\mathrm{green4}\) \(0111\), \(p=14\).

## Verdict

`LEMMA` (\(G=1\) \(\mathrm{green4}\) has four shapes; covering
\(G=1\) CONT hits all four shapes).
`KILLED` (CONT only on \(G=0\); CONT only isolated; CONT is a
function of \(\mathrm{green4}\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_kd.md` (this note)
- `research/cycle_kd.py`
- `research/cycle_kd.json`
