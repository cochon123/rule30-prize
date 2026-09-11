# Cycle EC: extra is invariant under \(r\)-fold; extra 6 is odd-\(n_0\) alternating \(T\)

Cycle EB’s reconstruct commute implies the first ident-0 extra of any
O-type scar is unchanged by \(r\)-fold: odd \(r\) stays O-type with
the same extra and xorcat; even \(r\) is E-type with xorcat multiplied
by \(r\). This is not special to \(n_0=2\). At \(n_0=12\) the only
ident-0s in 400 extras are the sixteen 3-folds of \(n_0=4\) (8 at 89,
8 at 372). Extra 6 occurs iff \(T=T_0\|\neg T_0\) is cyclically
alternating, which for odd \(n_0\) is exactly the two words
`0101...0` and `1010...1` (\(n_4\equiv 0\), Cycle DY). A 2-power
\(n_0\) has no odd divisor \(\ge 3\), so it is fold-primitive.
Left-machine \(\pi\) is always a 2-power, hence \(n_0\) at every odd
ident-0 is a 2-power: after \(k=2\) the extra-6 (odd \(n_0\)) and
extra-22 (\(n_0=2\cdot\mathrm{odd}\ge 6\)) families are unreachable.
Kills extra \(\ge 22\) for all \(n_0\) (\(n_0=1\) extra 6). Do **not**
claim extra \(\ge 22\) for every even \(n_0\). Do **not** claim the
fold families appear on the prize orbit after \(k=2\). Do **not**
claim an 11-bit gap. Do **not** compute \(\varphi^{(3,5,9)}\) at
\(k=16\).

Not a prize claim: reducing the leftover attack to 2-power \(n_0\)
does not fill an annulus.

Helper: `python3 research/cycle_ec.py --certify`. Dump:
`research/cycle_ec.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles DE, DU, DY, EB (no new packed run, no Fermat
table).

## Lemma (type of \(T^r\) for any \(n_0\))

\(T\) has length \(2n_0\) and \(T_{t+n_0}=\neg T_t\). On \(T^r\),
positions \(t\) and \(t+n_0 r\) differ by \(n_0 r \bmod 2n_0\): odd
\(r\) gives shift \(n_0\) (NOT), even \(r\) gives shift \(0\) (equal).
Certified for \(n_0\le 8\) and \(r\le 7\).

## Lemma (extra invariant under \(r\)-fold)

The scar of \(T^r\) is the \(r\)-fold of the scar of \(T\) (Cycle EB
reconstruct commute). The first all-zero row stays at the same index;
the predecessor XOR becomes \(r\cdot\operatorname{xorcat}(a)\). Odd
\(r\) therefore preserves extra and xorcat on the standard O-type
scar of the half-word. Even \(r\) is an E-type lift with the same
extra. Certified on every \(T_0\) of length \(\le 5\) for odd
\(r\in\{3,5\}\), and on \(n_0\in\{2,3,4\}\) for even \(r\in\{2,4\}\).

## Lemma (\(n_0=12\) extra 89/372 are the \(n_0=4\) 3-folds)

All 4096 length-12 \(T_0\): 8 ident-0 at extra 89, 8 at 372, 4080
none in 400 extras. The 16 hits are exactly the 3-folds of Cycle DI’s
length-4 families. Do not claim the 4080 stay clean past 400.

## Lemma (extra 6 iff \(T\) is cyclically alternating)

\(T=T_0\|\neg T_0\) is cyclically alternating iff \(n_0\) is odd and
\(T_0\) is `0101...0` or `1010...1` (even \(n_0\) never: Cycle CH
junction). Those two O-types have \(n_4\equiv 0\) (Cycle DY), and the
first ident-0 is at extra 6 with odd xorcat. Certified for every odd
\(1\le n_0\le 11\), and no extra 6 in the first 10 extras for even
\(n_0\le 8\).

## Lemma (2-power \(n_0\) is fold-primitive; leftover families unreachable after \(k=2\))

The only odd positive divisor of \(2^e\) is 1, so a 2-power half-length
is not a nontrivial odd \(r\)-fold. Unique continuation doubles \(\pi\)
only on odd ident-0 and starts at \(\pi_1=1\) (Cycle DU), so \(\pi\) is
always a 2-power and \(n_0\) at an odd ident-0 equals that 2-power.
Prize periods through \(k=19\) match. After \(k=2\), \(n_0\ge 4\) is
\(0\bmod 4\): odd \(n_0\) (extra 6) and \(n_0\equiv 2\pmod 4\) (extra-22
folds) cannot occur. At-most-one-odd on the left machine therefore
reduces to extra-versus-leftover for 2-power \(n_0\) only. Do not claim
that bound for all \(k\).

## Killed

Extra \(\ge 22\) for all \(n_0\) is false: \(n_0=1\) (and every odd
alternating \(T\)) ident-0s at extra 6.

## Verdict

`LEMMA` (type of \(T^r\) for any \(n_0\); extra invariant under odd
and even \(r\)-fold; \(n_0=12\) extra 89/372 are \(n_0=4\) 3-folds;
extra 6 iff \(T\) alternating; 2-power \(n_0\) fold-primitive;
left-machine \(\pi\) always a 2-power; extra-6 and extra-22 folds
unreachable after \(k=2\)).
`KILLED` (extra \(\ge 22\) for all \(n_0\)).
`PREFIX` (extra \(\ge 22\) for every even \(n_0\); at-most-one-odd
for all \(k\); period-\(H\) seed; \(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ec.md` (this note)
- `research/cycle_ec.py`
- `research/cycle_ec.json`
