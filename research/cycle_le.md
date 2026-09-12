# Cycle LE: covering AND at \(p=16\) on \(G=1\) is always \(1001\)

On covering \(J_6,J_{10}\) for \(k\le 6\), packed AND at \(p=16\) with
\(G=1\) is only FRESH \(1001\). For \(k\ge 3\) the count equals Cycle
LC's \(p=4\) count, hence odd, so the \(p=16\) \(1001\) XOR is \(1\).
Small \(k\): empty at \(k\le 1\); \(1\) vs \(2\) at \(k=2\). This is
**not** \(0100\) at \(p=16\), **not** xor
\(0\) for \(k\ge 3\), **not** the \(p=4\) count for all \(k\), and
**not** empty for \(k<3\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: this is packed AND at \(p=16\), not a Green-only
formula for packed AND XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_le.py --certify` (~0.21s).
Dump: `research/cycle_le.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HG/HH/HI/HU/KH/LB/LC (covering \(k\le 6\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (\(p=16\) AND is \(1001\))

Certified \(k\le 6\) (\(47\) events). For \(k\ge 3\) the count equals
the \(p=4\) count. Covering \(J_6,J_{10}\) still have \(G=1\) columns
\(22659\); odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Lemma (\(p=6\) AND is \(0100\))

Cycle LD. Packed AND at \(p=6\) on \(G=1\) is always \(0100\).

## Lemma (\(p=4\) AND is \(1001\) with odd count)

Cycle LC. Lowest live packed AND slot is always \(1001\).

## Killed

Other AND at \(p=16\): \(k=3\), \(q=6\) is only \(1001\). Xor \(0\)
for \(k\ge 3\): count \(3\), xor \(1\). Equal to \(p=4\) count for
all \(k\): \(k=0\) is \(0\) vs \(1\). Empty for \(k<3\): \(k=2\),
\(q=6\) has \(1\).

## Verdict

`LEMMA` (\(p=16\) AND is \(1001\); \(p=6\) AND is \(0100\); \(p=4\)
AND is \(1001\) with odd count; \(1001\) AND xor remainder).
`KILLED` (other AND at \(p=16\); xor \(0\) for \(k\ge 3\); equal to
\(p=4\) count for all \(k\); empty for \(k<3\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_le.md` (this note)
- `research/cycle_le.py`
- `research/cycle_le.json`
