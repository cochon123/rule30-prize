# Cycle LH: covering AND at \(p=54\) on \(G=1\) is always \(0100\)

On covering \(J_6,J_{10}\) for \(k\le 6\), packed AND at \(p=54\) with
\(G=1\) is only FRESH \(0100\). Empty for \(k\le 3\); \(0\) vs \(1\)
at \(k=4\); \(2\) vs \(5\) at \(k=5\); \(5\) vs \(5\) at \(k=6\). This
is **not** \(1001\) at \(p=54\), **not** xor \(1\) at \(k=5\),
\(q=6\), **not** the \(p=6\) count, and **not** empty for \(k<5\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: this is packed AND at \(p=54\), not a Green-only
formula for packed AND XOR \(J\), so covering never-fail stays open.

Certify: `python3 research/cycle_lh.py --certify` (~0.22s).
Dump: `research/cycle_lh.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HG/HH/HI/HU/KH/LD (covering \(k\le 6\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (\(p=54\) AND is \(0100\))

Certified \(k\le 6\) (\(18\) events). Covering \(J_6,J_{10}\) still
have \(G=1\) columns \(22659\); odd-\(s\) \(J\) XOR matches Cycles
HF/HG.

## Lemma (\(p=32\) AND is \(0100\) for \(k\ge 4\))

Cycle LG. Packed AND at \(p=32\) on \(G=1\) is \(0100\) for
\(k\ge 4\).

## Lemma (\(p=14\) AND is \(0011\))

Cycle LF. Packed AND at \(p=14\) on \(G=1\) is always \(0011\).

## Lemma (\(p=6\) AND is \(0100\))

Cycle LD. Packed AND at \(p=6\) on \(G=1\) is always \(0100\).

## Killed

Other AND at \(p=54\): \(k=5\), \(q=10\) is only \(0100\). Xor \(1\)
at \(k=5\), \(q=6\): count \(2\), xor \(0\). Equal to the \(p=6\)
count: \(k=5\), \(q=6\) is \(2\) vs \(5\). Empty for \(k<5\): \(k=4\),
\(q=10\) has \(1\).

## Verdict

`LEMMA` (\(p=54\) AND is \(0100\); \(p=32\) AND is \(0100\) for
\(k\ge 4\); \(p=14\) AND is \(0011\); \(p=16\) AND is \(1001\);
\(p=6\) AND is \(0100\); \(p=4\) AND is \(1001\) with odd count;
\(1001\) AND xor remainder).
`KILLED` (other AND at \(p=54\); xor \(1\) at \(k=5\), \(q=6\); equal
to the \(p=6\) count; empty for \(k<5\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_lh.md` (this note)
- `research/cycle_lh.py`
- `research/cycle_lh.json`
