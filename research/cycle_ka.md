# Cycle KA: packed AND is not the trinomial adjacent AND

Rule 30 is \(a\oplus(b\lor c)=(a\oplus b\oplus c)\oplus(b\land c)\).
Packed AND fires on `AND_ONES` \(=\) FRESH \(\cup\) CONT. Trinomial
AND fires on FRESH \(\cup\{1111\}\). They disagree on CONT vs
\(1111\). Covering \(J\) is packed AND on \(G=1\), **not** trinomial
AND. Packed AND is **not** trinomial AND. Trinomial AND does **not**
vanish on \(G=1\). Do **not** claim
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not** push
the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: naming the nonlinear \(b\land c\) correction still
leaves packed AND on \(G=1\) (CONT and FRESH both fire), so covering
never-fail stays open.

Helper: `tri_bit`, `tri_and`, `TRI_ONES`. Certify:
`python3 research/cycle_ka.py --certify` (~0.11s).
Dump: `research/cycle_ka.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
AL/CA/GU/HF/HG/HH/HI/HU/JZ (\(16\)-row; covering \(k\le 6\); no
Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (Rule 30 is trinomial XOR adjacent AND)

On all \(16\) even-\(s\) 4-tuples,
\(a\oplus(b\lor c)=(a\oplus b\oplus c)\oplus(b\land c)\) and
\(z\oplus(a\lor b)=(z\oplus a\oplus b)\oplus(a\land b)\). Packed AND
is the product of those two Rule-30 bits.

## Lemma (trinomial AND is FRESH \(\cup\{1111\}\))

`tri_and` fires on `TRI_ONES` \(=\{0010,0100,1001,1111\}\). Packed
AND fires on `AND_ONES`. The symmetric difference is CONT \(0011\)
vs DIE \(1111\).

## Lemma (covering packed AND disagrees with trinomial AND)

Packed covering \(J_6,J_{10}\) for \(k\le 6\): \(G=1\) packed AND
\(4522\) (FRESH \(3376\), CONT \(1146\)); trinomial AND \(4543\)
(FRESH \(3376\), \(1111\) \(1167\)); disagreements \(2313\) all
CONT or \(1111\). Odd-\(s\) packed \(J\) XOR matches Cycles HF/HG
and is **not** the trinomial XOR.

## Killed

Packed AND equals trinomial AND: at \(k=1\), \(s=13\), \(n=3\),
\(j=1\), packed \(0011\), packed AND \(1\), trinomial AND \(0\),
\(p=18\). Covering \(J\) equals XOR of trinomial AND on \(G=1\):
the same witness. Trinomial AND vanishes on \(G=1\): at \(k=1\),
\(s=17\), \(n=1\), \(j=2\), packed \(1111\), trinomial AND \(1\),
packed AND \(0\), \(p=16\).

## Verdict

`LEMMA` (Rule 30 is trinomial XOR adjacent AND; trinomial AND is
FRESH \(\cup\{1111\}\); covering packed AND disagrees with
trinomial AND).
`KILLED` (packed AND equals trinomial AND; covering \(J\) equals
XOR of trinomial AND on \(G=1\); trinomial AND vanishes on \(G=1\)).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ka.md` (this note)
- `research/cycle_ka.py`
- `research/cycle_ka.json`
