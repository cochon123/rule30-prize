# Cycle LW: covering \(G=1\) at \(p=6\) always has packed AND

On covering \(J_6,J_{10}\) for \(k\le 6\), every Green one at packed
\(p=6\) has packed AND: there are no silent \(G=1\) columns. The
\(G=1\) count equals Cycle LD's AND count, so the \(p=6\)
contribution to \(J\) is the Green-ones XOR at \(p=6\): \(0\) at
\(k=0\), else \(1\). This is **not** AND iff \(G=1\), **not**
silent-free at \(p=14\), **not** equal to \(J\), and **not** the
\(p=4\) count. Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: the \(p=6\) slot contribution is Green-forced,
but the rest of packed AND XOR \(J\) still reads the packed row, so
covering never-fail stays open.

Certify: `python3 research/cycle_lw.py --certify` (~0.22s).
Dump: `research/cycle_lw.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HG/HH/HU/KH/LC/LD (covering \(k\le 6\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (\(G=1\) at \(p=6\) always has packed AND)

Certified \(k\le 6\) (\(46\) Green ones, \(0\) silent). XOR is
\(0\) at \(k=0\), else \(1\). Covering \(J_6,J_{10}\) still have
\(G=1\) columns \(22659\); odd-\(s\) \(J\) XOR matches Cycles
HF/HG.

## Lemma (\(G=1\) at \(p=4\) always has packed AND)

Cycle LV. Every Green one at packed \(p=4\) has packed AND.

## Lemma (\(p=6\) AND is \(0100\))

Cycle LD. Packed AND at \(p=6\) on \(G=1\) is always \(0100\).

## Killed

AND iff \(G=1\) at \(p=6\): \(k=0\), \(q=10\) has AND on \(G=0\).
Silent-free at \(p=14\): \(k=1\), \(q=10\) has a silent column.
Equal to \(J\): \(k=1\), \(q=6\) has slot XOR \(1\) and \(J=0\).
Equal to the \(p=4\) count: \(k=0\), \(q=6\) is \(2\) vs \(1\).

## Verdict

`LEMMA` (\(G=1\) at \(p=6\) always has packed AND; \(G=1\) at
\(p=4\) always has packed AND; \(p=6\) AND is \(0100\); \(p=4\) AND
is \(1001\) with odd count; \(1001\) AND xor remainder).
`KILLED` (AND iff \(G=1\) at \(p=6\); silent-free at \(p=14\); equal
to \(J\); equal to the \(p=4\) count).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_lw.md` (this note)
- `research/cycle_lw.py`
- `research/cycle_lw.json`
