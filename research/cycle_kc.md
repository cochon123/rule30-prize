# Cycle KC: dual of \(G=1\) extra terms takes all 16 packed 4-tuples

DIE \(1111\) and CONT \(0011\) are the packed-vs-trinomial AND extras
(Cycle KA). Covering dual 4-tuples of each hit every 16-row. Dual of
\(1111\) is **not** \(1111\). Dual of CONT is **not** bit-reverse.
Dual AND xor does **not** vanish. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: the HW fold's extra-term duals still read the
packed row, so covering never-fail stays open.

Certify: `python3 research/cycle_kc.py --certify` (~0.12s).
Dump: `research/cycle_kc.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HI/HU/HX/KA/KB (\(n<64\) reverse table; covering
\(k\le 6\); no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (reverse of the extra terms)

On the 16-row, reverse of \(1111\) is \(1111\) and reverse of CONT
\(0011\) is cob \(1100\). Packed AND of \(1111\) is \(0\); packed AND
of CONT is \(1\); packed AND of \(1100\) is \(0\).

## Lemma (covering dual of \(G=1\) \(1111\) hits all 16)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): \(G=1\) DIE \(1111\)
is \(1167\) (centers \(30\)); dual-in-support \(1137\); all \(16\)
dual 4-tuples occur; dual AND xor \(294\). Odd-\(s\) \(J\) XOR
matches Cycles HF/HG.

## Lemma (covering dual of \(G=1\) CONT hits all 16)

\(G=1\) CONT is \(1146\) (centers \(53\)); dual-in-support \(1093\);
all \(16\) dual 4-tuples occur; dual AND xor \(831\).

## Killed

Dual of \(G=1\) \(1111\) is \(1111\): at \(k=2\), \(s=31\), \(n=4\),
\(j=0\), \(j'=8\), packed \(1111\) vs dual \(1010\), \(p=40\),
\(p'=24\). Dual of \(G=1\) CONT is bit-reverse: at \(k=1\), \(s=13\),
\(n=3\), \(j=1\), \(j'=5\), packed \(0011\) vs dual \(0111\) (reverse
is \(1100\)), \(p=18\), \(p'=10\). Dual AND xor of \(G=1\) \(1111\)
vanishes: at \(k=4\), \(s=49\), \(n=23\), \(j=13\), \(j'=33\), packed
\(1111\) vs dual CONT \(0011\), \(p=70\), \(p'=30\).

## Verdict

`LEMMA` (reverse of the extra terms; covering dual of \(G=1\)
\(1111\) hits all \(16\); covering dual of \(G=1\) CONT hits all
\(16\)).
`KILLED` (dual of \(G=1\) \(1111\) is \(1111\); dual of \(G=1\) CONT
is bit-reverse; dual AND xor of \(G=1\) \(1111\) vanishes).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_kc.md` (this note)
- `research/cycle_kc.py`
- `research/cycle_kc.json`
