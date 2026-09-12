# Cycle EK: every \(n_0=2\) scar has at most one odd in \(k=16\); seed at \(k=17\)

Cycle EJ: \(n_0=2\) scars have at most one odd in each annulus
\(2..15\) and the period-\(H\) seed at \(k=16\). Extra 87468 from
\(k=8\) lands entirely in \(k=16\) (6 of 16 even-52809 words); the
other ten, including prize \(T_0\), have no odd in 131000 extras,
which covers that \(k=16\) window. After 87468, \(n_0=16\) has no
ident-0 in 262144 extras (Cycle DR), and leftover after the 87468
image is \(131072-87979=43093<262145\), so those six words have no
second ident-0 in \(k=16\) leftover. Hence at most one odd in
\(k=16\) on every \(n_0=2\) scar, and \(\pi_{17}\in\{16,32\}\)
divides \(2^{16}\). Kills: a \(k=16\) odd for every \(n_0=2\) scar.
Do **not** claim the seed for all \(k\). Do **not** bump \(n_0=16\)
extras past \(2^{18}\). Do **not** claim an 11-bit gap. Do **not**
compute \(\varphi^{(3,5,9)}\) at \(k=16\).

Not a prize claim: seed at \(k=17\) for \(n_0=2\) scars does not give
covering never-fail.

Helper: `python3 research/cycle_ek.py --certify`. Dump:
`research/cycle_ek.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles DR, DU, EH, EJ (no new packed run, no Fermat
table, no \(n_0=16\) window bump).

## Lemma (87468 lands in \(k=16\); leftover shorter than \(E_{16}\))

Image of extra 87468 from \(k=8\) is \((87724,87979]\subset(2^{16},2^{17}]\).
Leftover after the right endpoint is 43093. Cycle DR:
\(E_{16}=262145>43093\).

## Lemma (131000 extras cover the \(k=16\) window from \(k=8\))

The image stays in \(k=16\) for extra \(\le 130561\). Cycle EH scanned
131000 extras. Six words odd-double at 87468; ten have no odd in that
window.

## Lemma (period-\(H\) seed at \(k=17\) for every \(n_0=2\) scar)

At most one odd in annulus 16, on top of Cycle EJ’s counts through 15.
Then \(\pi_{17}=16\) or \(32\), both dividing \(2^{16}\). Cycle DU:
at most one odd per annulus implies the seed.

## Killed

Not every \(n_0=2\) scar has a \(k=16\) odd: ten of sixteen 52809-family
words, including prize \(T_0\), have none in the \(k=16\) window.

## Verdict

`LEMMA` (87468 from \(k=8\) lands in \(k=16\); leftover \(<E_{16}\);
131000 covers the window; at most one odd in \(k=16\) on \(n_0=2\);
period-\(H\) seed at \(k=17\) for every \(n_0=2\) scar).
`KILLED` (\(k=16\) odd for every \(n_0=2\) scar).
`PREFIX` (at-most-one-odd for all \(k\); seed for all \(k\); \(\pi\)
formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ek.md` (this note)
- `research/cycle_ek.py`
- `research/cycle_ek.json`
