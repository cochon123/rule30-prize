# Cycle KE: each FRESH pattern on \(G=1\) hits all four \(\mathrm{g1\_green4}\) shapes

Packed AND's shared FRESH terms \(0010\), \(0100\), \(1001\) each
occur on isolated ones, all three pair kinds, centers, and both
\(n\)-parities. FRESH is **not** only on \(G=0\). It is **not** only
isolated. It is **not** a function of \(\mathrm{green4}\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: every live packed-AND pattern is still
unconstrained by Green type, so covering never-fail stays open.

Certify: `python3 research/cycle_ke.py --certify` (~0.16s).
Dump: `research/cycle_ke.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HI/HJ/HU/IG/IN/IR/KB/KD (\(n<64\); covering
\(k\le 6\); no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (\(G=1\) \(\mathrm{green4}\) has four shapes)

For \(n<64\), every \(G=1\) column has
\(\mathrm{green4}=\mathrm{g1\_green4}\) in
\(\{0110,0111,1010,1011\}\). Isolated ones are exactly \(0111\)
(\(461\), including seed). (Cycle KB.)

## Lemma (each covering \(G=1\) FRESH pattern hits all four shapes)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): \(G=1\) FRESH is
\(3376\); also \(12670\) on \(G=0\). Per pattern:

- \(0010\): \(1014\) ( \(G=0\) \(3828\); \(0111\) \(354\), \(1011\)
  \(290\), \(0110\) \(253\), \(1010\) \(117\); left \(123\), right
  \(117\), iso \(167\); isolated \(354\); centers \(85\))
- \(0100\): \(1280\) ( \(G=0\) \(4335\); \(0111\) \(385\), \(1011\)
  \(341\), \(0110\) \(361\), \(1010\) \(193\); left \(127\), right
  \(193\), iso \(214\); isolated \(385\); centers \(68\))
- \(1001\): \(1082\) ( \(G=0\) \(4507\); \(0111\) \(407\), \(1011\)
  \(258\), \(0110\) \(344\), \(1010\) \(73\); left \(92\), right
  \(73\), iso \(166\); isolated \(407\); centers \(26\))

Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

FRESH only on \(G=0\): at \(k=0\), \(s=7\), \(n=1\), \(j=0\), packed
\(0010\), \(\mathrm{green4}\) \(1011\), \(p=10\). FRESH only
isolated: the same witness is left of a pair. FRESH is a function
of \(\mathrm{green4}\): at \(k=2\), \(s=39\), \(n=0\), \(j=0\),
isolated packed \(0010\) vs \(\mathrm{green4}\) \(0111\), \(p=40\).

## Verdict

`LEMMA` (\(G=1\) \(\mathrm{green4}\) has four shapes; each covering
\(G=1\) FRESH pattern hits all four shapes).
`KILLED` (FRESH only on \(G=0\); FRESH only isolated; FRESH is a
function of \(\mathrm{green4}\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ke.md` (this note)
- `research/cycle_ke.py`
- `research/cycle_ke.json`
