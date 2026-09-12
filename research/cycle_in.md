# Cycle IN: \(n\equiv 1\pmod{4}\) has only Green triples; isolated pairs only \(n\equiv 3\)

Even \(n\) has no consecutive ones (Cycle IM), so consecutive \(G=1\)
lives on odd \(n=2m+1\). When \(m\) is even (\(n\equiv 1\pmod{4}\)),
\(G(m)\) has no \(11\), and every \(G=1\) lifts to a run-3: there are
**no** isolated pairs and **no** isolated ones. Isolated pairs occur
**only** for \(n\equiv 3\pmod{4}\). \(n\equiv 1\) **does** have ones
(all in triples). \(n\equiv 3\) **does** have run-3. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: the \(\bmod 4\) split still leaves packed AND on
odd-\(n\) Green pairs and triples, so covering never-fail stays open.

Helper: `g_run_kind`. Certify:
`python3 research/cycle_in.py --certify` (~0.13s).
Dump: `research/cycle_in.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HU/IM (\(n<64\); covering \(k\le 6\); no Fermat
table, no extra window, no \(n_0=16\) window).

## Lemma (\(n\equiv 1\pmod{4}\) has only Green triples)

For \(n<64\) with \(n\equiv 1\pmod{4}\), ones-runs of \(G(n,\cdot)\)
are length \(3\) only: run-1 \(0\), run-2 \(0\), run-3 \(128\).
Consecutive \(G=1\) pairs \(256\) are all left/right of a triple
(\(128\) each), never isolated.

## Lemma (isolated Green pairs occur only for \(n\equiv 3\pmod{4}\))

For \(n<64\), every isolated pair is \(n\equiv 3\pmod{4}\): run-2
\(230\), all residue \(3\). Residue \(3\) also has run-1 \(45\) and
run-3 \(13\). Even residues have no consecutive ones.

## Lemma (covering \(G=1\) pairs split by \(n\bmod 4\))

Packed covering \(J_6,J_{10}\) for \(k\le 6\): consecutive \(G=1\)
\(8577\) split as \(n\equiv 1\) \(4294\) (left \(2147\), right
\(2147\), isolated \(0\)) and \(n\equiv 3\) \(4283\) (isolated
\(3817\), left \(233\), right \(233\)). Odd-\(s\) \(J\) XOR matches
Cycles HF/HG.

## Killed

\(n\equiv 1\pmod{4}\) has an isolated Green pair: at \(k=0\),
\(s=3\), \(n=1\), \(G(1)=(1,1,1)\), `g_run_kind` is left not iso,
\(p=6\). \(n\equiv 3\pmod{4}\) has no run-3: at \(k=1\), \(s=5\),
\(n=7\), \(j=6\), \(G=(1,1,1)\), \(p=8\). \(n\equiv 1\pmod{4}\) has
no Green ones: at \(k=0\), \(s=3\), \(n=1\), \(j=0\), \(G(1,0)=1\),
\(p=6\).

## Verdict

`LEMMA` (\(n\equiv 1\pmod{4}\) has only Green triples; isolated Green
pairs occur only for \(n\equiv 3\pmod{4}\); covering \(G=1\) pairs
split by \(n\bmod 4\)).
`KILLED` (\(n\equiv 1\) has an isolated Green pair; \(n\equiv 3\) has
no run-3; \(n\equiv 1\) has no Green ones).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_in.md` (this note)
- `research/cycle_in.py`
- `research/cycle_in.json`
