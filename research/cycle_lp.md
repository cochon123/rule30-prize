# Cycle LP: covering AND at \(p=72\) on \(G=1\) is \(1001\) for \(k\ge 4\)

On covering \(J_6,J_{10}\) for \(k\le 6\), packed AND at \(p=72\) with
\(G=1\) is only FRESH \(1001\) when \(k\ge 4\). The count is \(0\) vs
\(2\) at \(k=4\), \(1\) vs \(2\) at \(k=5\), and \(4\) vs \(10\) at
\(k=6\) (\(19\) events). XOR is the count mod \(2\). This is **not**
\(1001\) for all \(k\), **not** xor \(1\) for all \(k\ge 4\), **not**
the \(p=4\) count, and **not** empty for \(k<5\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: this is packed AND at \(p=72\), not a Green-only
formula for packed AND XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_lp.py --certify` (~0.22s).
Dump: `research/cycle_lp.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HG/HH/HI/HU/KH/LB/LC (covering \(k\le 6\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (\(p=72\) AND is \(1001\) for \(k\ge 4\))

Certified \(k\le 6\) (\(19\) events at \(k\ge 4\)). XOR is the count
mod \(2\). Covering \(J_6,J_{10}\) still have \(G=1\) columns
\(22659\); odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Lemma (\(p=42\) AND is \(0011\) for \(k\ge 4\))

Cycle LO. Packed AND at \(p=42\) on \(G=1\) is \(0011\) for
\(k\ge 4\).

## Lemma (\(p=4\) AND is \(1001\))

Cycle LC. Packed AND at \(p=4\) on \(G=1\) is always \(1001\).

## Killed

\(1001\) for all \(k\): \(k=3\), \(q=10\) is \(0011\). Xor \(1\) for
all \(k\ge 4\): \(k=4\), \(q=10\) count \(2\), xor \(0\). Equal to
the \(p=4\) count: \(k=5\), \(q=6\) is \(1\) vs \(5\). Empty for
\(k<5\): \(k=4\), \(q=10\) has \(2\).

## Verdict

`LEMMA` (\(p=72\) AND is \(1001\) for \(k\ge 4\); \(p=42\) AND is
\(0011\) for \(k\ge 4\); \(p=38\) AND is \(0100\) for \(k\ge 5\);
\(p=52\) AND is \(1001\) for \(k\ge 5\); \(p=4\) AND is \(1001\) with
odd count; \(1001\) AND xor remainder).
`KILLED` (\(1001\) for all \(k\); xor \(1\) for all \(k\ge 4\); equal
to the \(p=4\) count; empty for \(k<5\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_lp.md` (this note)
- `research/cycle_lp.py`
- `research/cycle_lp.json`
