# Cycle DY: even-\(n_0\) \(n_4\) is type N; 8-bit post-odd ident-0 gap

For even half-length \(n_0\ge 2\), an O-type word is never alternating
(the two alternating words of length \(2n_0\) are the \(01\)- and
\(10\)-repeats, both E-type). Hence \(s\ne n_3\) and
\(n_4=\operatorname{reconstruct}(s,n_3)\not\equiv 0\). Pair invariants
force at least one empty pair: \(Z=0\) would give \(\operatorname{ov}=Z=0\)
and \(n_4\equiv 0\). Empty pairs have both \(n_4=1\), so \(n_4\) is not
O-type; \(\operatorname{ov}=Z\ge 1\) gives a disagreeing pair, so \(n_4\)
is not E-type. Hence \(n_4\) is type N. Moreover \(n_3=D(n_4)\) iff
\(s_t=n_{3,t}\land n_{4,t}\), which on an empty pair forces
\(s_t=s_{t+n_0}=0\), contradicting O-type, so \(n_4\ne n_5\). Assuming
\(n_5=n_6\) forces \(n_5=0\) on empty pairs; the O-type side with
\(s=1\) then two-steps to \(n_3=\neg s'\) versus \(n_4=s'\). Thus
\(n_5\ne n_6\), and after an odd doubling there is no ident-0 at
\(p+1,\ldots,p+8\). Odd \(n_0\) can have \(n_4\equiv 0\);
\(\operatorname{ham}(n_4,n_5)\) is not \(n_0\); \(n_6\) is not always
type N. Do **not** compute \(\varphi^{(3,5,9)}\) at \(k=16\).

Not a prize claim: an 8-bit gap does not fill an annulus.

Helper: `python3 research/cycle_dy.py --certify`. Dump:
`research/cycle_dy.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycle DX (no new packed run, no Fermat table).

## Lemma (even O-type is never alternating)

A binary word of length \(\ge 2\) is alternating iff it is the
\(01\)-repeat or the \(10\)-repeat. For even \(n_0\) those two words of
length \(2n_0\) are E-type, so no O-type is alternating. Then
\(\operatorname{reconstruct}(1,s)=s\) iff \(1=D(s)\) iff \(s\) is
alternating, and \(\operatorname{reconstruct}(s,n_3)\equiv 0\) iff
\(s=n_3\). Certified on every O-type of even \(2\le n_0\le 12\).

## Lemma (\(n_4\) is type N for even \(n_0\))

Pair invariants (Cycle DX): empty pairs have both \(d=1\), hence both
\(n_4=1\); \(\operatorname{ov}=Z\). Combined with \(n_4\not\equiv 0\),
\(Z=0\) is impossible, so \(Z\ge 1\). An empty pair forbids type O; a
disagreeing pair (\(\operatorname{ov}=Z\ge 1\)) forbids type E. Certified
exhaustively for even \(2\le n_0\le 12\) and on 40 random \(n_0=16\)
words. Prize \(k=4,8,16\) have \(n_4\) of type N.

## Lemma (\(n_3\ne D(n_4)\), so \(n_4\ne n_5\))

The reconstruct recurrence gives \(D(n_4)_t=s_t\oplus(n_{3,t}\land\neg n_{4,t})\),
hence \(n_3=D(n_4)\) iff \(s_t=n_{3,t}\land n_{4,t}\) at every \(t\). On
an empty pair both \(n_3=0\) and both \(n_4=1\), so both \(s=0\), which
O-type forbids. Therefore \(n_4\ne n_5\): no ident-0 at packed bit
\(p+7\) after an odd doubling.

## Lemma (\(n_5\ne n_6\); 8-bit gap)

Equality \(n_5=n_6\) iff \(n_{3,t}=n_{4,t}\land n_{5,t}\) at every \(t\),
hence \(n_5=0\) on empty pairs. Every empty pair has a side with
\(s=1\). From \((s,n_3,n_4,n_5)=(1,0,1,0)\) the recurrences produce
\((0,0,1)\) then, for both values of \(s'\),
\((n_3,n_4,n_5)=(\neg s',s',1)\), so \(n_3=\neg s'\) cannot equal
\(n_4\land n_5=s'\). Thus \(n_5\ne n_6\): no ident-0 at \(p+8\).
Together with Cycle DH’s 6-bit gap and \(n_4\ne n_5\), there is no
ident-0 at \(p+1,\ldots,p+8\) after an odd doubling of even half-length
(prize \(\pi_k\) is even for \(k\ge 2\)). Certified on every even
\(T_0\) of length \(\le 8\) via `scar_lift`, and on prize \(k=4,8,16\).

## Odd \(n_0\), Hamming, \(n_6\) type — killed

The two alternating O-types of odd \(n_0\in\{1,3,5,7\}\) have
\(n_4\equiv 0\). Length-4 even O-type has
\(\operatorname{ham}(n_4,n_5)\in\{3,4\}\). Length-4 \(n_6\) realizes
both types O and N. **Killed** as identities.

## Verdict

`LEMMA` (even O-type never alternating; \(n_4\) type N for even \(n_0\);
\(n_3\ne D(n_4)\); \(n_5\ne n_6\); 8-bit post-odd gap for even \(n_0\)).
`PREFIX` (period-\(H\) seed; \(\pi\) formula; Fermat covering).
`KILLED` (\(n_4\not\equiv 0\) for odd \(n_0\); \(\operatorname{ham}(n_4,n_5)=n_0\);
\(n_6\) always type N).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_dy.md` (this note)
- `research/cycle_dy.py`
- `research/cycle_dy.json`
