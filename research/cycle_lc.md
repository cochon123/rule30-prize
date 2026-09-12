# Cycle LC: covering AND at \(p=4\) on \(G=1\) is always \(1001\), with odd count

On covering \(J_6,J_{10}\) for \(k\le 6\), packed AND at \(p=4\) with
\(G=1\) is only FRESH \(1001\), never \(0010\), \(0100\), or \(0011\).
The count is \(k+1-(k\bmod 2)\) for \(q=6\) and \(k+1+(k\bmod 2)\)
for \(q=10\), hence odd, so the \(p=4\) \(1001\) XOR is \(1\). This is
**not** another AND-live pattern at \(p=4\), **not** xor \(0\),
**not** a \(q\)-independent count, and **not** count \(k+1\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do
**not** push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\).

Not a prize claim: this is the lowest live packed AND slot, not a
Green-only formula for packed AND XOR \(J\), so covering never-fail
stays open.

Certify: `python3 research/cycle_lc.py --certify`.
Dump: `research/cycle_lc.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HG/HH/HI/HU/KH/LB (covering \(k\le 6\); no Fermat table, no
extra window, no \(n_0=16\) window).

## Lemma (\(p=4\) AND is \(1001\) with odd count)

Certified \(k\le 6\) (\(56\) events). \(p=4\) is the lowest packed
index at which AND can fire on \(G=1\). Covering \(J_6,J_{10}\) still
have \(G=1\) columns \(22659\); odd-\(s\) \(J\) XOR matches Cycles
HF/HG.

## Lemma (\(1001\) AND xor remainder)

Cycle LB. Covering FRESH \(1001\) AND xor equals \(J\) except when
\(q=6\) and \(k\equiv 2\pmod{4}\).

## Killed

Other AND at \(p=4\): \(k=0\), \(q=6\) is only \(1001\). Xor \(0\):
that walk has count \(1\). \(q\)-independent: \(k=1\) is \(1\) vs
\(3\). Count \(k+1\): \(k=1\), \(q=6\) is \(1\) not \(2\).

## Verdict

`LEMMA` (\(p=4\) AND is \(1001\) with odd count; \(1001\) AND xor
remainder; tri specials from Mersenne unique).
`KILLED` (other AND at \(p=4\); xor \(0\); \(q\)-independent; count
\(k+1\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_lc.md` (this note)
- `research/cycle_lc.py`
- `research/cycle_lc.json`
