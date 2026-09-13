# Cycle LO: covering AND at \(p=42\) on \(G=1\) is \(0011\) for \(k\ge 4\)

On covering \(J_6,J_{10}\) for \(k\le 6\), packed AND at \(p=42\) with
\(G=1\) is only CONT \(0011\) when \(k\ge 4\). The count is \(1\) vs
\(2\) at \(k=4\), \(3\) vs \(7\) at \(k=5\), and \(7\) vs \(9\) at
\(k=6\). XOR is the count mod \(2\) (0 only at \(k=4\), \(q=10\)).
This is **not** \(0011\) for all \(k\), **not** xor \(1\) for all
\(k\ge 4\), **not** the \(p=14\) count, and **not** empty for
\(k<5\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: this is packed AND at \(p=42\), not a Green-only
formula for packed AND XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_lo.py --certify` (~0.22s).
Dump: `research/cycle_lo.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HG/HH/HI/HU/KH/LF (covering \(k\le 6\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (\(p=42\) AND is \(0011\) for \(k\ge 4\))

Certified \(k\le 6\) (\(29\) events at \(k\ge 4\)). XOR is the count
mod \(2\). Covering \(J_6,J_{10}\) still have \(G=1\) columns
\(22659\); odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Lemma (\(p=38\) AND is \(0100\) for \(k\ge 5\))

Cycle LN. Packed AND at \(p=38\) on \(G=1\) is \(0100\) for
\(k\ge 5\).

## Lemma (\(p=14\) AND is \(0011\))

Cycle LF. Packed AND at \(p=14\) on \(G=1\) is always \(0011\).

## Killed

\(0011\) for all \(k\): \(k=3\), \(q=6\) is \(1001\). Xor \(1\) for
all \(k\ge 4\): \(k=4\), \(q=10\) count \(2\), xor \(0\). Equal to
the \(p=14\) count: \(k=4\), \(q=6\) is \(1\) vs \(5\). Empty for
\(k<5\): \(k=4\), \(q=6\) has \(1\).

## Verdict

`LEMMA` (\(p=42\) AND is \(0011\) for \(k\ge 4\); \(p=38\) AND is
\(0100\) for \(k\ge 5\); \(p=52\) AND is \(1001\) for \(k\ge 5\);
\(p=14\) AND is \(0011\); \(p=4\) AND is \(1001\) with odd count;
\(1001\) AND xor remainder).
`KILLED` (\(0011\) for all \(k\); xor \(1\) for all \(k\ge 4\); equal
to the \(p=14\) count; empty for \(k<5\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_lo.md` (this note)
- `research/cycle_lo.py`
- `research/cycle_lo.json`
