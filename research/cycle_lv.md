# Cycle LV: covering \(G=1\) at \(p=4\) always has packed AND

On covering \(J_6,J_{10}\) for \(k\le 6\), every Green one at packed
\(p=4\) has packed AND: there are no silent \(G=1\) columns. The
\(G=1\) count equals Cycle LC's AND count, so the \(p=4\)
contribution to \(J\) is the Green-ones XOR at \(p=4\), which is
\(1\). This is **not** AND iff \(G=1\), **not** silent-free at
\(p=14\), **not** silent-free at every unique \(p\), and **not** a
Green-only formula for \(J\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: the \(p=4\) slot contribution is Green-forced,
but the rest of packed AND XOR \(J\) still reads the packed row, so
covering never-fail stays open.

Certify: `python3 research/cycle_lv.py --certify`.
Dump: `research/cycle_lv.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HG/HH/HU/KH/LB/LC (covering \(k\le 6\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (\(G=1\) at \(p=4\) always has packed AND)

Certified \(k\le 6\) (\(56\) Green ones, \(0\) silent). XOR is
\(1\). Covering \(J_6,J_{10}\) still have \(G=1\) columns \(22659\);
odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Lemma (\(p=4\) AND is \(1001\) with odd count)

Cycle LC. Packed AND at \(p=4\) on \(G=1\) is always \(1001\).

## Lemma (\(p=114\) AND is \(0100\) for \(k\ge 6\))

Cycle LU. Packed AND at \(p=114\) on \(G=1\) is \(0100\) for
\(k\ge 6\).

## Killed

AND iff \(G=1\) at \(p=4\): \(k=0\), \(q=10\) has AND on \(G=0\).
Silent-free at \(p=14\): \(k=1\), \(q=10\) has a silent column.
Equal to \(J\): \(k=1\), \(q=6\) has slot XOR \(1\) and \(J=0\).
Silent-free at every unique \(p\): \(p=14\) is not.

## Verdict

`LEMMA` (\(G=1\) at \(p=4\) always has packed AND; \(p=4\) AND is
\(1001\) with odd count; \(p=114\) AND is \(0100\) for \(k\ge 6\);
\(1001\) AND xor remainder).
`KILLED` (AND iff \(G=1\) at \(p=4\); silent-free at \(p=14\); equal
to \(J\); silent-free at every unique \(p\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_lv.md` (this note)
- `research/cycle_lv.py`
- `research/cycle_lv.json`
