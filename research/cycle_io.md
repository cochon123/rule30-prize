# Cycle IO: even-\(m\) ones lift to triples; isolated pairs come from half \(11\)

Freshman on \(n=2m+1\) sends an isolated \(G(m,k)=1\) to a run-3 at
\(2k\). Even \(m\) has no \(11\), so every even-\(m\) one lifts to
the 5-window \((0,1,1,1,0)\) on \(n\), which is why
\(n\equiv 1\pmod{4}\) has only triples. Isolated pairs on \(n\)
require consecutive ones on \(m=n//2\), so they occur only when \(m\)
is odd (\(n\equiv 3\pmod{4}\)). Even-\(m\) ones do **not** lift to
isolated pairs. Odd-\(m\) ones **can** lift to triples. Isolated
pairs **are** from half \(11\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: the half-index lift still leaves packed AND on
odd-\(n\) Green pairs and triples, so covering never-fail stays open.

Helper: `even_one_neigh`, `iso_from_half11`. Certify:
`python3 research/cycle_io.py --certify` (~0.13s).
Dump: `research/cycle_io.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IN (\(n<64\); covering \(k\le 6\); no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (even-\(m\) ones lift to triples)

For even \(m<32\), every \(G(m,k)=1\) has
`even_one_neigh(m,k)==(0,1,1,1,0)` on \(n=2m+1\). Census
\(n_{\mathrm{lift}}=128\). Every run-3 for \(n<64\),
\(n\equiv 1\pmod{4}\), starts at even \(j=2k\) with \(G(m,k)=1\).
Census \(n_{\mathrm{run3,n1}}=128\).

## Lemma (isolated pairs come from half \(11\))

For \(n<64\), \(n\equiv 3\pmod{4}\), every isolated pair at \(j\)
has consecutive ones on \(m=n//2\) at the half-index
(`iso_from_half11`). Census \(n_{\mathrm{iso}}=230\).

## Lemma (covering clocks half-lift)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): unique-clock run-3 on
\(n\equiv 1\) \(2547\), all even-\(m\) lifts; unique-clock isolated
pairs \(4550\), all from half \(11\). In-support consecutive \(G=1\)
\(8577\) with \(n\equiv 1\) \(4294\) and isolated \(n\equiv 3\)
\(3817\). Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

Even-\(m\) \(1\) lifts to an isolated pair: at \(k=0\), \(s=3\),
\(n=1\), \(m=0\), 5-window \(01110\), `g_run_kind` left, \(p=6\).
Isolated pair is not from half \(11\): at \(k=0\), \(s=3\), \(n=3\),
\(j=0\), half \(G(1)=111\), \(p=10\). Odd-\(m\) \(1\) never lifts to
a triple: at \(k=1\), \(s=5\), \(n=7\), \(m=3\), \(G(3,3)=1\) lifts
to \(111\) at \(j=6\), \(p=8\).

## Verdict

`LEMMA` (even-\(m\) ones lift to triples; isolated pairs come from
half \(11\); covering clocks half-lift).
`KILLED` (even-\(m\) \(1\) lifts to an isolated pair; isolated pair
is not from half \(11\); odd-\(m\) \(1\) never lifts to a triple).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_io.md` (this note)
- `research/cycle_io.py`
- `research/cycle_io.json`
