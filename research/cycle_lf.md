# Cycle LF: covering AND at \(p=14\) on \(G=1\) is always \(0011\)

On covering \(J_6,J_{10}\) for \(k\le 6\), packed AND at \(p=14\) with
\(G=1\) is only CONT \(0011\). For \(k\ge 3\) the count equals Cycle
LC's \(p=4\) count, hence odd, so the \(p=14\) \(0011\) XOR is \(1\).
Small \(k\): empty at \(k=0\); \(0\) vs \(1\) at \(k=1\); \(2\) vs
\(3\) at \(k=2\). This is **not** \(1001\) at \(p=14\), **not** xor
\(0\) for \(k\ge 3\), **not** the \(p=4\) count for all \(k\), and
**not** empty for \(k<3\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: this is packed AND at \(p=14\), not a Green-only
formula for packed AND XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_lf.py --certify`.
Dump: `research/cycle_lf.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HG/HH/HI/HU/KH/LC (covering \(k\le 6\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (\(p=14\) AND is \(0011\))

Certified \(k\le 6\) (\(50\) events). For \(k\ge 3\) the count equals
the \(p=4\) count. Covering \(J_6,J_{10}\) still have \(G=1\) columns
\(22659\); odd-\(s\) \(J\) XOR matches Cycles HF/HG.

## Lemma (\(p=16\) AND is \(1001\))

Cycle LE. Packed AND at \(p=16\) on \(G=1\) is always \(1001\).

## Lemma (\(p=6\) AND is \(0100\))

Cycle LD. Packed AND at \(p=6\) on \(G=1\) is always \(0100\).

## Lemma (\(p=4\) AND is \(1001\) with odd count)

Cycle LC. Lowest live packed AND slot is always \(1001\).

## Killed

Other AND at \(p=14\): \(k=3\), \(q=6\) is only \(0011\). Xor \(0\)
for \(k\ge 3\): count \(3\), xor \(1\). Equal to \(p=4\) count for
all \(k\): \(k=0\) is \(0\) vs \(1\). Empty for \(k<3\): \(k=1\),
\(q=10\) has \(1\).

## Verdict

`LEMMA` (\(p=14\) AND is \(0011\); \(p=16\) AND is \(1001\); \(p=6\)
AND is \(0100\); \(p=4\) AND is \(1001\) with odd count; \(1001\) AND
xor remainder).
`KILLED` (other AND at \(p=14\); xor \(0\) for \(k\ge 3\); equal to
\(p=4\) count for all \(k\); empty for \(k<3\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_lf.md` (this note)
- `research/cycle_lf.py`
- `research/cycle_lf.json`
