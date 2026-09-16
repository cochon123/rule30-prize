# Period-2 \(L_0\): every extra \(\ge 3\) clip descends by 2 at \(T+2\)

Checked lemma: a ugap onset (isolated or bump) whose Q-forced tail
clips with extra \(e\ge 3\) — by `11`, `00000`, or even \(F_{2n}>T\) —
has \(Su\) a bump of the same clip kind at \(T+2\) with extra \(e-2\).
Isolated onsets become bumps; bumps stay bumps. Extra of every finite
clip family is a rank. Uniform extra \(\le 8\) is equivalent to extra
\(\le 8\) at every \(S\)-minimal member, which is **not** proved.
Infinite \(B_0\) is a fixed point of \(e\mapsto e-2\). Not a prize
claim.

Helper: `python3 research/period2_alldesc.py --certify`. Dump:
`research/period2_alldesc.json`. Skip identity from
`research/period2_qshift.md`; \(B_0\) pattern from
`research/period2_b0.md`; clip-to-\(R\) from
`research/period2_qextra.md`; bump 11 special case from
`research/period2_exdesc.md`.

## Lemma (skip and \(nvars\) for extra \(\ge 3\))

Write \(n_0=\mathrm{nvars}(T)\) and \(n_\ast=n_0+e\). Then
\(\mathrm{nvars}(T+2)=n_0+1\), so a clip of \(Su\) at \(n_\ast-1\)
has extra \(e-2\). Extra \(e\ge 3\) gives
\(R\ge 6\) on a `11`/`00000`-clip and \(R\ge 5\) on an even-\(F\)
clip, hence \(R\ge 4\) (the \(B_0\) hypothesis) and the three-zero
skip at both \(n_\ast\) and \(n_\ast-1\). The four-zero even skip
window \(2n_\ast-4>T\) holds as well. Certified as arithmetic for
every \(T\in[5,80]\) and \(e\in[3,11]\).

## Lemma (all-class extra descent)

Assume a ugap onset at \(T\neq 4\) with extra \(e\ge 3\). The
\(B_0\) identities send \(u\) to a bump at \(T+2\): isolated
\(R\ge 4\) gives \(F_{T+1}(Su)=F_{T+2}(Su)=1\), and a bump
\(R\ge 4\) does the same via \(B_0(S)\mapsto B_0(S+2)\) at
\(S=T-1\). The skip identities then propagate the clip: a `11` or
`00000` at \(n_\ast\) becomes the same clip of \(Su\) at \(n_\ast-1\);
an even fire \(F_{2n_\ast}(u)=1\) becomes \(F_{2n_\ast-2}(Su)=1\).
An earlier clip of \(Su\) would pull back, under the same skip, to an
earlier clip of \(u\), which does not exist. Hence \(Su\) is a bump of
the same clip kind at \(T+2\) with extra \(e-2\).

Certified on every ugap onset of extra \(\ge 3\) through \(T=40\):
1761 onsets, 1761 descents, 0 failures, of which 860 are isolated
(all become bumps). Class counts: bump `11` 122, bump even-\(F\) 774,
bump `00000` 5, isolated `11` 135, isolated even-\(F\) 703, isolated
`00000` 22. Max extra is still \(8\), uniquely at \(T=20\) and
\(T=37\) (bump `11`). Isolated max extra is \(7\), attained at
\(T=33,35,37,38,40\).

The \(T=20\) and \(T=37\) bump `11` extra-\(8\) families descend to
extra \(6\) as in `research/period2_exdesc.md`. The three \(T=33\)
isolated even-\(F\) extra-\(7\) words (shared tail `00010100100100`,
\(R=14\)) descend to bump even-\(F\) extra \(5\) at \(T=35\).

## Corollary (rank, not a bound)

Iterating, every finite clip of extra \(e\ge 3\) reaches extra
\(<3\) after \(\lfloor(e-1)/2\rfloor\) shifts of \(+2\) in \(T\).
Isolated onsets of extra \(\ge 3\) are births of bump families.
A uniform extra \(\le 8\) for *all* ugap onsets is therefore the
statement that no \(S\)-minimal member has extra \(\ge 9\). That
statement is a census through \(T=40\), not a theorem.

## What this does not do

\(S\)-minimal extra is not bounded independently of \(T\). Infinite
\(B_0\) (infinite extra) is a fixed point of \(e\mapsto e-2\) and is
not killed. A probe through \(T=48\) still has extra \(\le 8\), with
isolated even-\(F\) extra \(=8\) at \(T=43\); that probe is not in
the certificate. Other periods of \(c_t\) are untouched.

## Verdict

`LEMMA`, wall time ~8s.

- Kill of period 2: no.
- Extra rank on every clip class: yes.
- Isolated extra \(\mapsto\) bump extra\(-2\): yes.
- Uniform extra \(\le 8\): no.

## Files

- `research/period2_alldesc.md` (this note)
- `research/period2_alldesc.py` (`--certify`)
- `research/period2_alldesc.json` (dump)
