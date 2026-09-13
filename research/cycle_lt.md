# Cycle LT: covering AND at \(p=76\) on \(G=1\) is \(0011\) for \(k\ge 6\)

On covering \(J_6,J_{10}\) for \(k\le 6\), packed AND at \(p=76\) with
\(G=1\) is only CONT \(0011\) when \(k\ge 6\). The count is \(5\) vs
\(11\), hence odd, so the \(p=76\) \(0011\) XOR is \(1\). This is
**not** \(0011\) for all \(k\), **not** xor \(0\) for \(k\ge 6\),
**not** the \(p=14\) count, and **not** empty for \(k<6\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: this is packed AND at \(p=76\), not a Green-only
formula for packed AND XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_lt.py --certify` (~0.22s).
Dump: `research/cycle_lt.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HG/HH/HI/HU/KH/LF (covering \(k\le 6\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (\(p=76\) AND is \(0011\) for \(k\ge 6\))

Certified \(k\le 6\) (\(16\) events at \(k\ge 6\)). XOR is \(1\).
Covering \(J_6,J_{10}\) still have \(G=1\) columns \(22659\);
odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Lemma (\(p=86\) AND is \(0011\) for \(k\ge 6\))

Cycle LS. Packed AND at \(p=86\) on \(G=1\) is \(0011\) for
\(k\ge 6\).

## Lemma (\(p=14\) AND is \(0011\))

Cycle LF. Packed AND at \(p=14\) on \(G=1\) is always \(0011\).

## Killed

\(0011\) for all \(k\): \(k=3\), \(q=10\) is \(1001\). Xor \(0\) for
\(k\ge 6\): count \(5\), xor \(1\). Equal to the \(p=14\) count:
\(k=6\), \(q=6\) is \(5\) vs \(7\). Empty for \(k<6\): \(k=5\),
\(q=6\) has events.

## Verdict

`LEMMA` (\(p=76\) AND is \(0011\) for \(k\ge 6\); \(p=86\) AND is
\(0011\) for \(k\ge 6\); \(p=58\) AND is \(0011\) for \(k\ge 6\);
\(p=14\) AND is \(0011\); \(p=4\) AND is \(1001\) with odd count;
\(1001\) AND xor remainder).
`KILLED` (\(0011\) for all \(k\); xor \(0\) for \(k\ge 6\); equal to
the \(p=14\) count; empty for \(k<6\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_lt.md` (this note)
- `research/cycle_lt.py`
- `research/cycle_lt.json`
