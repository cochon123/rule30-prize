# Cycle W: coupled drain on \(T=20\), and \(c_{2^k}\) templates

Three leftover attacks. All three hit their kill criteria. Not a prize
claim.

Helper: `python3 research/cycle_w.py --certify`. Dump:
`research/cycle_w.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Uses `F_of_u` from `research/period2_vacuum.py` without
modifying that file.

## 1. Coupled drain on the three \(X\)-legal \(T=20\) models

Ideas15 asked for a \(T\)-uniform identity that uses Cycle P’s 4-step
\((e,f)\) drain (a `0000` in \(u\)) as a multiplier, so that \(F_T=1\)
plus four zeros of \(u\) already forces a later \(F_{T+j}=1\).

Two of the three \(X\)-legal last-sat words at \(T=20\), \(R=16\)
contain `0000`:

```
001000010010010001   max zero run 4
101000010010010001   max zero run 4
```

On both, \(F_{20}=1\) and the next 16 columns of \(F\) are 0
(\(F_{37}=1\) only after the extra legal bit `0`). The drain window
**can** be placed inside a model that still realises \(R=16\). A
uniform “four zeros of \(u\) imply a later 1 of \(F\)” identity is
impossible.

The remaining word `010100010010010001` has max zero run 3, so the
4-step drain is not even present at every worst-case onset. **Killed.**

The same three models disagree with vacuum \(F_k=k\bmod 2\) on 12 or
13 odd columns. Ideas15’s odd-column vacuum gadget is killed by the
same witnesses.

## 2. Templates for \(b_k=c_{2^k}\)

If \((c_{2^k})_{k\ge 0}\) were not eventually periodic, neither would
\(c\) be (the subsequence \(2^k\bmod p\) is eventually periodic for
every \(p\)). Closed forms
\(k\bmod 2\), popcount, \(v_2(k+1)\), Rowland’s \(a(k)\bmod 2\),
and constants all fail by \(k\le 7\). **Killed.**

A centre `11` at time \(2^k\) occurs for 5 of the 16 values
\(k=0,\ldots,15\) (namely \(k=2,3,6,7,8\)), not uniformly. The spatial
triple \((x(2^k,-1),c_{2^k},x(2^k,1))\) is `010` or `011` at those
hits and `111,100,110,001` at the misses.

## 3. Right diagonals from the centre

The path \(j\mapsto x(k+j,j)\) is Rowland’s right diagonal of index
\(k\), hence periodic of period \(2^\alpha\). On a prefix \(j<128\)
the detected periods begin
\(1,2,2,4,8,8,16,32,32,64^{(6)}\) and then exceed the window. That
is Rowland’s lemma, not a formula for \(c_k\). The right-edge 1-run
at time \(2^k\) is length 1 for \(1\le k\le 7\) and does not encode
\(b_k\).

## Verdict

`KILLED` (all three), wall time 0.24s. Prize unsolved.

## Files

- `research/cycle_w.md` (this note)
- `research/cycle_w.py`
- `research/cycle_w.json`
