# Cycle PG: bit \(10\) freeze; covering \(p=12\) silent for \(k\ge 2\)

Cycle PF froze bits \(7,8,9\). Bit \(10(t+1)=\) bit \(8(t)\oplus 1\)
for \(t\ge 5\), so bit \(10=1\) iff \(t\bmod 4\in\{0,3\}\) for
\(t\ge 6\). On even \(t\ge 8\) the \(p=12\) 4-tuple is then
\(1100\) (\(t\bmod 4=0\)) or \(1011\) (\(t\bmod 4=2\)), never an
AND-one. Cycle PD's bits \(11..14\) period \(4\) still starts at
even \(t\ge 12\). The \(p=12\) 4-tuple is already non-AND on even
\(t\ge 8\).

Covering even \(s\) starts at \(2U\ge 8\) for \(k\ge 2\), hence
covering \(p=12\) is silent. **Not** rest \(=S\oplus T\). **Not**
\(E_k=0\) for all \(k\). Do **not** claim covering \(p=16\) silent
for all \(k\). Do **not** catalogue further \(S\)/\(T\) subregions
unless the experiment answers why \(E_k=0\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).
Do **not** claim packed rest equals \(S\oplus T\) for all \(k\).

Certify: `python3 research/cycle_pg.py --certify`.
Dump: `research/cycle_pg.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/PF/PD/GU/HG/HH/HU (bit \(10\), even-\(t\) \(p=12\)
4-tuple; prefix PF silent \(p=8,10\), PD bits \(11..14\); no
Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (bit \(10\))

Bit \(10=1\) iff \(t\bmod 4\in\{0,3\}\) for \(t\ge 6\). Status:
**lemma**. Checked on \(0\le t\le 64\).

## Lemma (AND at \(p=12\) on even \(t\ge 8\))

Even \(t\ge 8\): the \(p=12\) 4-tuple is \(1100\) or \(1011\),
AND \(=0\). Cycle PD's bits \(11..14\) period \(4\) is used from
\(t\ge 12\). Status: **lemma**.

## Lemma (covering \(p=12\) silent for \(k\ge 2\))

Covering even \(s\) starts at \(2U\ge 8\), so packed AND at
\(p=12\) never fires. Status: **lemma**. Thin packed check on
\(k\le 8\).

## Verdict

`LEMMA` (bit \(10\); AND \(p=12=0\) on even \(t\ge 8\); covering
\(p=12\) silent for \(k\ge 2\); PF bits \(7,8,9\); PD forced xor).
`CERTIFIED` (\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`PREFIX` (packed rest \(=S\oplus T\) for all \(k\); \(E_k=0\) for
all \(k\); covering \(p=16\) silent for all \(k\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_pg.md` (this note)
- `research/cycle_pg.py`
- `research/cycle_pg.json`
