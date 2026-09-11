# Cycle DZ: even-\(n_0\) \(n_5\) is type N; 9-bit post-odd ident-0 gap

Empty pairs have both \(n_4=1\). If \(n_5\) were O-type, the reconstruct
half-shift on an empty pair yields \(0=1\). If \(n_5\) were E-type, the
empty side with \(s=1\) steps to \(n_3^{+}=1\) with \(n_5^{+}=1\), while
the half-shift on agree1 requires \(n_5=0\) at every \(n_3=1\). Hence
\(n_5\) is type N. Assuming \(n_6=n_7\) iff \(n_4=n_5\land n_6\), so empty
pairs have \(n_5=n_6=1\); the O-type side with \(s=1\) then steps to
\(n_4^{+}=1\) versus \(n_5^{+}\land n_6^{+}=0\). Thus \(n_6\ne n_7\), and
after an odd doubling there is no ident-0 at \(p+1,\ldots,p+9\).
\(\operatorname{xorcat}(n_5)\) is not always odd; \(n_6\) is not always
type N. Do **not** claim a 10-bit gap. Do **not** compute
\(\varphi^{(3,5,9)}\) at \(k=16\).

Not a prize claim: a 9-bit gap does not fill an annulus.

Helper: `python3 research/cycle_dz.py --certify`. Dump:
`research/cycle_dz.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycle DY (no new packed run, no Fermat table).

## Lemma (\(n_5\) is type N for even \(n_0\))

Cycle DY: \(Z\ge 1\) empty pairs, both \(n_4=1\). The reconstruct
recurrence \(n_{5,t+1}=n_{3,t}\oplus(n_{4,t}\lor n_{5,t})\) with an
O-type half-shift \(n_{5,t+n_0}=\neg n_{5,t}\) forces
\((1\lor n_5)\oplus(1\lor\neg n_5)=1\) on an empty pair, but the left
side is \(1\oplus 1=0\). An E-type half-shift \(n_{5,t+n_0}=n_{5,t}\)
on agree1 forces \(n_4\land\neg n_5=1\), hence \(n_5=0\) at every
\(n_3=1\); from empty \(s=1\) the two sides step to \(n_3^{+}=1\) and
\(n_5^{+}=1\). Certified on the two bits of \(n_5\), and as type N on
every O-type of even \(2\le n_0\le 12\) plus 40 random \(n_0=16\) words.
Prize \(k=4,8,16\) have \(n_5\) of type N.

## Lemma (\(n_6\ne n_7\); 9-bit gap)

\(n_6=n_7\) iff \(n_{4,t}=n_{5,t}\land n_{6,t}\) at every \(t\), hence
\(n_5=n_6=1\) on empty pairs. From \((s,n_3,n_4,n_5,n_6)=(1,0,1,1,1)\)
the recurrences produce \((0,0,1,0)\) on the \(s=1\) side and
\((1,1,1,0)\) on the \(s=0\) side, so \(n_4^{+}=1\ne n_5^{+}\land n_6^{+}\).
Thus \(n_6\ne n_7\): no ident-0 at packed bit \(p+9\). Together with
Cycle DY’s 8-bit gap, there is no ident-0 at \(p+1,\ldots,p+9\) after an
odd doubling of even half-length. Certified on every even \(T_0\) of
length \(\le 8\) via `scar_lift`, and on prize \(k=4,8,16\).

## xorcat, \(n_6\) type, 10-bit gap

Every length-4 even O-type has \(\operatorname{xorcat}(n_5)=0\). Length-4
\(n_6\) realizes both types O and N (Cycle DY). \(n_7\ne n_8\) holds
through even \(n_0\le 12\) but is not claimed for all \(n_0\). **Killed**
as identities: always-odd xorcat of \(n_5\); \(n_6\) always type N.
**Prefix:** 10-bit gap.

## Verdict

`LEMMA` (\(n_5\) type N for even \(n_0\); \(n_6\ne n_7\); 9-bit post-odd
gap for even \(n_0\)).
`PREFIX` (10-bit gap; period-\(H\) seed; \(\pi\) formula; Fermat covering).
`KILLED` (\(\operatorname{xorcat}(n_5)\) always odd; \(n_6\) always type N).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_dz.md` (this note)
- `research/cycle_dz.py`
- `research/cycle_dz.json`
