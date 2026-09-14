# Cycle RE: covering silent xor leftover \(n\bmod 4\) is \((1,1,1,0)\) for every \(k\ge 6\)

Silent xor leftover on a residue is Green xor unique. Cycle QY Green
\(n\bmod 4\) is \((0,1,1,1)\) for \(k\ge 3\) and Cycle RB unique
\(n\bmod 4\) is \((1,0,0,1)\) for \(k\ge 6\), so the xor is
\((1,1,1,0)\). Unique \(n\equiv 2\) tot is \(0\), so silent xor
leftover on \(n\equiv 2\) equals Green \(n\equiv 2\) tot for every
\(k\). This is **not** the tuple \((1,1,1,0)\) for all \(k\)
(\(k=0\) is \((1,0,1,1)\)). **Not** silent equals leftover on all
residues for \(k\ge 6\) (only \(n\equiv 3\) agrees). This is **not**
rest \(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
catalogue leftover \(p\) one-by-one. Do **not** catalogue further
\(S\)/\(T\) subregions unless the experiment answers why \(E_k=0\).
Do **not** claim pal-left leftover xor vanishes for all \(k\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim Green rest \(n\bmod 4\) equals packed rest \(n\bmod 4\).
Do **not** claim silent xor leftover is \((1,1,1,0)\) for all \(k\).
Do **not** claim silent equals leftover on all residues for
\(k\ge 6\). Do **not** claim leftover \(n\bmod 4\) has a small
period. Do **not** claim cellwise 2-fold packed AND. Do **not**
claim even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\).

Certify: `python3 research/cycle_re.py --certify`.
Dump: `research/cycle_re.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/QX/QY/QO/RB/RC/RD (silent xor leftover from Green xor
unique; no Fermat table, no extra window, no \(n_0=16\) window, no
packed covering \(k=11\)).

## Lemma (silent xor leftover \(n\bmod 4\) is \((1,1,1,0)\) for every \(k\ge 6\))

Green xor unique is that tuple. Silent xor leftover on \(n\equiv 2\)
equals Green \(n\equiv 2\) tot for every \(k\). Status: **lemma**.
**Killed:** the tuple \((1,1,1,0)\) for all \(k\). **Killed:** silent
equals leftover on all residues for \(k\ge 6\).

## Verdict

`LEMMA` (silent xor leftover \(n\bmod 4\) is \((1,1,1,0)\) for every
\(k\ge 6\); silent xor leftover on \(n\equiv 2\) equals Green
\(n\equiv 2\) tot; QY Green \(n\bmod 4\); RB unique \(n\bmod 4\); RD
silent \(n\equiv 3\) equals leftover iff unique \(n\equiv 3\)).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (silent xor leftover is \((1,1,1,0)\) for all \(k\); silent
equals leftover on all residues for \(k\ge 6\); Green rest
\(n\bmod 4\) equals packed rest \(n\bmod 4\)).
`PREFIX` (even-\(n\) rest xor at \(k\) equals odd-\(n\) rest xor at
\(k-1\) for all \(k\); packed rest \(=S\oplus T\) for all \(k\);
\(E_k=0\) for all \(k\); leftover after classified columns equals
\(S\oplus T\); \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\);
11-bit gap; formula for extra 414990; at-most-one-odd for all \(k\);
seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_re.md` (this note)
- `research/cycle_re.py`
- `research/cycle_re.json`
