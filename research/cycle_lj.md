# Cycle LJ: covering AND at \(p=98\) on \(G=1\) is always \(0010\)

On covering \(J_6,J_{10}\) for \(k\le 6\), packed AND at \(p=98\) with
\(G=1\) is only FRESH \(0010\). Empty for \(k\le 4\); \(0\) vs \(2\)
at \(k=5\); \(2\) vs \(5\) at \(k=6\). This is **not** \(1001\) at
\(p=98\), **not** xor \(1\) at \(k=5\), \(q=10\), **not** the
\(p=4\) count, and **not** empty for \(k<6\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: this is packed AND at \(p=98\), not a Green-only
formula for packed AND XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_lj.py --certify`.
Dump: `research/cycle_lj.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HG/HH/HI/HU/KH/LC (covering \(k\le 6\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (\(p=98\) AND is \(0010\))

Certified \(k\le 6\) (\(9\) events). This is the first unique packed
slot that is always FRESH \(0010\). Covering \(J_6,J_{10}\) still
have \(G=1\) columns \(22659\); odd-\(s\) \(J\) XOR matches Cycles
HF/HG.

## Lemma (\(p=106\) AND is \(1001\))

Cycle LI. Packed AND at \(p=106\) on \(G=1\) is always \(1001\).

## Lemma (\(p=14\) AND is \(0011\))

Cycle LF. Packed AND at \(p=14\) on \(G=1\) is always \(0011\).

## Lemma (\(p=4\) AND is \(1001\) with odd count)

Cycle LC. Lowest live packed AND slot is always \(1001\).

## Killed

Other AND at \(p=98\): \(k=5\), \(q=10\) is only \(0010\). Xor \(1\)
at \(k=5\), \(q=10\): count \(2\), xor \(0\). Equal to the \(p=4\)
count: \(k=6\), \(q=6\) is \(2\) vs \(7\). Empty for \(k<6\): \(k=5\),
\(q=10\) has \(2\).

## Verdict

`LEMMA` (\(p=98\) AND is \(0010\); \(p=106\) AND is \(1001\);
\(p=54\) AND is \(0100\); \(p=16\) AND is \(1001\); \(p=6\) AND is
\(0100\); \(p=4\) AND is \(1001\) with odd count; \(1001\) AND xor
remainder).
`KILLED` (other AND at \(p=98\); xor \(1\) at \(k=5\), \(q=10\);
equal to the \(p=4\) count; empty for \(k<6\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_lj.md` (this note)
- `research/cycle_lj.py`
- `research/cycle_lj.json`
