# Cycle LD: covering AND at \(p=6\) on \(G=1\) is always \(0100\)

On covering \(J_6,J_{10}\) for \(k\le 6\), packed AND at \(p=6\) with
\(G=1\) is only FRESH \(0100\). The count is \(2\) at \(k=0\), else
Cycle LC's \(p=4\) count at \((k-1,q=6)\) for \(q=6\) and at
\((k,q=6)\) for \(q=10\). The XOR is \(0\) at \(k=0\) and \(1\) for
\(k\ge 1\). This is **not** \(1001\) at \(p=6\), **not** xor \(1\) at
\(k=0\), **not** a \(q\)-independent count, and **not** the \(p=4\)
count. Do **not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all
\(k\). Do **not** push the even-spine scan past \(k=18\). Do **not**
bump all \(n_0=16\) past 414990. Do **not** increment consecutive
`11` to \(n_8\). Do **not** walk \(32U\).

Not a prize claim: this is packed AND at \(p=6\), not a Green-only
formula for packed AND XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_ld.py --certify`.
Dump: `research/cycle_ld.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HG/HH/HI/HU/KH/LC (covering \(k\le 6\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (\(p=6\) AND is \(0100\))

Certified \(k\le 6\) (\(46\) events). Covering \(J_6,J_{10}\) still
have \(G=1\) columns \(22659\); odd-\(s\) \(J\) XOR matches Cycles
HF/HG.

## Lemma (\(p=4\) AND is \(1001\) with odd count)

Cycle LC. Lowest live packed AND slot is always \(1001\).

## Killed

Other AND at \(p=6\): \(k=0\), \(q=6\) is only \(0100\). Xor \(1\) at
\(k=0\): count \(2\), xor \(0\). \(q\)-independent: \(k=2\) is \(1\)
vs \(3\). Equal to \(p=4\) count: \(k=0\) is \(2\) vs \(1\).

## Verdict

`LEMMA` (\(p=6\) AND is \(0100\); \(p=4\) AND is \(1001\) with odd
count; \(1001\) AND xor remainder).
`KILLED` (other AND at \(p=6\); xor \(1\) at \(k=0\); \(q\)-independent;
equal to \(p=4\) count).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ld.md` (this note)
- `research/cycle_ld.py`
- `research/cycle_ld.json`
