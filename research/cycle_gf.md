# Cycle GF: unclipped cone-hi AND is live iff \(s\) is odd

Unclipped cone-hi sits at packed bit \(T+(2s-T)=2s\), the right edge, so
Cycle GE’s odd-\(t\) criterion applies: the AND is live iff \(s\) is
odd. Covering \(W\) is even, so among \(s=W+2^j\) only \(j=0\)
(\(s=W+1\)) is odd; the other in-cone \(G=1\) times have **dead**
cone-hi AND. After clip the band-hi is \(r=W\), not the right edge, and
that AND is **not** iff \(s\) odd. The dual-column AND is **not** iff
\(s\) odd, and clip cone-hi AND is **dead** for \(k\ge 1\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all \(n_0=16\)
past 414990. Do **not** increment consecutive `11` to \(n_8\). Do
**not** walk \(32U\).

Not a prize claim: only one live cone-hi AND among the in-cone \(G=1\)
times does not prove covering never-fail (other band indices still
contribute).

Helper: `python3 research/cycle_gf.py --certify` (~0.01s). Dump:
`research/cycle_gf.json`. Packed centre matches `experiment.center_bits`
on 20 bits. Reads Cycles CA/GD/GE (packed AND \(k\le 6\); algebraic
\(k\le 20\); no Fermat table, no extra window, no \(n_0=16\) window).

## Lemma (packed cone-hi is bit \(2s\))

\(T+(2s-T)=2s\). Certified endpoint samples \(k\le 20\).

## Lemma (unclipped cone-hi AND iff \(s\) odd)

Certified full unclipped window \(k\le 6\), \(W\in\{4U,8U,16U\}\).

## Lemma (only \(j=0\) among \(W+2^j\) has live cone-hi AND)

\(W\) even; \(2^j\) even for \(j\ge 1\). Certified \(k\le 20\).

## Killed

After-clip band-hi AND iff \(s\) odd: at \(k=2\), \(W=8U\), 2
mismatches. \(r_*\) AND iff \(s\) odd: 1 live and 5 dead on odd \(s\).
Clip cone-hi AND live for \(k\ge 1\): at \(k=2\), \(W=8U\), clip even,
AND 0.

## Verdict

`LEMMA` (packed bit \(2s\); AND iff \(s\) odd; only \(j=0\) live among
\(W+2^j\)).
`KILLED` (after-clip iff odd; \(r_*\) iff odd; clip AND live).
`PREFIX` (\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit
gap; formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_gf.md` (this note)
- `research/cycle_gf.py`
- `research/cycle_gf.json`
