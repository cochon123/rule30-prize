# Period-2 \(L_0\): extra descent at \(T+2\), kernels \(\{0,1\}\) for SFT clips

Checked lemma: a ugap onset (isolated or bump) whose Q-forced tail
clips by `11` or `00000` with extra \(e\ge 2\), or by even \(F_{2n}>T\)
with extra \(e\ge 3\) (and also \(e=2\) at odd \(T\)), has \(Su\) a
bump of the same clip kind at \(T+2\) with extra \(e-2\). Isolated
onsets become bumps. Extra of every finite clip family is a rank;
`11`/`00000` kernels are extra in \(\{0,1\}\). Uniform extra \(\le 8\)
is equivalent to extra \(\le 8\) at every \(S\)-minimal member, which
is **not** proved. Infinite \(B_0\) is a fixed point of
\(e\mapsto e-2\). Not a prize claim.

Helper: `python3 research/period2_alldesc.py --certify`. Dump:
`research/period2_alldesc.json`. Skip identity from
`research/period2_qshift.md`; \(B_0\) pattern from
`research/period2_b0.md`; clip-to-\(R\) from
`research/period2_qextra.md`; bump 11 special case from
`research/period2_exdesc.md`.

## Lemma (skip at \(n_\ast\) for extra \(\ge 2\))

Write \(n_0=\mathrm{nvars}(T)\) and \(n_\ast=n_0+e\). Then
\(\mathrm{nvars}(T+2)=n_0+1\), so a clip of \(Su\) at \(n_\ast-1\)
has extra \(e-2\). The three-zero skip begins at extra index \(2\):
\(2(n_0+1)-3\le T<2(n_0+2)-3\). Extra \(e\ge 2\) therefore gives the
skip at \(n_\ast\), which is enough to copy the clip bit
\(Q_{n_\ast}(u)=Q_{n_\ast-1}(Su)\). A `11`/`00000`-clip has
\(R\ge 4\) (the \(B_0\) hypothesis). An even-\(F\) clip has \(R\ge 5\)
once \(e\ge 3\), and \(R=4\) at extra \(2\) on odd \(T\). Certified as
arithmetic for every \(T\in[5,80]\) and \(e\in[2,11]\).

The skip at \(n_\ast-1\) is *not* required for a `11`-clip of \(Su\):
the last bit of the length-\(n_\ast-1\) prefix of \(Su\) is
\(u_{n_\ast-1}\), already \(1\) by the clip of \(u\).

## Lemma (all-class extra descent)

Assume a ugap onset at \(T\neq 4\) meeting the extra threshold above.
The \(B_0\) identities send \(u\) to a bump at \(T+2\). The skip at
\(n_\ast\) propagates the clip: a `11` or `00000` at \(n_\ast\)
becomes the same clip of \(Su\) at \(n_\ast-1\); an even fire
\(F_{2n_\ast}(u)=1\) becomes \(F_{2n_\ast-2}(Su)=1\). An earlier clip
of \(Su\) would pull back to an earlier clip of \(u\), which does not
exist. Hence \(Su\) is a bump of the same clip kind at \(T+2\) with
extra \(e-2\).

At extra \(=2\) the clip of \(Su\) is at the first Q-index
\(\mathrm{nvars}(T+2)\), so no earlier clip is possible.

Certified through \(T=40\): 3040 claimed onsets, 3040 descents, 0
failures. `11` extra \(\ge 2\): bump 352, isolated 374. `00000` extra
\(\ge 2\): bump 35, isolated 40. Even-\(F\) extra \(\ge 3\), plus extra
\(=2\) at odd \(T\): bump 1232, isolated 1007. Max extra is still
\(8\), uniquely at \(T=20\) and \(T=37\) (bump `11`). Isolated max
extra is \(7\).

The \(T=20\) and \(T=37\) bump `11` extra-\(8\) families descend to
extra \(6\). The three \(T=33\) isolated even-\(F\) extra-\(7\) words
(shared tail `00010100100100`, \(R=14\)) descend to bump even-\(F\)
extra \(5\) at \(T=35\); they are not \(S\)-minimal births, but
\(R=3\) images of bump even-\(F\) extra \(=2\) at \(T=32\)
(`research/period2_r3pull.md`).

## Corollary (rank, not a bound)

Iterating, every finite `11`/`00000`-clip of extra \(e\ge 2\) reaches
extra \(\in\{0,1\}\) after \(\lfloor e/2\rfloor\) shifts of \(+2\) in
\(T\). Even-\(F\) families reach extra \(<3\), or extra \(<2\) along
odd \(T\). Isolated onsets meeting the threshold are births of bump
families. A uniform extra \(\le 8\) for *all* ugap onsets is the
statement that no \(S\)-minimal member has extra \(\ge 9\). That
statement is a census through \(T=40\), not a theorem.

## What this does not do

\(S\)-minimal extra is not bounded independently of \(T\). Infinite
\(B_0\) (infinite extra) is a fixed point of \(e\mapsto e-2\) and is
not killed. Even-\(F\) extra \(=2\) at even \(T\) has \(R=3\), below
the \(B_0\) threshold, and is not this identity. Under \(S\) it
becomes an isolated onset at \(T+1\) (`research/period2_r3iso.md`),
without an extra rank. A probe through
\(T=48\) still has extra \(\le 8\), with isolated even-\(F\) extra
\(=8\) at \(T=43\); that probe is not in the certificate. Other
periods of \(c_t\) are untouched.

## Verdict

`LEMMA`, wall time ~8s.

- Kill of period 2: no.
- Extra rank on every clip class: yes.
- `11`/`00000` extra \(\ge 2\): yes.
- Isolated extra \(\mapsto\) bump extra\(-2\): yes.
- Uniform extra \(\le 8\): no.

## Files

- `research/period2_alldesc.md` (this note)
- `research/period2_alldesc.py` (`--certify`)
- `research/period2_alldesc.json` (dump)
- `research/period2_silent.md` (\(u_0\) silent in \(F_k\) for \(k\ge 3\))
- `research/period2_gsilent.md` (\(u_1\) silent in \(G_k\) for \(k\ge 8\))
- `research/period2_r3iso.md` (\(R=3\) even fire \(\mapsto\) isolated at \(T+1\))
- `research/period2_r3pull.md` (\(T=33\) isolated extra \(=7\) is an \(R=3\) image)
