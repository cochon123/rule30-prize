# Cycle LG: covering AND at \(p=32\) on \(G=1\) is \(0100\) for \(k\ge 4\)

On covering \(J_6,J_{10}\) for \(k\le 6\), packed AND at \(p=32\) with
\(G=1\) is only FRESH \(0100\) when \(k\ge 4\). For \(k\ge 5\) the
count equals Cycle LD's \(p=6\) count; at \(k=4\) it is \(3\) vs
\(6\) (the \(p=6\) count plus \(1\) on \(q=10\)). This is **not**
\(0100\) for all \(k\), **not** xor \(1\) for all \(k\ge 4\), **not**
the \(p=6\) count, and **not** empty for \(k<5\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: this is packed AND at \(p=32\), not a Green-only
formula for packed AND XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_lg.py --certify`.
Dump: `research/cycle_lg.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HG/HH/HI/HU/KH/LD (covering \(k\le 6\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (\(p=32\) AND is \(0100\) for \(k\ge 4\))

Certified \(k\le 6\) (\(31\) events at \(k\ge 4\)). For \(k\ge 5\) the
count equals the \(p=6\) count. Covering \(J_6,J_{10}\) still have
\(G=1\) columns \(22659\); odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Lemma (\(p=14\) AND is \(0011\))

Cycle LF. Packed AND at \(p=14\) on \(G=1\) is always \(0011\).

## Lemma (\(p=16\) AND is \(1001\))

Cycle LE. Packed AND at \(p=16\) on \(G=1\) is always \(1001\).

## Lemma (\(p=6\) AND is \(0100\))

Cycle LD. Packed AND at \(p=6\) on \(G=1\) is always \(0100\).

## Killed

\(0100\) for all \(k\): \(k=2\), \(q=10\) mixes \(1001\). Xor \(1\)
for all \(k\ge 4\): \(k=4\), \(q=10\) count \(6\), xor \(0\). Equal
to the \(p=6\) count: \(k=4\), \(q=10\) is \(6\) vs \(5\). Empty for
\(k<5\): \(k=4\), \(q=6\) has \(3\).

## Verdict

`LEMMA` (\(p=32\) AND is \(0100\) for \(k\ge 4\); \(p=14\) AND is
\(0011\); \(p=16\) AND is \(1001\); \(p=6\) AND is \(0100\); \(p=4\)
AND is \(1001\) with odd count; \(1001\) AND xor remainder).
`KILLED` (\(0100\) for all \(k\); xor \(1\) for all \(k\ge 4\); equal
to the \(p=6\) count; empty for \(k<5\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_lg.md` (this note)
- `research/cycle_lg.py`
- `research/cycle_lg.json`
