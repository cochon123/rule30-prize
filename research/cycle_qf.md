# Cycle QF: covering UNIQUE_REST packed AND xor tot is \(0\) for every \(k\)

Cycles PH–QE close packed AND xor on every column of Cycle MD's
UNIQUE_REST set
\(\{16,30,32,38,42,52,54,58,60,72,76,86,88,98,106,114\}\).
The sixteen formulas xor to \(0\) for every \(k\). The case split
is finite: the formulas stabilize for \(k\ge 7\), where ten
columns fire. Unique tot \(=0\) lifts Cycles ME/MF/MG (unique-rest
xor vanishes through \(k\le 10\)) to all \(k\), so leftover xor
equals rest on covering \(q=10\) for every \(k\). This is **not**
leftover after classified leftover columns
(\(p=34,40,62,64,70\)) equals rest: unclassified leftover still
fires. **Not** unique-rest xor tot equals rest (tot is \(0\);
rest is not). **Not** rest \(=S\oplus T\). **Not** \(E_k=0\) for
all \(k\). Do **not** catalogue leftover \(p\) one-by-one. Do
**not** catalogue further \(S\)/\(T\) subregions unless the
experiment answers why \(E_k=0\). Do **not** claim pal-left
leftover xor vanishes for all \(k\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).

Certify: `python3 research/cycle_qf.py --certify`.
Dump: `research/cycle_qf.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/MD/PB/PH/PK/PM/PN/PR/PS/PV/PW/PX/PY/PZ/QA/QB/QC/QD/QE
(sixteen UNIQUE_REST packed xor formulas; prefix QE \(p=114\) xor,
MG unique tot through \(k\le 10\), MD rest10; no Fermat table, no
extra window, no \(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (UNIQUE_REST packed xor tot \(=0\) for every \(k\))

Firing UNIQUE_REST columns:

| \(k\) | fire | tot |
|---|---|---|
| \(0,1\) | none | \(0\) |
| \(2\) | \(30,38\) | \(0\) |
| \(3\) | \(16,32,38,42,52,58,72,76\) | \(0\) |
| \(4\) | \(16,54,58,60,88,114\) | \(0\) |
| \(5\) | \(16,32,42,54,76,86,106,114\) | \(0\) |
| \(6\) | \(16,32,42,54,58,76,88,98\) | \(0\) |
| \(\ge 7\) | \(16,32,42,54,58,76,88,98,106,114\) | \(0\) |

`want_p32_pack` is \(k\ge 3\) and \(k\ne 4\) (fires at \(k=3\)).
Checked on \(0\le k\le 64\). Status: **lemma**. **Killed:**
unique-rest xor tot equals rest; unique-rest xor tot equals
\(S\oplus T\).

## Lemma (leftover xor equals rest on covering \(q=10\), all \(k\))

Packed rest is unique xor leftover by partitioning AND columns
off \(\{4,6,14\}\). Unique tot \(=0\) therefore leftover tot
equals rest for every \(k\). On \(k\le 10\) that rest is
\(\mathrm{want}_{\mathrm{rest}10}\). Status: **lemma**.
**Killed:** leftover after classified leftover columns equals
rest.

## Verdict

`LEMMA` (UNIQUE_REST packed xor tot \(=0\) for every \(k\);
leftover xor equals rest on covering \(q=10\), all \(k\);
leftover equals rest10 on \(k\le 10\); QE \(p=114\) xor).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (unique-rest xor tot equals rest; leftover after
classified leftover columns equals rest).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); leftover after classified columns equals \(S\oplus T\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_qf.md` (this note)
- `research/cycle_qf.py`
- `research/cycle_qf.json`
