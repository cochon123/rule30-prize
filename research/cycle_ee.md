# Cycle EE: every \(n_0=2\) scar lifts to FAM372; 89-orbit unreachable after \(k=2\)

Every length-2 \(T_0\) odd-ident-0s at extra 22 with predecessor \(a\) a
rotation of `0111` (Cycle DI). \(\operatorname{unfold}(a)\) is
`0010`,`0100`,`0101`, or `0110`, all in the \(n_0=4\) extra-372 family.
A left-machine \(n_0=2\) doubling never produces the extra-89 orbit.
Extra 22 sends annulus \(k=2\) into \(k=4\); extra 372 sends \(k=4\)
into \(k=8\); extra 89 would send \(k=4\) into \(k=6\), but that family
is unreachable from \(n_0=2\). Prize \(T_0=0010\) is
\(\operatorname{unfold}(0111)\). Kills: 89-orbit reachable from
\(n_0=2\); every \(n_0=4\) waits for a 2-power (89 still hits \(k=6\),
but not on the left machine after \(k=2\)). Do **not** claim an
\(n_0=8\) lift closed form. Do **not** claim \(k=8\) maps to \(k=16\).
Do **not** claim an 11-bit gap. Do **not** compute
\(\varphi^{(3,5,9)}\) at \(k=16\).

Not a prize claim: forcing the next two odds into \(k=4\) and \(k=8\)
does not fill later annuli.

Helper: `python3 research/cycle_ee.py --certify`. Dump:
`research/cycle_ee.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles DI, ED (no new packed run, no Fermat table).

## Lemma (\(\operatorname{unfold}\) of rotations of `0111` is FAM372)

The four rotations of `0111` unfold to `{0010,0100,0101,0110}`, each in
Cycle DI’s extra-372 family, each starting with 0 (unfold always has
\(u_0=0\)). In particular \(\operatorname{unfold}(0111)=0010\), the
prize \(n_0=4\) \(T_0\).

## Lemma (every \(n_0=2\) \(T_0\) lifts to FAM372)

Cycle DI: every length-2 scar has extra 22 with \(a\) a rotation of
`0111`. The next \(T_0=\operatorname{unfold}(a)\) is therefore in
FAM372 and itself extra-372. None is in FAM89.

## Lemma (extra-interval mapping)

Packed next \(=p+E-1\). The image of \((2^k,2^{k+1}]\) is
\((2^k+E,2^{k+1}+E-1]\). Certified:

- \(E=22\), \(k=2\): \((26,29]\subset(16,32]\), annulus 4
- \(E=372\), \(k=4\): \((388,403]\subset(256,512]\), annulus 8
- \(E=89\), \(k=4\): \((105,120]\subset(64,128]\), annulus 6

Prize: \(8+21=29\), \(29+371=400\). So left-machine \(n_0=2\) in
\(k=2\) forces the next odd into \(k=4\) in FAM372, which forces the
following odd into \(k=8\). Cycle ED: \(k=4<v(4)=7\) and
\(k=8<v(8)=15\).

## Killed

The extra-89 orbit is unreachable from \(n_0=2\). It still lands in
\(k=6\) if started as a generic \(n_0=4\) scar, so “every \(n_0=4\)
waits for a 2-power” remains false (Cycle DI); it is false as a
statement about all \(T_0\), not as a statement about the left machine
after \(k=2\).

## Verdict

`LEMMA` (unfold of `0111`-rotations in FAM372; every \(n_0=2\) lifts
to FAM372; FAM372 all extra 372; extra 22 from \(k=2\) lands in
\(k=4\); extra 372 from \(k=4\) lands in \(k=8\); extra 89 from
\(k=4\) lands in \(k=6\)).
`KILLED` (89-orbit reachable from \(n_0=2\); every \(n_0=4\) waits
for a 2-power).
`PREFIX` (\(n_0=8\) lift closed form; \(k=8\) lands in \(k=16\);
at-most-one-odd for all \(k\); period-\(H\) seed; \(\pi\) formula;
Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ee.md` (this note)
- `research/cycle_ee.py`
- `research/cycle_ee.json`
