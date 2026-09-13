# Cycle OT: clip-removed \(S(8t+7)\) at \(5\cdot 2^k\) equals rem\((2t+1)\) at \(5\cdot 2^{k-2}\)

Cycle ON folds unclipped pal-right \(S(4s+3)=S(s)\) for every odd
\(s\), so \(S(8t+7)=S(2t+1)\). Two Green doublings scale pal-right
cells by four. On covering-shaped clip lines \(j_{\max}=5\cdot 2^k\)
(\(k\ge 2\)), the clip \(j>5\cdot 2^k\) on \(n=8t+7\) is the clip
\(j>5\cdot 2^{k-2}\) on \(s=2t+1\). Clip-removed pal-right \(S\)
therefore folds the same way.

When \(t\) is even, \(s=4p+1\) and Cycle OS writes the parent rem as
an \(R_2\) tail. This is **not** the fold for \(n=8t+3\) (even \(s\):
\(n=51\), \(j_{\max}=80\) has rem \(=1\)). **Not** one doubling
(\(n=11\), \(j_{\max}=10\)). **Not** arbitrary \(j_{\max}\)
(\(j_{\max}=44\)). **Not** covering \(S\) for all \(k\). **Not**
\(E_k=0\) for all \(k\). Do **not** catalogue further \(S\)/\(T\)
subregions unless the experiment answers why \(E_k=0\). Do **not**
claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\). Do **not**
push the even-spine scan past \(k=18\). Do **not** bump all
\(n_0=16\) past 414990. Do **not** increment consecutive `11` to
\(n_8\). Do **not** walk \(32U\). Do **not** walk \(k=11\) covering
packed. Do **not** walk \(k=12\) \(T\)-bands.

Not a prize claim: covering never-fail stays open. Odd-\(s\) rest
is not FR \(J\). Do **not** claim Green-only rest for all \(k\).

Certify: `python3 research/cycle_ot.py --certify`.
Dump: `research/cycle_ot.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OJ/OS/OQ/OR/OG (clip fold of \(S(8t+7)\); even-\(t\) \(R_2\)
tail; prefix OS even-parent rem, ON unclipped fold, OR unclipped
covering window, OG \(E_k\); no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (clip-removed \(S(8t+7)\) folds on \(5\cdot 2^k\))

For \(k\ge 2\), clip-removed pal-right \(S\) of \(n=8t+7\) at
\(j_{\max}=5\cdot 2^k\) equals clip-removed \(S\) of \(2t+1\) at
\(5\cdot 2^{k-2}\), whenever \(2n>j_{\max}\). Status: **lemma**.
Checked on \(t<40\), \(2\le k\le 8\), and on covering \(q=10\)
\(n=8t+7\) for \(k\le 8\).

## Lemma (even \(t\) is an \(R_2\) tail)

If \(t\) is even then \(2t+1=4p+1\), so the parent rem is Cycle OS's
residue-2 tail. Status: **lemma**. Checked on even \(t<40\).

## Killed

Fold for \(n=8t+3\): \(n=51\), \(j_{\max}=80\) has rem \(=1\). One
doubling: \(n=11\), \(j_{\max}=10\) has rem \(=1\) against
rem\((5,5)=0\). Arbitrary \(j_{\max}=44\): rem\((23,44)=1\) against
rem\((5,11)=0\).

## Verdict

`LEMMA` (clip-removed \(S(8t+7)\) fold on \(5\cdot 2^k\); even-\(t\)
\(R_2\) tail; even-parent rem; unclipped covering-window \(S\)).
`CERTIFIED` (covering \(n=8t+7\) rem on \(q=10\), \(k\le 8\);
\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (fold for \(n=8t+3\); one doubling; \(j_{\max}=44\)).
`PREFIX` (covering \(S\) for all \(k\); \(E_k=0\) for all \(k\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_ot.md` (this note)
- `research/cycle_ot.py`
- `research/cycle_ot.json`
