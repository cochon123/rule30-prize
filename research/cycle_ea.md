# Cycle EA: \(n_7\ne n_8\) for even \(n_0\); 10-bit post-odd ident-0 gap

\(n_3=n_4=1\) forces \(n_5=1\): \(n_3=1\) gives \(s_{t-1}=n_{3,t-1}=0\),
hence \(n_{4,t-1}=1\) and \(n_5=n_3^{\mathrm{prev}}\oplus(n_4^{\mathrm{prev}}\lor n_5^{\mathrm{prev}})=1\).
Empty pairs cannot follow empty pairs (\(s\) and \(\neg s\) cannot both
meet \(\operatorname{NOR}(\cdot,0)=0\)). Equality \(n_7=n_8\) iff
\(n_5=n_6\land n_7\); on an empty pair the 16 allowed triples preserve
that iff both sides are \((n_5,n_6,n_7)=(0,0,1)\), which needs both
\(n_6=0\). That empty \(n_6=00\) can only come from agree1 with
zero-side \(n_5=n_6=0\). Pair invariants on the predecessor then force
the one-side to \((n_4,n_5,n_6)=(0,1,1)\), so \(n_4\ne n_5\lor n_6\) and
next \(n_6\) cannot both vanish. Hence \(n_7\ne n_8\), and after an odd
doubling there is no ident-0 at \(p+1,\ldots,p+10\). Do **not** claim an
11-bit gap. Do **not** compute \(\varphi^{(3,5,9)}\) at \(k=16\).

Not a prize claim: a 10-bit gap does not fill an annulus.

Helper: `python3 research/cycle_ea.py --certify`. Dump:
`research/cycle_ea.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycle DZ (no new packed run, no Fermat table).

## Lemma (\(n_3=n_4=1\Rightarrow n_5=1\))

\(n_{3,t}=1\) is \(\operatorname{NOR}(s_{t-1},n_{3,t-1})=1\), so both
bits are 0. Then \(n_{4,t}=s_{t-1}\oplus(n_{3,t-1}\lor n_{4,t-1})=n_{4,t-1}\).
If also \(n_{4,t}=1\), then \(n_{5,t}=0\oplus(1\lor n_{5,t-1})=1\).
Certified on every O-type of even \(2\le n_0\le 12\).

## Lemma (empty does not follow empty)

Next-empty would need \(\operatorname{NOR}(s,0)=\operatorname{NOR}(\neg s,0)=0\),
hence \(s=\neg s\).

## Lemma (\(n_7=n_8\) only via both-empty \((0,0,1)\))

\(n_7=n_8\) iff \(n_{5,t}=n_{6,t}\land n_{7,t}\) at every \(t\). The
allowed empty-side triples are the four solutions of that AND. Of the
16 pairs, only \((0,0,1)\) with \((0,0,1)\) preserves the AND on both
next sides. That pair has both \(n_6=0\).

## Lemma (empty \(n_6\lor n_6^{+}=1\); \(n_7\ne n_8\); 10-bit gap)

Empty cannot follow empty, so empty \(n_6=00\) would have to come from
agree1 with zero-side \(n_5=n_6=0\) and one-side \(n_4=n_5\lor n_6\).
The recurrences back one step plus pair invariants force the one-side
to \((n_4,n_5,n_6)=(0,1,1)\) (the predecessor pair is empty, hence
\(n_5^{\mathrm{prev}}=1\), and ov on the plus side). Then
\(n_4\ne n_5\lor n_6\), so next \(n_6\) cannot both vanish. Hence both
empty \((0,0,1)\) is impossible and \(n_7\ne n_8\): no ident-0 at
\(p+10\). Together with Cycle DZ’s 9-bit gap, there is no ident-0 at
\(p+1,\ldots,p+10\). Certified on every even \(T_0\) of length \(\le 8\)
via `scar_lift`, and on prize \(k=4,8,16\). \(n_8\ne n_9\) holds through
even \(n_0\le 10\) but is not claimed for all \(n_0\).

## Verdict

`LEMMA` (\(n_3=n_4=1\Rightarrow n_5=1\); empty not follow empty;
\(n_7=n_8\) only both-\((0,0,1)\); empty \(n_6\lor n_6^{+}\);
\(n_7\ne n_8\); 10-bit post-odd gap for even \(n_0\)).
`PREFIX` (11-bit gap; period-\(H\) seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ea.md` (this note)
- `research/cycle_ea.py`
- `research/cycle_ea.json`
