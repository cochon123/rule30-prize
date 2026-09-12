# Cycle KF: dual of each \(G=1\) FRESH pattern takes all 16 packed 4-tuples

Covering dual 4-tuples of \(0010\), \(0100\), and \(1001\) each hit
every 16-row. Dual of \(0010\) is **not** \(0010\). Dual of \(0010\)
is **not** bit-reverse \(0100\). Dual AND xor does **not** vanish.
Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: the HW fold's FRESH duals still read the packed
row, so covering never-fail stays open.

Certify: `python3 research/cycle_kf.py --certify` (~0.12s).
Dump: `research/cycle_kf.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HI/HU/HX/KE (\(n<64\) reverse table; covering
\(k\le 6\); no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (reverse permutes FRESH)

On the 16-row, reverse sends \(0010\leftrightarrow 0100\) and fixes
palindrome \(1001\). Packed AND of each FRESH pattern is \(1\).

## Lemma (covering dual of each \(G=1\) FRESH hits all 16)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): \(G=1\) FRESH is
\(3376\); dual-in-support \(3197\). Per pattern:

- \(0010\): \(1014\) (centers \(85\)); dual-in-support \(929\); all
  \(16\) dual 4-tuples; dual AND xor \(686\)
- \(0100\): \(1280\) (centers \(68\)); dual-in-support \(1212\); all
  \(16\) dual 4-tuples; dual AND xor \(919\)
- \(1001\): \(1082\) (centers \(26\)); dual-in-support \(1056\); all
  \(16\) dual 4-tuples; dual AND xor \(810\)

Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Dual of \(G=1\) \(0010\) is \(0010\): at \(k=2\), \(s=25\), \(n=7\),
\(j=4\), \(j'=10\), packed \(0010\) vs dual \(0001\), \(p=32\),
\(p'=20\). Dual of \(G=1\) \(0010\) is bit-reverse: the same witness
is not \(0100\). Dual AND xor of \(G=1\) \(0010\) vanishes: the same
witness has dual packed AND \(0\).

## Verdict

`LEMMA` (reverse permutes FRESH; covering dual of each \(G=1\) FRESH
hits all \(16\)).
`KILLED` (dual of \(G=1\) \(0010\) is \(0010\); dual of \(G=1\)
\(0010\) is bit-reverse; dual AND xor of \(G=1\) \(0010\) vanishes).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_kf.md` (this note)
- `research/cycle_kf.py`
- `research/cycle_kf.json`
