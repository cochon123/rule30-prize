# Cycle AD: white stripes, freshman Green, 00-production kills

Cycle AC asked for a CA production of one of the eight 5-window
preimages of centre `00`. Bounded-depth nested left cannot be that
production: each fixed left-diagonal meets the centred 5-window at
most five times. 1-run endings occur infinitely often, but occupy all
eight `11***` windows, only four of which yield `00`. White stripes
(\(e_j\) eventually 0) exist beyond \(e_2\), including \(e_7\) by a
closed form and \(e_28\) by the same implication on period-4 tails;
their onsets are `01`, not `00`. Not a prize claim: infinitely many
`00`s remain unproved.

Helper: `python3 research/cycle_ad.py --certify`. Dump:
`research/cycle_ad.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (freshman Green)

Over \(\mathrm{GF}(2)\),

\[
(1+x+x^2)^m
=\prod_{i:\,m_i=1}\bigl(1+x^{2^i}+x^{2^{i+1}}\bigr),
\]

so \(G(m,d)=[x^d](1+x+x^2)^m\) is the parity of the number of writings

\[
d=\sum_{i:\,m_i=1}\varepsilon_i,
\qquad
\varepsilon_i\in\{0,2^i,2^{i+1}\}.
\]

This is the generating-function form of Cycle AA’s doubling recurrence.
Certified against that recurrence on all \(m<40\). If \(m\) has no two
adjacent 1s, the pairs \(\{i,i+1\}\) are disjoint, so there is at most
one writing: \(G(m,d)=1\) iff the bits of \(d\) lie in those pairs and
no pair is taken as `11`. Certified on all such \(m<64\).

The dyadic annulus for \(I_k\) still sums over every \(m<2^{k-1}\),
not only Fibonacci \(m\). This is not a closed form for \(I_k\).

## Lemma (reset / integrator)

The left-diagonal recurrence is \(x_{t+1}=a_t\oplus(b_t\lor x_t)\) with
periodic drivers \((a,b)\) of joint period \(P\) (Cycle AC). If some
\(b=1\) on the tail (reset), the first such time forces
\(x'=a\oplus 1\), and the next reset \(P\) steps later repeats that
value, so the eventual period of \(x\) divides \(P\). If \(b\equiv 0\)
(integrator), then \(x_{t+1}=a_t\oplus x_t\): the period divides \(P\)
or \(2P\) according as the XOR of one period of \(a\) is \(0\) or \(1\),
and the phase is a free bit. This is the left-hand form of the
period-doubling observation recorded by Wolfram and proved for the
right-diagonals by Rowland; OEIS A363345 tracks the left periods.

## Lemma (white stripe)

If \(e_{j-2}\equiv e_{j-1}\not\equiv 0\) eventually, then
\(e_j(t+1)=a_t\oplus(a_t\lor e_j(t))\) with \(a=e_{j-2}\). The four
boolean cases give \(x'=0\) whenever \(a=1\) and \(x'=x\) whenever
\(a=0\). After the first 1 in the common tail, \(e_j\equiv 0\).
Certified as a 4-row truth table.

## Lemma (closed forms through \(e_9\))

On the prize orbit, packed bits satisfy, for all \(t\) at least the
stated onset (certified \(t<128\)):

| \(j\) | tail | onset |
| ---: | --- | ---: |
| 0 | \(1\) | \(0\) |
| 1 | \(1\) | \(1\) |
| 2 | \(0\) | \(2\) |
| 3 | \(t\bmod 2\) | \(3\) |
| 4 | \(1\) | \(4\) |
| 5 | \(t\bmod 2\) | \(5\) |
| 6 | \(t\bmod 2\) | \(6\) |
| 7 | \(0\) | \(7\) |
| 9 | \(1\) | \(9\) |

Proof: \(e_3'=e_1\oplus(e_2\lor e_3)=1\oplus e_3\) and \(e_3(3)=1\);
\(e_4'=e_3\lor e_4\) is sticky at 1 after \(e_4(4)=1\);
\(e_5'=e_3\oplus 1=\lnot e_3\);
\(e_6'=1\oplus(e_5\lor e_6)\) forces \(e_6(6)=0\) and then
\(e_6(t)=t\bmod 2\);
\(e_5\equiv e_6\not\equiv 0\) so the white-stripe lemma gives
\(e_7\equiv 0\) after \(e_7(7)=0\);
\(e_9'=e_8\lor e_9\) is sticky at 1 after \(e_9(9)=1\).

Thus \(e_7\) is a second white stripe, not only \(e_2\). The same
implication on the identified period-4 tails of \(e_{26}\) and
\(e_{27}\) (which agree and are not zero) yields \(e_{28}\equiv 0\)
after a transient of length 3. At the onsets,
\((c_2,c_3)=(0,1)\) and \((c_7,c_8)=(0,1)\); \((c_{28},c_{29})=(1,1)\).
White-stripe indices are not a production of centre `00`.

## Lemma (infinitely many 1-run endings)

Infinitely many 0s and 1s in \(c\) (Jen/Kopra plus monotonicity) give
infinitely many colour changes, hence infinitely many times with
\((c,c')=(1,0)\). Among the eight 5-windows with \((\ell,c)=(1,1)\),
exactly four produce a following `00`:

\[
01100,\quad 11101,\quad 11110,\quad 11111,
\]

and four produce an isolated 0:
`01101`, `01110`, `01111`, `11100`. Certified by enumerating the eight
neighbourhoods. Infinitely many centre `00`s is therefore infinitely
many 1-run endings in the first quartet (every 0-run of length
\(\ge 2\) starts at such an ending).

## Nested left and 1-run endings — killed as 00 productions

For each fixed \(j\), the spatial coordinate of \(e_j(t)\) is \(-t+j\),
which lies in the centred 5-window \([-2,2]\) iff
\(t\in[j-2,j+2]\), at most five times. No finite family of
left-diagonals — white stripes included — can occupy that window
infinitely often. The centre samples a new diagonal at every time.

On \(t<256\) every one of the eight `11***` windows occurs at a 1-run
ending (counts 29 `00` / 30 isolated), not a forced production.
**Killed** as an infinitude proof.

## Verdict

`LEMMA` (freshman \(G\); Fibonacci-binary \(G\); reset/integrator;
white-stripe implication; closed forms through \(e_9\); \(e_{28}\)
stripe; infinitely many `10`s; finite incidence of a fixed diagonal).
`KILLED` (nested-left 5-window `00`; 1-run ending forces `00`; only
\(e_2\) is a white stripe; white-stripe onset is `00`).
`OPEN` (infinitely many `00`s; infinitely many white stripes).
Wall time 0.01s. Prize unsolved.

## Files

- `research/cycle_ad.md` (this note)
- `research/cycle_ad.py`
- `research/cycle_ad.json`
