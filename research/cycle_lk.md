# Cycle LK: covering AND at \(p=30\) on \(G=1\) is \(0011\) for \(k\ge 5\)

On covering \(J_6,J_{10}\) for \(k\le 6\), packed AND at \(p=30\) with
\(G=1\) is only CONT \(0011\) when \(k\ge 5\). The count is \(6\) at
\(k=5\) and \(6\) vs \(10\) at \(k=6\), hence even, so the \(p=30\)
\(0011\) XOR is \(0\). This is **not** \(0011\) for all \(k\), **not**
xor \(1\) for \(k\ge 5\), **not** the \(p=14\) count, and **not**
empty for \(k<6\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: this is packed AND at \(p=30\), not a Green-only
formula for packed AND XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_lk.py --certify` (~0.22s).
Dump: `research/cycle_lk.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HG/HH/HI/HU/KH/LF (covering \(k\le 6\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (\(p=30\) AND is \(0011\) for \(k\ge 5\))

Certified \(k\le 6\) (\(28\) events at \(k\ge 5\)). XOR is \(0\).
Covering \(J_6,J_{10}\) still have \(G=1\) columns \(22659\);
odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Lemma (\(p=98\) AND is \(0010\))

Cycle LJ. Packed AND at \(p=98\) on \(G=1\) is always \(0010\).

## Lemma (\(p=14\) AND is \(0011\))

Cycle LF. Packed AND at \(p=14\) on \(G=1\) is always \(0011\).

## Killed

\(0011\) for all \(k\): \(k=2\), \(q=10\) is \(0010\). Xor \(1\) for
\(k\ge 5\): count \(6\), xor \(0\). Equal to the \(p=14\) count:
\(k=5\), \(q=6\) is \(6\) vs \(5\). Empty for \(k<6\): \(k=5\),
\(q=6\) has \(6\).

## Verdict

`LEMMA` (\(p=30\) AND is \(0011\) for \(k\ge 5\); \(p=98\) AND is
\(0010\); \(p=106\) AND is \(1001\); \(p=54\) AND is \(0100\);
\(p=16\) AND is \(1001\); \(p=14\) AND is \(0011\); \(p=6\) AND is
\(0100\); \(p=4\) AND is \(1001\) with odd count; \(1001\) AND xor
remainder).
`KILLED` (\(0011\) for all \(k\); xor \(1\) for \(k\ge 5\); equal to
the \(p=14\) count; empty for \(k<6\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_lk.md` (this note)
- `research/cycle_lk.py`
- `research/cycle_lk.json`
