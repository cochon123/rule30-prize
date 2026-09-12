# Cycle LI: covering AND at \(p=106\) on \(G=1\) is always \(1001\)

On covering \(J_6,J_{10}\) for \(k\le 6\), packed AND at \(p=106\)
with \(G=1\) is only FRESH \(1001\). Empty for \(k\le 4\); \(0\) vs
\(3\) at \(k=5\); \(4\) vs \(10\) at \(k=6\). This is **not**
\(0100\) at \(p=106\), **not** xor \(1\) at \(k=6\), **not** the
\(p=4\) count, and **not** empty for \(k<6\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: this is packed AND at \(p=106\), not a Green-only
formula for packed AND XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_li.py --certify`.
Dump: `research/cycle_li.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HG/HH/HI/HU/KH/LB/LC (covering \(k\le 6\); no Fermat table,
no extra window, no \(n_0=16\) window).

## Lemma (\(p=106\) AND is \(1001\))

Certified \(k\le 6\) (\(17\) events). Covering \(J_6,J_{10}\) still
have \(G=1\) columns \(22659\); odd-\(s\) \(J\) XOR matches Cycles
HF/HG.

## Lemma (\(p=54\) AND is \(0100\))

Cycle LH. Packed AND at \(p=54\) on \(G=1\) is always \(0100\).

## Lemma (\(p=16\) AND is \(1001\))

Cycle LE. Packed AND at \(p=16\) on \(G=1\) is always \(1001\).

## Lemma (\(p=4\) AND is \(1001\) with odd count)

Cycle LC. Lowest live packed AND slot is always \(1001\).

## Killed

Other AND at \(p=106\): \(k=5\), \(q=10\) is only \(1001\). Xor \(1\)
at \(k=6\): count \(4\), xor \(0\). Equal to the \(p=4\) count:
\(k=6\), \(q=6\) is \(4\) vs \(7\). Empty for \(k<6\): \(k=5\),
\(q=10\) has \(3\).

## Verdict

`LEMMA` (\(p=106\) AND is \(1001\); \(p=54\) AND is \(0100\);
\(p=32\) AND is \(0100\) for \(k\ge 4\); \(p=16\) AND is \(1001\);
\(p=6\) AND is \(0100\); \(p=4\) AND is \(1001\) with odd count;
\(1001\) AND xor remainder).
`KILLED` (other AND at \(p=106\); xor \(1\) at \(k=6\); equal to the
\(p=4\) count; empty for \(k<6\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_li.md` (this note)
- `research/cycle_li.py`
- `research/cycle_li.json`
