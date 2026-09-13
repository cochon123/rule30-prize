# Cycle QG: covering Green UNIQUE_REST xor tot is \(1\) iff \(k\in\{3,4,5\}\)

Cycle QF closes packed UNIQUE_REST AND xor tot \(=0\) for every
\(k\). The Green \(G=1\) xor on the same sixteen columns is
different: it is \(1\) iff \(k\in\{3,4,5\}\). Each unique packed
\(p\) doubles to a known Green parent. If \(p\equiv 2\pmod{4}\)
then \(j\) is odd, even \(n\) vanish, and odd \(n=2m+1\) map onto
parent \(p'=(p+2)/2\) at scale \(k-1\). If \(p\equiv 0\pmod{4}\)
then even-\(n\) xor of parent \(p/2\) cancels the odd-\(n\)
\(p/2\) piece, so tot is parent \(p/2+2\) at \(k-1\). Live
windows match for \(k\ge 3\). Parents reduce to Cycles
PM/PN/PC/PV/PT/PY/QA/QC/QD/QE (\(p=10,\ldots,30\)), via extras
\(p=40,44,46,50\) whose Green xor is \(1\) iff \(k\ge 5\). Hence
Green xor at every UNIQUE_REST column is \(1\) for \(k\ge 6\)
(sixteen ones, tot \(0\)). Dual of packed tot \(=0\): packed is
\(0\) at \(k=3,4,5\) while Green is \(1\). **Not** rest
\(=S\oplus T\). **Not** \(E_k=0\) for all \(k\). Do **not**
catalogue leftover \(p\) one-by-one. Do **not** catalogue further
\(S\)/\(T\) subregions unless the experiment answers why \(E_k=0\).
Do **not** claim pal-left leftover xor vanishes for all \(k\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not** bump
all \(n_0=16\) past 414990. Do **not** increment consecutive `11`
to \(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\)
covering packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).
Do **not** claim Green unique tot equals packed unique tot.

Certify: `python3 research/cycle_qg.py --certify` (~0.25s).
Dump: `research/cycle_qg.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/MD/PC/PM/PN/PT/PV/PY/QA/QC/QD/QE/QF (Green UNIQUE_REST
xor tot; doubling parents; prefix QF packed unique tot \(=0\); no
Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (Green doubling of packed column xor)

For covering \(q=10\) and \(k\ge 3\): if \(p\equiv 2\pmod{4}\) then
Green xor at \(p\) equals Green xor at \((p+2)/2\) at \(k-1\); if
\(p\equiv 0\pmod{4}\) then Green xor at \(p\) equals Green xor at
\(p/2+2\) at \(k-1\). Live \(m\)-windows match. Status: **lemma**.

## Lemma (UNIQUE_REST Green xor tot \(=1\) iff \(k\in\{3,4,5\}\))

Firing thresholds: \(p=16\) for \(k\ge 3\); \(p=30,32\) for
\(k\ge 4\); \(p=38,42,52,54,58,60\) for \(k\ge 5\); the rest
(\(p=72,76,86,88,98,106,114\)) for \(k\ge 6\). Counts \(1,3,9,16\)
so tot is odd iff \(k\in\{3,4,5\}\). For \(k\ge 6\) every unique
column has Green xor \(=1\). Status: **lemma**. **Killed:** Green
unique tot equals packed unique tot.

## Verdict

`LEMMA` (Green doubling of packed column xor; UNIQUE_REST Green xor
tot \(=1\) iff \(k\in\{3,4,5\}\); every unique column Green xor
\(=1\) for \(k\ge 6\); QF packed unique tot \(=0\)).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (Green unique tot equals packed unique tot; unique-rest
xor tot equals rest).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_qg.md` (this note)
- `research/cycle_qg.py`
- `research/cycle_qg.json`
