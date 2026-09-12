# Cycle HV: covering \(J\) is the \(G=1\) FRESH \(\oplus\) CONT slice

Odd-\(s\) covering \(J\) XORs `and_clause` only on Green ones. That
slice is FRESH plus CONT on \(G=1\), not all AND and not all FRESH.
\(G=1\) AND does **not** force packed copy(\(j\)). Covering \(J\) is
**not** the XOR of all odd-\(s\) AND. Covering \(J\) is **not** the
XOR of all FRESH. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: the \(G=1\) FRESH/CONT XOR is still not AND along
Green ones, so covering never-fail stays open.

Helper: `g1_slice_cover`. Certify: `python3 research/cycle_hv.py --certify`.
Dump: `research/cycle_hv.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HI/HJ/HT/HU (covering \(k\le 6\); no Fermat table,
no extra window, no \(n_0=16\) window).

## Lemma (covering \(J\) equals \(G=1\) FRESH \(\oplus\) CONT)

On packed covering \(J_6,J_{10}\) for \(k\le 6\), odd-\(s\) \(J\) is
the XOR of FRESH and CONT events with \(G(n,j)=1\). Census:
\(n_{G=1}=22659\), cob \(13628\), FRESH \(3376\), CONT \(1146\),
non-cob-AND=0 \(4509\). Odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Killed

\(G=1\) AND implies packed copy(\(j\)): at \(k=0\), \(s=3\), \(n=1\),
\(j=0\), \(p=6\), FRESH \(0100\), packed AND \(=1\), Green copy
\(G(1,0)=1\) but packed \(b=0\). Covering \(J\) equals XOR of all
AND: at \(k=1\), \(q=6\), \(s=5\), \(n=3\), \(j=4\), \(p=4\), FRESH
\(1001\) on \(G=0\). Covering \(J\) equals XOR of all FRESH: the
same \(k=1\), \(q=6\) window.

## Verdict

`LEMMA` (covering \(J\) equals \(G=1\) FRESH \(\oplus\) CONT; \(G=1\)
AND is FRESH or CONT).
`KILLED` (\(G=1\) AND implies packed copy(\(j\)); \(J\) equals XOR of
all AND; \(J\) equals XOR of all FRESH).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_hv.md` (this note)
- `research/cycle_hv.py`
- `research/cycle_hv.json`
