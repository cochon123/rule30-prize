# Cycle FS: \(G(m,d)=G(m,2m-d)\); unclipped cone-hi is \(G(m,2U-2)\)

The polynomial \((1+x+x^2)^m\) is reciprocal of degree \(2m\), so
\(G(m,d)=G(m,2m-d)\). Cycle FK’s corners \(G(n,0)=G(n,2n)=1\) are
palindrome duals, and Cycle FR’s band lo-edge \(G(m,2m)=1\) is the
palindrome of \(G(m,0)=1\). On the unclipped unified band
(\(s\le U+W\)) the cone-upper degree \(W-(2s-T)\) palindromes to the
constant \(2U-2\), independent of \(W\) and \(s\), so that edge is
\(G(m,2U-2)\). It is **not** identically 1. Do **not** claim
palindrome about \(m\) (\(G(m,d)=G(m,m-d)\)). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: a Green palindrome plus a constant palindrome
degree does not prove covering never-fail.

Helper: `python3 research/cycle_fs.py --certify` (~0.01s). Dump:
`research/cycle_fs.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles AL/CA/FK/FQ/FR (algebraic \(k\le 7\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (\(G(m,d)=G(m,2m-d)\))

Certified \(0\le m<64\), all \(d\in[0,2m]\).

## Lemma (unclipped cone-hi is \(G(m,2U-2)\))

Palindrome degree \(2m-(W-(2s-T))=T-W-2=2U-2\). Certified on
endpoint samples \(k\le 7\), \(W\in\{4U,8U,16U\}\).

## Killed

Palindrome about \(m\): \(G(5,2)=1\neq G(5,3)=0\). Unclipped hi-edge
Green identically 1: at \(k=2\), \(W=8U\), \(s=9U-1\) the value is
0.

## Verdict

`LEMMA` (palindrome \(G(m,d)=G(m,2m-d)\); unclipped cone-hi
\(G(m,2U-2)\)).
`KILLED` (palindrome about \(m\); unclipped hi \(\equiv 1\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_fs.md` (this note)
- `research/cycle_fs.py`
- `research/cycle_fs.json`
