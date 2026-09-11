# Cycle DX: pair invariants for every odd 2-copy; \(\operatorname{ham}(n_3,n_4)=n_0\)

Write \(P_1(t)\) for \(n_{4,t}\lor n_{3,t}\lor n_{3,t+n_0}=1\) and
\(P_2(t)\) for \(n_{4,t}\land n_{3,t+n_0}=0\). At any site with
\(n_{3,t}=1\), complementary support forces \(n_{3,t+n_0}=0\), so both
hold. The NOR / reconstruct recurrences send \((P_1,P_2)\) at \(t\) to
\((P_1,P_2)\) at \(t+1\) for every bit \(s_t\). An O-type word is never
all-1s, so \(\operatorname{reconstruct}(1,s)\) is not identically 0
and a seed exists. Hence the pair invariants hold at every \(t\), for
every half-length. Cycle DW’s bijection then gives
\(\operatorname{ham}(n_3,n_4)=n_0\) with no \(n_0\) bound. Pair
invariants still fail for generic \(s\) and for E-type. Do **not**
compute \(\varphi^{(3,5,9)}\) at \(k=16\).

Not a prize claim: Hamming \(n_0\) does not fill an annulus.

Helper: `python3 research/cycle_dx.py --certify`. Dump:
`research/cycle_dx.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycle DW (no new packed run, no Fermat table).

## Lemma (seed; \(n_3\not\equiv 0\); step preserves \(P_1,P_2\))

If \(n_3=1\) and \(n_{3}^{+}=0\) then \(P_1\) and \(P_2\) hold for both
values of \(n_4\). Certified on those two bits. O-type has weight
\(n_0\), so it is not all-1s (that word is E-type);
\(\operatorname{reconstruct}(1,1\cdots 1)\equiv 0\), and every O-type
of half-length \(1\le n_0\le 8\) has a 1 in \(n_3\). On every
complementary triple \((n_3,n_3^{+},n_4)\) that already satisfies
\(P_1,P_2\), both values of \(s\) produce a complementary next triple
that again satisfies \(P_1,P_2\) (8 hold steps, 0 failures).

## Lemma (pair invariants for all \(n_0\))

Complementary support (Cycle DW) plus a seed plus the 1-step
implication give \(P_1(t)\) and \(P_2(t)\) at every \(t\). Those are
exactly Cycle DW’s pair invariants: both \(n_3=0\) implies both
\(d=1\), and exactly one \(n_3=1\) implies \(d=0\) on the zero side.
Certified as a match on every O-type of half-length \(1\le n_0\le 8\).
Cycle DW already checked the invariants exhaustively through
\(n_0=16\). **LEMMA** for all \(n_0\), not a prefix.

## Lemma (\(\operatorname{ham}(n_3,n_4)=n_0\) for every odd 2-copy)

Cycle DW: the pair invariants make \(\varphi(i)=(i-1)\bmod n_0\) a
bijection from \(\{n_3=1,d=0\}\) onto the empty pair-slots, hence
Hamming \(n_0\). That argument had no further \(n_0\) bound once the
invariants hold. Prize \(k=4,8,16\) remain Hamming \(\pi\).

## Generic \(s\) and E-type — killed

Length-8 non-O-type words can have \(n_{3,t}=n_{3,t+4}=1\). E-type
length-16 words realize Hamming other than 8. **Killed** as identities.

## Verdict

`LEMMA` (seed; step preserves \(P_1,P_2\); O-type \(n_3\not\equiv 0\);
pair invariants for all \(n_0\); Hamming \(n_0\) for every odd
2-copy).
`PREFIX` (period-\(H\) seed; \(\pi\) formula; Fermat covering).
`KILLED` (pair invariants for generic \(s\); pair invariants / Hamming
\(n_0\) for E-type).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_dx.md` (this note)
- `research/cycle_dx.py`
- `research/cycle_dx.json`
