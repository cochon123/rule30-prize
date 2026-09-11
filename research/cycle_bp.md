# Cycle BP: 9-fold unique bit \(p=5U+1\) fires

Cycle BF: packed bit \(p=5U+1\) is unique-Green on the 9-fold annulus
and fires iff \(\gamma_k:=c_{5U}\land r_{5U}\). That AND vanished on
\(3\le k\le 12\), which was a prefix, not a theorem. Packed samples
give \(\gamma_{13}=\gamma_{14}=1\) and \(\gamma_{15}=0\). Hence
\(c_{5\cdot 2^k}\land r_{5\cdot 2^k}\) is not identically 0, and the
9-fold unique XOR is not identically \(\alpha_k\). Not a prize claim:
the Fermat covering remains a prefix.

Helper: `python3 research/cycle_bp.py --certify` (~1.3s). Dump:
`research/cycle_bp.json`. Packed centre matches `experiment.center_bits`
on 20 bits.

## Lemma (\(\gamma_{13}=\gamma_{14}=1\))

Let \(U=2^k\). Direct evolution of the prize packed row gives the
centre-right pair at time \(5U\) for \(2\le k\le 15\):

| \(k\) | \(c_{5U}\) | \(r_{5U}\) | \(\gamma_k\) |
|------:|:----------:|:----------:|:------------:|
| 2–12 | 0 or 1 | 0 or 1 | 0 |
| 13 | 1 | 1 | 1 |
| 14 | 1 | 1 | 1 |
| 15 | 0 | 0 | 0 |

Neither factor is identically 0: \(c_{5U}=1\) already at \(k=6\), and
\(r_{5U}=1\) already at \(k=5\). They first become 1 together at
\(k=13\). Cycle BF’s Mersenne uniqueness still says this bit is the
unique Green slot for \(p=5U+1\) on the 9-fold annulus, for every
\(k\ge 1\); only the firing vanishes on the short prefix.

## \(\gamma_k\equiv 0\) — killed

The vanishing through \(k=12\) does not persist. **Killed** as a
theorem, and as the claim that the 9-fold unique XOR equals
\(\alpha_k=c_U\land r_U\) for every \(k\). \(\alpha_k\) itself still
takes both values on this range (1 at \(k=3,7,10,13,15\)).

## Verdict

`LEMMA` (\(\gamma_{13}=\gamma_{14}=1\); \(\alpha_k\) takes both
values). `KILLED` (\(\gamma_k\equiv 0\); 9-fold unique XOR
identically \(\alpha_k\)). `PREFIX` (Fermat covering for all
\(k\ge 2\)). `OPEN` (some \(\varphi^{(q)}_k=1\) infinitely often).
Prize unsolved.

## Files

- `research/cycle_bp.md` (this note)
- `research/cycle_bp.py`
- `research/cycle_bp.json`
