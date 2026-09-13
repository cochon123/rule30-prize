# Cycle OH: dyadic \(T\)-band xor of \(G(j-1)\) vanishes for \(3\le k\le 11\)

Palindrome-right xor of \(G(n,j-1)\) on \(G=1\) for
\(n\in[2^{k-1},2^k)\) (unclipped; no packed row) is \(1\) iff
\(k\in\{1,2\}\), through \(k\le 11\). This is the increment in
\[
T_k=\bigoplus_{i<k} B_i,
\]
where covering \(T_k\) uses \(n<U/2=2^{k-1}\). So \(B_1=B_2=1\)
and \(B_i=0\) for \(3\le i\le 11\) is why the \(T\) piece of
\(E_k=R_k\oplus S_k\oplus T_k\) is \(1\) iff \(k=2\) on that
range. This is **not** \(B_1=0\), **not** \(B_2=0\), **not**
empty (\(k=11\): \(n_T=164352\)), **not** pointwise \(0\)
(\(k=11\): \(n_{\mathrm{fire}}=62976\)), **not** rest, **not**
\(S\), and **not** the band vanish for all \(k\). Do **not**
claim \(T\) is \(1\) iff \(k=2\) for all \(k\). Do **not** walk
\(k=12\) \(T\)-bands. Do **not** catalogue further \(S\)/\(T\)
subregions unless the experiment answers why \(E_k=0\). Do
**not** claim \(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\).
Do **not** push the even-spine scan past \(k=18\). Do **not**
bump all \(n_0=16\) past 414990. Do **not** increment consecutive
`11` to \(n_8\). Do **not** walk \(32U\). Do **not** walk
\(k=11\) covering packed.

Not a prize claim: covering never-fail stays open. Odd-\(s\)
rest is not FR \(J\). Do **not** claim Green-only rest for all
\(k\). Do **not** record unique-slot XOR vs \(J\).

Certify: `python3 research/cycle_oh.py --certify`.
Dump: `research/cycle_oh.json`. Packed centre matches
`experiment.center_bits` on 20 bits. Reads Cycles
CA/KH/AL/OG/NA (Green-only dyadic \(n\)-bands \(k\le 11\); prefix
OG \(E_k\) and NA \(T\); no Fermat table, no extra window, no
\(n_0=16\) window, no packed covering \(k=11\)).

## Lemma (dyadic \(T\)-band vanishes for \(3\le k\le 11\))

Unclipped \(n\in[2^{k-1},2^k)\). At \(k=1\), the unique cell
\(n=1\) has \(G(j-1)=1\). At \(k=2\), \(n_T=3\) and xor \(=1\).
At \(k=11\), \(n_T=164352\) and xor \(=0\) with \(62976\) fires.
Covering \(T_m=\bigoplus_{i<m}B_i\) is then \(1\) iff \(m=2\) for
\(m\le 12\). Status: **certified** on this range, not a lemma for
all \(k\).

## Killed

\(B_1=0\): xor \(=1\). \(B_2=0\): xor \(=1\). Empty: \(k=11\) has
\(n_T=164352\). Pointwise \(0\): \(k=11\) has \(n_{\mathrm{fire}}=62976\).
Equals rest: \(k=1\) is \(1\) vs \(0\). Equals covering \(S\):
\(k=2\) band \(=1\), covering \(S=0\). The band vanish for all
\(k\). \(T=1\) iff \(k=2\) for all \(k\).

## Verdict

`CERTIFIED` (dyadic \(T\)-band xor vanishes for \(3\le k\le 11\);
\(E_k=0\) on odd-\(s\) rest for \(q=10\), \(k\le 10\)).
`KILLED` (\(B_1=0\); \(B_2=0\); empty; pointwise \(0\); equals
rest; equals \(S\); the band vanish for all \(k\)).
`PREFIX` (\(T=1\) iff \(k=2\) for all \(k\);
\(J_6=J_{10}=0\Rightarrow J_{18}=1\) for all \(k\); 11-bit gap;
formula for extra 414990; at-most-one-odd for all \(k\); seed;
\(\pi\) formula; Fermat covering).
`OPEN` (\(I_k=1\) infinitely often; some \(\varphi^{(q)}_k=1\)
infinitely often). Prize unsolved.

## Files

- `research/cycle_oh.md` (this note)
- `research/cycle_oh.py`
- `research/cycle_oh.json`
