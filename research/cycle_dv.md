# Cycle DV: \(\operatorname{ham}(n_3,n_4)=n_0\) after odd doubling; \(I=0\) dual

Unique continuation of \((1,s)\) is the NOR recurrence
\(u_{t+1}=\operatorname{NOR}(s_t,u_t)\). If \(s\) is an odd 2-copy of
half-length \(n_0\), then \(\operatorname{ham}(n_3,n_4)=n_0\) where
\(n_3=\operatorname{reconstruct}(1,s)\) and
\(n_4=\operatorname{reconstruct}(s,n_3)\). After an odd ident-0 the
scar is O-type of length \(2\pi\), so the first type-N pair differs in
exactly \(\pi\) bits and cannot be equal. That is every odd 2-copy, not
only the prize toggle. It fails for a generic \(s\). Do **not** claim
\(\operatorname{ham}(s,n_3)=n_0\), and do **not** claim the first
odd-weight bit is at offset \(+3\).

Covering never fails iff
\(\varphi^{(6)}=\varphi^{(10)}=I\Rightarrow\varphi^{(18)}\ne I\). The
\(I=0\) slice is \(\varphi^{(6)}=\varphi^{(10)}=I=0\Rightarrow
\varphi^{(18)}=1\). On Cycle DS that antecedent occurs only at \(k=15\),
where \(\varphi^{(18)}=1\). Together with Cycle DT’s \(11\Rightarrow 0\)
(the \(I=1\) slice), both covering-relevant slices hold through
\(k=18\). Do **not** compute \(\varphi^{(3,5,9)}\) at \(k=16\).

Not a prize claim: Hamming \(n_0\) does not fill an annulus, and the
dual remains a prefix.

Helper: `python3 research/cycle_dv.py --certify`. Dump:
`research/cycle_dv.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles DS/DT (no new packed run).

## Lemma (NOR form; shifted-not preserves O; first-three Hamming \(n_0\))

For every nonzero \(s\), \(\operatorname{reconstruct}(1,s)_{t+1}
=1\oplus(s_t\lor u_t)\). If \(O\) is O-type of half-length \(n_0\) then
\(O_{t+n_0}=\neg O_t\), so \(s_t=\neg O_{t-1}\) satisfies
\(s_{t+n_0}=\neg s_t\). Weight of an O-type is \(n_0\), hence
\(\operatorname{ham}(0,O)=\operatorname{ham}(O,1)=\operatorname{ham}(1,s)
=n_0\). Certified for \(1\le n_0\le 8\) (weight/Hamming) and
\(1\le n_0\le 10\) (shifted-not).

## Lemma (\(\operatorname{ham}(n_3,n_4)=n_0\) on every odd 2-copy)

For every odd 2-copy \(s\) of half-length \(n_0\in\{1,\ldots,8,10,12\}\)
(exhaustive) and 80 random length-16 odd 2-copies,
\(\operatorname{ham}(n_3,n_4)=n_0\). On even half-length, \(n_3\) is
type N (Cycle DH). Prize \(k=4,8,16\): after the odd toggle at packed
bits \(29,400,87867\), the scar is O-type and
\(\operatorname{ham}(n_3,n_4)=\pi\in\{4,8,16\}\). So those consecutive
bits cannot be equal, with Hamming exactly the pre-doubling period.

## Generic \(s\), \(\operatorname{ham}(s,n_3)=n_0\), first odd-weight at \(+3\) — killed

Length-8 non-O-type \(s\) realize Hamming \(\{3,4,5\}\), not \(\{4\}\).
Length-4 odd 2-copies have \(\operatorname{ham}(s,n_3)\in\{3,6\}\), not
\(\{4\}\). First odd xorcat after \((0,O,1)\) on length-4 scars is at
\(n_3\) or two steps later, not always at offset \(+3\); the \(k=16\)
prize is offset \(+7\) (Cycle DH). **Killed** as identities.

## Lemma (covering never-fail iff matched complement; dual kills \(I=0\))

Write \(a=\varphi^{(6)}\), \(b=\varphi^{(10)}\), \(g=\varphi^{(18)}\),
\(I=I_{k+1}\). Covering fails iff \(a=b=g=I\), iff it is not the case
that \(a=b=I\Rightarrow g\ne I\). The \(I=0\) slice
\(a=b=I=0\Rightarrow g=1\) forbids the all-zero kernel. Certified on
all bit tuples. Cycle DT’s \(11\Rightarrow 0\) is the \(I=1\) slice.

## Prefix (dual on \(2\le k\le 18\))

Cycle DS even spines: \(I=\varphi^{(6)}=\varphi^{(10)}=0\) only at
\(k=15\), and \(\varphi^{(18)}=1\) there. Match-00 rows at
\(k=13,14,15,17\) are otherwise \(I=1\). No \(I=0\) dangerous row.
**PREFIX**, not a theorem that
\(I=\varphi^{(6)}=\varphi^{(10)}=0\Rightarrow\varphi^{(18)}=1\) for all
\(k\). Hamming \(n_0\) delays the next equal type-N pair by one extra
and does not fill a dyadic annulus.

## Verdict

`LEMMA` (NOR form; shifted-not preserves O; first-three Hamming \(n_0\);
\(\operatorname{ham}(n_3,n_4)=n_0\) on O-type; prize \(k=4,8,16\);
covering never-fail iff matched complement; dual kills the \(I=0\)
kernel).
`PREFIX` (dual on \(2\le k\le 18\); dual / Fermat covering / period-\(H\)
seed / \(\pi\) formula for all \(k\)).
`KILLED` (Hamming \(n_0\) for generic \(s\);
\(\operatorname{ham}(s,n_3)=n_0\); first odd-weight always at offset
\(+3\)).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_dv.md` (this note)
- `research/cycle_dv.py`
- `research/cycle_dv.json`
