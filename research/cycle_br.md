# Cycle BR: packed bits \(p\le 2U+1\) are silent on \(B\) and \(C\)

The Green cone for packed bit \(p\) hitting target \(T\) is
\(t\le(T+p-2)/2\). On the covering blocks \(B=[6U,10U)\to 10U\) and
\(C=[10U,18U)\to 18U\) this forces every \(p\le 2U+1\) to have zero
hits, for every \(k\ge 1\) (Cycle BQ is the \(p=1\) case). Packed bit
\(p=2U+2\) is unique-Green on each block: at \(t=6U\) on \(B\) and at
\(t=10U\) on \(C\), both on the diagonal \(G(m,2m)=1\). That unique
AND takes both firing values, so it is not a 1-production for
\(S_B\) or \(S_C\). Not a prize claim: the Fermat covering remains a
prefix.

Helper: `python3 research/cycle_br.py --certify` (~0.1s). Dump:
`research/cycle_br.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (general cone)

Packed bit \(p\) at time \(t\) Green-hits target \(T\) iff
\(G(T-t-1,T-p)=1\). The support bound \(d\le 2m\) is
\(T-p\le 2(T-t-1)\), i.e. \(t\le(T+p-2)/2\). Cycle BQ is \(p=1\).
Certified: no counterexample for \(2\le T\le 24\) and
\(1\le p\le\min(8,2T)\).

## Lemma (low bits silent on \(B\) and \(C\))

Let \(U=2^k\) and \(p\le 2U+1\). Then
\((10U+p-2)/2\le(12U-1)/2\), so integer times satisfy
\(t\le 6U-1<6U\), hence no hits on \(B\). Likewise
\((18U+p-2)/2\le(20U-1)/2\), so \(t\le 10U-1<10U\), hence no hits
on \(C\). For every \(k\ge 1\). Certified inequalities \(k\le 12\).

Thus \(S_B\) and \(S_C\) are Green parities of packed bits
\(p\ge 2U+2\) only. Nested-left bits with bounded \(p\) cannot
contribute to those remainders.

## Lemma (\(p=2U+2\) unique-Green on \(B\) and on \(C\))

On \(B\), write \(t=6U+s\) with \(s\in[0,4U)\). Then
\(m=4U-s-1\) and \(d=8U-2\), so \(d\le 2m\) iff \(s=0\). At
\(s=0\), \(d=2m\) and \(G(m,2m)=1\). Hence a unique hit at
\(t=6U\). On \(C\), write \(t=10U+s\) with \(s\in[0,8U)\):
\(m=8U-s-1\), \(d=16U-2\), and \(d\le 2m\) iff \(s=0\), with
\(G(8U-1,16U-2)=1\). Unique hit at \(t=10U\). Certified by a
direct Green scan for \(1\le k\le 6\).

On the earlier block \(A\) the same bit is *not* unique (several
hits targeting \(10U\)).

## Unique firing is not identically 1 — killed

The AND of packed bits \(2U+1\) and \(2U+2\) at \(t=6U\) (resp.
\(t=10U\)) takes both values on \(1\le k\le 8\). **Killed** as a
1-production for \(S_B\) or \(S_C\). Covering still fails iff
\(S_A=1\) and \(S_B=S_C=0\), now with those remainders supported
only on \(p\ge 2U+2\).

## Verdict

`LEMMA` (general cone; \(p\le 2U+1\) silent on \(B,C\);
\(p=2U+2\) unique-Green on \(B\) at \(t=6U\) and on \(C\) at
\(t=10U\)).
`KILLED` (that unique AND identically fires).
`PREFIX` (Fermat covering for all \(k\ge 2\)).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_br.md` (this note)
- `research/cycle_br.py`
- `research/cycle_br.json`
