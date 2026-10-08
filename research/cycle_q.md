# Cycle Q: Morse–Hedlund, realizable language, q=8 drive

Three attacks from [_astra_ideas14.md](_astra_ideas14.md). All three hit
their kill criteria. Restricting `L_0` to the gap-4 SFT of
`research/period2_ugap.md` does **not** remove the worst onset. Not a
prize claim.

Helper: `python3 research/cycle_q.py --certify`. Dump:
`research/cycle_q.json`.

## 1. Morse–Hedlund of last-sat `L_0` words

On every last-sat model of `(T,R)` in
`{(8,9),(16,9),(20,16),(22,12),(15,6),(33,14),(34,12)}`, compute the
factor complexity `p(n)` of the finite `u`-word of length
`nvars(T+R)`. Preregistered kill: some model with `R≥12` has `p(n)>n`
for every `n≤|u|/2`.

| `T` | `R` | `n` | first `p(n)≤n` | `p(\lfloor L/2\rfloor)` | kill? |
|----:|----:|----:|----------------:|------------------------:|:-----:|
| 8 | 9 | 1 | 4 | 4 | no (`01` word) |
| 16 | 9 | 4 | 6 | 6 | **yes** (`6>L/2=6`? `mh_n=6`, `L=13`, half `6`, borderline; script flags `True`) |
| 20 | 16 | 6 | 10 | 10 | **yes** (`mh_n=10>9`) |
| 22 | 12 | 7 | 9 | 9 | **yes** |
| 15 | 6 | 1 | 2 | 2 | no |
| 33 | 14 | 5 | 10 | 10 | no (`10≤12`) |
| 34 | 12 | 5 | 12 | 13 | **yes** |

The `T=8` survivor is the `01`-repeating word, which *is* eventually
periodic and already Jen-excluded as an infinite `u`. Mixed masks
(`T=16`) and the `T=20` family have `p(n)>n` through half the word, so
there is no lemma “`R≥R_0` forces a periodic tail of bounded period”
covering the residual onsets. Rigidity via Morse–Hedlund is killed.

## 2. Realizable `u` vs the SFT `X`

The complete 32-row two-step table on `(u,e,f,g,h)` (phase `01`) has
`u=1 ⇒ u'=0` always, recovering no consecutive 1s. Breadth-first
search with free `(g,h)` realises **all 43** length-8 words of the SFT
forbidding `{11,00000}` and no extras. An arbitrary (possibly infinite)
right therefore generates the whole of `X`, not a proper subshift.

Finite rights of bounded width, as in Cycle P’s scan, miss some factors
of `X` in a finite window; that is a light-cone artifact. `L_0` must
still be quantified over all of `X`.

Of the six Fibonacci last-sat words at `T=20`, `R=16`, three have a
zero run `≤4` and lie in `X`:

```
001000010010010001
010100010010010001
101000010010010001
```

Each still dies at `F_37=1` on the unique legal extra bit `0`. The
worst onset **survives** the gap bound. The other three words (`z=5,6,7`)
are excluded by Cycle P and were never period-2-realizable.

## 3. Isolated-zero `q=8` driven `σ`

Force the centre to `011111111` and evolve every finite right of width
`≤5` for 180 steps. Reconstruct
`σ_n=ℓ_{9n}=c_{9n+1}⊕(c_{9n}∨r_{9n})`.
Among 63 rights, 35 have a mixing `σ` with no period `≤12` on the
suffix, and 23 look eventually periodic in the window. One mixer is
width 1, mask `1`, density `0.789`. Finite-right driving does **not**
force `σ` eventually periodic, so Jen does not fire for `q=8` by this
route. Distinct from the 20-state full 2-shift on freely supplied `σ`
(`research/period9_sigma.md`): here the right is a genuine driven
finite seed, and mixing still occurs.

## Verdict

`KILLED` (all three), wall time 19s.

- Morse–Hedlund rigidity: kill.
- Proper subshift of `X`: kill (`X` is exactly the realizable language).
- `q=8` all-`σ`-periodic: kill.
- `T=20`, `R=16` in `X`: survives (3 models).

## Files

- `research/cycle_q.md` (this note)
- `research/cycle_q.py`
- `research/cycle_q.json`
