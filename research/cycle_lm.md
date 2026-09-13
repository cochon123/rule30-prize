# Cycle LM: covering AND at \(p=52\) on \(G=1\) is \(1001\) for \(k\ge 5\)

On covering \(J_6,J_{10}\) for \(k\le 6\), packed AND at \(p=52\) with
\(G=1\) is only FRESH \(1001\) when \(k\ge 5\). The count is \(4\) vs
\(10\) at \(k=5\) and \(10\) vs \(10\) at \(k=6\), hence even, so the
\(p=52\) \(1001\) XOR is \(0\). This is **not** \(1001\) for all
\(k\), **not** xor \(1\) for \(k\ge 5\), **not** the \(p=4\) count,
and **not** empty for \(k<6\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: this is packed AND at \(p=52\), not a Green-only
formula for packed AND XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_lm.py --certify` (~0.22s).
Dump: `research/cycle_lm.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HG/HH/HI/HU/KH/LB/LC (covering \(k\le 6\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (\(p=52\) AND is \(1001\) for \(k\ge 5\))

Certified \(k\le 6\) (\(34\) events at \(k\ge 5\)). XOR is \(0\).
Covering \(J_6,J_{10}\) still have \(G=1\) columns \(22659\);
odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Lemma (\(p=60\) AND is \(0100\) for \(k\ge 5\))

Cycle LL. Packed AND at \(p=60\) on \(G=1\) is \(0100\) for
\(k\ge 5\).

## Lemma (\(p=4\) AND is \(1001\))

Cycle LC. Packed AND at \(p=4\) on \(G=1\) is always \(1001\).

## Killed

\(1001\) for all \(k\): \(k=3\), \(q=10\) is \(0010\). Xor \(1\) for
\(k\ge 5\): count \(4\), xor \(0\). Equal to the \(p=4\) count:
\(k=5\), \(q=6\) is \(4\) vs \(5\). Empty for \(k<6\): \(k=5\),
\(q=6\) has \(4\).

## Verdict

`LEMMA` (\(p=52\) AND is \(1001\) for \(k\ge 5\); \(p=60\) AND is
\(0100\) for \(k\ge 5\); \(p=30\) AND is \(0011\) for \(k\ge 5\);
\(p=98\) AND is \(0010\); \(p=6\) AND is \(0100\); \(p=4\) AND is
\(1001\) with odd count; \(1001\) AND xor remainder).
`KILLED` (\(1001\) for all \(k\); xor \(1\) for \(k\ge 5\); equal to
the \(p=4\) count; empty for \(k<6\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_lm.md` (this note)
- `research/cycle_lm.py`
- `research/cycle_lm.json`
