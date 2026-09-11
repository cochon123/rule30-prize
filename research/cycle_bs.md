# Cycle BS: four leftmost unique-Green bits on \(B\) and \(C\)

On \(B=[6U,10U)\to 10U\), write \(t=6U+s\). The Green cone allows
\(s\le(p-2U-2)/2\). For \(p=2U+2,2U+3,2U+4,2U+5\) that window has
length at most 2, and a one-line \(G\) evaluation leaves a unique
time: \(6U\), \(6U\), \(6U+1\), \(6U\). The same four bits are
unique-Green on \(C\) at \(10U\), \(10U\), \(10U+1\), \(10U\). Their
firing XOR takes both values, so it is not a 1-production for
\(S_B\) or \(S_C\). Not a prize claim: the Fermat covering remains a
prefix.

Helper: `python3 research/cycle_bs.py --certify` (~0.05s). Dump:
`research/cycle_bs.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (\(G(m,1)=m\bmod 2\))

Even \(m\) and odd target give \(G=0\). Odd \(m=2n+1\) gives
\(G(2n+1,1)=G(n,0)=1\), since \(G(n,0)=1\) for every \(n\ge 0\).
Palindrome \(G(m,2m-1)=G(m,1)\). Certified \(m\le 64\), including
\(G(m,2m)=1\).

## Lemma (four unique bits on \(B\))

Let \(U=2^k\) and \(t=6U+s\) with \(s\in[0,4U)\). Then
\(m=4U-s-1\) and \(d=10U-p\), so \(d\le 2m\) iff
\(s\le(p-2U-2)/2\).

- \(p=2U+2\): \(s=0\), \(d=2m\), \(G=1\) (Cycle BR).
- \(p=2U+3\): \(s=0\), \(d=2m-1\), \(G(m,1)=1\) because \(m=4U-1\)
  is odd.
- \(p=2U+4\): cone \(s\in\{0,1\}\). At \(s=0\),
  \(G(4U-1,8U-4)=G(2U-1,4U-2)\oplus G(2U-1,4U-3)=1\oplus G(2U-1,1)=1\oplus 1=0\).
  At \(s=1\), \(G(4U-2,8U-4)=G(2U-1,4U-2)=G(m',2m')=1\).
- \(p=2U+5\): cone \(s\in\{0,1\}\). At \(s=1\), \(m\) even and \(d\)
  odd, so \(G=0\). At \(s=0\), \(d=2m-3\),
  \(G(4U-1,3)=G(2U-1,1)=1\).

Certified by a Green scan for \(1\le k\le 5\). These are all the
admissible bits with \(p<2U+6\) (the next offset has cone length 3
and is not unique).

## Lemma (the same four unique bits on \(C\))

Replace \(4U\) by \(8U\) and the block start \(6U\) by \(10U\). The
same four evaluations give unique times \(10U\), \(10U\), \(10U+1\),
\(10U\) targeting \(18U\). Certified \(1\le k\le 5\).

## Unique XOR is not identically 1 — killed

The XOR of the four unique firings on \(B\) takes both values on
\(1\le k\le 8\) (zero at \(k=5,6\)). **Killed** as a 1-production
for \(S_B\). Covering still fails iff \(S_A=1\) and \(S_B=S_C=0\).

## Verdict

`LEMMA` (\(G(m,1)=m\bmod 2\); four unique-Green bits
\(p=2U+2,\ldots,2U+5\) on \(B\) and on \(C\), with closed times).
`KILLED` (their firing XOR identically 1).
`PREFIX` (Fermat covering for all \(k\ge 2\)).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_bs.md` (this note)
- `research/cycle_bs.py`
- `research/cycle_bs.json`
