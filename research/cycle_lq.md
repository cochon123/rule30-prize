# Cycle LQ: covering AND at \(p=88\) on \(G=1\) is \(0100\) for \(k\ge 6\)

On covering \(J_6,J_{10}\) for \(k\le 6\), packed AND at \(p=88\) with
\(G=1\) is only FRESH \(0100\) when \(k\ge 6\). The count is \(9\) vs
\(19\), hence even, so the \(p=88\) \(0100\) XOR is \(0\). This is
**not** \(0100\) for all \(k\), **not** xor \(1\) for \(k\ge 6\),
**not** the \(p=6\) count, and **not** empty for \(k<6\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: this is packed AND at \(p=88\), not a Green-only
formula for packed AND XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_lq.py --certify`.
Dump: `research/cycle_lq.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HG/HH/HI/HU/KH/LD (covering \(k\le 6\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (\(p=88\) AND is \(0100\) for \(k\ge 6\))

Certified \(k\le 6\) (\(28\) events at \(k\ge 6\)). XOR is \(0\).
Covering \(J_6,J_{10}\) still have \(G=1\) columns \(22659\);
odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Lemma (\(p=72\) AND is \(1001\) for \(k\ge 4\))

Cycle LP. Packed AND at \(p=72\) on \(G=1\) is \(1001\) for
\(k\ge 4\).

## Lemma (\(p=6\) AND is \(0100\))

Cycle LD. Packed AND at \(p=6\) on \(G=1\) is always \(0100\).

## Killed

\(0100\) for all \(k\): \(k=4\), \(q=6\) is \(0010\). Xor \(1\) for
\(k\ge 6\): count \(9\), xor \(0\). Equal to the \(p=6\) count:
\(k=6\), \(q=6\) is \(9\) vs \(5\). Empty for \(k<6\): \(k=5\),
\(q=6\) has events.

## Verdict

`LEMMA` (\(p=88\) AND is \(0100\) for \(k\ge 6\); \(p=72\) AND is
\(1001\) for \(k\ge 4\); \(p=42\) AND is \(0011\) for \(k\ge 4\);
\(p=6\) AND is \(0100\); \(p=4\) AND is \(1001\) with odd count;
\(1001\) AND xor remainder).
`KILLED` (\(0100\) for all \(k\); xor \(1\) for \(k\ge 6\); equal to
the \(p=6\) count; empty for \(k<6\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_lq.md` (this note)
- `research/cycle_lq.py`
- `research/cycle_lq.json`
