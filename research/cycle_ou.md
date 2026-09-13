# Cycle OU: clip-removed \(S\) of \(n=8t+3\) is the 8-scale off0 image of \(G(t)\)

Cycle OL writes unclipped pal-right \(S(8t+3)\) as the pal-right
off-residue-0 xor of \(G(t)\); Cycle OO evaluates that xor as \(1\)
for \(t\ge 1\). Even-halve \(G(2t,2e)=G(t,e)\) and two Green
doublings stretch pal-right of \(t\) by eight onto pal-right of
\(n=8t+3\). Off-residue-0 ones land at fire-images
\(j=8(t+d)+5\) when \(d\bmod 3=1\) and \(j=8(t+d)\) when
\(d\bmod 3=2\); residue 2 also has a silent partner at
\(j=8(t+d)+3\). Clip-removed pal-right \(S\) is therefore the xor
of \(G(t,t+d)\) over those off0 \(d\) with fire-image \(j>j_{\max}\).
This holds for every \(j_{\max}\), not only covering \(5\cdot 2^k\).

On covering \(q=10\), the xor of those rem bits over \(n=8t+3\) is
\(1\) iff \(k\ge 2\) and \(k\) is even, through \(k\le 8\). This is
**not** a single \(d_{\min}\) tail of off0 (\(n=11\),
\(j_{\max}=20\): rem \(=1\), tail \(=0\)). **Not** Cycle OT's
\(8t+7\) fold. **Not** covering \(S\) for all \(k\). **Not**
\(E_k=0\) for all \(k\). Do **not** catalogue further \(S\)/\(T\)
subregions unless the experiment answers why \(E_k=0\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).

Certify: `python3 research/cycle_ou.py --certify` (~0.17s).
Dump: `research/cycle_ou.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/OL/OS/OT/OG (8-scale off0 image of \(S(8t+3)\); prefix
OT \(8t+7\) fold, OS even-parent rem, OL off0, OG \(E_k\); no
Fermat table, no extra window, no \(n_0=16\) window, no packed
covering \(k=11\)).

## Lemma (fire-image of off0 on \(n=8t+3\))

S-fires of \(n=8t+3\) are \(j=8(t+d)+5\) for pal-right \(d\equiv 1
\pmod{3}\) with \(G(t,t+d)=1\), and \(j=8(t+d)\) for
\(d\equiv 2\pmod{3}\) with \(G(t,t+d)=1\). Status: **lemma**.
Checked on \(t<48\).

## Lemma (clip-removed \(S(8t+3)\) is that image past \(j_{\max}\))

\(\mathrm{removed}\_S(8t+3,j_{\max})\) equals the xor of
\(G(t,t+d)\) over off-residue-0 \(d\) with fire-image \(j>j_{\max}\).
Status: **lemma** for every \(j_{\max}\). Checked on \(t<48\) and
on covering \(q=10\), \(k\le 8\).

## Killed

Naive 8-scale tail \(d_{\min}=j_{\max}/8-t+1\): \(n=11\),
\(j_{\max}=20\) has rem \(=1\) against tail \(=0\). Cycle OT fold
on \(n=8t+3\): \(n=51\), \(j_{\max}=80\) has rem \(=1\) against
the \(8t+7\) parent rem \(=0\).

## Verdict

`LEMMA` (8-scale off0 fire-image; clip-removed \(S(8t+3)\);
even-parent rem; \(8t+7\) clip fold).
`CERTIFIED` (covering \(n=8t+3\) rem xor \(=1\) iff \(k\ge 2\) even,
\(k\le 8\); \(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (single \(d_{\min}\) off0 tail; OT fold on \(n=8t+3\)).
`PREFIX` (covering \(S\) for all \(k\); \(E_k=0\) for all \(k\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ou.md` (this note)
- `research/cycle_ou.py`
- `research/cycle_ou.json`
