# Cycle GH: exactly one in-cone cone-hi hit (\(s=W+1\)); pre-cone has \(Q-1\)

Cycle GG’s \(Q\) hits \(s=t_0+1+q\cdot 2U\) end at \(W+1\). Only that
last time is in-cone (\(s\ge W+1\)); the other \(Q-1\) are pre-cone
(\(r_*\) not yet in the cone, but cone-hi AND still live). In-cone
cone-hi XOR is 1; pre-cone XOR is \((Q-1)\bmod 2\). Not all \(Q\) hits
are in-cone, and in-cone XOR is **not** 0. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push the
even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\) past
414990. Do **not** increment consecutive `11` to \(n_8\). Do **not**
walk \(32U\).

Not a prize claim: splitting the cone-hi edge by the cone cutoff does
not prove covering never-fail (other band indices still contribute).

Helper: `python3 research/cycle_gh.py --certify` (~0.01s). Dump:
`research/cycle_gh.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/GB/GF/GG (times \(k\le 11\); packed
\(k\le 6\); no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (exactly one in-cone hit \(s=W+1\))

Certified \(k\le 11\), \(W\in\{4U,8U,16U\}\).

## Lemma (pre-cone has \(Q-1\) hits; XOR split)

First pre-cone hit is \(t_0+1\) when \(Q>1\). In-cone XOR \(=1\);
pre-cone XOR \(=(Q-1)\bmod 2\). Packed \(k\le 6\).

## Killed

All \(Q\) hits in-cone: at \(k=2\), \(W=8U\), \(t_0+1<W+1\). No
pre-cone hits: \(W=8U\) has \(Q-1=1\). In-cone XOR \(=0\): it is 1.

## Verdict

`LEMMA` (one in-cone hit \(s=W+1\); \(Q-1\) pre-cone; in-cone XOR 1).
`KILLED` (all in-cone; no pre-cone; in-cone XOR 0).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_gh.md` (this note)
- `research/cycle_gh.py`
- `research/cycle_gh.json`
