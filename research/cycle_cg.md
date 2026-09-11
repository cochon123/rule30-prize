# Cycle CG: odd \(2\)-copy scar drives have no later ident-\(0\) for \(|T_0|\in\{4,8\}\)

Unique continuation after ident-\(0\), \(T=T_0\|\lnot T_0\), ident-\(1\)
depends only on \(T\): every later packed bit is reconstructed from
those three. Every nonconstant \(T_0\) of length \(4\) (resp. \(8\))
produces no AND-triple and no later ident-\(0\) in the next \(80\)
(resp. \(130\)) bits. Length \(2\) always hits a second odd doubling.
Both implications with \(c\not\equiv 0\) still occur. The prize
\(k=4\) and \(k=8\) odd lifts are instances (\(\pi=4,8\), high tails
shorter than those windows). Not a prize claim: longer \(T_0\) and
the Fermat covering remain prefixes.

Helper: `python3 research/cycle_cg.py --certify` (~0.1s). Dump:
`research/cycle_cg.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (tail after ident-\(1\) is a function of \(T\))

Ident-\(1\) at \(I\) has driver \(T=\lambda_{I-1}\) and bit \(I\)
identically \(1\). Every later bit is the unique continuation of the
previous two, so the tail \(\lambda_{I+1},\lambda_{I+2},\ldots\) is
determined by \(T\). Pre-scar bits to the right of \(T\) do not
appear. Later ident-\(0\) at \(r\ge I+2\) is therefore an AND-triple
in this tail.

## Lemma (\(|T_0|=2\) always doubles again)

The two nonconstant blocks of length \(2\) are \(01\) and \(10\).
Both unique-continuation tails hit a later ident-\(0\) whose driver
XOR is odd (second doubling), within \(20\) steps. Exhaustive.

## Lemma (\(|T_0|=4\): no later ident-\(0\))

All \(14\) nonconstant blocks of length \(4\), \(80\) extra bits:
zero AND-triples, zero later ident-\(0\), zero second doublings.
Exhaustive. The prize \(k=4\) odd lift has \(\pi=4\) and only four
high bits.

## Lemma (\(|T_0|=8\): no later ident-\(0\))

All \(254\) nonconstant blocks of length \(8\), \(130\) extra bits:
zero AND-triples, zero later ident-\(0\), zero second doublings.
Exhaustive. The prize \(k=8\) odd lift has \(\pi=8\) and \(113\)
post-toggle bits.

## No both-implications after the scar — killed

The same exhaustions produce \(40\) and \(30\) later triples with
\(c\to a\), \(c\to b\), and \(c\not\equiv 0\). **Killed.** Those
triples still have \(011\), so they are not AND.

## Prefix (every \(2\)-power \(|T_0|\))

The same clean tail is not proved for \(|T_0|\ge 16\) on a window
as long as the next high half. **PREFIX**, not a theorem for every
odd lift. Combined with Cycle BY this keeps \(r\le 1\) and the
period-\(H\) seed as prefixes for all \(k\).

## Verdict

`LEMMA` (tail is a function of \(T\); \(|T_0|=2\) always doubles
again; \(|T_0|=4\) and \(8\) have no later ident-\(0\) on those
windows).
`PREFIX` (every \(2\)-power \(|T_0|\); at most one odd toggle for
all \(k\); seed for all \(k\); Fermat covering).
`KILLED` (no both-implications with \(c\not\equiv 0\) after the
scar).
`OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often). Prize unsolved.

## Files

- `research/cycle_cg.md` (this note)
- `research/cycle_cg.py`
- `research/cycle_cg.json`
