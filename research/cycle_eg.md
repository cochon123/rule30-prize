# Cycle EG: even-52809 leaves no later odd in its \(k=15\) landing

Every length-8 \(T_0\) in Cycle DM’s even-52809 family (16 words,
including prize `00000110` and all eight FAM372 unfolds) has first
ident-0 extra 52809 even. From \(k=8\) that extra lands in annulus
\(k=15\). The next odd extra is 87468 on six words (remaining 34659)
and none in 131000 on the other ten (remaining \(>78191\)), both
strictly larger than \(2^{15}\). Worst-case leftover in \(k=15\) is
\(2^{15}=32768<34659\), so a later odd cannot fit in that high half.
The six 87468 words land in \(k=16\), which is
\(\mathrm{threshold}(34659)\); \(2^{16}=65536>34659\) so they can fit
there. Kills: leftover after even 52809 empty at every later \(k\);
next odd after 52809 forced before \(k=16\). Do **not** claim a closed
form for 34659/87468. Do **not** equate scar extra 87468 with packed
bit 87867 on prize \(T_0\). Do **not** claim an 11-bit gap. Do **not**
compute \(\varphi^{(3,5,9)}\) at \(k=16\).

Not a prize claim: skipping a second odd in \(k=15\) does not fill
later annuli.

Helper: `python3 research/cycle_eg.py --certify`. Dump:
`research/cycle_eg.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles DM, ED, EE, EF (no new packed run, no Fermat
table, no \(n_0=16\) window bump).

## Lemma (52809-family next odd is 87468 or none in 131000)

All 16 words have first ident-0 extra 52809 even. Six scar-odd-double
at extra 87468; ten, including prize `00000110`, have no odd ident-0
in 131000 extras (the \(k=16\) window from \(k=8\)). Remaining extra
is 34659 or \(>78191\).

## Lemma (remaining 34659 exceeds \(k=15\) leftover)

\(\mathrm{threshold}(34659)=16\) because \(2^{15}<34659\le 2^{16}\).
Worst-case leftover in annulus \(k=15\) is \(2^{15}=32768<34659\).
Prize leftover after the even at packed 53208 is
\(2^{16}-53208=12328<34659\). Extra 52809 from \(k=8\) lands entirely
in \(k=15\). So neither the worst-case nor the prize leftover can hold
the next odd.

## Lemma (at \(k=16\), remaining 34659 can fit)

At the remaining-threshold \(k=16\), \(2^{16}=65536>34659\). The six
87468 words land in annulus 16 from \(k=8\). This is Cycle ED’s
skip-becomes-dangerous pattern for the post-even gap, not for the
first odd extra 26357.

## Killed

Leftover after even 52809 is not empty at every later \(k\): six words
odd-double at extra 87468 in \(k=16\). The next odd is not forced
before \(k=16\); it occurs at \(k=16\) or later.

## Verdict

`LEMMA` (52809-family next odd 87468 or none in 131000; remaining
\(>2^{15}\); \(k=15\) worst leftover cannot fit the next odd; prize
\(k=15\) leftover cannot; \(\mathrm{threshold}(34659)=16\)).
`KILLED` (leftover after 52809 empty at every later \(k\); next odd
after 52809 before \(k=16\)).
`PREFIX` (closed form for 87468; scar 87468 is packed 87867 on prize
\(T_0\); at-most-one-odd for all \(k\); period-\(H\) seed; \(\pi\)
formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_eg.md` (this note)
- `research/cycle_eg.py`
- `research/cycle_eg.json`
