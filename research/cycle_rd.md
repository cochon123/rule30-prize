# Cycle RD: covering silent \(n\equiv 3\pmod{4}\) tot equals leftover \(n\equiv 3\pmod{4}\) tot iff \(k=4\) or \(k\ge 6\)

Silent is Green rest xor packed rest. Leftover is packed rest xor
unique. Their xor on a residue is Green xor unique. Cycle QY Green
\(n\equiv 3\) rest is \(1\) for every \(k\), so silent \(n\equiv 3\)
equals leftover \(n\equiv 3\) iff unique \(n\equiv 3\) is \(1\), which
Cycle RB says is \(k=4\) or \(k\ge 6\). This is **not** silent
\(n\equiv 3\) equals leftover \(n\equiv 3\) for all \(k\) (\(k=0\):
silent \(1\), leftover \(0\)). **Not** silent \(n\equiv 3\) equals
\(S\oplus T\) (\(k=7\): silent \(1\), ST \(0\)). This is **not** rest
\(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not** catalogue
leftover \(p\) one-by-one. Do **not** catalogue further \(S\)/\(T\)
subregions unless the experiment answers why \(E_k=0\). Do **not**
claim pal-left leftover xor vanishes for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\). Do **not** walk \(k=11\) covering packed. Do
**not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim Green rest \(n\bmod 4\) equals packed rest \(n\bmod 4\).
Do **not** claim silent \(n\equiv 3\) equals leftover \(n\equiv 3\)
for all \(k\). Do **not** claim silent \(n\equiv 3\) equals \(S\oplus T\).
Do **not** claim leftover \(n\bmod 4\) has a small period. Do **not**
claim cellwise 2-fold packed AND. Do **not** claim even-\(n\) rest
xor at \(k\) equals odd-\(n\) rest xor at \(k-1\) for all \(k\).

Certify: `python3 research/cycle_rd.py --certify`.
Dump: `research/cycle_rd.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/OJ/PB/QO/QX/QY/RB/RC (silent \(n\equiv 3\) from QY Green xor
QO packed rest; leftover from RC; no Fermat table, no extra window,
no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (silent \(n\equiv 3\pmod{4}\) tot equals leftover \(n\equiv 3\) tot iff \(k=4\) or \(k\ge 6\))

Green \(n\equiv 3\) rest is identically \(1\). Silent xor leftover
is Green xor unique, hence \(0\) iff unique \(n\equiv 3\) is \(1\).
Status: **lemma**. **Killed:** silent \(n\equiv 3\) equals leftover
\(n\equiv 3\) for all \(k\). **Killed:** silent \(n\equiv 3\) equals
\(S\oplus T\).

## Verdict

`LEMMA` (silent \(n\equiv 3\pmod{4}\) tot equals leftover \(n\equiv 3\)
tot iff \(k=4\) or \(k\ge 6\); QY Green \(n\equiv 3\) rest \(1\); RB
unique \(n\equiv 3\) tot; RC leftover \(n\bmod 4\)).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (silent \(n\equiv 3\) equals leftover \(n\equiv 3\) for all
\(k\); silent \(n\equiv 3\) equals \(S\oplus T\); Green rest
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

- `research/cycle_rd.md` (this note)
- `research/cycle_rd.py`
- `research/cycle_rd.json`
