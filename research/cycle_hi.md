# Cycle HI: odd-\(s\) AND splits into \(0011\) continuation and three fresh patterns

On covering \((n,j)\), odd-\(s\) AND is the even-\(s\) 4-tuple at
\(p=T-2j\). It equals even-\(s\) AND at the same \(p\) iff the tuple
is \(0011\) (continuation); otherwise it is a fresh \(0010\),
\(0100\), or \(1001\). Odd-\(s\) AND is **not** even-\(s\) AND.
Even-\(s\) AND live does **not** imply odd-\(s\) AND (tuple \(0111\)).
The \(0011\)-slice XOR is **not** odd-\(s\) \(J_6\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: splitting AND into continuation versus fresh does
not give a closed form along Green ones, so covering never-fail stays
open.

Helper: `FRESH` / `CONT` / `and_from_tuple` from Cycle HH. Certify:
`python3 research/cycle_hi.py --certify` (~0.08s). Dump:
`research/cycle_hi.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/GU/HF/HG/HH (packed \(J_6,J_{10}\)
\(k\le 6\); no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (odd-\(s\) AND \(=\) even-\(s\) 4-tuple; continuation iff \(0011\))

Certified \(k\le 6\). Fresh iff \(\{0010,0100,1001\}\). Disjoint from
continuation. Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Odd-\(s\) AND \(=\) even-\(s\) AND: at \(k=0\), \(J_6\), three fresh
and no continuation. Even-\(s\) AND implies odd-\(s\) AND: at \(k=2\),
\(s=9\), \(n=7\), \(j=7\), tuple \(0111\). \(0011\) XOR \(=\) odd-\(s\)
\(J_6\): at \(k=0\), \(0\neq 1\).

## Verdict

`LEMMA` (4-tuple lift on \((n,j)\); continuation iff \(0011\); fresh
iff \(0010/0100/1001\)).
`KILLED` (odd-\(s\) AND \(=\) even-\(s\) AND; even-\(s\) AND \(\Rightarrow\)
odd-\(s\) AND; \(0011\) XOR \(=J_6^{\mathrm{odd}}\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_hi.md` (this note)
- `research/cycle_hi.py`
- `research/cycle_hi.json`
