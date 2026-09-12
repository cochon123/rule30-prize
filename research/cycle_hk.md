# Cycle HK: even-\(s\) AND without odd-\(s\) AND splits into three die patterns

On covering \((n,j)\), die (even-\(s\) AND live, odd-\(s\) AND dead)
iff the even-\(s\) 4-tuple is \(0111\), \(1011\), or \(1111\). Dual
of Cycle HI fresh. Die is **not** only \(0111\). Die is **not** only
on \(G(n,j)=1\). Even-\(s\) AND is **not** iff \(0011\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: classifying die 4-tuples does not give a closed
form along Green ones, so covering never-fail stays open.

Helper: `DIE` / `DIE_SLOT` / `slot_mask` from Cycle HJ. Certify:
`python3 research/cycle_hk.py --certify`. Dump:
`research/cycle_hk.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/GU/HF/HG/HH/HI/HJ (covering \(k\le 6\);
no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (die iff \(\{0111,1011,1111\}\))

Certified \(J_6,J_{10}\), \(k\le 6\). Counts match Cycle HI.
\(0111\) occupies cob(\(j+1\))+copy(\(j\))+cob(\(j\)); \(1011\)
occupies copy(\(j+1\))+copy(\(j\))+cob(\(j\)); \(1111\) occupies all
four slots. Disjoint from fresh and continuation. Odd-\(s\) \(J\) XOR
matches Cycles HF/HG.

## Killed

Die only \(0111\): at \(k=1\), \(s=11\), \(n=0\), \(j=0\), \(p=12\),
tuple \(1011\). Die only on \(G=1\): at \(k=2\), \(s=11\), \(n=6\),
\(j=5\), \(p=14\), tuple \(1111\), \(G=0\). Even-\(s\) AND iff
\(0011\): the same \(1011\) has even AND live.

## Verdict

`LEMMA` (die iff \(0111/1011/1111\); occupation of the three die
patterns).
`KILLED` (die only \(0111\); die only on \(G=1\); even-\(s\) AND iff
\(0011\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_hk.md` (this note)
- `research/cycle_hk.py`
- `research/cycle_hk.json`
