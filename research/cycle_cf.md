# Cycle CF: ident-1 at \(p\ge 2\) iff ident-0 at \(p-2\)

Packed update at an identically-\(1\) bit is \(1=\lambda_{p-2}\oplus 1\),
so ident-\(1\) at \(p\ge 2\) forces ident-\(0\) at \(p-2\). Twin gives
the converse. Consecutive ident-\(1\) at \(p\ge 2\) would force
ident-\(0\) at \(p+2\) and then ident-\(0\) at \(p\), a contradiction;
the only consecutive ident-\(1\) pair is packed bits \(0\) and \(1\).
Both implications with \(c\not\equiv 0\), and identically AND with
\(c\not\equiv 0\), occur on consistent length-\(4\) windows
(**killed** as orbit-free claims). After the scar, both implications
hold together only at \(c\equiv 0\) (prefix). Not a prize claim: the
Fermat covering remains a prefix.

Helper: `python3 research/cycle_cf.py --certify` (~0.6s). Dump:
`research/cycle_cf.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (ident-\(1\) iff ident-\(0\) two to the right)

If \(\lambda_p\equiv 1\) and \(p\ge 2\), the update
\(\lambda_p(t+1)=\lambda_{p-2}(t)\oplus(\lambda_{p-1}(t)\lor\lambda_p(t))\)
collapses to \(1=\lambda_{p-2}(t)\oplus 1\), hence
\(\lambda_{p-2}\equiv 0\). Cycle BY's twin is the converse: ident-\(0\)
at \(q\ge 2\) with a live left neighbour forces ident-\(1\) at
\(q+2\). Certified pointwise, and on prize cycles for
\(3\le k\le 12\) the two lists agree except at bits \(0,1\).

## Lemma (consecutive ident-\(1\) only at bits \(0,1\))

If \(p\ge 2\) and \(\lambda_p\equiv\lambda_{p+1}\equiv 1\), then
\(a=b\equiv 1\) forces ident-\(0\) at \(p+2\) (Cycle BZ). The
AND-triple for that ident-\(0\) is bits \((p-2,p-1,p)\), so
\(\lambda_{p-2}=\lambda_{p-1}\), hence ident-\(0\) at \(p\),
contradicting \(\lambda_p\equiv 1\). The origin pair \((0,1)\) is
the exception because the AND-triple would use negative indices.
Certified: on prize cycles \(3\le k\le 12\) the only consecutive
ident-\(1\) is bit \(0\). Three consecutive ident-\(1\)s are
impossible even at the origin (\(1\oplus(1\lor 1)=0\)).

## Both implications \(\Rightarrow c\equiv 0\) — killed orbit-free

Among \(256\) consistent length-\(4\) five-bit windows, \(30\) have
\(c\to a\), \(c\to b\), and \(c\not\equiv 0\), and \(14\) of those
are identically AND. **Killed** as statements on the whole affine
space. After the scar they remain prefixes on the prize orbit
(\(k=4\): only bit \(31\); \(k=8\): only bit \(402\), both with
\(c\equiv 0\)).

## Verdict

`LEMMA` (ident-\(1\) at \(p\ge 2\) iff ident-\(0\) at \(p-2\);
consecutive ident-\(1\) only at bits \(0,1\)).
`PREFIX` (both implications only at the scar \(c\equiv 0\); no
AND-triple after the scar; at most one odd toggle for all \(k\);
seed for all \(k\); Fermat covering).
`KILLED` (both implications \(\Rightarrow c\equiv 0\) orbit-free;
AND \(\Rightarrow c\equiv 0\) orbit-free).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_cf.md` (this note)
- `research/cycle_cf.py`
- `research/cycle_cf.json`
